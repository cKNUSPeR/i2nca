
import subprocess

from i2nca.qctools.dependencies import *

from i2nca import cut_dataset_imzml

# instance the parser
parser = argparse.ArgumentParser()

# register positional arguments
parser.add_argument("input_path", help="Path to imzML file.")
parser.add_argument("output", help="Path to output file.")
parser.add_argument("region_path", help="Path to csv file containing annotations of signals to monitor.")

# parse arguments from CLI
args = parser.parse_args()

# cut the file into different regions
cut_dataset_imzml(args.input_path,args.region_path, args.output)