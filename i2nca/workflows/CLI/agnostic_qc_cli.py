
import subprocess

from i2nca.qctools.dependencies import *

from i2nca import report_agnostic_qc

# instance the parser
parser = argparse.ArgumentParser()

# register the positional arguments
parser.add_argument("input_path", help="Path to imzML file.")

#register optional arguments
parser.add_argument("output", help="Path to output file.")

# parse arguments from CLI
args = parser.parse_args()

# parse dataset
I = m2.ImzMLReader(args.input_path)
# report QC
report_agnostic_qc(I, args.output)

# CLI command
# [python instance] [file.py]  [input_path] [output]
# C:\Users\Jannik\.conda\envs\QCdev\python.exe C:\Users\Jannik\Documents\Uni\Master_Biochem\4_Semester\QCdev\src\i2nca\i2nca\workflows\CLI\agnostic_qc_cli.py C:\Users\Jannik\Documents\Uni\Master_Biochem\4_Semester\QCdev\src\i2nca\i2nca\tests\testdata\cc.imzML C:\Users\Jannik\Documents\Uni\Master_Biochem\4_Semester\QCdev\src\i2nca\i2nca\tests\tempfiles\empty
