
# namespace and import declaration
import m2aia as m2
import numpy as np
import pandas as pd

import matplotlib as mpl
mpl.use('svg')

import matplotlib.backends as mpb
import matplotlib.pyplot as plt # best to shoot for 3.5.3 to resolve userwarings
import matplotlib.cm as cm
import matplotlib.ticker as ticker
import matplotlib.backends.backend_pdf
from mpl_toolkits.axes_grid1 import make_axes_locatable

import random as rnd
import statistics as stat

import scipy.stats as SST
import scipy.signal as SSI
from scipy.signal import argrelextrema, find_peaks, find_peaks_cwt

#import skimage.measure as skim
#from sklearn.cluster import DBSCAN

# imports for type linting
from typing import Optional, Union, Callable

# argparse for cli tools
import argparse as argparse

# namespace availabiliy of modifed ImzMLWriter
from pyimzml.ImzMLWriter import ImzMLWriter



import warnings as warm
# catch of FutueWarnings (looking at you, pandas  )
warm.simplefilter(action='ignore', category=FutureWarning)
# catch of plt decrep warning (honestly, they have no docs on implementing the required_interactive_framework i could find )
warm.filterwarnings(action="ignore", category=mpl.MatplotlibDeprecationWarning)

