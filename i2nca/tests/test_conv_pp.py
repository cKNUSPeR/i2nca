import unittest
import os as os

from m2aia import ImzMLReader
from i2nca import convert_pp_to_pp_imzml, convert_pp_to_cp_imzml, convert_profile_to_pc_imzml, loc_max_preset


def get_wdir(rel_path:str):
    return str(os.path.join(os.getcwd(), rel_path))

def delete_output():
    return False

class TestConvToolsPP(unittest.TestCase):

    def test_convert_pp_to_pp_imzml(self):
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
        if delete_output() == True:
            os.remove(result)

    def test_convert_pp_to_cp_imzml_def_param(self):
        # get data paths
        input_data = get_wdir(r"testdata\pp.imzML")
        output = get_wdir(r"tempfiles\cp")

        # convert data
        convert_pp_to_cp_imzml(input_data, output)

        # expected result
        result = output + "_conv_output_cont_profile.imzML"


        self.assertTrue(os.path.isfile(result))


        # check if m2aia parses new file
        I = ImzMLReader(result)

        # cleanup temp files
        if delete_output() == True:
            os.remove(result)


    def test_convert_pp_to_cp_imzml_coverage(self):
        # get data paths
        input_data = get_wdir(r"testdata\pp.imzML")
        output = get_wdir(r"tempfiles\cp")
        coverage = 0.5

        # convert data
        convert_pp_to_cp_imzml(input_data, output, coverage=coverage)

        # expected result
        result = output + "_conv_output_cont_profile.imzML"


        self.assertTrue(os.path.isfile(result))


        # check if m2aia parses new file
        I = ImzMLReader(result)

        # cleanup temp files
        if delete_output() == True:
            os.remove(result)




    def test_convert_pp_to_cp_imzml_fixbins(self):
        # get data paths
        input_data = get_wdir(r"testdata\pp.imzML")
        output = get_wdir(r"tempfiles\cp")
        method = "fixed"
        accuracy = 20

        # convert data
        convert_pp_to_cp_imzml(input_data, output, method=method, accuracy=accuracy)

        # expected result
        result = output + "_conv_output_cont_profile.imzML"

        self.assertTrue(os.path.isfile(result))

        # check if m2aia parses new file
        I = ImzMLReader(result)

        # cleanup temp files
        if delete_output() == True:
            os.remove(result)


    def test_conv_pp_to_pc_imzml(self):
        # get data paths
        input_data = get_wdir(r"testdata\pp.imzML")
        output = get_wdir(r"tempfiles\pc")

        # convert data
        convert_profile_to_pc_imzml(input_data, output, loc_max_preset)

        # expected result
        result = output + "_conv_output_proc_centroid.imzML"


        self.assertTrue(os.path.isfile(result))


        # check if m2aia parses new file
        I = ImzMLReader(result)

        # cleanup temp files
        if delete_output() == True:
            os.remove(result)


if __name__ == "__main__":
    unittest.main()