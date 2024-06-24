from .utils import *
from .visualization import *


def report_agnostic_qc(I,  # m2.imzMLReader (passing by ref allows faster computation)
                       outfile_path: str,  # path for output file
                       ) -> str:
    """
    Generates a QC report without taking in any information om the dataset.
    Statistics that are present in any kind on MSI dataset are evaluated and visualized.
    
    A report is created at output location with all calculated visualizations.


    Parameters
    ----------
    I : 
        A m2aia.ImzMLReader image object, or similar
    outfile_path : string
        Path to filename where the pdf output file should be built.


    Returns
    -------
    output_file : str
        File path as string of succesfully generated pdf report.
    """

    # Create a PDF file to save the figures
    pdf_pages = make_pdf_backend(outfile_path, "_agnostic_QC")

    # create format flag dict to check formatting of imzML file
    format_flags = evaluate_formats(I.GetSpectrumType())

    # get the image limits to crop and display only relevant parts
    x_lims, y_lims = evaluate_image_corners(I.GetMaskArray()[0])

    image_full_binary(I.GetMaskArray()[0],
                      pdf_pages)

    image_cropped_binary(I.GetMaskArray()[0],
                         pdf_pages, x_lims, y_lims)

    image_pixel_index(I.GetIndexArray()[0], I.GetMaskArray()[0],
                      pdf_pages, x_lims, y_lims)

    image_stats = collect_image_stats(I,
                                      ['index_nr', 'peak_nr', 'tic_nr', 'median_nr', 'max_int_nr', 'min_int_nr',
                                       'max_mz_nr', 'min_mz_nr', 'max_abun_nr'])

    # visualize the feature numbers
    plot_feature_number(image_stats, pdf_pages)
    image_feature_number(image_stats, I,
                         pdf_pages, x_lims, y_lims)

    # vis the tic metrics
    plot_tic_number(image_stats, pdf_pages)
    image_tic_number(image_stats, I,
                     pdf_pages, x_lims, y_lims)

    # vis the mab metrics
    plot_max_abun_number(image_stats, pdf_pages)
    image_max_abun_number(image_stats, I,
                          pdf_pages, x_lims, y_lims)

    # vis the median metrics
    plot_median_number(image_stats, pdf_pages)
    image_median_number(image_stats, I,
                        pdf_pages, x_lims, y_lims)

    # vis the max intensitsy metrics
    plot_max_int_number(image_stats, pdf_pages)
    image_max_int_number(image_stats, I,
                         pdf_pages, x_lims, y_lims)

    # vis the  min intensitsy metrics
    plot_min_int_number(image_stats, pdf_pages)
    image_min_int_number(image_stats, I,
                         pdf_pages, x_lims, y_lims)

    # vis the max intensitsy metrics
    plot_max_mz_number(image_stats, pdf_pages)
    image_max_mz_number(image_stats, I,
                        pdf_pages, x_lims, y_lims)

    # vis the  min intensitsy metrics
    plot_min_mz_number(image_stats, pdf_pages)
    image_min_mz_number(image_stats, I,
                        pdf_pages, x_lims, y_lims)

    # visualize the mean spectra
    if format_flags["centroid"]:
        plot_centroid_spectrum(I.GetXAxis(), I.GetMeanSpectrum(), "Averaged centroid mass spectrum", pdf_pages)
    elif format_flags["profile"]:
        plot_profile_spectrum(I.GetXAxis(), I.GetMeanSpectrum(), pdf_pages)

    # equates to interval of plus/minus noise_interval
    noise_interval = 2
    # get noise data on mean spectrum
    noise_medain, _, noise_axis = collect_noise(I.GetXAxis(), I.GetMeanSpectrum(), noise_interval)

    # PLOT NOISES'
    plot_noise_spectrum(noise_axis, noise_medain,
                        f'Noise estimation within interval of {2 * noise_interval}', pdf_pages)

    # get spectral coverage data:
    mean_bin, mean_coverage = calculate_spectral_coverage(I.GetXAxis(), I.GetMeanSpectrum())

    # plot spectral coverage data
    plot_coverage_barplot(mean_bin, mean_coverage, f'Spectral coverage of mean spectrum', pdf_pages)

    write_summary_table(generate_table_data(I, x_lims, y_lims, image_stats),
                        pdf_pages)

    pdf_pages.close()
    print("QC sussefully generated at: ", outfile_path + "_agnostic_QC.pdf")
    return outfile_path + "_agnostic_QC.pdf"


