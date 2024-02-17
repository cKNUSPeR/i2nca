import unittest
import os as os

from m2aia import ImzMLReader
from i2nca import convert_profile_to_pc_imzml, loc_max_preset, set_find_peaks_cwt

def get_wdir(rel_path:str):
    return str(os.path.join(os.getcwd(), rel_path))


def delete_output():
    return False


class TestConvToolsCP(unittest.TestCase):

    def test_conv_cp_to_pc_imzml_loc_max_preset(self):
        # get data paths
        input_data = get_wdir(r"testdata\cp.imzML")
        output = get_wdir(r"tempfiles\pc")

        # convert data
        convert_profile_to_pc_imzml(input_data, output, loc_max_preset)

        # expected result
        result = output + "_conv_output_proc_centroid.imzML"
        result2 = output + "_control_report_prof_to_pc.pdf"

        self.assertTrue(os.path.isfile(result))
        self.assertTrue(os.path.isfile(result2))

        # check if m2aia parses new file
        I = ImzMLReader(result)

        # cleanup temp files
        if delete_output() == True:
            os.remove(result)
            os.remove(result2)

    def test_conv_cp_to_pc_imzml(self):
        # get data paths
        input_data = get_wdir(r"testdata\cp.imzML")
        output = get_wdir(r"tempfiles\pc")

        # convert data
        convert_profile_to_pc_imzml(input_data, output, set_find_peaks_cwt(widths=[5,7,9,11], min_snr=3))

        # expected result
        result = output + "_conv_output_proc_centroid.imzML"
        result2 = output + "_control_report_prof_to_pc.pdf"

        self.assertTrue(os.path.isfile(result))
        self.assertTrue(os.path.isfile(result2))

        # check if m2aia parses new file
        I = ImzMLReader(result)

        # cleanup temp files
        if delete_output() == True:
            os.remove(result)
            os.remove(result2)


if __name__ == "__main__":
    unittest.main()