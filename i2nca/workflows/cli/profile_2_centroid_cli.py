
import subprocess
from typing import Optional

from i2nca.dependencies.dependencies import *

from i2nca import set_find_peaks, write_profile_to_pc_imzml, loc_max_preset, set_find_peaks_cwt

def i2nca_convert_to_pc():
    # instance the parser
    parser = argparse.ArgumentParser()

    # register the positional arguments
    parser.add_argument("input_path", help="Path to imzML file.")
    parser.add_argument("output", help="Path to output file.")
    parser.add_argument("method", help="Method of Spectral Conversion. Currently 'set_find_peaks' or 'set_find_peaks_cwt'", type=str)

    #register optional arguments for find_peaks:
    parser.add_argument("--fp_hei", help="Required height of peaks", default=None, type=float)
    parser.add_argument("--fp_thr", help="Required threshold of peaks, the vertical distance to its neighboring samples.", default=None ,type=float)
    parser.add_argument("--fp_dis", help="Required minimal horizontal distance (>= 1) in samples between neighbouring peaks.", default=None ,type=float)
    parser.add_argument("--fp_pro", help="Required prominence of peaks.", default=None ,type=float)
    parser.add_argument("--fp_wid", help="Required width of peaks in samples.", default=None ,type=float)
    parser.add_argument("--fp_wlen", help="Used for calculation of the peaks width, thus it is only used if `width` is given.", default=None ,type=float)
    parser.add_argument("--fp_rhei", help="Required width of peaks in samples.", default=None ,type=float)
    parser.add_argument("--fp_pla", help="Required size of the flat top of peaks in samples.", default=None ,type=float)

    #register optuianal args for find_peaks_cwt:
    parser.add_argument("--cwt_wid", help="Single width to use for calculating the CWT matrix", default=None, type=float)
    parser.add_argument("--cwt_gap", help=" A ridge line is discontinued if there are more than gap_thresh points without connecting a new relative maximum.",
                        default=None, type=float)
    parser.add_argument("--cwt_mlen", help="Minimum length a ridge line needs to be acceptable.", default=None, type=int)
    parser.add_argument("--cwt_snr", help="Minimum SNR ratio.", default=1.0, type=float)
    parser.add_argument("--cwt_nper", help="When calculating the noise floor, percentile of data points examined below which to consider noise.", default=10.0, type=float)
    parser.add_argument("--cwt_win", help="Size of window to use to calculate noise floor.", default=None, type=int)

    #register m2aia preprocessing options
    parser.add_argument("--bsl", help="m2aia Baseline Correction", default="None")
    parser.add_argument("--bsl_hws", help="m2aia Baseline Correction Half Window Size", default= 50, type=int)
    parser.add_argument("--nor", help="m2aia Normalization", default="None")
    parser.add_argument("--smo", help="m2aia Smoothing", default="None")
    parser.add_argument("--smo_hws", help="m2aia Smoothing Half Window Size", default=2, type=int)
    parser.add_argument("--itr", help="m2aia Intensity Transformation", default="None")

    # parse arguments from cli
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

    if args.method == "set_find_peaks":
        # get the detection function
        detection = set_find_peaks(height=args.fp_hei,
                                   threshold=args.fp_thr,
                                   distance=args.fp_dis,
                                   prominence=args.fp_pro,
                                   width=args.fp_wid,
                                   wlen=args.fp_wlen,
                                   rel_height=args.fp_rhei,
                                   plateau_size=args.fp_pla)
    elif args.method == "set_find_peaks_cwt":
        detection = set_find_peaks_cwt(widths=args.cwt_wid,
                                       gap_thresh=args.cwt_gap,
                                       min_length=args.cwt_mlen,
                                       min_snr=args.cwt_snr,
                                       noise_perc=args.cwt_nper,
                                       window_size=args.cwt_win)
    else:
        detection = loc_max_preset


    # write the continous file
    write_profile_to_pc_imzml(Image, args.output, detection)

if __name__ == "__main__":
    i2nca_convert_to_pc()

# cli command
# [python instance] [file.py] --accuracy[20] --cov [0.0.5] --bsl [Median] --bsl_hws [20] --nor [RMS] --smo [Gaussian]  --smo_hws [3] --itr [Log2] [input_path] [output] [method]
# C:\Users\Jannik\.conda\envs\QCdev\python.exe C:\Users\Jannik\Documents\Uni\Master_Biochem\4_Semester\QCdev\src\i2nca\i2nca\workflows\cli\calibrant_qc_cli.py --ppm 50 --sample_size 1  C:\Users\Jannik\Documents\Uni\Master_Biochem\4_Semester\QCdev\src\i2nca\i2nca\tests\testdata\cc.imzML C:\Users\Jannik\Documents\Uni\Master_Biochem\4_Semester\QCdev\src\i2nca\i2nca\tests\tempfiles\empty C:\Users\Jannik\Documents\Uni\Master_Biochem\4_Semester\QCdev\src\i2nca\i2nca\tests\testdata\calibrant.csv
