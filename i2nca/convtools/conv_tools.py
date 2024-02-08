from i2nca.qctools.visualization import make_pdf_backend, plot_feature_number, image_feature_number, \
    plot_max_mz_number, image_max_mz_number, plot_min_mz_number, image_min_mz_number, plot_bin_spreads, \
    plot_noise_spectrum, plot_profile_spectrum
from i2nca.qctools.utils import make_subsample, evaluate_formats, collect_image_stats, evaluate_image_corners, \
    test_formats, check_uniform_length, evaluate_group_spacing, evaluate_polarity, get_polarity, get_pixsize, \
    collect_noise

import numpy as np
import m2aia as m2
import random as rnd
from pyimzml.ImzMLWriter import ImzMLWriter
from scipy.signal import find_peaks

# tools for processed profile


def convert_pp_to_pp_imzml(file_path, output_path=None):
    """ Top-level converter for
    processed profile imzML to processed profile imzML.

    Introduces no changes to file."""
    if output_path is None:
        output_path = file_path[:-6]

    # parse imzml file
    Image = m2.ImzMLReader(file_path)

    # write the profile processed  file
    return write_pp_to_pp_imzml(Image, output_path)


def write_pp_to_pp_imzml(Image,
                         output_dir: str
                         ) -> str:
    """
        Writer for processed profile imzml files within m2aia.


        Parameters:
            Image: parsed izML file (by m2aia or equvalent object that emulates the methods)
            output_dir (Opt): File path for output. in same folder as tsf if not specified.


        Returns:
           (str): imzML File path,
           additionally, imzML file is written there

        """
    # specification of output imzML file location and file extension
    output_file = output_dir + "_conv_output_proc_profile.imzML"

    # Get total spectrum count:
    n = Image.GetNumberOfSpectra()

    # get the polarity
    polarity = get_polarity(evaluate_polarity(Image))

    # get the pixel size
    pix_size = get_pixsize(Image)

    # writing of the imzML file, based on pyimzML
    with ImzMLWriter(output_file,
                     polarity=polarity,
                     mz_dtype=np.float32,
                     # intensity_dtype=np.uintc,
                     mode='processed',
                     spec_type='profile',
                     pixel_size_x=pix_size,
                     pixel_size_y=pix_size,
                     # the laser movement param are adapted to TTF presets
                     scan_direction='top_down',
                     line_scan_direction='line_right_left',
                     scan_pattern='meandering',
                     scan_type='horizontal_line',
                     ) as w:
        # m2aia is 0-indexed
        for id in range(0, n):
            #
            mz, intensities = Image.GetSpectrum(id)

            xyz_pos = Image.GetSpectrumPosition(id)

            #image offset (m2aia5.1 quirk, persistent up to 5.10)
            img_offset = 1
            # offset needs to be added fro 1-based indexing of xyz system
            pos = (xyz_pos[0] + img_offset, xyz_pos[1] + img_offset)

            # writing with pyimzML

            w.addSpectrum(mz, intensities, pos)

            # progress print statement
            # if (id % 100) == 0:
            #    print(f"pixels {id}/{n} written.")
    return output_file




#  Tools for Continous Profile conversion


def convert_pp_to_cp_imzml(file_path, output_path = None, pixel_nr = 100):
    """Top-level converter for processed profile imzml to
     continuous profile imzml.
     This is achieved my mz axis alignment.
     This function is silent and does not produce a report

     functions returns filepath of new file for further use.
     """
    if output_path is None:
        output_path = file_path[:-6]

    # parse imzml file
    Image = m2.ImzMLReader(file_path)

    # get the polarity
    polarity = get_polarity(evaluate_polarity(Image))

    # get the pixel size
    pix_size = get_pixsize(Image)

    # get the refernce mz value
    ref_mz = imzml_check_spacing(Image, pixel_nr)

    # write the continous file
    return write_pp_to_cp_imzml(Image, ref_mz, output_path)


