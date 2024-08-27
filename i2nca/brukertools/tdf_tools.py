import i2nca.brukertools.timsdata as timsdata
import numpy as np
from i2nca.dependencies.ImzMLWriter import ImzMLWriter
import matplotlib.pyplot as plt


class TdfReader:
    def __init__(self, tsf_superdir):

        # get .d directory
        self.superdir = tsf_superdir

        # setting up of sqlite reader
        self.tdf = timsdata.TimsData(self.superdir)

        # set up connection
        self.conn = self.tdf.conn

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

    def GetAverageMassFrame(self,id):
        scan_nr = self.conn.execute(f"SELECT NumScans FROM Frames WHERE Id={id}").fetchone()[0]

        total_mzs = np.array([])
        total_ints =np.array([])


        for scan in self.tdf.readScans(id, 0, scan_nr):
            intens = np.array(scan[1], dtype=np.float64)
            mz = self.tdf.indexToMz(id, np.array(scan[0], dtype=np.float64))

            total_mzs = np.hstack((total_mzs, mz))
            total_ints = np.hstack((total_ints, intens))

        min_mz = np.floor(min(total_mzs))
        max_mz = np.ceil(max(total_mzs))

        mz_range = int(max_mz - min_mz) * 10000 # automatic binning to 0.0001 accuracy
        bins = np.linspace(min_mz, max_mz, mz_range, endpoint=False)

        bin_indices = np.digitize(total_mzs, bins)

        # Filter out empty bins
        non_empty_bins = np.unique(bin_indices)
        # sum up per non-empty bin
        sum_ints = [np.sum(total_ints[bin_indices == i]) for i in non_empty_bins]
        return bins[non_empty_bins], sum_ints




def write_tdf_to_pc_imzml(TdfReader,
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
    output_file = output_dir + "_conv_output_proc_cent.imzML"

    # setting up of  reader

    # Get total spectrum count:
    n = TdfReader.GetNumberOfSpectra()

    # get polarity
    polarity = TdfReader.GetPolarity()

    # get pixel size
    pixel_size = TdfReader.GetSpotSize()

    # writing of the imzML file, based on pyimzML
    with ImzMLWriter(output_file,
                     polarity=polarity,
                     mz_dtype=np.float32,
                     # intensity_dtype=np.uintc,
                     mode='processed',
                     spec_type='centroid',
                     # the laser movement param are taken from scilslab export for ttf
                     scan_direction='top_down',
                     line_scan_direction='line_right_left',
                     scan_pattern='meandering',
                     scan_type='horizontal_line',
                     pixel_size_x=pixel_size,
                     pixel_size_y=pixel_size,
                     ) as w:
        #tsf is 1-indexed
        for id in range(1, n+1):
            #
            mz, intensities = TdfReader.GetAverageMassFrame(id)

            pos = TdfReader.GetSpectrumPosition(id)

            # writing with pyimzML

            w.addSpectrum(mz, intensities, pos)

            #'progress print statement
            if (id % 10) == 0:
                print(f"pixels {id}/{n} written.")
    return output_file


def convert_tdf_to_pc_imzml(file_path, output_path):
    """ top-level converter for tdf files to processed centroids"""
    if output_path is None:
        output_path = file_path[:-6]

    # parse imzml file
    Image = TdfReader(file_path)

    # write the  file
    outfile_path = write_tdf_to_pc_imzml(Image, output_path)
    return outfile_path



if __name__ == "__main__":

    file_superdir = r"C:\Users\Jannik\Documents\Uni\Master_Biochem\4_Semester\mzWonderland\outdatet_version_0_!\test_data\CF048_tryp1_0025_TIMSON.d"
    file_outdir = r"C:\Users\Jannik\Documents\Uni\Master_Biochem\4_Semester\mzWonderland\outdatet_version_0_!\test_data\CF048_tryp1_0025_TIMSON.d\test"
    I = TdfReader(file_superdir)
    # mz, ints = a.GetAverageMassFrame(500)
    # plt.stem(mz, ints)
    # #plt.xlim(2386.5,2387.5)
    # plt.show()
    write_tdf_to_pc_imzml(I,file_outdir)
