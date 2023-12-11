import numpy as np

mz_start = 10
mz_end = 20
bin_nr = (mz_end - mz_start) * 1


pixels = [(np.array([10, 10.23, 14.05,19.99]), np.array([15, 14.0,4.2,2])),
          (np.array([10.23, 15.1, 15.2]), np.array([15.0,4.2, 3.9])),
          (np.array([10.23, 16.01]), np.array([16.0,4.2]))]

n = len(pixels)

# set up the collection df for the binned ranges:
bins = np.linspace(mz_start, mz_end, num=bin_nr, endpoint=False)
print(bins)
# array for collection of intensity values
collector_array = np.full(bin_nr, np.nan)
print(collector_array)

# make a loop:
for mz, ints in pixels:

    # mzs and ints of the pixel
    # mz, ints = Image.GetSpectrum(idx)

    # Digitize the data into bins
    bin_indices = np.digitize(mz, bins) -1
    print(bin_indices)

    # Calculate the sum of intensities within each bin
    bin_sums = np.bincount(bin_indices, weights=ints, minlength=bin_nr)

    # means of grouped bins and normalized to pixels
    collector_array[bin_indices] = np.nansum([bin_sums[bin_indices], collector_array[bin_indices]], axis=0)


# filter out NaN values and normalize over n
bins = bins[~np.isnan(collector_array)]
collector_array = collector_array[~np.isnan(collector_array)] / n

print(bins, collector_array)