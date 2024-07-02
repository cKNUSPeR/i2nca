"""inca - INteractive quality Control and Assesment using m2aia"""

__author__ = "Jannik Witte"

__version__ = "0.2.9"

# registery of main function for i2nca namespace, each defined over their own group.

from i2nca.main import get_version

from i2nca.qctools import *

from i2nca.convtools import *

# from i2nca.brukertools import *

# bruker tools are excluded here. checkout the branch "bruker inclusive" to get acces to these functions.


