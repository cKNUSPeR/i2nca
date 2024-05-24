# import random as rnd
# from typing import Optional, Callable
#
# import m2aia as m2
# import numpy as np
# from pyimzml.ImzMLWriter import ImzMLWriter
# from scipy.signal import find_peaks, find_peaks_cwt

from i2nca.qctools.dependencies import *


from i2nca.qctools.utils import make_subsample, evaluate_formats, collect_image_stats, evaluate_image_corners, \
    test_formats, check_uniform_length, evaluate_group_spacing, evaluate_polarity, get_polarity, get_pixsize, \
    collect_noise
from i2nca.qctools.visualization import make_pdf_backend, plot_feature_number, image_feature_number, \
    plot_max_mz_number, image_max_mz_number, plot_min_mz_number, image_min_mz_number, plot_bin_spreads, \
    plot_noise_spectrum, plot_profile_spectrum


# tools for processed profile


def convert_pp_to_pp_imzml(file_path,
                           output_path: Optional[str] = None) -> str:
    """
      Top-level converter for processed profile imzML to processed profile imzML.

      This converter does not explicitly change files.
      Converts all read data to float32 arrays.

      Parameters
      ----------
      file_path : string
          Path of imzML file.
      output_path : string ,optional
          Path to filename where the output file should be built.
          If ommitted, the file_path is used.

      Returns
      -------
      output_file : str
          File path as string of succesfully converted imzML file.
    """

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

            # image offset (m2aia5.1 quirk, persistent up to 5.10)
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

def squeeze_pp_to_cp_imzml(file_path, output_path=None, pixel_nr=100):
    """
    shelfed pp to cp imzml converter, replaced by convert_pp_to_cp_imzml
    Top-level converter for processed profile imzml to
     continuous profile imzml.
     This is achieved my mz axis alignment.
     THis functin does not create a conversion report.
     It is meant to be used in batch datasets

     functions returns filepath of new file for further use.
     """
    if output_path is None:
        output_path = file_path[:-6]

    # parse imzml file
    Image = m2.ImzMLReader(file_path)

    # get the refernce mz value
    ref_mz = imzml_check_spacing(Image, pixel_nr)

    # write the continous file
    return write_pp_to_cp_imzml(Image, ref_mz, output_path)


def convert_pp_to_cp_imzml(file_path: str,
                           output_path: Optional[str] = None,
                           coverage: float = 0.25,
                           method = "fixed_alignment",
                           accuracy = 20) -> str:
    """
    Top-level converter for processed profile imzml to continuous profile imzml.

    This converter does theconversion by alingning the mz axis to the mean axis from a subsample.
    A conversion report is created at output location monitoring all the assumptions for this.

    Parameters
    ----------
    file_path : string
        Path of imzML file.
    output_path : string , optional
        Path to filename where the output file should be built.
        If ommitted, the file_path is used.
    coverage : float , optional
        Percentage of sample used for shared mz axis calculation.
        Between 0 and 1.
    mwethod:
        The method for conversion:
            - aq_bins allows to create a experimental binning apporach for the TTF data
            - fixed allows to create a mass axis based on a fix ppm cutoff

    Returns
    -------
    output_file : str
      File path as string of succesfully converted imzML file.
    """
    if output_path is None:
        output_path = file_path[:-6]

    # parse imzml file
    Image = m2.ImzMLReader(file_path)

    # get the refernce mz value
    ref_mz = make_profile_axis(Image, output_path, method, coverage, accuracy)

    # write the continous file
    return write_pp_to_cp_imzml(Image, ref_mz, output_path)


def make_profile_axis(Image, output_path, method, coverage, accuracy):
        """Helper function to make bins fro profile axis"""
        if method == "fixed_bins":
            bins = report_pp_to_cp(Image, output_path, coverage)
            return bins
        elif method == "fixed_alignment":
            start = min(Image.GetXAxis())
            end = max(Image.GetXAxis())
            return np.array(list(mz_range(start, end, accuracy)))
        else:
            return sorted(Image.GetXAxis())


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

            mz, intensities = Image.GetSpectrum(id)
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
                binned_ints = get_averaged_intensites(mz, ref_mz, intensities)
                w.addSpectrum(ref_mz, binned_ints, pos)

    return output_file