def report_calibrant_qc(I,  # m2.imzMLReader (passing by ref allows faster computation)
                        outfile_path: str,  # path for output file
                        calfile_path: str,  # path to tsv file for calibrants
                        ppm: float,  # +- ppm cutoff for accuracy determination
                        sample_size: float = 1.0  # coverage of sample to be used for bulk calc, between 0 and 1
                        ) -> str:

    """
    Generates a QC report aimed at controling the accuracy of predefined mz values.
    Statistics show the raw data, accuracies and spatial distrbtuíon of these mz values.
    
    A report is created at output location with all calculated visualizations.


    Parameters
    ----------
    I : 
        A m2aia.ImzMLReader image object, or similar
    outfile_path : string
        Path to filename where the pdf output file should be built.
    calfile_path : str
        Path to csv file containing annotations of singals to monitor.
        File must use ";" as delimiter. The column annotaions "mz" and "name" must be used.
    ppm : float
        The allowed accuracy cutoff. Given in ppm.
    sample_size: : float
        Percentage of sample that is plotted in the raw data overview. Between 0 and 1.
        

    Returns
    -------
    output_file : str
        File path as string of succesfully generated calibrant QC pdf report.
    """

    #  read in the calibrants
    calibrants = read_calibrants(calfile_path, ppm)

    # Create a PDF file to save the figures
    pdf_pages = make_pdf_backend(outfile_path, "_calibrant_QC")

    # Make a subsample to test accuracies on
    randomlist = make_subsample(I.GetNumberOfSpectra(), sample_size)

    # create format flag dict to check formatting of imzML file
    format_flags = evaluate_formats(I.GetSpectrumType())

    # get the image limits to crop and display only relevant parts
    x_lims, y_lims = evaluate_image_corners(I.GetMaskArray()[0])

    # per calibrant, bulk data is calculated inside the randomlist subsample
    for i in range(len(calibrants)):
        # adressing the field in df: calibrants.loc[i, "name"]

        # Create the data points for calibrant bulk accuracy cals
        cal_spectra = extract_calibrant_spectra(I, calibrants.loc[i, "mz"], randomlist, calibrants.loc[i, "interval"])

        # compute the metrics for bulk calibrant accuracies
        calibrants = collect_calibrant_stats(cal_spectra, calibrants, i)

        # plot the spectral data of a calibrant
        plot_calibrant_spectra(cal_spectra,
                               calibrants, i,
                               format_flags,
                               pdf_pages)

    # barplot of the accuracies
    plot_accuracy_barplots(calibrants, pdf_pages)

    # calculate per pixel for nearest loc-max the accuracy
    accuracy_images, pixel_order = collect_accuracy_stats(I, calibrants, format_flags)

    # calculate coverage from accuracy images
    calibrants = collect_calibrant_converage(accuracy_images, calibrants, ppm)

    # calculate the DBSCAN clustering for dynamic coloring
    # calibrants = collect_dynamic_cmaps(accuracy_images, calibrants, ppm)

    # make accuracy images
    plot_accuracy_images(I, accuracy_images, calibrants, ppm, pixel_order, x_lims, y_lims, pdf_pages)

    # plot the accuracy boxplots.
    plot_accuracy_boxplots(accuracy_images, calibrants, ppm, pdf_pages)

    # sanitize randomlist
    clean_rndlist = check_uniform_length(I, randomlist)

    # visualize random pixel position (black, red, green)

    # get the spacings of each pseudobins
    mean_bin, intra_bin_spread, inter_bin_spread = evaluate_group_spacing(I, clean_rndlist)

    # visualize the spread
    plot_bin_spreads(mean_bin, intra_bin_spread, inter_bin_spread, pdf_pages)

    # sumamary with coverage and avg. accuracy in non-zero pixels
    write_calibrant_summary_table(calibrants, pdf_pages)

    pdf_pages.close()
    print("QC sussefully generated at: ", outfile_path + "_calibrant_QC.pdf")
    return outfile_path + "_calibrant_QC.pdf"