def report_pp_to_cp_imzml(file_path, output_path=None, coverage=0.25):
    """Top-level converter for processed profile imzml to
     continuous profile imzml.
     This is achieved my mz axis alignment.
     This function is produces a report.

     functions returns filepath of new file for further use.
     """
    if output_path is None:
        output_path = file_path[:-6]

    # parse imzml file
    Image = m2.ImzMLReader(file_path)


    # get the refernce mz value
    ref_mz = report_pp_to_cp(Image, output_path, coverage)

    # write the continous file
    return write_pp_to_cp_imzml(Image, ref_mz, output_path)



def write_pp_to_cp_imzml(Image,
                           ref_mz: np.ndarray,
                           output_dir: str
                           ) -> str:
    """
        Writer for continous profile imzml files within m2aia.

        Sparcity implementation:
        pixel is skipped if it does not fit the lenght requirement of the mz axis.
        Further implementations could be an intensity array of 0 together with shared mass maxis
        or a binary tree implementation to only fit this t the nearest neighbours.


        Parameters:
            Image: parsed izML file (by m2aia or equvalent object that emulates the methods)
            ref_mz(np.ndarray): An array containing the reference mz axis.
            output_dir (Opt): File path for output. in same folder as tsf if not specified.


        Returns:
           (str): imzML File path,
           additionally, imzML file is written there

        """
    # specification of output imzML file location and file extension
    output_file = output_dir + "_conv_output_cont_profile.imzML"

    # get the polarity
    polarity = get_polarity(evaluate_polarity(Image))

    # get the pixel size
    pix_size = get_pixsize(Image)

    # Get total spectrum count:
    n = Image.GetNumberOfSpectra()
    len_ref_mz = len(ref_mz)

    # writing of the imzML file, based on pyimzML
    with ImzMLWriter(output_file,
                     polarity=polarity,
                     pixel_size_x=pix_size,
                     pixel_size_y=pix_size,
                     mz_dtype=np.float32,
                     # intensity_dtype=np.uintc,
                     mode='continuous',
                     spec_type='profile',
                     # the laser movement param are taken from scilslab export for ttf
                     scan_direction='top_down',
                     line_scan_direction='line_right_left',
                     scan_pattern='meandering',
                     scan_type='horizontal_line',
                     ) as w:

        # m2aia is 0-indexed
        for id in range(0, n):

            _, intensities = Image.GetSpectrum(id)
            length = len(intensities)

            xyz_pos = Image.GetSpectrumPosition(id)

            # image offset (m2aia5.1 quirk, persistent up to 5.10.)
            img_offset = 1

            # offset needs to be added for 1-based indexing of xyz system
            pos = (xyz_pos[0] + img_offset, xyz_pos[1] + img_offset)

            # writing with pyimzML
            if length == len_ref_mz:
                w.addSpectrum(ref_mz, intensities, pos)
            else:
                print(f"Sparce pixel at {id}")

    return output_file



