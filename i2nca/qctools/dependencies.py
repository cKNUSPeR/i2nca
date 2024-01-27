
# namespace and import declaration
import matplotlib.backends as mpb
import m2aia as m2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt # best to shoot for 3.5.3 to resolve userwarings
import matplotlib.cm as cm
import matplotlib.ticker as ticker
import matplotlib.backends.backend_pdf

import random as rnd
import statistics as stat

import scipy.stats as SST
import scipy.signal as SSI
from scipy.signal import argrelextrema

import skimage.measure as skim
from sklearn.cluster import DBSCAN


import warnings
# catch of FutueWarnings (looking at you, pandas  )
warnings.simplefilter(action='ignore', category=FutureWarning)
