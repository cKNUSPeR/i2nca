
import subprocess

from i2nca.qctools.dependencies import *

from i2nca import report_regions_qc

# instance the parser
parser = argparse.ArgumentParser()

# register positional arguments
parser.add_argument("input_path", help="Path to imzML file.")
parser.add_argument("output", help="Path to output file.")
parser.add_argument("region_path", help="Path to csv file containing annotations of signals to monitor.")

# parse arguments from CLI
args = parser.parse_args()

# parse dataset
I = m2.ImzMLReader(args.input_path)
# report QC
report_regions_qc(I, args.output, args.region_path)

# CLI command
# [python instance] [file.py]  [input_path] [output] [region_path]
