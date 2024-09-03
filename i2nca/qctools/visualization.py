from i2nca.dependencies.dependencies import *
from .utils import mask_bad_image, average_cont_spectra, average_processed_spectra, calculate_spectral_coverage, \
    make_index_image, collect_noise, sanizite_image

# custom colormaps with white backgrounds (via out-of-lower-bound)
my_vir = cm.get_cmap('viridis').copy()
my_vir.set_under('white')  # Color for values less than vmin
my_vir.set_bad(color='white', alpha=1.0)

my_rbw = cm.get_cmap('gist_rainbow').copy()
my_rbw.set_under('white')  # Color for values less than vmin
my_rbw.set_bad('white')

my_coolwarm = cm.get_cmap('coolwarm').copy()
my_coolwarm.set_under('white')  # Color for values less than vmin
my_coolwarm.set_over('darkorange')

my_cw = cm.get_cmap('coolwarm').copy()
my_cw.set_under('dimgrey')  # Color for values less than vmin
my_cw.set_over('dimgrey')
my_cw.set_bad(color='white', alpha=1.0)


def discrete_cmap(n, base_cmap=None, nan_color="white"):
    """Create an N-bin discrete colormap from the specified input map"""

    # Note that if base_cmap is a string or None, you can simply do
    #    return plt.cm.get_cmap(base_cmap, N)
    # The following works for string, None, or a colormap instance:

    base = plt.cm.get_cmap(base_cmap)
    color_list = base(np.linspace(0, 1, n))

    # Set the color for np.nan values
    nan_color_value = plt.cm.colors.to_rgba(nan_color)
    nan_color_list = [nan_color_value] * int(np.isnan(n).sum())

    color_list = np.concatenate((color_list, nan_color_list))

    cmap_name = base.name + str(n)
    return base.from_list(cmap_name, color_list, n + len(nan_color_list))


def make_pdf_backend(report_path, title):
    pdf_file_path = report_path + title + ".pdf"
    pdf_pages = mpb.backend_pdf.PdfPages(pdf_file_path)
    return pdf_pages


def image_full_binary(Image, pdf):
    """plots a binary image of the imaging run with the origin coordinates
        Saves this plot to a pdf."""

    fig = plt.figure(figsize=[7, 5])
    ax = plt.subplot(111)

    ax.set_xlabel('x axis')
    ax.set_ylabel('y axis')
    ax.set_title('Full view of binary image from origin')
    ax.imshow(Image,
              cmap=my_vir, vmin=-0.5,
              interpolation='none',  # attention, large images tend to get a smoohing under the hood by plt
              origin='lower')
    pdf.savefig(fig)
    plt.close()


def image_cropped_binary(Image, pdf, x_limits, y_limits):
    """generates a plot of binary image cropped to size.
    This behavior is somewhat redundant with m2aia0.5 onwards
        Saves the plot to a pdf"""

    fig = plt.figure(figsize=[7, 5])
    ax = plt.subplot(111)

    ax.set_xlabel('x axis')
    ax.set_ylabel('y axis')
    ax.set_xlim(x_limits[0], x_limits[1])
    ax.set_ylim(y_limits[0], y_limits[1])
    ax.set_title('Cropped view of binary image within pixel limits')
    ax.imshow(Image,
              cmap=my_vir, vmin=-0.5,
              interpolation='none',
              origin='lower')
    pdf.savefig(fig)
    plt.close()


def image_pixel_index(image, binary_mask, pdf, x_limits, y_limits):
    """generates a plot of the index of each pixel. Image cropped to size.
        Saves the plot to a pdf"""

    fig = plt.figure(figsize=[7, 5])
    ax = plt.subplot(111)

    ax.set_title('Index of pixel')
    ax.set_xlabel('x axis')
    ax.set_ylabel('y axis')
    ax.set_xlim(x_limits[0], x_limits[1])
    ax.set_ylim(y_limits[0], y_limits[1])

    # cleanup with binary mask
    image_masked = np.ma.masked_where(binary_mask == 0, image)

    im = ax.imshow(image_masked,
                   cmap=my_rbw, vmin=-0.1, interpolation='none')

    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    fig.colorbar(im, extend='min', cax=cax)

    pdf.savefig(fig)
    plt.close()


