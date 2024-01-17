from i2nca.qctools.visualization import make_pdf_backend, plot_feature_number, image_feature_number, plot_max_mz_number, image_max_mz_number, plot_min_mz_number, image_min_mz_number
from i2nca.qctools.utils import make_subsample, evaluate_formats, collect_image_stats, evaluate_image_corners
import numpy as np
import matplotlib.pyplot as plt
import m2aia as m2
import random as rnd
from pyimzml.ImzMLWriter import ImzMLWriter

def convert_pp_to_cp_imzml(file_path, output_path = None, pixel_nr = 100):
    """ top-level converter for pp imzml to cp imzml"""
    if output_path is None:
        output_path = file_path[:-6]

    # parse imzml file
    I = m2.ImzMLReader(file_path)

    # get the refernce mz value
    ref_mz = imzml_check_spacing(I, pixel_nr)

    # write the continous file
    write_pp_to_cp_imzml(I, ref_mz, output_path)


def report_pp_to_cp_imzml(file_path, output_path=None, coverage=0.25):
    """ test-wise converter, also creates a conversion report for file."""
    if output_path is None:
        output_path = file_path[:-6]

    # parse imzml file
    I = m2.ImzMLReader(file_path)

    # get the refernce mz value
    ref_mz = report_pp_to_cp(I, output_path, coverage)

    # write the continous file
    write_pp_to_cp_imzml(I, ref_mz, output_path)


def report_pp_to_cp(I, outfile_path, coverage):
    """creates a pdf report that checks if the following assumptions are correct:
    The file has the same number of data points in each pixel.
    The data points start and end at nearly the same value.
    The data points if all pixels are arranged into distinct clusters. (or a subsample of the pixels)"""

    # Create a PDF file to save the figures
    pdf_pages = make_pdf_backend(outfile_path, "_control_report_pp_to_cp")

    # Make a subsample to test accuracies on
    randomlist = make_subsample(I.GetNumberOfSpectra(), coverage)

    # create format flag dict to check formatting of imzML file
    format_flags = evaluate_formats(I.GetSpectrumType())

    # get the image limits to crop and display only relevant parts
    x_lims, y_lims = evaluate_image_corners(I.GetMaskArray()[0])

    # check if the porvided file is profile and processed
    test_formats(format_flags, ["profile", "processed"])

    # find the bulk data for assumption check
    image_stats = collect_image_stats(I,
                                      ['index_nr', 'peak_nr', 'max_mz_nr', 'min_mz_nr'])

    # visualize the feature numbers
    plot_feature_number(image_stats, pdf_pages)
    image_feature_number(image_stats, I,
                         pdf_pages, x_lims, y_lims)

    # vis the max intensitsy metrics
    plot_max_mz_number(image_stats, pdf_pages)
    image_max_mz_number(image_stats, I,
                        pdf_pages, x_lims, y_lims)

    # vis the  min intensitsy metrics
    plot_min_mz_number(image_stats, pdf_pages)
    image_min_mz_number(image_stats, I,
                        pdf_pages, x_lims, y_lims)

    # sanitize randomlist
    clean_rndlist = check_uniform_length(I, randomlist)

    # visualize random pixel position (black, red, green)

    # get the spacings of each pseudobins
    mean_bin, intra_bin_spread, inter_bin_spread = evaluate_group_spacing(I, clean_rndlist)

    # visualize the spread
    plot_bin_spreads(mean_bin, intra_bin_spread, inter_bin_spread, pdf_pages)

    pdf_pages.close()
    print("report generated at: ", outfile_path + "control_report_pp_to_cp.pdf")

    return mean_bin


def write_pp_to_cp_imzml(I,
                           ref_mz: np.ndarray,
                           output_dir: str,
                           polarity: str = "positive",
                           pixel_size: str = "20",
                           ) -> str:
    """
        Writer for continous profile imzml files within m2aia.

        Sparcity implementation:
        pixel is skipped if it does not fit the lenght requirement of the mz axis.


        Parameters:
            I: parsed izML file (by m2aia or equvalent object that emulates the methods)
            ref_mz(np.ndarray): An array containing the reference mz axis.
            polarity  : Polarity, either "positive" or "negative", not accessible in pym2aia
            pixel_size (Opt): pixel size of imaging run, currently not accessible in pym2aia
            output_dir (Opt): File path for output. in same folder as tsf if not specified.


        Returns:
           (str): imzML File path,
           additionally, imzML file is written there

        """
    # specification of output imzML file location and file extension
    output_file = output_dir + "_conv_output_cont_profile.imzML"

    # setting up of  reader

    # Get total spectrum count:
    n = I.GetNumberOfSpectra()
    len_ref_mz = len(ref_mz)

    # writing of the imzML file, based on pyimzML
    with ImzMLWriter(output_file,
                     # TODO get polarity from file
                     polarity=polarity,
                     mz_dtype=np.float32,
                     # intensity_dtype=np.uintc,
                     mode='continuous',
                     spec_type='profile',
                     # the laser movement param are taken from scilslab export for ttf
                     scan_direction='top_down',
                     line_scan_direction='line_right_left',
                     scan_pattern='meandering',
                     scan_type='horizontal_line',
                     # preinstalled pixel sizes TODO get correct ones
                     pixel_size_x="20",
                     pixel_size_y="20",
                     ) as w:

        # m2aia is 0-indexed
        for id in range(0, n):

            #
            _, intensities = I.GetSpectrum(id)
            length = len(intensities)

            xyz_pos = I.GetSpectrumPosition(id)
            pos = (xyz_pos[0], xyz_pos[1])

            # writing with pyimzML
            if length == len_ref_mz:
                w.addSpectrum(ref_mz, intensities, pos)
            else:
                print(f"Sparce pixel at {id}")

            #if (id % 100) == 0:
            #    print(f"pixels {id}/{n} written.")
    return output_file


