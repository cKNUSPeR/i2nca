# -*- coding: utf-8 -*-
"""Test program using Python wrapper for timsdata.dll to read tsf (spectrum) data"""
# this script converts .tsf data into centroid processed imzML files
import tsfdata
import numpy as np
from pyimzml.ImzMLWriter import ImzMLWriter
from scipy.signal import find_peaks
from typing import Optional
from datetime import datetime

def convert_tsf_to_proc_cent_imzml(tsffile_superdir: str,
                                   output_dir: Optional[str] = None,
                                   intensity_cutoff:int = 100) -> str:
    """
        Converts tsf composite file to imzML.
        Assumes tsf file as processed profile spectra.
        Converts the profile spectra on the fly to centroids by manual cutoff.

        Parameters:
            tsffile_superdir (str): File path to folder that stores analysis.tsf file.
            output_dir (Opt): File path for output. in same folder as tsf if not specified.
            intensity_cutoff (int): Intesity parameter that does cutoff for on the fly centroiding


        Returns:
           (str): imzML File directory
           also imzML file

        """
    # specification of output imzML file location and file extension
    if output_dir is None:
        output_dir = tsffile_superdir
    output_file = output_dir + "\\conv_output_centroided.imzML"

    # setting up of sqlite reader
    tsf = tsfdata.TsfData(tsffile_superdir)
    conn = tsf.conn

    # Get total spectrum count:
    q = conn.execute("SELECT COUNT(*) FROM Frames")
    row = q.fetchone()
    n = row[0]

    # readout of polarity, defensive
    polarity_scan= conn.execute(f"SELECT Polarity FROM Frames").fetchone()[0]
    if polarity_scan == "+":
        polarity = "positive"
    elif polarity_scan == "-":
        polarity = "negative"
    else:
        raise ValueError("Polarity was not defined.")

    # get the pixel size, is assumed to be square
    spot_size = conn.execute(f"SELECT SpotSize FROM MaldiFrameLaserInfo").fetchone()[0]
    spot_size = str(int(spot_size))

    # writing of the imzML file, based on pyimzML
    with ImzMLWriter(output_file,
                     polarity=polarity,
                     mz_dtype=np.float64,
                     # intensity_dtype=np.uintc,
                     # ttf specific parameters, should not be changed
                     mode='processed',
                     spec_type='centroid',
                     scan_direction='top_down',
                     line_scan_direction='line_right_left',
                     scan_pattern='meandering',
                     scan_type='horizontal_line',
                     # pixel sizes
                     pixel_size_x=spot_size,
                     pixel_size_y=spot_size,
                     ) as w:
        # tsf data is 1-, full range at n+1
        for id in range(1, n+1):
            x_pos = conn.execute(f"SELECT XIndexPos FROM MaldiFrameInfo WHERE Frame={id}").fetchone()[0]
            y_pos = conn.execute(f"SELECT YIndexPos FROM MaldiFrameInfo WHERE Frame={id}").fetchone()[0]
            pos = (x_pos, y_pos)

            # generation of int and mz
            intensities = tsf.readProfileSpectrum(id).astype(np.int32)
            mz = tsf.indexToMz(id, list(range(len(intensities))))

            # peak location TODO: add a threshold for S/N from QC of profile spectra
            peaks, _ = find_peaks(intensities, height=intensity_cutoff)

            # error handling: no peaks ins spectrum found:
            if len(peaks) > 0:
                # writing with pyimzML
                try:
                    w.addSpectrum(mz[peaks], intensities[peaks], pos)
                except:
                    print(f"pixel {id} is faulty, gets defaulted to 0,0")
                    w.addSpectrum([0], [0], pos)
            # console output to estimate runtime 
            if (id % 100)==0:
                print(f"pixel {id}/{n} written.")
            
    return output_file


if __name__ == "__main__":
    print(datetime.now())
    print("File succesfully generated at: ",
          convert_tsf_to_proc_cent_imzml("C:\\Users\\wittej\\Documents\\quickdata\\testdata\\",
                                         "C:\\Users\\wittej\\Documents\\quickdata\\testdata\\",
                                         20)
          )
    print(datetime.now())