def image_regions(regionarray, binary_mask, max_nr_region, pdf, x_limits, y_limits):
    """Images the annotated regions image as colorful blops-
    # 0 as non-recorded pixels, 1 as non-annotated pixels, 2-> end for
    # add numbers written on the pixel centra (with black border and their resp. color fill0)"""
    fig = plt.figure(figsize=[7, 5])
    ax = plt.subplot(111)

    ax.set_title('Connected Objects Analysis')
    ax.set_xlabel('x axis')
    ax.set_ylabel('y axis')

    image_masked = np.ma.masked_where(binary_mask == 0, regionarray)

    im = ax.imshow(image_masked,  # cmap=discrete_cmap(max_nr_region, my_rbw, "white"),
                   cmap=my_rbw,
                   vmin=-0.1, interpolation='none', origin='lower')
    # extent=[x_limits[0], x_limits[1], y_limits[0], y_limits[1]])

    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    fig.colorbar(im, extend='min', format=lambda x, _: f"{int(x)}", label="Index of group", cax=cax)

    pdf.savefig(fig)
    plt.close()


def plot_basic_scatter(x, y,
                       title, x_lab, y_lab,
                       pdf):
    """makes a simple scatterplot, functional template"""
    fig = plt.figure(figsize=[7, 5])
    ax = plt.subplot(111)

    ax.set_title(title)
    ax.set_xlabel(x_lab)
    ax.set_ylabel(y_lab)
    ax.grid(visible=True, c='lightgray', ls="--")

    ax.scatter(x, y, color='k', marker=".", zorder=-1)
    ax.set_rasterization_zorder(0)

    pdf.savefig(fig)
    plt.close()



def image_basic_heatmap(Image,
                        title, x_lab, y_lab,
                        pdf, x_limits, y_limits):
    """makes basic heatmap, intended as functional template"""
    fig = plt.figure(figsize=[7, 5])
    ax = plt.subplot(111)

    ax.set_title(title)
    ax.set_xlabel(x_lab)
    ax.set_ylabel(y_lab)
    ax.set_xlim(x_limits[0], x_limits[1])
    ax.set_ylim(y_limits[0], y_limits[1])

    im = ax.imshow(Image, cmap=my_vir, vmin=-0.1)

    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    fig.colorbar(im, cax=cax, extend='min')

    pdf.savefig(fig)
    plt.close()


def plot_feature_number(image_stats, pdf):
    """plot a scatterplot for the number of feautes per pixel"""
    plot_basic_scatter(image_stats["index_nr"], image_stats["peak_nr"],
                       "Number of data points per pixel",
                       "Index of pixel",
                       "Number of data points",
                       pdf)


def image_feature_number(image_stats, Image, pdf, x_limits, y_limits):
    """Images a heatmap of the number of features. Image cropped to size.
        Saves the plot to a pdf"""
    image_basic_heatmap(mask_bad_image(image_stats["index_nr"], image_stats["peak_nr"], make_index_image(Image)),
                        'Number of data points per pixel projection',
                        "x axis",
                        "y axis",
                        pdf, x_limits, y_limits)


def plot_tic_number(image_stats, pdf):
    """plot a scatterplot for the Total Ion Count per pixel"""
    plot_basic_scatter(image_stats["index_nr"], image_stats["tic_nr"],
                       "TIC per pixel",
                       "Index of pixel",
                       "Intensity",
                       pdf)


def image_tic_number(image_stats, Image, pdf, x_limits, y_limits):
    """Images a heatmap of the TIC. Image cropped to size.
        Saves the plot to a pdf"""
    image_basic_heatmap(mask_bad_image(image_stats["index_nr"], image_stats["tic_nr"], make_index_image(Image)),
                        'TIC per pixel projection',
                        "x axis",
                        "y axis",
                        pdf, x_limits, y_limits)


def plot_max_abun_number(image_stats, pdf):
    """plot a scatterplot for the Highest abundance mz value per pixel"""
    plot_basic_scatter(image_stats["index_nr"], image_stats["max_abun_nr"],
                       "Most abundand mz value per pixel",
                       "Index of pixel",
                       "m/z",
                       pdf)


def image_max_abun_number(image_stats, Image, pdf, x_limits, y_limits):
    """Images a heatmap of the Highest abundance mz  value. Image cropped to size.
        Saves the plot to a pdf"""
    image_basic_heatmap(mask_bad_image(image_stats["index_nr"], image_stats["max_abun_nr"], make_index_image(Image)),
                        'Most abundand mz value per pixel projection',
                        "x axis",
                        "y axis",
                        pdf, x_limits, y_limits)


def plot_median_number(image_stats, pdf):
    """plot a scatterplot for the median intensity per pixel"""
    plot_basic_scatter(image_stats["index_nr"], image_stats["median_nr"],
                       "Median intensity per pixel",
                       "Index of pixel",
                       "Intensity",
                       pdf)


def image_median_number(image_stats, Image, pdf, x_limits, y_limits):
    """Images a heatmap of the median intensity. Image cropped to size.
        Saves the plot to a pdf"""
    image_basic_heatmap(mask_bad_image(image_stats["index_nr"], image_stats["median_nr"], make_index_image(Image)),
                        'Median intensity per pixel projection',
                        "x axis",
                        "y axis",
                        pdf, x_limits, y_limits)


