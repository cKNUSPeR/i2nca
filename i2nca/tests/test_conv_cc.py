import unittest
import os as os

from m2aia import ImzMLReader
from i2nca import convert_pp_to_pp_imzml, convert_pp_to_cp_imzml, convert_profile_to_pc_imzml, loc_max_preset
from i2nca.convtools.conv_tools import convert_pc_to_cc_imzml



def get_wdir(rel_path:str):
    return str(os.path.join(os.getcwd(), rel_path))


class TestConvToolsCC(unittest.TestCase):

    def test_conv_pc_to_cc_imzml_unique(self):
        # get data paths
        input_data = get_wdir(r"testdata\pc.imzML")
        output = get_wdir(r"tempdata\cc")

        # convert data
        convert_pc_to_cc_imzml(input_data, output, bin_strategy="unique")

        # expected result
        result = output + "_conv_output_cont_centroid.imzML"

        self.assertTrue(os.path.isfile(result))

        # check if m2aia parses new file
        I = ImzMLReader(result)
        # cleanup temp files
        os.remove(result)

    def test_conv_pc_to_cc_imzml_fixed(self):
        # get data paths
        input_data = get_wdir(r"testdata\pc.imzML")
        output = get_wdir(r"tempdata\cc")

        # convert data
        convert_pc_to_cc_imzml(input_data, output, bin_strategy="fixed", bin_accuracy=200)

        # expected result
        result = output + "_conv_output_cont_centroid.imzML"

        self.assertTrue(os.path.isfile(result))

        # check if m2aia parses new file
        I = ImzMLReader(result)
        # cleanup temp files
        os.remove(result)

    def test_conv_pc_to_cc_imzml_fallback(self):
        # get data paths
        input_data = get_wdir(r"testdata\pc.imzML")
        output = get_wdir(r"tempdata\cc")

        # convert data
        convert_pc_to_cc_imzml(input_data, output, bin_strategy="random_input", bin_accuracy=200)

        # expected result
        result = output + "_conv_output_cont_centroid.imzML"

        self.assertTrue(os.path.isfile(result))

        # check if m2aia parses new file
        I = ImzMLReader(result)
        # cleanup temp files
        os.remove(result)



if __name__ == "__main__":
    unittest.main()