# utils
def test_formats(form_dict, keywords):
    """Tests is keywords are True in the provided flag dictionary.
    Alowe dkeywords are: profile, centroid, processed, continuous"""
    for key in keywords:
        if form_dict[key] is False:
            raise ValueError(
                f"The provided file does not match the provided keywords: {keywords}. "
                f" Check the accensions in the imzML file to ensure the correct file type."
                "}"
            )

def check_uniform_length(I, randomlist):
    """check the lenght (datapoints in spectrum) of a list with ids and returns only those with maxim"""
    lenght_collector = []

    # get length of each element:
    for id in randomlist:
        lenght_collector.append(len(I.GetSpectrum(id)[0]))

    # get max element
    max_lenght = max(lenght_collector)

    # zip through lists to only the datapoints with maximal length
    result = [idx for idx, length in zip(randomlist, lenght_collector) if length == max_lenght]

    return result


def evaluate_group_spacing(I, randomlist):
    """checks how the spacing of each pseudo-bin looks.
    return the mean bin, the spread inside that bin and the spread to the right neighbouring bin"""

    # spectra are assumed to be of equal length

    # collection via list comprehension
    processed_collector = np.vstack([I.GetSpectrum(id)[0] for id in randomlist])

    processed_collector = processed_collector.T  # transpose to easily access each group of masses

    dpoint_mean = np.mean(processed_collector, axis=1)
    dpoint_spread = np.std(processed_collector, axis=1)
    dbin_spread = np.diff(dpoint_mean)  # calculation of inter-bin step size

    return dpoint_mean, dpoint_spread, dbin_spread

# % visuals
def plot_bin_spreads(mean_bins, intrabin_spread, interbin_spread, pdf):
    fig = plt.figure(figsize=[7, 5])
    ax = plt.subplot(111)

    ax.set_title('Comparison of aquisition-based binning')
    ax.set_xlabel('mz of each pseudo-bin')
    ax.set_ylabel('mz deviation')

    ax.grid(visible=True, c='lightgray', ls="--")

    ax.plot(mean_bins[:-1], interbin_spread, color='g', zorder=-1,
            label=f"Stepsize between \neach pseudo-bin \n(median: {np.median(interbin_spread):.6f})")

    ax.plot(mean_bins, intrabin_spread, color='r', zorder=-1,
            label=f"standard deviation \nwithin each pseudo-bin \n(median: {np.median(intrabin_spread):.6f})")

    ax.legend()

    pdf.savefig(fig)
    plt.close()


# special checker, return the mean points with specified pixel numbers,
# intented for workflows
def imzml_check_spacing(I, batch_size: int = 100) -> np.ndarray:
    # setting up of  reader
    # I = m.ImzMLReader(imzML_filename)
    # I.Execute()

    # Get total spectrum count:
    n = I.GetNumberOfSpectra()
    if batch_size < n:
        # create the small sample list (100 pixels)
        randomlist = rnd.sample(range(0, n), batch_size)
    else:
        randomlist = [i for i in range(0, n)]

    # instance and collect mass values from the small batch
    #first_mz, _ = I.GetSpectrum(0)
    len_first_mz = len(I.GetSpectrum(0)[0])
   # processed_collector = first_mz

    # 'for id in randomlist:
    # ''    mz, _ = I.GetSpectrum(id)
    #    # assumes that the instrument makes same amount of data points in each pixel
    #     if len_first_mz == len(mz):
    #         processed_collector = np.vstack((processed_collector, mz))

    # collection via list comprehension
    processed_collector = np.vstack([I.GetSpectrum(id)[0] for id in randomlist if len_first_mz == len(I.GetSpectrum(id)[0])])

    processed_collector = processed_collector.T  # transpose to easily access each group of masses

    dpoint_mean = np.mean(processed_collector, axis=1)

    return dpoint_mean

if __name__ == "__main__":
    #file_name = r"C:\Users\Jannik\Documents\Uni\Master_Biochem\4_Semester\QCdev\testfiles\metabolomics_small_mz_processed_centroid.imzML"
    file_name = r"C:\Users\Jannik\Documents\Uni\Master_Biochem\4_Semester\M2aia\data\output.imzML"

    report_pp_to_cp_imzml(file_name)

    out_file = file_name[:-6] + "silent_conv"
    convert_pp_to_cp_imzml(file_name, out_file)