import unittest
import os as os

from m2aia import ImzMLReader
from i2nca import convert_pp_to_pp_imzml, squeeze_pp_to_cp_imzml, squeeze_profile_to_pc_imzml, loc_max_preset



def get_wdir(rel_path:str):
    return str(os.path.join(os.getcwd(), rel_path))


class TestConvTools(unittest.TestCase):

    def test_conv_pp_to_pp_imzml(self):
        # get data paths
        input_data = get_wdir(r"testdata\pp.imzML")
        output = get_wdir(r"tempfiles\pp")

        # convert data
        convert_pp_to_pp_imzml(input_data, output)

        # expected result
        result = output + "_conv_output_proc_profile.imzML"

        self.assertTrue(os.path.isfile(result))

        # check if m2aia parses new file
        I = ImzMLReader(result)
        # cleanup temp files
        os.remove(result)

    def test_conv_pp_to_cp_imzml(self):
        # get data paths
        input_data = get_wdir(r"testdata\pp.imzML")
        output = get_wdir(r"tempfiles\cp")

        # convert data
        squeeze_pp_to_cp_imzml(input_data, output)

        # expected result
        result = output + "_conv_output_cont_profile.imzML"

        self.assertTrue(os.path.isfile(result))

        # check if m2aia parses new file
        I = ImzMLReader(result)
        # cleanup temp files
        os.remove(result)

    def test_conv_pp_to_pc_imzml(self):
        # get data paths
        input_data = get_wdir(r"testdata\pp.imzML")
        output = get_wdir(r"tempfiles\pc")

        # convert data
        squeeze_profile_to_pc_imzml(input_data, output, loc_max_preset)

        # expected result
        result = output + "_conv_output_proc_centroid.imzML"

        self.assertTrue(os.path.isfile(result))

        # check if m2aia parses new file
        I = ImzMLReader(result)
        # cleanup temp files
        os.remove(result)

    def test_conv_cp_to_pc_imzml(self):
        # get data paths
        input_data = get_wdir(r"testdata\cp.imzML")
        output = get_wdir(r"tempfiles\pc")

        # convert data
        squeeze_profile_to_pc_imzml(input_data, output, loc_max_preset)

        # expected result
        result = output + "_conv_output_proc_centroid.imzML"

        self.assertTrue(os.path.isfile(result))

        # check if m2aia parses new file
        I = ImzMLReader(result)
        # cleanup temp files
        os.remove(result)


if __name__ == "__main__":
    unittest.main()