def report_regions_qc(I,  # m2.imzMLReader (passing by ref allows faster computation)
                      outfile_path: str,  # path for output file
                      regionfile_path: Union[str,bool] = False,  # path to tsv file for region annotation
                      ) -> str:

    """
    Generates a QC report aimed at controlling differences in regions of interest.
    Statistics show the raw data, based on annotated regions.
    
    A report is created at output location with all calculated visualizations.


    Parameters
    ----------
    I : 
        A m2aia.ImzMLReader image object, or similar
    outfile_path : string
        Path to filename where the pdf output file should be built.
    regionfile_path: str, Optinal
        Path to tsv file containing annotations of regions of interest.
        The column names "x", "y" and "annotation" must be used.
        If left unspecified, ROIs are automatically generated by connected component analysis.


    Returns
    -------
    output_file : str
        File path as string of succesfully generated pdf report.
        Automatic ROI annotations are also saved in this location.
    """

    # Create a PDF file to save the figures
    pdf_pages = make_pdf_backend(outfile_path, "_region_QC")

    # get the image limits to crop and display only relevant parts
    x_lims, y_lims = evaluate_image_corners(I.GetMaskArray()[0])

    # create format flag dict to check formatting of imzML file
    format_flags = evaluate_formats(I.GetSpectrumType())

    # parse the regionAnnotations:
    if regionfile_path:
        # readable to get dataFrame, col=0 x , col1= y, clo2= name
        region_table, region_image, nr_regions = parse_regionfile(regionfile_path, "annotation", I)
    else:
        region_table, region_image, nr_regions = label_connected_region(
            I)  # in nothing provides, make the conCompAnalysis
        write_region_tsv(region_table, outfile_path)

    # from annotation, get unique names in list()

    # additioally, get unique colors to correspond to the regions (neither white nor black)

    # plot the whole binary image
    image_cropped_binary(I.GetMaskArray()[0],
                         pdf_pages, x_lims, y_lims)

    # Plot the regions as colored blobs
    image_regions(region_image, I.GetMaskArray()[0], nr_regions,
                  pdf_pages, x_lims, y_lims)

    # intensity boxplot analysis
    # collect the metrics
    image_stats = collect_image_stats(I, ['index_nr', 'tic_nr'])

    # get the data grouped by annotation column:
    names_tic_bp, tic_bp = group_region_stat(region_image, I.GetIndexArray()[0], nr_regions, image_stats, "tic_nr")

    # plot the grouped data in a boxplot
    plot_boxplots(names_tic_bp, tic_bp,
                  'Boxplots of TIC per pixel by segmented group',
                  'Index of group',
                  'log10 of TIC intensity per pixel',
                  pdf_pages)

    # collect average spectra per region
    region_spectra = collect_region_averages(I, format_flags, region_image, nr_regions)

    # plot the averaged spectra of each region
    plot_regions_averages(region_spectra, format_flags, nr_regions, pdf_pages)

    #plot region difference spectra to first region
    plot_regions_difference(region_spectra, format_flags, nr_regions, pdf_pages)

    # show spectral coveraage per mean spectrum
    plot_spectral_coverages(region_spectra, format_flags, nr_regions, pdf_pages)

    plot_region_noise(region_spectra, format_flags, nr_regions, noise_ivl=2, pdf=pdf_pages)

    pdf_pages.close()
    print("QC sussefully generated at: ", outfile_path + "_region_QC.pdf")
    return outfile_path + "_region_QC.pdf"
