from .dependencies import *


# M2aia-independent tools
def evaluate_formats(file_format  # metadata_string
                     ):
    """Evaluates a file format string and return a dict of flags."""

    # instance flags dict
    flags = dict()

    # check for different flags
    if "Profile" in file_format:
        flags["profile"] = True
        flags["centroid"] = False
    elif "Centroid" in file_format:
        flags["profile"] = False
        flags["centroid"] = True
    else:
        raise ValueError(
            "The loaded file has an undefined spectrum type.\n Please check for accessions 'MS:1000128' or 'MS:1000127'")

    if "Processed" in file_format:
        flags["processed"] = True
        flags["continuous"] = False
    elif "Continuous" in file_format:
        flags["processed"] = False
        flags["continuous"] = True
    else:
        raise ValueError(
            "The loaded file has an undefined alignment type.\n Please check for accessions 'IMS:1000030' or 'IMS:1000031'")

    return flags


def evaluate_image_corners(ndarray):
    """Givel the values of the corners of the pixel-filled ndarray """
    pix_pos = np.argwhere(ndarray)
    offset = 0.5  # 0.5 makes plt plots better as it offsets the pixel centering

    # get the corners of data entry, is useful to set limits of plotting
    x_min = pix_pos[np.argmin(pix_pos[:, 1])][1] - offset
    x_max = pix_pos[np.argmax(pix_pos[:, 1])][1] + offset
    y_min = pix_pos[np.argmin(pix_pos[:, 0])][0] - offset
    y_max = pix_pos[np.argmax(pix_pos[:, 0])][0] + offset

    return (x_min, x_max), (y_min, y_max)


def make_index_image(Image):
    """handler for creating a valid index image in which invalid pixels get set to -1 to allow better display.
    return only x-y dimension."""

    index_array = np.subtract(Image.GetMaskArray().astype(np.int_), 1)
    index_array = index_array + Image.GetIndexArray()
    return index_array[0]


def mask_bad_image(key_list,  # an iterable of valid pixel indices,
                   val_list,  # an iterable of projected Intensities, matched to key_list
                   image  # An array-like object with the given distribution of key variables
                   ):
    """make a mask approach to plot any feature based on mapping onto existing image array with a translation apporach.
    It transfers pixels from 0 (in binary image input ) to NaN, which allows them to be set to bad"""
    # set up a translational dictionary
    trans_dict = dict(zip(key_list, val_list))
    # was once Important zero-index conversion, otherwise rounding gives error
    trans_dict[-1] = np.nan  # changed for now, lets see what new undefined pixels look like

    # defines the callable function (juhu, we love functional programming
    translate = np.vectorize(lambda ele: trans_dict.get(ele, ele))

    return translate(image)


def calc_accuraciues(found_mz, theo_mz, mask):
    """Calculate the ppm accuracy of a list of found peaks comparative to a set of theroetical masses and a binary mask"""
    ppm = []
    for o, t, m in zip(found_mz, theo_mz, mask):
        if m:
            ppm.append(np.abs((o - t) / t * 10 ** 6))
    return ppm


# M2aia-dependant tools


def label_connected_region(Image):
    labeled_image, max_regions = label_connected_components(Image.GetMaskArray()[0], connectivity=1)

    # shape of image array:
    rows, cols = labeled_image.shape
    # get a meshed grid to make x-y accesible
    x_coords, y_coords = np.meshgrid(range(cols), range(rows))

    # make a dataframe
    df = pd.DataFrame({'x': x_coords.flatten(), 'y': y_coords.flatten(), 'annotation': labeled_image.flatten()})
    # remove 0-entries (they represent empty pixels)
    df = df.loc[df["annotation"] > 0]


    return df, labeled_image, max_regions

# helper function to remove skimage dependency