def plot_max_int_number(image_stats, pdf):
    """plot a scatterplot for the maximal intensity per pixel"""
    plot_basic_scatter(image_stats["index_nr"], image_stats["max_int_nr"],
                       "Maximal intensity per pixel",
                       "Index of pixel",
                       "Intensity",
                       pdf)


def image_max_int_number(image_stats, Image, pdf, x_limits, y_limits):
    """Images a heatmap of the maximal intensity. Image cropped to size.
        Saves the plot to a pdf"""
    image_basic_heatmap(mask_bad_image(image_stats["index_nr"], image_stats["max_int_nr"], make_index_image(Image)),
                        'Maximal intensity per pixel projection',
                        "x axis",
                        "y axis",
                        pdf, x_limits, y_limits)


def plot_min_int_number(image_stats, pdf):
    """plot a scatterplot for the minimal intensity per pixel"""
    plot_basic_scatter(image_stats["index_nr"], image_stats["min_int_nr"],
                       "Minimal intensity per pixel",
                       "Index of pixel",
                       "Intensity",
                       pdf)


def image_min_int_number(image_stats, Image, pdf, x_limits, y_limits):
    """Images a heatmap of the minimal intensity. Image cropped to size.
        Saves the plot to a pdf"""
    image_basic_heatmap(mask_bad_image(image_stats["index_nr"], image_stats["min_int_nr"], make_index_image(Image)),
                        'Minimal intensity per pixel projection',
                        "x axis",
                        "y axis",
                        pdf, x_limits, y_limits)  #


def plot_max_mz_number(image_stats, pdf):
    """plot a scatterplot for the largest mz value per pixel"""
    plot_basic_scatter(image_stats["index_nr"], image_stats["max_mz_nr"],
                       "Maximal m/z value per pixel",
                       "Index of pixel",
                       "m/z",
                       pdf)


def image_max_mz_number(image_stats, Image, pdf, x_limits, y_limits):
    """Images a heatmap of the largest mz value. Image cropped to size.
        Saves the plot to a pdf"""
    image_basic_heatmap(mask_bad_image(image_stats["index_nr"], image_stats["max_mz_nr"], make_index_image(Image)),
                        'Maximal m/z value per pixel projection',
                        "x axis",
                        "y axis",
                        pdf, x_limits, y_limits)


def plot_min_mz_number(image_stats, pdf):
    """plot a scatterplot for the smallest mz value per pixel"""
    plot_basic_scatter(image_stats["index_nr"], image_stats["min_mz_nr"],
                       "Minimal m/z value per pixel",
                       "Index of pixel",
                       "m/z",
                       pdf)


def image_min_mz_number(image_stats, Image, pdf, x_limits, y_limits):
    """Images a heatmap of the smallest mz value. Image cropped to size.
        Saves the plot to a pdf"""
    image_basic_heatmap(mask_bad_image(image_stats["index_nr"], image_stats["min_mz_nr"], make_index_image(Image)),
                        'Minimal m/z value per pixel projection',
                        "x axis",
                        "y axis",
                        pdf, x_limits, y_limits)


def plot_centroid_spectrum(mz_axis, spectrum_data, title, pdf):
    fig = plt.figure(figsize=[10, 6])
    ax = plt.subplot(111)

    ax.set_title(title)
    ax.set_xlabel('m/z')
    ax.set_ylabel('Intensity')
    ax.set_xlim(min(mz_axis).round(0), max(mz_axis).round(0))

    ax.vlines(mz_axis, 0, spectrum_data, linewidth=0.8)
    ax.set_ylim(bottom=0)

    pdf.savefig(fig)
    plt.close()

def plot_centroid_difference_spectrum(spectrum_axis, spectrum_data, spectrum_id,
                                      ref_axis, ref_data, ref_id,
                                      title, pdf):
    fig = plt.figure(figsize=[10, 6])
    ax = plt.subplot(111)

    ax.set_title(title)
    ax.set_xlabel('m/z')
    ax.set_ylabel('Intensity')
    ax.set_xlim(min(spectrum_axis).round(0), max(spectrum_axis).round(0))

    ax.vlines(spectrum_axis, 0, spectrum_data, linewidth=0.8, color="blue",
              label=f"Centroid spectrum of region {spectrum_id}")
    ax.vlines(ref_axis, 0, -ref_data, linewidth=0.8, color="gray",
              label=f"Centroid spectrum of region {ref_id}")

    ax.legend()

    pdf.savefig(fig)
    plt.close()

def plot_profile_spectrum(mz_axis, spectrum_data, pdf):
    fig = plt.figure(figsize=[10, 6])
    ax = plt.subplot(111)

    ax.set_title('Averaged profile mass spectrum')
    ax.set_xlabel('m/z')
    ax.set_ylabel('Intensity')
    ax.set_xlim(min(mz_axis).round(0), max(mz_axis).round(0))

    ax.plot(mz_axis, spectrum_data, linewidth=0.8)
    ax.set_ylim(bottom=0)

    pdf.savefig(fig)
    plt.close()


