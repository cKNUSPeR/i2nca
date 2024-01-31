from scipy.signal import find_peaks
import numpy as np
import matplotlib.pyplot as plt

def add_four(a,b,c,d):
    return a+b+c+d

add_preset = lambda x,y: add_four(x,y, 3, 14)

print(add_preset(1,2))


def my_function(b):
    def inner_function(a):
        inout(a, b)
    return inner_function


def inout(x, y):
    print("inner:", str(x))
    print("outer:", str(y))


print(my_function(3)(8))
###

# Define parameters
s_mz = np.linspace(520, 580, 1000)  # Mass-to-charge ratio range
peak1_intensity = np.exp(-(s_mz - 540) ** 2 / (2 * 2 ** 2))  # Gaussian peak 1
peak2_intensity = np.exp(-(s_mz - 550) ** 2 / (2 * 2 ** 2))  # Gaussian peak 2
peak3_intensity = np.exp(-(s_mz - 560) ** 2 / (2 * 2 ** 2))  # Gaussian peak 3

# Combine intensities
s_intensity = peak1_intensity + peak2_intensity + peak3_intensity

# Plot the mass spectrum
plt.plot(s_mz, s_intensity)
plt.xlabel('Mass-to-Charge Ratio (m/z)')
plt.ylabel('Intensity')
plt.title('Simulated Mass Spectrum with Gaussian Peaks')
plt.grid(True)



####



def set_peak_finding(height=None,
                   threshold=None,
                   distance=None,
                   prominence=None,
                   width=None,
                   wlen=None,
                   rel_height=0.5,
                   plateau_size=None):
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


default_find_locmax = lambda mz, ints: set_peak_finding(height=0.4,
                                                distance=5)(mz, ints)


mz_cent, int_cent = default_find_locmax(s_mz, s_intensity)


plt.scatter(mz_cent, int_cent, c="r")
plt.show()