def report_pp_to_cp(Image, outfile_path, coverage):
    """creates a pdf report that checks if the following assumptions are correct:
    The file has the same number of data points in each pixel.
    The data points start and end at nearly the same value.
    The data points if all pixels are arranged into distinct clusters. (or a subsample of the pixels)"""

    # Create a PDF file to save the figures
    pdf_pages = make_pdf_backend(outfile_path, "_control_report_pp_to_cp")

    # Make a subsample to test accuracies on
    randomlist = make_subsample(Image.GetNumberOfSpectra(), coverage)

    # create format flag dict to check formatting of imzML file
    format_flags = evaluate_formats(Image.GetSpectrumType())

    # get the image limits to crop and display only relevant parts
    x_lims, y_lims = evaluate_image_corners(Image.GetMaskArray()[0])

    # check if the porvided file is profile and processed
    test_formats(format_flags, ["profile", "processed"])

    # find the bulk data for assumption check
    image_stats = collect_image_stats(Image,
                                      ['index_nr', 'peak_nr', 'max_mz_nr', 'min_mz_nr'])

    # visualize the feature numbers
    plot_feature_number(image_stats, pdf_pages)
    image_feature_number(image_stats, Image,
                         pdf_pages, x_lims, y_lims)

    # vis the max intensitsy metrics
    plot_max_mz_number(image_stats, pdf_pages)
    image_max_mz_number(image_stats, Image,
                        pdf_pages, x_lims, y_lims)

    # vis the  min intensitsy metrics
    plot_min_mz_number(image_stats, pdf_pages)
    image_min_mz_number(image_stats, Image,
                        pdf_pages, x_lims, y_lims)

    # sanitize randomlist
    clean_rndlist = check_uniform_length(Image, randomlist)

    # visualize random pixel position (black, red, green)

    # get the spacings of each pseudobins
    mean_bin, intra_bin_spread, inter_bin_spread = evaluate_group_spacing(Image, clean_rndlist)

    # visualize the spread
    plot_bin_spreads(mean_bin, intra_bin_spread, inter_bin_spread, pdf_pages)

    pdf_pages.close()

    return mean_bin



# special checker, return the mean points with specified pixel numbers,
# intented for workflows
def imzml_check_spacing(Image, batch_size: int = 100) -> np.ndarray:
    # setting up of  reader
    # I = m.ImzMLReader(imzML_filename)
    # I.Execute()

    # Get total spectrum count:
    n = Image.GetNumberOfSpectra()
    if batch_size < n:
        # create the small sample list (100 pixels)
        randomlist = rnd.sample(range(0, n), batch_size)
    else:
        randomlist = [i for i in range(0, n)]

    # instance and collect mass values from the small batch
    #first_mz, _ = I.GetSpectrum(0)
    len_first_mz = len(Image.GetSpectrum(0)[0])
   # processed_collector = first_mz

    # 'for id in randomlist:
    # ''    mz, _ = I.GetSpectrum(id)
    #    # assumes that the instrument makes same amount of data points in each pixel
    #     if len_first_mz == len(mz):
    #         processed_collector = np.vstack((processed_collector, mz))

    # collection via list comprehension
    processed_collector = np.vstack([Image.GetSpectrum(id)[0] for id in randomlist if len_first_mz == len(Image.GetSpectrum(id)[0])])

    processed_collector = processed_collector.T  # transpose to easily access each group of masses

    dpoint_mean = np.mean(processed_collector, axis=1)

    return dpoint_mean


# peak detection and stuff


def set_find_peaks(height=None,
                   threshold=None,
                   distance=None,
                   prominence=None,
                   width=None,
                   wlen=None,
                   rel_height=0.5,
                   plateau_size=None):
    """higher order function to pass peak-detection arguments without performing peak-finding.

    Example usage:
    set_find_peaks(height=2500, width=4)(mz, intensity)

    set_find_peaks(height=20, prominence=3) can be passed as argument to peak centroiding funktions.
    see the loc_max_preset for an example.
        """

    def inner_function(mz, intensity):
        # a call of scipy.find_peaks with all available parameters.
        peaks, _ = find_peaks(intensity,
                              height=height,
                              threshold=threshold,
                              distance=distance,
                              prominence=prominence,
                              width=width,
                              wlen=wlen,
                              rel_height=rel_height,
                              plateau_size=plateau_size)
        return mz[peaks], intensity[peaks]
    return inner_function


def loc_max_preset(mz, intensity):
    """preset peak finding settings.
    Heigth above 20 and a width of 5"""
    return set_find_peaks(height=20, width=5)(mz, intensity)


def convert_profile_to_pc_imzml(file_path,
                                output_path=None,
                                detection_function=loc_max_preset):

    """ Top-level converter for
     profile imzML to processed centroid imzML.
     The centroiding is implemented by user definition of a peak detection function.

    Introduces no changes to file."""
    if output_path is None:
        output_path = file_path[:-6]

    # parse imzml file
    Image = m2.ImzMLReader(file_path)

    # get the polarity
    polarity = get_polarity(evaluate_polarity(Image))

    # get the pixel size
    pix_size = get_pixsize(Image)

    # write the profile processed  file
    return write_profile_to_cp_imzml(Image, output_path, detection_function)