def plot_profile_difference_spectrum(spectrum_axis, spectrum_data, spectrum_id,
                                      ref_axis, ref_data, ref_id,
                                      title, pdf):
    fig = plt.figure(figsize=[10, 6])
    ax = plt.subplot(111)

    ax.set_title(title)
    ax.set_xlabel('m/z')
    ax.set_ylabel('Intensity')
    ax.set_xlim(min(spectrum_axis).round(0), max(spectrum_axis).round(0))

    ax.plot(spectrum_axis, spectrum_data, linewidth=0.8, color="blue",
              label=f"Profile spectrum of region {spectrum_id}")
    ax.plot(ref_axis, -ref_data, linewidth=0.8, color="gray",
              label=f"Profile spectrum of region {ref_id}")

    ax.legend()

    pdf.savefig(fig)
    plt.close()

def plot_noise_spectrum(mz_axis, spectral_data, title, pdf):
    fig = plt.figure(figsize=[10, 6])
    ax = plt.subplot(111)

    ax.set_title(title)
    ax.set_xlabel('m/z')
    ax.set_ylabel('Intensity of noise level')
    ax.set_xlim(min(mz_axis).round(0), max(mz_axis).round(0))

    ax.plot(mz_axis, spectral_data, linewidth=0.8)
    ax.set_ylim(bottom=0)

    pdf.savefig(fig)
    plt.close()


def write_summary_table(table, pdf):
    # Create a figure and add the table
    fig = plt.figure(figsize=[10, 10])
    ax = plt.subplot(111)
    ax.axis("off")  # Turn off axis
    table = ax.table(cellText=table,
                     colLabels=["Property", "Values"],
                     loc="center", cellLoc="left")

    # Style the table
    table.auto_set_font_size(True)
    # table.set_fontsize(14)
    table.scale(1.2, 1.2)  # Adjust table scale for better layout
    # weird error, where some text is not getting passed

    pdf.savefig(fig, bbox_inches="tight")
    plt.close()


def write_calibrant_summary_table(data_frame, pdf):
    data_frame = data_frame.round({'mz': 6,
                                   'value_wavg': 6,
                                   'distance_wavg': 4,
                                   'value_map': 6,
                                   'distance_map': 4,
                                   'coverage': 2})

    # Create a figure and add the table
    fig = plt.figure(figsize=[10, 10])
    ax = plt.subplot(111)
    ax.axis("off")  # Turn off axis
    table = ax.table(cellText=data_frame.to_numpy(),
                     colLabels=data_frame.columns,
                     loc="center", cellLoc="center")

    # Style the table
    table.auto_set_font_size(True)
    # table.set_fontsize(12)
    table.scale(1.2, 1.2)  # Adjust table scale for better layout
    # weird error, where some text is not getting passed

    pdf.savefig(fig, bbox_inches="tight")
    plt.close()


def plot_boxplots(name_boxplot, stat_boxplot,
                  title, xlabel, ylabel,
                  pdf):
    # 2DO: scaling adjusted to 20, also parametrized with titles, and mabe make a subfunction for plotting
    len_b20 = len(name_boxplot) // 20
    if (len(name_boxplot) % 20) > 0:
        len_b20 = len_b20 + 1

    # plotting functions based on single-line or multi-line plotting:
    if len_b20 > 1:
        fig, ax = plt.subplots(len_b20, figsize=(10, len_b20 * 4))
        fig.suptitle(title)

        for j in range(1, len_b20 + 1):  # change to 1-base index
            ax[j - 1].boxplot(stat_boxplot[(j - 1) * 20:20 * j],
                              labels=name_boxplot[(j - 1) * 20:20 * j])
            ax[j - 1].set_xlabel(xlabel)
            ax[j - 1].set_ylabel(ylabel)

    else:
        fig = plt.figure(figsize=[10, len_b20 * 4])
        ax = plt.subplot(111)
        ax.set_title(title)

        ax.boxplot(stat_boxplot,
                   labels=name_boxplot)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)

    plt.tight_layout()
    pdf.savefig(fig)
    plt.close()


def plot_accuracy_boxplots(accuracy_images, calibrants_df, ppm_cutoff, pdf):
    names = calibrants_df["name"].to_list()

    # lambda magic to make a list of the accuracy values inside the ppm_cutoff range
    cleanup_row = lambda row: list(np.array(row)[(row >= -ppm_cutoff) & (row <= +ppm_cutoff)])

    accuracies = list(map(cleanup_row, accuracy_images))  # plt takes multi-dim data as list of vectors

    plot_boxplots(names, accuracies,
                  "Boxplot of mass accuracies within ppm interval by calibrant",
                  "Calibrant", "Accuracy in ppm", pdf)


