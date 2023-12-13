
# namespace and import declaration
import matplotlib.backends as mpb
import m2aia as m2
import numpy as np
import matplotlib.pyplot as plt # best to shoot for 3.5 to resolve userwarings
import matplotlib.cm as cm
import random as rnd
import statistics as stat
import scipy.stats as SST
import scipy.signal as SSI
import skimage.measure as skim
import pandas as pd
import matplotlib.ticker as ticker
import warnings
from scipy.signal import argrelextrema
import matplotlib.backends.backend_pdf
from sklearn.cluster import DBSCAN

# catch of FutueWarnings (looking at you, pandas  )
warnings.simplefilter(action='ignore', category=FutureWarning)