def write_profile_to_cp_imzml(Image,
                              output_dir: str,
                              detection_function
                         ) -> str:
    """
        Writer for processed profile imzml files within m2aia.


        Parameters:
            Image: parsed izML file (by m2aia or equvalent object that emulates the methods)

            detection function: this can be any function that takes two arrays, (mzs and intensities) and return
            the result of peak detection on that daatset.

            output_dir (Opt): File path for output. in same folder as tsf if not specified.


        Returns:
           (str): imzML File path,
           additionally, imzML file is written there

        """
    # specification of output imzML file location and file extension
    output_file = output_dir + "_conv_output_proc_centroid.imzML"

    # Get total spectrum count:
    n = Image.GetNumberOfSpectra()

    # get the polarity
    polarity = get_polarity(evaluate_polarity(Image))

    # get the pixel size
    pix_size = get_pixsize(Image)

    # writing of the imzML file, based on pyimzML
    with ImzMLWriter(output_file,
                     polarity=polarity,
                     pixel_size_x=pix_size,
                     pixel_size_y=pix_size,
                     mz_dtype=np.float32,
                     # intensity_dtype=np.uintc,
                     mode='processed',
                     spec_type='centroid',
                     # the laser movement param are taken from scilslab export for ttf
                     scan_direction='top_down',
                     line_scan_direction='line_right_left',
                     scan_pattern='meandering',
                     scan_type='horizontal_line',
                     ) as w:
        # m2aia is 0-indexed
        for id in range(0, n):
            #
            mz, intensities = Image.GetSpectrum(id)

            mz, intensities = detection_function(mz, intensities)

            xyz_pos = Image.GetSpectrumPosition(id)

            # image offset (m2aia5.1 quirk, persistent up to 5.10)
            img_offset = 1
            # offset needs to be added fro 1-based indexing of xyz system
            pos = (xyz_pos[0] + img_offset, xyz_pos[1] + img_offset)

            # writing with pyimzML
            if len(intensities) != 0:
                w.addSpectrum(mz, intensities, pos)
            else:
                print(f"Sparce pixel at {id}")

            # progress print statement
            # if (id % 100) == 0:
            #    print(f"pixels {id}/{n} written.")
    return output_file


# add a conversion report for profile to centroids.

def report_prof_to_centroid(Image, outfile_path):
    """creates a pdf report that checks:
    The file has the same number of data points in each pixel.
    The data points start and end at nearly the same value.
    The data points if all pixels are arranged into distinct clusters. (or a subsample of the pixels)"""

    # Create a PDF file to save the figures
    pdf_pages = make_pdf_backend(outfile_path, "_control_report_pc_to_cp")

    # create format flag dict to check formatting of imzML file
    format_flags = evaluate_formats(Image.GetSpectrumType())

    # check if the porvided file is profile.
    # fro efficientcy purpose, continuous filetype is not controlled
    test_formats(format_flags, ["profile"])

    # visualize the mean spectra
    if format_flags["profile"]:
        plot_profile_spectrum(Image.GetXAxis(), Image.GetMeanSpectrum(), pdf_pages)

    # equates to interval of plus/minus noise_interval
    noise_interval = 2
    # get noise data on mean spectrum
    noise_medain, _, noise_axis = collect_noise(Image.GetXAxis(), Image.GetMeanSpectrum(), noise_interval)

    # PLOT NOISES'
    plot_noise_spectrum(noise_axis, noise_medain,
                        f'Noise estimation within interval of {2 * noise_interval}', pdf_pages)

    # how nice would it be if the QC score would be plotted here

    pdf_pages.close()
    print("report generated at: ", outfile_path + "control_report_pp_to_cp.pdf")