def report_pp_to_cp(Image, outfile_path, coverage):
    """
    Reporter function for mz alignment.

    This reporter creates a pdf report that checks if the following assumptions are correct.
        - The file has the same number of data points in each pixel.
        - The data points start and end at nearly the same value.
        - The data points of all pixels in a subsample are arranged into distinct clusters.
    Output is only graphically presented

    Parameters
    ----------
    Image :
        A m2aia.ImzMLReader image object, or similar
    outfile_path : string
        Path to filename where the pdf output file should be built.
    coverage : float
        Percentage of sample used for shared mz axis calculation.
        Between 0 and 1.


    Returns
    -------
    report : file
      PDF file at specified location with report on assumptions.
    """

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
    # first_mz, _ = I.GetSpectrum(0)
    len_first_mz = len(Image.GetSpectrum(0)[0])
    # processed_collector = first_mz

    # 'for id in randomlist:
    # ''    mz, _ = I.GetSpectrum(id)
    #    # assumes that the instrument makes same amount of data points in each pixel
    #     if len_first_mz == len(mz):
    #         processed_collector = np.vstack((processed_collector, mz))

    # collection via list comprehension
    processed_collector = np.vstack(
        [Image.GetSpectrum(id)[0] for id in randomlist if len_first_mz == len(Image.GetSpectrum(id)[0])])

    processed_collector = processed_collector.T  # transpose to easily access each group of masses

    dpoint_mean = np.mean(processed_collector, axis=1)

    return dpoint_mean

# profile to centroid conversion

def set_find_peaks(height=None,
                   threshold=None,
                   distance=None,
                   prominence=None,
                   width=None,
                   wlen=None,
                   rel_height=0.5,
                   plateau_size=None):
    """
    Higher order function to pass peak-detection arguments without performing peak-finding.
    set_find_peaks(height=20, prominence=3) can be passed as argument to peak centroiding funktions.
    See the loc_max_preset for an example.

     Parameters
    ----------
     parameters : float, Optinal

     See the documentation of scipy.singal.find_peaks for further info

    Returns
    -------
    [[peaks_mz], [peaks_intensity]] : tuple(array)
        A nested tuple of arrays containing mz and intensity vaules of found peaks.


    """

    def inner_locmax_function(mz, intensity):
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

    return inner_locmax_function


def set_find_peaks_cwt(widths,
                       wavelet=None,
                       max_distances=None,
                       gap_thresh=None,
                       min_length=None,
                       min_snr=1,
                       noise_perc=10,
                       window_size=None):
    """
    Higher order function to pass peak-detection arguments without performing peak-finding.
    set_find_peaks_cwt([6,7,8], min_snr=3) can be passed as argument to peak centroiding functions.
    Example usage: set_find_peaks_cwt(widths=np.arange(1,10), min_snr = 3)(mz, intensity)

    Parameters
    ----------
     parameters : float, Optinal

     See the documentation of scipy.singal.find_peaks_cwt for further info

    Returns
    -------
    [[peaks_mz], [peaks_intensity]] : tuple(array)
        A nested tuple of arrays containing mz and intensity vaules of found peaks.
    """

    def inner_cwt_function(mz, intensity):
        # a call of scipy.find_peaks_cwt with all available parameters.
        # unspecified parameters are set to default value
        peaks = find_peaks_cwt(intensity,
                               widths=widths,
                               wavelet=wavelet,
                               max_distances=max_distances,
                               gap_thresh=gap_thresh,
                               min_length=min_length,
                               min_snr=min_snr,
                               noise_perc=noise_perc,
                               window_size=window_size)
        return mz[peaks], intensity[peaks]

    return inner_cwt_function


def loc_max_preset(mz, intensity):
    """Preset peak detection function.
    Shows the application of the funtional set_find_peaks.
    Preset Arguments are a peak heigth above 20 and a width of 5.

    Parameters
    ----------
    mz :  array-like
        An array of mz values.
    intensity : array-like
        An array of intensities.

    Returns
    -------
    [[peaks_mz], [peaks_intensity]] : tuple(array)
        A nested tuple of arrays containing mz and intensity vaules of found peaks.
    """
    return set_find_peaks(height=20, width=5)(mz, intensity)


