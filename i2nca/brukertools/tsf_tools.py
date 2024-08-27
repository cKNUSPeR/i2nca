import i2nca.brukertools.tsfdata as tsfdata
import numpy as np
from i2nca.dependencies.ImzMLWriter import ImzMLWriter
from scipy.signal import find_peaks
from typing import Optional
from datetime import datetime
import m2aia as m

class TsfReader:
    def __init__(self, tsf_superdir):

        # get .d directory
        self.superdir = tsf_superdir

        # setting up of sqlite reader
        self.tsf = tsfdata.TsfData(self.superdir)

        # set up connection
        self.conn = self.tsf.conn

    def GetNumberOfSpectra(self):
        return self.conn.execute("SELECT COUNT(*) FROM Frames").fetchone()[0]

    def GetPolarity(self):
        polarity_scan = self.conn.execute(f"SELECT Polarity FROM Frames").fetchone()[0]
        if polarity_scan == "+":
            return "positive"
        elif polarity_scan == "-":
            return "negative"
        else:
            raise ValueError("Polarity was not defined.")

    def GetSpotSize(self):
        spot_size = self.conn.execute(f"SELECT SpotSize FROM MaldiFrameLaserInfo").fetchone()[0]
        return str(int(spot_size))

    def GetSpectrumPosition(self, id):
        x_pos = self.conn.execute(f"SELECT XIndexPos FROM MaldiFrameInfo WHERE Frame={id}").fetchone()[0]
        y_pos = self.conn.execute(f"SELECT YIndexPos FROM MaldiFrameInfo WHERE Frame={id}").fetchone()[0]
        return (x_pos, y_pos)

    def GetSpectrum(self, id):
        intensities = self.tsf.readProfileSpectrum(id).astype(np.int32)
        mz = self.tsf.indexToMz(id, list(range(len(intensities))))
        return mz, intensities



def convert_tsf_to_pp_imzml(file_path, output_path):
    """ top-level converter for pp imzml to cp imzml"""
    if output_path is None:
        output_path = file_path[:-6]

    # parse imzml file
    Image = TsfReader(file_path)

    # write the continous file
    outfile_path = write_tsf_to_pp_imzml(Image, output_path)
    return output_file


def write_pp_to_pp_imzml(Image,
                         output_dir: str,
                         polarity: str = "positive",
                         pixel_size: str = "20",
                         ) -> str:
    """
        Writer for processed profile imzml files within m2aia.


        Parameters:
            I: parsed izML file (by m2aia or equvalent object that emulates the methods)
            polarity  : Polarity, either "positive" or "negative", not accessible in pym2aia
            pixel_size (Opt): pixel size of imaging run, currently not accessible in pym2aia
            output_dir (Opt): File path for output. in same folder as tsf if not specified.


        Returns:
           (str): imzML File path,
           additionally, imzML file is written there

        """
    # specification of output imzML file location and file extension
    output_file = output_dir + "_conv_output_proc_profile.imzML"

    # setting up of  reader

    # Get total spectrum count:
    n = Image.GetNumberOfSpectra()

    # get polarity

    # get pixel size

    # writing of the imzML file, based on pyimzML
    with ImzMLWriter(output_file,
                     # TODO get polarity from file
                     polarity=polarity,
                     mz_dtype=np.float32,
                     # intensity_dtype=np.uintc,
                     mode='processed',
                     spec_type='profile',
                     # the laser movement param are taken from scilslab export for ttf
                     scan_direction='top_down',
                     line_scan_direction='line_right_left',
                     scan_pattern='meandering',
                     scan_type='horizontal_line',
                     # preinstalled pixel sizes TODO get correct ones
                     pixel_size_x=pixel_size,
                     pixel_size_y=pixel_size,
                     ) as w:
        # m2aia is 0-indexed
        for id in range(0, n):
            #
            mz, intensities = Image.GetSpectrum(id)

            xyz_pos = Image.GetSpectrumPosition(id)
            pos = (xyz_pos[0], xyz_pos[1])

            # writing with pyimzML

            w.addSpectrum(mz, intensities, pos)

            # progress print statement
            # if (id % 100) == 0:
            #    print(f"pixels {id}/{n} written.")
    return output_file


def write_tsf_to_pp_imzml(TsfReader,
                         output_dir: str
                         ) -> str:
    """
        Writer for processed profile imzml files within m2aia.


        Parameters:
            I: parsed izML file (by m2aia or equvalent object that emulates the methods)
            output_dir (Opt): File path for output. in same folder as tsf if not specified.


        Returns:
           (str): imzML File path,
           additionally, imzML file is written there

        """
    # specification of output imzML file location and file extension
    output_file = output_dir + "_conv_output_proc_profile.imzML"

    # setting up of  reader

    # Get total spectrum count:
    n = TsfReader.GetNumberOfSpectra()

    # get polarity
    polarity = TsfReader.GetPolarity()

    # get pixel size
    pixel_size = TsfReader.GetSpotSize()

    # writing of the imzML file, based on pyimzML
    with ImzMLWriter(output_file,
                     # TODO get polarity from file
                     polarity=polarity,
                     mz_dtype=np.float32,
                     # intensity_dtype=np.uintc,
                     mode='processed',
                     spec_type='profile',
                     # the laser movement param are taken from scilslab export for ttf
                     scan_direction='top_down',
                     line_scan_direction='line_right_left',
                     scan_pattern='meandering',
                     scan_type='horizontal_line',
                     # preinstalled pixel sizes TODO get correct ones
                     pixel_size_x=pixel_size,
                     pixel_size_y=pixel_size,
                     ) as w:
        #tsf is 1-indexed
        for id in range(1, n+1):
            #
            mz, intensities = TsfReader.GetSpectrum(id)

            pos = TsfReader.GetSpectrumPosition(id)

            # writing with pyimzML

            w.addSpectrum(mz, intensities, pos)

            # progress print statement
            # if (id % 100) == 0:
            #    print(f"pixels {id}/{n} written.")
    return output_file


if __name__ == "__main__":
    file_path = r"C:\Users\Jannik\Documents\Uni\Master_Biochem\4_Semester\mzWonderland\data"

    output_path = r"C:\Users\Jannik\Documents\Uni\Master_Biochem\4_Semester\mzWonderland\data\output_i2nca_pp"

    convert_tsf_to_pp_imzml(file_path, output_path)