def plot_regions_averages(regional_spectra, format_dict, region_number, pdf):
    """case handler to address coccrect plottig of averaged spectra."""

    for i in range(region_number):
        avg_mz, avg_ints = regional_spectra[i]
        if format_dict["centroid"]:
            plot_centroid_spectrum(avg_mz, avg_ints,
                                   f"Averaged centroid mass spectrum of group {i + 1}", pdf)
        elif format_dict["profile"]:
            plot_profile_spectrum(avg_mz, avg_ints, pdf)

def plot_regions_difference(regional_spectra, format_dict, region_number, pdf):
    """Helper to plot difference spectrum against first region"""

    for i in range(region_number):
        ref_mz, ref_ints = regional_spectra[0]
        avg_mz, avg_ints = regional_spectra[i]
        if format_dict["centroid"]:
            plot_centroid_difference_spectrum(avg_mz, avg_ints, i+1,
                                              ref_mz, ref_ints, 1,
                                            f"Spectral comparison of Region {i + 1} against {1}", pdf)
        elif format_dict["profile"]:
            plot_profile_difference_spectrum(avg_mz, avg_ints, i+1,
                                              ref_mz, ref_ints, 1,
                                            f"Spectral comparison of Region {i + 1} against {1}", pdf)


def old_plot_regions_average(Image, format_dict, regions_image, region_number, pdf):
    """
    decrepatated
    plot the average spectrum of each region of the regioned image as a spectrum plot.
    
    Input: 
        - image
        - format_flag
        - ragions_image
        
    Output:
        plot of mean in region, adapted to format flag. 
        Also, additional plotting of full mean spectrum in background (for later)
    """

    lab_ar = np.reshape(regions_image, -1)
    ind_ar = np.reshape(Image.GetIndexArray()[0], -1)

    for index in range(1, region_number + 1):
        # get the index per segment
        pindex = ind_ar[np.where(lab_ar == index)]  # extracion of pixel indices per segment

        # make averages
        if format_dict["continuous"]:
            avg_mz, avg_ints = average_cont_spectra(Image, pindex)

            if format_dict["centroid"]:
                plot_centroid_spectrum(avg_mz, avg_ints, "", pdf)
            elif format_dict["profile"]:
                plot_profile_spectrum(avg_mz, avg_ints, pdf)

        elif format_dict["processed"]:
            avg_mz, avg_ints = average_processed_spectra(Image, pindex)

            if format_dict["centroid"]:
                plot_centroid_spectrum(avg_mz, avg_ints, "", pdf)
            elif format_dict["profile"]:
                plot_profile_spectrum(avg_mz, avg_ints, pdf)


# plot functions for calibrant QC


def plot_calibrant_spectra(cal_spectra, calibrant_df, index, format_dict, pdf):
    """case handler for empty spectra"""

    if calibrant_df.loc[index, "found"]:
        # plot the calibrant spectra panel
        plot_calibrant_spectra_panel(cal_spectra, calibrant_df, format_dict, index, pdf)

    else:
        # plot an empty box
        plot_empty_peak(calibrant_df.loc[index, "mz"], calibrant_df.loc[index, "name"], pdf)