def squeeze_profile_to_pc_imzml(file_path,
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

    # write the profile processed  file
    return write_profile_to_pc_imzml(Image, output_path, detection_function)


def convert_profile_to_pc_imzml(file_path: str,
                                output_path: Optional[str] = None,
                                detection_function: Callable = loc_max_preset) -> str:
    """
    Top-level converter for any profile imzml to processed centroid imzml.

    This converter maps the detection_function on the mass spectrum on a pixel_by_pixel basis.
    A conversion report is created at output location for monitoring of relevant metrics before converion.

    Parameters
    ----------
    file_path : string
        Path of imzML file.
    output_path : string , optional
        Path to filename where the output file should be built.
        If ommitted, the file_path is used.
    detection_function : function , optional
        Function object that takes 2 arrays and returns the decected peaks.
        If ommitted, local maxima detection with preset paramerters is used.
        See set_find_peaks for further information


    Returns
    -------
    output_file : str
      File path as string of succesfully converted imzML file.
    """

    if output_path is None:
        output_path = file_path[:-6]

    # parse imzml file
    Image = m2.ImzMLReader(file_path)

    # make the file converion report
    report_prof_to_centroid(Image, output_path)

    # write the continous file
    return write_profile_to_pc_imzml(Image, output_path, detection_function)


def write_profile_to_pc_imzml(Image,
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
                w.addSpectrum(mz, np.zeores(len(intensities)), pos)

            # progress print statement
            # if (id % 100) == 0:
            #    print(f"pixels {id}/{n} written.")
    return output_file


# add a conversion report for profile to centroids.

def report_prof_to_centroid(Image, outfile_path):
    """
    Reporter function for peak detection.

    This reporter creates a pdf report that shows the following metrics for help in peak detection parametrization:
        - The mean spectrum over the file
        - The simga-clipping estiamted noise in an interval of 4 mz
    Output is only graphically presented

    Parameters
    ----------
    Image :
        A m2aia.ImzMLReader image object, or similar
    outfile_path : string
        Path to filename where the pdf output file should be built.

    Returns
    -------
    report : file
      PDF file at specified location with report on assumptions.
    """

    # Create a PDF file to save the figures
    pdf_pages = make_pdf_backend(outfile_path, "_control_report_prof_to_pc")

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


# tools for the conversion of pc to cc

def convert_pc_to_cc_imzml(file_path: str,
                           output_path: str = None,
                           bin_strategy: str = "fixed",
                           bin_accuracy: int = 100) -> str:
    """
    Top-level converter for processed centroid imzml to continuous centroid imzml.

    This converter bins the data of each mass spectrum on a pixel_by_pixel basis to a comon mass axis.
    The common mass axis can be instanced by different means.

    Parameters
    ----------
    file_path : string
        Path of imzML file.
    output_path : string , optional_
        Path to filename where the output file should be built.
        If ommitted, the file_path is used.
    bin_strategy : string , {"unique","fixed"}
        Employed strategy for generation of common mass axis.
        If "unique", all unique mz values of all pixels are used. Only recommended for small datasets.
        If "fixed", a common mass axis is generated and used.
        If ommitted, "fixed" is used.
    bin_accuracy : int, optional
        The inaccuracy in ppm of the "fixed" mz axis.
        If ommited, mass axis is generated at 100 ppm accuracy.


    Returns
    -------
    output_file : str
      File path as string of succesfully converted imzML file.
    """
    if output_path is None:
        output_path = file_path[:-6]

    # parse imzml file
    Image = m2.ImzMLReader(file_path)

    ref_mz = create_bins(Image, bin_strategy, bin_accuracy)

    # write the continous file
    return write_pc_to_cc_imzml(Image, ref_mz, output_path)


def create_bins(Image, method="unique", accuracy=100):
    """make bins to represent the continous bins"""
    if method == "unique":
        bins = get_unique_masses(Image)
        return bins
    elif method == "fixed":
        start = min(Image.GetXAxis())
        end = max(Image.GetXAxis())
        return np.array(list(mz_range(start, end, accuracy)))
    else:
        return sorted(Image.GetXAxis())


def get_unique_masses(Image):
    """get all the unique mass values"""
    unique_values = set()

    n = Image.GetNumberOfSpectra()

    # Iterate through arrays and collect unique values
    for id in range(0, n):
        mz, _ = Image.GetSpectrum(id)
        unique_values.update(mz)

    return sorted(unique_values)


def mz_range(start, end, step):
    """generator, creates a list of mz values begining with start and incrementing with step as ppm stepsize"""
    yield start
    current = start
    while current <= end:
        current = current + (current * step / (10 ** 6))
        yield current

def find_nearest_element(values, search_array):
    """find nearest elements with a binary search in sorted array"""

    # make and vectoize function
    search_bisect = lambda x: np.searchsorted(search_array, x)
    vsearch_bisect = np.vectorize(search_bisect)

    indices = vsearch_bisect(values)  # applythis, there really should be a one-liner

    indices = np.clip(indices, 0, len(search_array) - 1)  # drop all invalid right indices

    return indices


def get_averaged_intensites(mz, ref_mz, intensities):
    """helper fuction to obtain binned intensities for a set of given mz and intensities by a reference mz axis"""
    # get test parameter
    corr_length = len(ref_mz)
    # make the ref axis
    index_array = find_nearest_element(mz, ref_mz)
    # get the binned intensity axis
    binned_ints = np.bincount(index_array, weights=intensities)

    # check if binned_ints has no trailing lenthgs
    # (bincount only instances the index array till the highest count, not to match the shape of the reference_mz)
    if len(binned_ints) != corr_length:
        # get the number of missing entries
        missing = corr_length - len(binned_ints)
        binned_ints = np.concatenate((binned_ints, np.zeros(missing)), axis=0)

    return binned_ints


def write_pc_to_cc_imzml(Image,
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
    output_file = output_dir + "_conv_output_cont_centroid.imzML"

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
                     spec_type='centroid',
                     # the laser movement param are taken from scilslab export for ttf
                     scan_direction='top_down',
                     line_scan_direction='line_right_left',
                     scan_pattern='meandering',
                     scan_type='horizontal_line',
                     ) as w:
        # m2aia is 0-indexed
        for id in range(0, n):
            # get the data from Image
            mz, intensities = Image.GetSpectrum(id)
            xyz_pos = Image.GetSpectrumPosition(id)

            # image offset (m2aia5.1 quirk, persistent up to 5.10.)
            img_offset = 1
            # offset needs to be added for 1-based indexing of xyz system
            pos = (xyz_pos[0] + img_offset, xyz_pos[1] + img_offset)

            # make the ref axis
            binned_ints = get_averaged_intensites(mz, ref_mz, intensities)

            # writing with pyimzML
            w.addSpectrum(ref_mz, binned_ints, pos)

    return output_file


# general writer


def write_out_imzml(Image,
                    output_dir: str,
                    spectrum_type: str,
                    alignment_type: str) -> str:
    """
    Writer for any imzml files within m2aia to their respective format.


    Parameters:
        Image:
            parsed izML file (by m2aia or equvalent object that emulates the methods)
        output_path : string ,optional
            Path to filename where the output file should be built.
            If ommitted, the file_path is used.
        spectrum_type: string
            The spectrum type. Either 'profile' or 'centroid'.
        alignment_type: string
            The alignment type. Either 'processed' or 'continuous'.
        sample_size: interget
            The number of pixels that are written in the new snippet dataset
        scattered : bool, optional
            Determines if random number of pixels are randomly distributed over image or grouped as one block
            If ommitted, True is used.


    Returns:
       (str): imzML File path,
       additionally, imzML file is written there

        """
    # specification of output imzML file location and file extension
    output_file = output_dir + "_data_snippet.imzML"

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
                     mode=alignment_type,
                     spec_type=spectrum_type,
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

            # image offset (m2aia5.1 quirk, persistent up to 5.10)
            img_offset = 1
            # offset needs to be added fro 1-based indexing of xyz system
            pos = (xyz_pos[0] + img_offset, xyz_pos[1] + img_offset)

            # writing with pyimzML

            w.addSpectrum(mz, intensities, pos)

            # progress print statement
            # if (id % 100) == 0:
            #    print(f"pixels {id}/{n} written.")
    return output_file