def label_connected_components(binary_image, connectivity=1):
    """
    Labels connected components in a binary image.

    Parameters:
        binary_image (ndarray): The binary image to be labeled.
        connectivity (int): The connectivity to use (1 for 4-connectivity, 2 for 8-connectivity).

    Returns:
        labeled_image (ndarray): The labeled image where each connected component has a unique label.
        num_features (int): The number of connected components.
    """
    # checks the connectivity
    def get_neighbors(r, c):
        if connectivity == 1:
            return [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
        elif connectivity == 2:
            return [(r - 1, c - 1), (r - 1, c), (r - 1, c + 1),
                    (r, c - 1), (r, c + 1),
                    (r + 1, c - 1), (r + 1, c), (r + 1, c + 1)]

    # fill for one blob
    def flood_fill(r, c, label):
        stack = [(r, c)]
        while stack:
            x, y = stack.pop()
            if labeled_image[x, y] == 0 and binary_image[x, y] == 1:
                labeled_image[x, y] = label
                for nx, ny in get_neighbors(x, y):
                    if 0 <= nx < binary_image.shape[0] and 0 <= ny < binary_image.shape[1]:
                        stack.append((nx, ny))

    labeled_image = np.zeros_like(binary_image, dtype=int)
    # zero already given
    label = 1

    for row in range(binary_image.shape[0]):
        for col in range(binary_image.shape[1]):
            if binary_image[row, col] == 1 and labeled_image[row, col] == 0:
                flood_fill(row, col, label)
                label += 1

    # reduce for final label_increase
    num_features = label - 1
    return labeled_image, num_features

def parse_regionfile(file, annotation_group, image):
    """parses the regions tsv file. Assumes that the regions are annotated
    within the coordinates of the imaging file (the point of origin is at (0,0))."""

    # mark invariants of "x", "y" , "annotation"
    df = pd.read_csv(file, sep="\t", header=0)

    # translate the annotation to values starting from 1
    try:
        df['annotation_values'] = pd.factorize(df[annotation_group])[0] + 1
    except KeyError:
        raise KeyError('The supplied annotation file does not have the required column heads.'
                       'These columns are required: [x    y    annotation ]')

    # the maximum number of regions (counting starts at 1)
    max_regions = df['annotation_values'].max()

    # get the shape
    x_lims = (0, image.GetShape()[0])
    y_lims = (0, image.GetShape()[1])

    # set up empty array with xlims any ylims ranges
    labeled_image = np.zeros((y_lims[1] - y_lims[0], x_lims[1] - x_lims[0]))  # 0-indexed

    # fill the labeled image with the annotations:
    for index, row in df.iterrows():
        x, y = row['x'], row['y']
        labeled_image[y, x] = row['annotation_values']  # Set pixel to annotation group

    return df, labeled_image, max_regions


def write_region_tsv(df, path):
    """writes a region pd.df to a tsv for reimport later."""
    file_name = path + "annotated_regions.tsv"
    df.to_csv(file_name, sep="\t", columns=["x", "y", "annotation"], index=False)


def group_region_stat(labeled_image, index_image, label_nr, image_stats, keyword):
    """Groups the statistics of a region into a list of lists.
    Input:
    - labeled_image: An image-like array containing the regions labeled with a non-zero int
    - index_image: An image-like array containing the pixel index
    - image_stats: a dict of image statistics per pixel as tuple, accessible by keywords
    -keyword: the keyword for which data is collected (eg. tic_nr)
    - label_nr: the number of labeled regions

    Output:
    - tuple(list[int], list[list]: Tuple with names and statistics:
    ordered in list order of keywords (currently hardcoded)

    """

    # linear reshaping of pixel index image and segmented image
    lab_ar = np.reshape(labeled_image, -1)
    ind_ar = np.reshape(index_image, -1)

    # arrayization of pixel index counting and TICperPixel counting
    # via np.asarray(image_stats["index_nr"]), best to do inplace

    # collectors for plotable boxplot data
    # collectors for plotable boxplot data
    stat_coll_boxplot = []
    name_coll_boxplot = []

    # loop over all segments
    for seg in range(1, label_nr + 1):
        stat_nr_arr = np.asarray(image_stats[keyword])
        ind_nr_array = np.asarray(image_stats["index_nr"])

        pindex = ind_ar[np.where(lab_ar == seg)]  # extracion of pixel indices per segment

        col = stat_nr_arr[np.isin(ind_nr_array, pindex)]  # extraction of tics from pixel index
        col = np.log2(col)

        stat_coll_boxplot.append(col)
        name_coll_boxplot.append(seg)

    return name_coll_boxplot, stat_coll_boxplot


def collect_region_averages(Image, format_dict, regions_image, region_number):
    """handler for collection of mean spectra of different regions"""
    lab_ar = np.reshape(regions_image, -1)
    ind_ar = np.reshape(Image.GetIndexArray()[0], -1)

    averaged_spectra = []

    # get the mz dim to be constant over full comparison
    min_mz, max_mz = int(np.floor(min(Image.GetXAxis()))), int(np.ceil(max(Image.GetXAxis())))
    # get the spacing in 1/100 per unit m/z value in mz range
    spacing = (max_mz - min_mz) * 100


    for index in range(1, region_number + 1):
        # get the index per segment
        pindex = ind_ar[np.where(lab_ar == index)]  # extracion of pixel indices per segment

        # make averages
        if format_dict["continuous"]:
            avg_mz, avg_ints = average_cont_spectra(Image, pindex)
        elif format_dict["processed"]:
            avg_mz, avg_ints = average_processed_spectra(Image, pindex, spacing)

        # collect averaged spectra
        averaged_spectra.append((avg_mz, avg_ints))

    return averaged_spectra


def average_cont_spectra(Image, pixels):
    """
    Input:
    - sequence of pixel indices
    :return:
    array of mz, array of intensities
    """
    # get lngth
    n = len(pixels)

    # get first element
    mz, ints = Image.GetSpectrum(pixels[0])
    ints = ints / n

    # iterate over remaining elements
    for idx in pixels[1:]:
        _, intensity = Image.GetSpectrum(idx)
        intensity = intensity / n
        ints = np.add(ints, intensity)

    return mz, ints


def average_processed_spectra(Image, pixels, bin_nr=0):
    """Averages processed spectra by their pixels.
    Calculates a mz window with start, end and stepsize and bins the data into this.
    the amount of bins is equal to 10 times the highest number of datapoints recorded.
    Masses are returned to the head of their respective bin.
    Input:
        - Image: an m2aia imzML reader
        - pixels: a sequence of pixel indices
        - bins: a predetermined number of bins,
            if =0 then this gets dynamically assumed to be 10 times the size of the most data point occurence
    returns:
        mzs, ints
        two arrays with mz values and intensity values of the respective average
    """
    # get the normalization numbers
    n = len(pixels)

    # get the mz value range, floored and ceiled to fix the edge values
    mz_start, mz_end = np.floor(min(Image.GetXAxis())), np.ceil(max(Image.GetXAxis()))  # minimum is reduced by a bit.

    if bin_nr == 0:
        # get the number of bins (estimation by getting the largest number of spectra in the file)
        for ids in pixels:
            cbin_nr = Image.GetSpectrumDepth(ids)
            if cbin_nr > bin_nr:
                bin_nr = cbin_nr
        # binning is enhanced by factor of 10, to counteract spectral pixelation
        bin_nr = bin_nr * 10

    # set up the collection df for the binned ranges:
    bins = np.linspace(mz_start, mz_end, num=bin_nr, endpoint=False)

    # array for collection of intensity values
    collector_array = np.full(bin_nr, np.nan)

    # make a loop:
    for idx in pixels:
        # mzs and ints of the pixel
        mz, ints = Image.GetSpectrum(idx)

        # Digitize the data into bins
        bin_indices = np.digitize(mz, bins) - 1
        # needs to be recuced by 1

        # Calculate the sum of intensities within each bin
        bin_sums = np.bincount(bin_indices, weights=ints, minlength=bin_nr)

        # means of grouped bins and normalized to pixels
        collector_array[bin_indices] = np.nansum([bin_sums[bin_indices], collector_array[bin_indices]], axis=0)

    # filter out NaN values and normalize over n
    bins = bins[~np.isnan(collector_array)]
    collector_array = collector_array[~np.isnan(collector_array)] / n

    return bins, collector_array


def calculate_spectral_coverage(mz_values, intensities):
    """
    calulates how much signal is recorded in a portion of the spectrum.
    Cuts spectrum into bins of 100mz or 10mz, depending of input range.
    output is percentage of Total Ion signal in that range

    :param mz_values: array-like, set of mz values
    :param intensities: array-like, intensities corresponding to mz values

    :returns

    bins : array
     center of bins used for cutting the data
    coverage: array
     the coverage in spectral bin
    """
    min_mz = np.floor(min(mz_values))
    max_mz = np.ceil(max(mz_values))
    mz_range = int(max_mz - min_mz)

    # dynamic scaling
    if mz_range < 200:
        # binsize of 10
        bin_size = 10
        bin_nr = mz_range // bin_size if mz_range % bin_size == 0 else mz_range // bin_size + 1
        bins = [min_mz + i * bin_size for i in range(bin_nr + 1)]

    else:
        # binsize of 100
        bin_size = 100
        bin_nr = mz_range // bin_size if mz_range % bin_size == 0 else mz_range // bin_size + 1
        bins = [min_mz + i * bin_size for i in range(bin_nr + 1)]

    # set up a dataframe
    df = pd.DataFrame({'mz': mz_values, "intensity": intensities})
    # normalize to TIC
    df["intensity"] = df["intensity"] / sum(intensities)
    # sort into bins
    df['binned'] = pd.cut(mz_values, bins)

    # sum per bin
    coverage = df.groupby(['binned'])['intensity'].sum().to_numpy()

    # last bin (right index) is dropped
    bins = bins[:-1]
    return bins, coverage


def read_calibrants(filepath: str, ppm_cutoff: float):
    """Reads calibrant files and gives a list of name and thr. mz values
    INVARIANTS: Needs a header column with 'name' and a col with 'mz'."""
    cal = pd.read_csv(filepath, sep=';', header=0)
    cal["found"] = np.NaN
    cal["value_wavg"] = np.NaN
    cal["distance_wavg"] = np.NaN
    cal["value_map"] = np.NaN
    cal["distance_map"] = np.NaN
    cal["coverage"] = np.NaN
    # cal["accuracy_llimits"] = np.NaN
    # cal["accuracy_ulimits"] = np.NaN

    # some oneliner magic to ease applying a function to a df
    calc_dist_ivl = lambda x: x * ppm_cutoff / 1e6

    cal["interval"] = cal["mz"].apply(calc_dist_ivl)
    return cal


def make_subsample(samplenumber: int, percent_sample: float) -> list:
    """Makes a subsample out of the samplenumber with the given percentage (as float)"""
    # Determine the size of a batch
    batch_size = int(samplenumber * percent_sample)
    # get random numbers according to the batch size
    return rnd.sample(range(0, samplenumber), batch_size)


def find_nearest_centroid(mzs, value, distance=0):
    """search in distance interval and return the mz of the value nearest to the specified value"""

    if distance != False:
        try:
            lindex = min(np.where(mzs > (value - distance))[0])
            hindex = min(np.where(mzs > (value + distance))[0])
        except:
            return value + 2 * distance  # invalid pixels get defaulted to be twice the distance
    else:
        lindex = 0
        hindex = len(mzs)

    mzs = np.asarray(mzs)[lindex:hindex]

    if len(mzs) == 0:  # stop caculation and return out-of-distacne value
        return value + 2 * distance  # invalid pixels get defaulted to be +1

    idx = (np.abs(mzs - value)).argmin()
    return mzs[idx]


def find_nearest_loc_max(mzs, intensites, value, distance=0):
    """Finds the nearest local maxima of a profile line to a certain mass.
    It disqualifies local maxima that are below 1 % of the highest point found inside the specified range.
    If no distance is specified, the search is applied to the whole spectrum.

    """

    try:
        lindex = min(np.where(mzs > (value - distance))[0])
        hindex = min(np.where(mzs > (value + distance))[0])
    except:
        return value + 2 * distance  # invalid pixels get defaulted to be +1
    else:
        lindex = 0
        hindex = len(mzs)

    # ensure arrayztion for mapping and slice array for shorter calc time
    intensites = np.asarray(intensites)[lindex:hindex]
    mzs = np.asarray(mzs)[lindex:hindex]

    if len(mzs) == 0:  # stop caculation and return out-of-distacne value
        return value + 2 * distance  # invalid pixels get defaulted to be +1

    # get local maxima indices
    max_index = SSI.argrelextrema(intensites, np.greater)
    # and detuple this
    max_index = max_index[0]

    # get all the values from max_index
    locmax_ints = intensites[max_index]
    # and the maximaum intensity found
    max_intensity = max(locmax_ints)
    # get all the intensity indices where the locmax_intensity surpasses 1% of max intensity
    max_index = max_index[np.where(locmax_ints >= max_intensity * 0.01)]

    # get values of those local maxima

    mzs = mzs[max_index]
    idx = (np.abs(mzs - value)).argmin()
    return mzs[idx]


def extract_calibrant_spectra(Image, cal_mass, subsample, mz_bin):
    """Read the full image. Collects the spectral data for a given mass in the given mz bin."""
    accu_list = [[], []]
    # accu_list[0] is a list with mz values in np.arrays
    # accu_list[1] is a list with mz values in np.arrays

    # looping over sample
    for ind in subsample:
        mass, intensity = Image.GetSpectrum(ind)
        try:
            # mindex needs to be inclusive
            mindex = min(np.where(mass > (cal_mass - mz_bin))[0])
            mindex_flag = True
        except:
            mindex_flag = False
        try:
            # maxdex needs to be exclusive
            maxdex = min(np.where(mass > (cal_mass + mz_bin))[0])
            maxdex_flag = True
        except:
            maxdex_flag = False

        # pixels are only written if there is data present in the specified part
        if maxdex_flag and mindex_flag:
            # collecting of masses and intensities
            mass_adder, int_adder = mass[mindex:maxdex], intensity[mindex:maxdex]
            accu_list[0].append(mass_adder)
            accu_list[1].append(int_adder)
        elif mindex_flag and not maxdex_flag:
            mass_adder, int_adder = mass[mindex:], intensity[mindex:]
            accu_list[0].append(mass_adder)
            accu_list[1].append(int_adder)
        elif not mindex_flag and maxdex_flag:
            mass_adder, int_adder = mass[:maxdex], intensity[:maxdex]
            accu_list[0].append(mass_adder)
            accu_list[1].append(int_adder)


    return accu_list


def collect_calibrant_stats(cal_spectra, calibrant_df, index):
    """collects bulk statistics of the calibrants. Adds to the provided df the following infos:
    0) df["found"]: Whether spectral data was found for the mass
    1) cal["value_wavg"]: the value of the weighted average
    2) cal["distance_wavg"]: the distance in ppm of weight. avg to the theo. mz
    3) cal["value_map"]: the value of the most abundant peak in interval
    4) cal["distance_map"]: the distance in ppm of m.a.p. to the theo. mz
    # defunc.) the nearest local maxima to the calibrant mass.
    """

    # deep-copy the df (it gets mutated over function call)
    calibrant_df = calibrant_df.copy(deep=True)


    # extraction of most Abundant Peaks and peak centers and their validity
    # check if there are any pixels
    if len(cal_spectra[1]) > 0:

        mz_vals = np.concatenate(cal_spectra[0], axis=0)
        int_vals = np.concatenate(cal_spectra[1], axis=0)
        # check length in each pixel
        if len(int_vals) > 0:

            # peak with hightest intensity
            most_abundant_peak = mz_vals[np.where(int_vals == max(int_vals))][0]

            # weighted average of mz values weighted by their intensity
            wavg = np.ma.average(mz_vals, weights=int_vals)

            # update the dataframe
            calibrant_df.loc[index, "found"] = True
            calibrant_df.loc[index, "value_wavg"] = wavg
            calibrant_df.loc[index, "value_map"] = most_abundant_peak

            # calculate distane ppm
            calibrant_df.loc[index, "distance_wavg"] = calculate_ppm(wavg, calibrant_df.loc[index, "mz"])
            calibrant_df.loc[index, "distance_map"] = calculate_ppm(most_abundant_peak, calibrant_df.loc[index, "mz"])

        else:
            calibrant_df.loc[index, "found"] = False
            # values are not updated, NaN signifies non-found peaks

    else:
        calibrant_df.loc[index, "found"] = False
        # values are not updated, NaN signifies non-found peaks

    return calibrant_df


def calculate_disance(theo_mass,
                      ppm_cutoff: float):
    """calcualtes the distance in delmz for a given mass and ppm"""
    return theo_mass * ppm_cutoff / 1e6


def calculate_ppm(exp_mass,
                  theo_mass: float):
    """Calulates ppm of na experimental mass againt a theoretical mass.
    Input:
        - exp_mass: observed mz as float
        - theo_mass: theoretical mz value as flaot
    :return
        - ppm value: float
    """
    return ((exp_mass - theo_mass) / theo_mass) * 1e6


def collect_accuracy_stats(Image, calibrants_df, format_dict):
    """ Finds and collects the nearest signals around all provided calibrant masses.
    Input:
        - Image: ImzMLReader object
        - calibrants_df: dataframe of calibrant information
        - format_dict: dict of imzML formats to handle signal evaluation

    :returns  accuracies_ar, index_nr
    accuracies_ar: the array for the data of accurasies per pixels, linearized images, index by calibrants as dim1 and pixel by dim2
    index_nr: tuple of pixel indix sorted to match the shape of accuracies_ar

    """
    # make a matrix for each pixel and
    accuracies_ar = np.zeros((Image.GetNumberOfSpectra(), len(calibrants_df["name"])))
    index_nr = tuple()  # container for pixel index, corrected for 0-index

    if format_dict["centroid"]:
        for ind, mass, inten in Image.SpectrumIterator():  # loop to run over full imzML dataset
            # get nearest elements
            accuracies_ar[ind] = [find_nearest_centroid(mass, calmass, dist) for calmass, dist in
                                  zip(calibrants_df["mz"], calibrants_df["interval"])]
            # collect image index in order of iteration
            index_nr = index_nr + (ind,)  # pixel order is 0 in new m2aia version


    elif format_dict["profile"]:
        for ind, mass, inten in Image.SpectrumIterator():  # loop to run over full imzML dataset
            # get nearest loc, max
            accuracies_ar[ind] = [find_nearest_loc_max(mass, inten, calmass, dist) for calmass, dist in
                                  zip(calibrants_df["mz"], calibrants_df["interval"])]
            # collect image index in order of iteration
            index_nr = index_nr + (ind,)  # pixel order is 0 from m2aia 0.5.0 onw

    # transpose to match  ppm calcs form
    accuracies_ar = accuracies_ar.T

    # convert the mass into ppm ranges
    for i, mass in enumerate(calibrants_df["mz"]):
        accuracies_ar[i] = calculate_ppm(accuracies_ar[i], mass)

    return accuracies_ar, index_nr


def collect_calibrant_converage(accuracy_images, calibrants_df, accuracy_cutoff):
    """Evalualtes how many pixels within a accuracy image fall outsde of the defined accuracy cutoff.
    saves these into the calibrant_df as converage, normed on the amount of pixels."""

    # 2DO change so that coverage gets dynamically calculated
    # deep-copy the df
    calibrant_df = calibrants_df.copy(deep=True)

    # loop over the calibrants
    for i, mass in enumerate(calibrant_df["mz"]):
        # count how many values are larger than higher cutoff cutoff:
        high_dist = np.sum(accuracy_images[i] > +accuracy_cutoff)
        # count how many values are lower  than lowest cutoff value:
        low_dist = np.sum(accuracy_images[i] < -accuracy_cutoff)

        # add to calibrants_df
        calibrant_df.loc[i, "coverage"] = (low_dist + high_dist)

    # divide over number of pixels
    pixel_nr = len(accuracy_images[0])
    # normalize over pixel number and
    calibrant_df["coverage"] = calibrant_df["coverage"] / pixel_nr
    # take difference of 1 to get actual coverage
    calibrant_df["coverage"] = 1 - calibrant_df["coverage"]
    return calibrant_df


"""def collect_dynamic_cmaps(accuracy_images, calibrants_df, accuracy_cutoff):
    # cool but sadly decrep.
    'Dynamically calculates range of interest for cmapping for each calibrant.
    This is achieved by using DBSCAN to cluster the data, and then get the cluster nearest to 0 ppm.
    The color range is adapted to include 0 for ease of readablility'

    # copy df for
    calibrant_df = calibrants_df.copy(deep=True)

    # Access an accuracy image as linear dataset for DBSCAN
    for i, mass in enumerate(calibrant_df["mz"]):
        # 'linearization of image
        dataset = accuracy_images[i].reshape(-1, 1)

        # 'evaluate DBSCAN parameters
        min_samples = 2  # 2*dim with dim = 1 for lineraized data
        eps = accuracy_cutoff * 2  # twice the accuracy cutoff for full window

        # 'perform clustering
        db = DBSCAN(eps=eps, min_samples=min_samples).fit(dataset)
        unique_labels = set(db.labels_)

        # 'acess unique labes
        cluster_mean = []
        cluster_limits = []

        for label in unique_labels:
            if label != -1:  # noise points labeled as -1

                # ''get the mean, minimal and maximal points of the cluster
                cluster_points = dataset[db.labels_ == label]
                cluster_mean.append(np.mean(cluster_points, axis=0))
                cluster_limits.append((min(cluster_points), max(cluster_points)))

        # 'calc the distance of mean to 0 and get index of minimal distane
        idx = (np.abs(np.asarray(cluster_mean) - 0)).argmin()

        # 'get the (min,max) cluster limits
        i_min, i_max = cluster_limits[idx]

        # 'check if 0-offsetting is needed and return them to df
        if i_min < 0 and i_max < 0:
            # if both below 0
            i_max = 0
        elif i_min > 0 and i_max > 0:
            i_min = 0

        # 'enter them them to df
        calibrant_df.loc[i, 'accuracy_llimits'] = i_min
        calibrant_df.loc[i, 'accuracy_ulimits'] = i_max

    return calibrant_df"""

def collect_image_stats(Image, statistic_keywords):
    """ Expensive function to call. iterates over the full spectrum and returns the specified metrics.
    Input:
        -Image: a m2aia ImzML reader
        -statistic_keywords: a controlled set of keyword strings
            The following keywords are supported:
            ['index_nr', 'peak_nr', 'tic_nr', 'median_nr', 'max_int_nr', 'min_int_nr', 'max_mz_nr', 'min_mz_nr', 'max_abun_nr']

    Output:
        -dict[keyword] -> tuple: a dict with tuples of the required statistic per pixel.
    """
    # Create a dictionary to store the results for each statistic
    statistics_result = {keyword: () for keyword in statistic_keywords}

    for ind, mass, inten in Image.SpectrumIterator():  # loop to run over the full imzML dataset
        for keyword in statistic_keywords:
            if keyword == 'index_nr':
                statistics_result[keyword] += (ind,)  # index of spectrum is now zero-based
            elif keyword == 'peak_nr':
                statistics_result[keyword] += (len(inten),)
            elif keyword == 'tic_nr':
                statistics_result[keyword] += (sum(inten),)
            elif keyword == 'median_nr':
                statistics_result[keyword] += (stat.median(inten),)
            elif keyword == 'max_int_nr':
                statistics_result[keyword] += (max(inten),)
            elif keyword == 'min_int_nr':
                statistics_result[keyword] += (min(inten),)
            elif keyword == 'max_mz_nr':
                statistics_result[keyword] += (max(mass),)
            elif keyword == 'min_mz_nr':
                statistics_result[keyword] += (min(mass),)
            elif keyword == 'max_abun_nr':
                max_abun_index = np.where(inten == max(inten))[0][0]
                statistics_result[keyword] += (mass[max_abun_index],)

    return statistics_result


def generate_table_data(Image, x_limits, y_limits, im_stats):
    table = [
        ["Spectral Type:", str(Image.GetSpectrumType())],
        ["Numeric shape of Image (x, y, z):", str(Image.GetShape())],
        ["Number of recorded Pixels:", str(Image.GetNumberOfSpectra())],
        ["Number of unrecorded Pixels:", str(np.abs(np.product(Image.GetShape()) - Image.GetNumberOfSpectra()))],
        ["mz range:", str((min(im_stats['min_mz_nr']), max(im_stats['max_mz_nr'])))],
        ["Spacing:", str(Image.GetSpacing())],
        # ["m/z Bins:", str(Image.GetXAxisDepth())],
        ["Intensity range:", str((min(im_stats['min_int_nr']), max(im_stats['max_int_nr'])))],
        ["Number of individual data points:", str(np.sum(im_stats['peak_nr']))],
        ["Mean number of data points per pixel ± sd:",
         str(f"{int(stat.mean(im_stats['peak_nr']))} ± {int(stat.stdev(im_stats['peak_nr']))}")],
        ["Median number of data points per pixel ± MAD:",
         str(f"{int(stat.median(im_stats['peak_nr']))} ± {int(SST.median_abs_deviation(im_stats['peak_nr']))}")],
        ["Mean TIC ± sd:", str(f"{int(stat.mean(im_stats['tic_nr']))} ± {int(stat.stdev(im_stats['tic_nr']))}")],
        ["Median TIC ± MAD:",
         str(f"{int(stat.median(im_stats['tic_nr']))} ± {int(SST.median_abs_deviation(im_stats['tic_nr']))}")],
        ["Range of median intensities per pixel:", str((min(im_stats['median_nr']), max(im_stats['median_nr'])))],
        ["Range of maximal intensity per pixel:", str((min(im_stats['max_int_nr']), max(im_stats['max_int_nr'])))],
        ["Range of most abundant mz per pixel:", str((min(im_stats['max_abun_nr']), max(im_stats['max_abun_nr'])))],

    ]
    return table


def collect_noise(mz_vals, int_vals, mz_window_halfsize, theta_threshold=0.001, alpha=1):
    """Noise estimation with simga-clipping function.
    PErforms noise estimation in int steps along the provided mz axis.

     Output:
     - median of estimated noise
     - std-dev of noise median
     - mz steps, useful for plotting
     """
    mz_start = np.floor(min(mz_vals))
    mz_end = np.ceil(max(mz_vals))

    #
    mz_steps = np.arange(mz_start, mz_end + 1)
    medians = np.zeros(len(mz_steps))
    stds = np.zeros(len(mz_steps))
    # get window
    for i, mass in enumerate(mz_steps):
        lower_lim = mass - mz_window_halfsize
        upper_lim = mass + mz_window_halfsize

        # bitwise addition for final mask
        mask = np.bitwise_and(mz_vals > lower_lim, mz_vals < upper_lim)

        # cut the windows
        mz_window = mz_vals[mask]
        int_window = int_vals[mask]

        # test here if mz_window actually contains n>1 elements, else everything is 0
        if len(mz_window) < 2:
            medians[i] = 0
            stds[i] = 0
            continue  # continue with next iteration

        # get median and std.dev
        median_old = stat.median(int_window)
        std_dev_old = stat.stdev(int_window)

        # instance sigma_threshold
        theta = 1

        # sigma-clip in action
        while theta > theta_threshold:
            # get the interval
            l_lim = median_old - alpha * std_dev_old
            u_lim = median_old + alpha * std_dev_old

            # bitwise addition for final mask
            mask = np.bitwise_and(int_window > l_lim, int_window < u_lim)

            # keep only values in interval
            mz_window = mz_window[mask]
            int_window = int_window[mask]

            # stop recursion for either one or zero value case
            if len(int_window) == 1:
                # one value remains, it gets returned with +- 0
                median_old = int_window[0]
                std_dev_old = 0
                break

            elif len(mz_window) == 0:
                # no values remain, last value gets returned
                break

            median_new = stat.median(int_window)
            std_dev_new = stat.stdev(int_window)

            # recursion stop when std_dev_new is 0
            if std_dev_new == 0:
                median_old = median_new
                std_dev_old = std_dev_new
                break

            theta = (std_dev_old - std_dev_new) / std_dev_new
            median_old = median_new
            std_dev_old = std_dev_new

        # get the old_values
        medians[i] = median_old
        stds[i] = std_dev_old

    return medians, stds, mz_steps


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

    # collect at least one
    if len(randomlist) == 0:
        randomlist.append(0)

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


def evaluate_polarity(Image):
    """Evaluates the m2aia image to return a polarity dict
    allowed keywords are "positive" and "negative"
    """

    metadata = Image.GetMetaData()

    polarity_dict = {
        "positive": False,
        "negative": False
    }

    try:
        if metadata["[MS:1000129] spectrum1.negative scan"] == "true":
            polarity_dict["negative"] = True
    except:
        pass

    try:
        if metadata["[MS:1000130] spectrum1.positive scan"] == "true":
            polarity_dict["positive"] = True
    except:
        pass

    if polarity_dict["negative"] == False and polarity_dict["positive"] == False:
        raise ValueError(f"The provided dataset has no defined polarity. \n"
                         f" Check the [MS:1000129] and [MS:1000130] assencions.")

    return polarity_dict


def get_polarity(polarity_dict):
    """Getter for ploarity dict."""
    if polarity_dict["negative"] == True:
        return "negative"
    elif polarity_dict["positive"] == True:
        return "positive"
    else:
        raise ValueError(f"The provided dataset has no defined polarity. \n"
                         f" Check the [MS:1000129] and [MS:1000130] assencions.")


def get_pixsize(Image):
    """ Getter for pixel size.
    Evaluates the m2aia image to return a pixel size
    Looks wonky to avoid misrepresentation
    """

    metadata = Image.GetMetaData()

    try:
        x_size = float(metadata['[IMS:1000046] pixel size x'])
        # m2aia 0.5.1 gives pixel size in cm and not in um
        x_size = x_size * 1000
    except:
        raise ValueError(f"The provided dataset has no x pixel size. \n"
                         f" Check the [IMS:1000046] assencion.")

    try:
        y_size = float(metadata["[IMS:1000047] pixel size y"])
        # m2aia 0.5.1 gives pixel size in cm and not in um
        y_size = y_size * 1000
    except:
        raise ValueError(f"The provided dataset has no y pixel size. \n"
                         f" Check the [IMS:1000047] assencion.")

    if x_size == y_size:
        return str(int(x_size))
    else:
        raise AssertionError(f"The provided dataset has non-sqare pixel sizes. \n"
                             f" That sucks. This is not yet implemented ")