def plot_calibrant_spectra_panel(cal_spectra,
                                 calibrants_df, format_dict, index,
                                 pdf):
    """ Cal spectrum is the sliced variable of cal_spectra[i]
            # differentiante the plotting :
        # 1) with profile or centriod  map&wavg
        # 2) only data points + map&wavg
        # 3) zoom on minimal and maximal data points ()
        # 4) zoom of 150% around both metrics with only data points"""

    name = calibrants_df.loc[index, "name"]
    mass = calibrants_df.loc[index, "mz"]
    mapeak = calibrants_df.loc[index, "value_map"]
    wavg = calibrants_df.loc[index, "value_wavg"]
    dist = calibrants_df.loc[index, "interval"]

    # reconvert the cal_spectra to large array
    mz_vals = np.concatenate(cal_spectra[0], axis=0)
    int_vals = np.concatenate(cal_spectra[1], axis=0)

    fig = plt.figure(figsize=[10, 10])  # constrained_layout=True)

    # make the panel layout
    widths = [1, 1]
    heights = [1, 4, 4]
    spec5 = fig.add_gridspec(ncols=2, nrows=3, width_ratios=widths,
                             height_ratios=heights)

    # write the header box with info text --------------------------------------------------------------
    axbig = fig.add_subplot(spec5[0, 0:2])
    axbig.xaxis.set_major_locator(ticker.NullLocator())
    axbig.yaxis.set_major_locator(ticker.NullLocator())

    axbig.text(0.5, 0.5, f'Calibrant spectra for {name}', ha="center", va="bottom", size="x-large")
    axbig.text(0.025, 0.1, f"Theo. m/z: {mass:.6f}", ha="left", va="bottom", size="large", color="red")
    axbig.text(0.5, 0.1, f"Most abundant signal: {mapeak:.6f}", ha="center", va="bottom", size="large", color="green")
    axbig.text(0.975, 0.1, f"Weighted average: {wavg:.6f}", ha="right", va="bottom", size="large", color="purple")

    # plot of full data as  spectrum --------------------------------------------------------------
    ax1 = fig.add_subplot(spec5[1, 0])
    ax1.set_title(f'full spectrum\n around calibrant')
    ax1.set_xlabel('m/z')
    ax1.set_ylabel('Intensity')
    # set axis limits
    ax1.set_xlim(mass - dist, mass + dist)
    # set style of y-axis
    ax1.ticklabel_format(useOffset=False, )
    ax1.ticklabel_format(axis="y", style='sci', scilimits=(0, 0))
    # set x-axis style
    ax1.tick_params(axis="x", labelrotation=-45, top=False, reset=True)

    # draw metrics and masses
    draw_vertical_lines(mass, mapeak, wavg, ax1)

    if format_dict["centroid"]:
        # plot centroid spectrum
        ax1.vlines(mz_vals, 0, int_vals, color='k', linewidth=0.8, zorder=-1)
        ax1.scatter(mz_vals, int_vals, s=6, color='k', marker="o", zorder=-1)

    elif format_dict["profile"]:
        # plot profile spectrum
        for mzs, ints in zip(cal_spectra[0], cal_spectra[1]):
            ax1.plot(mzs, ints, color='k', linewidth=0.5, zorder=-1)
        ax1.scatter(mz_vals, int_vals, s=6, color='k', marker="o", zorder=-1)

    # adjust y limits
    ax1.set_ylim(bottom=0)

    # rasterisazion for better user exerience
    ax1.set_rasterization_zorder(0)

    # plot full spectra with only data points--------------------------------------------------------------
    ax2 = fig.add_subplot(spec5[1, 1])
    ax2.set_title(f'full spectrum,\n only data points')
    ax2.set_xlabel('m/z')
    ax2.set_ylabel('Intensity')
    # set the axis range and styles
    ax2.set_xlim(mass - dist, mass + dist)
    ax2.ticklabel_format(useOffset=False, )
    ax2.ticklabel_format(axis="y", style='sci', scilimits=(0, 0))
    # set x-axis style
    ax2.tick_params(axis="x", labelrotation=-45, top=False, reset=True)

    # draw metrics and masses
    draw_vertical_lines(mass, mapeak, wavg, ax2)

    # control block for plotting spectra
    if format_dict["centroid"]:
        # scatter centroid spectrum
        ax2.scatter(mz_vals, int_vals, color='k', marker="x", zorder=-1)

    elif format_dict["profile"]:
        # plot profile spectrum
        ax2.scatter(mz_vals, int_vals, color='k', marker="x", zorder=-1)

    # adjust y limits
    ax2.set_ylim(bottom=0)

    # rasterisazion for better user exerience
    ax2.set_rasterization_zorder(0)

    # plot the zoom to minimal and maximal data points --------------------------------------------------------------
    offset = 0.001
    ax3 = fig.add_subplot(spec5[2, 0])
    ax3.set_title(f'calibrant spectrum,\n zoomed to value range')
    ax3.set_xlabel('m/z')
    ax3.set_ylabel('Intensity')
    # set the axis range and styles
    ax3.set_xlim(min(mz_vals) - offset, max(mz_vals) + offset)
    ax3.ticklabel_format(useOffset=False, )
    ax3.ticklabel_format(axis="y", style='sci', scilimits=(0, 0))
    # set x-axis style
    ax3.tick_params(axis="x", labelrotation=-45, top=False, reset=True)

    # draw metrics and masses
    draw_vertical_lines(mass, mapeak, wavg, ax3)

    # control block for profile/centroid case
    if format_dict["centroid"]:
        # plot centroid spectrum
        ax3.vlines(mz_vals, 0, int_vals, color='k', linewidth=0.8, zorder=-1)
        ax3.scatter(mz_vals, int_vals, s=6, color='k', marker="o", zorder=-1)

    elif format_dict["profile"]:
        # plot profile spectrum
        for mzs, ints in zip(cal_spectra[0], cal_spectra[1]):
            ax3.plot(mzs, ints, color='k', linewidth=0.5, zorder=-1)
        ax3.scatter(mz_vals, int_vals, s=6, color='k', marker="o", zorder=-1)

    # adjust yaxis bottom
    ax3.set_ylim(bottom=0)

    # rasterisazion for better user exerience
    ax3.set_rasterization_zorder(0)

    # plot zoom with all metrics  -------------------------------------------------------------------------
    ax4 = fig.add_subplot(spec5[2, 1])
    # get closest metric
    metrics = [calibrants_df.loc[index, "distance_map"], calibrants_df.loc[index, "distance_wavg"]]
    # get the farthest bulk metric
    closest = max(metrics, key=abs)

    # get the interval width (overscaled to 150%)
    interval = abs((mass * (closest * 1e-6 + 1) - mass) * 1.5)

    ax4.set_title(f'calibrant spectrum,\n zoomed to metrics')
    ax4.set_xlabel('m/z')
    ax4.set_ylabel('Intensity')
    # set the axis range and styles
    ax4.set_xlim(mass - interval, mass + interval)
    ax4.ticklabel_format(useOffset=False, )
    ax4.ticklabel_format(axis="y", style='sci', scilimits=(0, 0))
    # set x-axis style
    ax4.tick_params(axis="x", labelrotation=-45, top=False, reset=True)

    # draw metrics and masses
    draw_vertical_lines(mass, mapeak, wavg, ax4)

    # control block for profile/centroid case
    if format_dict["centroid"]:
        # scatter centroid spectrum
        ax4.vlines(mz_vals, 0, int_vals, color='k', linewidth=0.8, zorder=-1)
        ax4.scatter(mz_vals, int_vals, s=6, color='k', marker="o", zorder=-1)

    elif format_dict["profile"]:
        # plot profile spectrum
        for mzs, ints in zip(cal_spectra[0], cal_spectra[1]):
            ax4.plot(mzs, ints, color='k', linewidth=0.5, zorder=-1)
        ax4.scatter(mz_vals, int_vals, s=6, color='k', marker="o", zorder=-1)

    # adjust y limits
    ax4.set_ylim(bottom=0)

    # rasterisazion for better user exerience
    ax4.set_rasterization_zorder(0)

    fig.tight_layout()
    pdf.savefig(fig)
    plt.close()


