
import subprocess

from i2nca.qctools.dependencies import *

from i2nca import report_pp_to_cp, write_pp_to_cp_imzml

# instance the parser
parser = argparse.ArgumentParser()

# register the positional arguments
parser.add_argument("input_path", help="Path to imzML file.")
parser.add_argument("output", help="Path to output file.")

#register optional arguments:
parser.add_argument("--cov", help="Coverage used for the reference mz axis calculation.", default= 0.05, type=float)
parser.add_argument("--bsl", help="m2aia Baseline Correction", default="None")
parser.add_argument("--bsl_hws", help="m2aia Baseline Correction Half Window Size", default= 50, type=int)
parser.add_argument("--nor", help="m2aia Normalization", default="None")
parser.add_argument("--smo", help="m2aia Smoothing", default="None")
parser.add_argument("--smo_hws", help="m2aia Smoothing Half Window Size", default=2, type=int)
parser.add_argument("--itr", help="m2aia Intensity Transformation", default="None")

# parse arguments from CLI
args = parser.parse_args()

# parse dataset
Image = m2.ImzMLReader(args.input_path,
                   args.bsl, args.bsl_hws,
                   args.nor,
                   args.smo, args.smo_hws,
                   args.itr)

"""
baseline_correction: m2BaselineCorrection = "None",
                 baseline_correction_half_window_size: int = 50,
                 normalization: m2Normalization = "None",
                 smoothing: m2Smoothing = "None",
                 smoothing_half_window_size: int = 2,
                 intensity_transformation: m2IntensityTransformation = "None",
"""


# get the refernce mz value
ref_mz = report_pp_to_cp(Image, args.output, args.cov)

# write the continous file
write_pp_to_cp_imzml(Image, ref_mz, args.output)

# CLI command
# [python instance] [file.py]  --cov [1] --bsl [Median] --bsl_hws [20] --nor [RMS] --smo [Gaussian]  --smo_hws [3] --itr [Log2] [input_path] [output]
# C:\Users\Jannik\.conda\envs\QCdev\python.exe C:\Users\Jannik\Documents\Uni\Master_Biochem\4_Semester\QCdev\src\i2nca\i2nca\workflows\CLI\calibrant_qc_cli.py --ppm 50 --sample_size 1  C:\Users\Jannik\Documents\Uni\Master_Biochem\4_Semester\QCdev\src\i2nca\i2nca\tests\testdata\cc.imzML C:\Users\Jannik\Documents\Uni\Master_Biochem\4_Semester\QCdev\src\i2nca\i2nca\tests\tempfiles\empty C:\Users\Jannik\Documents\Uni\Master_Biochem\4_Semester\QCdev\src\i2nca\i2nca\tests\testdata\calibrant.csv