def plot_empty_peak(cal_mass, cal_name, pdf):
    fig = plt.figure(figsize=[10, 10])
    ax = plt.subplot(111)
    # offset for text annotations
    ax.set_xlim(0, 2)
    ax.set_ylim(0, 2)
    ax.set_xticks([])
    ax.set_yticks([])

    ax.set_title(f'calibrant spectra for {cal_name}')
    ax.text(1, 1, f'no peak data found \n for {cal_mass} \n in specified coverage interval',
            ha='center', fontsize=12)
    pdf.savefig(fig)
    plt.close()


def draw_vertical_lines(mass, mapeak, wavg, axes):
    # make a line of theoretical mass
    axes.axvline(mass, c='r', ls=(0, (1, 3)))
    # make a line for most abundant peak
    axes.axvline(mapeak, color='green', ls=(0, (2, 4)))
    # make a line for weighted average
    axes.axvline(wavg, c='purple', ls=(0, (3, 4, 1, 4, 1, 4)))


def plot_accuracy_barplots(calibrant_df, pdf):
    """handler for plots of barplot for different metrics:
        currently supported: - map,
                             - wavg
    """

    kw_list = ["distance_map", "distance_wavg"]
    color_list = ['green', "purple"]
    title_list = ["most abundant peak", "weigthed average"]

    for i, key in enumerate(kw_list):
        # drop invalid rows
        df = calibrant_df.copy(deep=True)
        df.dropna(subset=[key])

        # plot the accuracy plots
        plot_accu_barplot(df["name"], df[key],
                          title_list[i], color_list[i],
                          pdf)


def plot_accu_barplot(names, values, metric_name, color, pdf):
    """Makes a bar plot of a given accuracy metric.
    only plots existing values."""

    y_pos = np.arange(len(names))

    fig = plt.figure(figsize=[10, 7])
    ax = plt.subplot(111)

    ax.set_title(f'mass accuracy of calibrants ({metric_name} vs theoretical)')
    ax.set_xlabel('Calibrant')
    ax.set_ylabel('Mass accuracy in ppm')
    ax.set_xticks(y_pos)
    ax.set_xticklabels(names, rotation=-45, fontsize=8)
    # add a zero line
    ax.axhline(0, c='k', ls='--')

    bars = ax.bar(y_pos, values, color=color)
    # annotate the bar chart data on the data
    for bar in bars:
        height = bar.get_height()
        if height >= 5:
            ax.annotate(f'{height:.4f}', xy=(bar.get_x() + bar.get_width() / 2, height), xytext=(0, -15),
                        textcoords="offset points", ha='center', va='bottom')
        else:
            ax.annotate(f'{height:.4f}', xy=(bar.get_x() + bar.get_width() / 2, height), xytext=(0, +3),
                        textcoords="offset points", ha='center', va='bottom')

    fig.tight_layout()
    pdf.savefig(fig)
    plt.close()


def plot_accuracy_images(Image, accuracy_images, calibrants_df, ppm, index_nr, x_limits, y_limits, pdf):

    for i, mass in enumerate(calibrants_df["mz"]):
        img = mask_bad_image(index_nr, accuracy_images[i], make_index_image(Image), use_nan=True)
        if calibrants_df.loc[i, "found"]:
            # plot the calibrant spectra panel
            plot_accuracy_image_distribution(Image, img, calibrants_df, ppm, i, x_limits, y_limits, pdf)
            plot_intensity_image_distribution(Image, calibrants_df, ppm, i, x_limits, y_limits, pdf)

        else:
            # plot an empty box
            plot_empty_peak(calibrants_df.loc[i, "mz"], calibrants_df.loc[i, "name"], pdf)
            # Todo: add string for title to correct



def plot_accuracy_image_distribution(Image, accuracy_image, calibrants_df, ppm, calibrant_index,  x_limits, y_limits, pdf):
    """Makes accuracy heatmaps per pixel ofthe found calibrant accuracy."""
    # loop over the calibrants

    # plot each image
    fig = plt.figure(figsize=[7, 5])
    ax = plt.subplot(111)
    ax.set_title(f'Mass accuracy of {calibrants_df.loc[calibrant_index, "mz"]}, ({calibrants_df.loc[calibrant_index, "name"]})')
    ax.set_xlabel('x axis')
    ax.set_ylabel('y axis')

    ax.set_xlim(x_limits[0], x_limits[1])
    ax.set_ylim(y_limits[0], y_limits[1])
    im = ax.imshow(accuracy_image, cmap=my_cw,
                   vmin=-ppm,
                   vmax=+ppm)

    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    fig.colorbar(im, extend='both', label="ppm", cax=cax)

    pdf.savefig(fig)
    plt.close()


def plot_intensity_image_distribution(Image, calibrants_df, ppm, calibrant_index, x_limits, y_limits,
                                             pdf):
    fig = plt.figure(figsize=[7, 5])
    ax = plt.subplot(111)
    ax.set_title(f'Intensity of {calibrants_df.loc[calibrant_index, "mz"]} ± {ppm} ppm, ({calibrants_df.loc[calibrant_index, "name"]})')
    ax.set_xlabel('x axis')
    ax.set_ylabel('y axis')

    ax.set_xlim(x_limits[0], x_limits[1])
    ax.set_ylim(y_limits[0], y_limits[1])
    im = ax.imshow(sanizite_image(Image, Image.GetArray(calibrants_df.loc[calibrant_index, "mz"], tol=ppm)[0], use_nan=True),
                   cmap=my_vir)

    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    fig.colorbar(im, extend='min', label="Intensity", cax=cax)
    pdf.savefig(fig)
    plt.close()



def plot_region_noise(region_spectra, format_flags, nr_regions, noise_ivl, pdf):
    " handler for noise estiamtion per regional mean spectrum"
    for i in range(nr_regions):
        avg_mzs, avg_ints = region_spectra[i]
        noise_medain, _, noise_axis = collect_noise(avg_mzs, avg_ints, noise_ivl)
        plot_noise_spectrum(noise_axis, noise_medain,
                            f'Noise estimation within interval of {2 * noise_ivl} in group {i + 1}', pdf)


def plot_spectral_coverages(region_spectra, format_flags, nr_regions, pdf):
    """handler for spectral coverage of each mean spectrum """
    for i in range(nr_regions):
        avg_mzs, avg_ints = region_spectra[i]
        mean_bin, mean_coverage = calculate_spectral_coverage(avg_mzs, avg_ints)
        plot_coverage_barplot(mean_bin, mean_coverage,
                              f'Spectral coverage of mean spectrum in group {i + 1}', pdf)


def plot_coverage_barplot(names, data, title, pdf):
    """Makes a bar plot of a given spectral coverage.
    """

    y_pos = np.arange(len(names))

    fig = plt.figure(figsize=[7, 5])
    ax = plt.subplot(111)

    ax.set_title(title)
    ax.set_xlabel('m/z bin')
    ax.set_ylabel('Contribution to TIC')
    ax.set_xticks(y_pos)
    ax.set_xticklabels(names, rotation=-45, fontsize=8)

    bars = ax.bar(y_pos, data, width=0.95, color="blue")

    # making the bar chart on the data
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.4f}', xy=(bar.get_x() + bar.get_width() / 2, height), xytext=(0, 3),
                    textcoords="offset points", ha='center', va='bottom')

    plt.tight_layout()
    pdf.savefig(fig)
    plt.close()


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

