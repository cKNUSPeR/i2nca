import os as os
import unittest

from m2aia import ImzMLReader

from i2nca import combine_datasets_imzml

from i2nca import cut_dataset_imzml


def get_wdir(rel_path: str):
    return str(os.path.join(os.getcwd(), rel_path))


def delete_output():
    return False


class TestCombineToolProfile(unittest.TestCase):

    def test_join_two_pp_imzML_def_param(self):
        # get data paths
        input_data = get_wdir(r"testdata\pp.imzML")
        input_data2 = get_wdir(r"testdata\pp.imzML")

        output = get_wdir(r"tempfiles\pp")

        # convert data
        combine_datasets_imzml([input_data, input_data2], output)

        # expected result
        result = output + "_combined.imzML"

        self.assertTrue(os.path.isfile(result))

        # check if m2aia parses new file
        I = ImzMLReader(result)

        # cleanup temp files
        if delete_output() == True:
            os.remove(result)

    def test_join_two_pp_imzML_user_param(self):
        # get data paths
        input_data = get_wdir(r"testdata\pp.imzML")
        input_data2 = get_wdir(r"testdata\pp.imzML")

        output = get_wdir(r"tempfiles\pp")

        # convert data
        combine_datasets_imzml([input_data, input_data2], output, norm_method="TIC", padding= 5)

        # expected result
        result = output + "_combined.imzML"

        self.assertTrue(os.path.isfile(result))

        # check if m2aia parses new file
        I = ImzMLReader(result)

        # cleanup temp files
        if delete_output() == True:
            os.remove(result)

    def test_join_multiple_pp_imzML_def_param(self):
        # get data paths
        input_data = get_wdir(r"testdata\pp.imzML")
        input_data2 = get_wdir(r"testdata\pp.imzML")
        input_data3 = get_wdir(r"testdata\pp.imzML")

        output = get_wdir(r"tempfiles\pp")

        # convert data
        combine_datasets_imzml([input_data, input_data2, input_data3], output)

        # expected result
        result = output + "_combined.imzML"

        self.assertTrue(os.path.isfile(result))

        # check if m2aia parses new file
        I = ImzMLReader(result)

        # cleanup temp files
        if delete_output() == True:
            os.remove(result)

    def test_join_cp_pp_imzML_def_param(self):
        # get data paths
        input_data = get_wdir(r"testdata\pp.imzML")
        input_data2 = get_wdir(r"testdata\cp.imzML")

        output = get_wdir(r"tempfiles\pp")

        # convert data
        combine_datasets_imzml([input_data, input_data2], output)

        # expected result
        result = output + "_combined.imzML"

        self.assertTrue(os.path.isfile(result))

        # check if m2aia parses new file
        I = ImzMLReader(result)

        # cleanup temp files
        if delete_output() == True:
            os.remove(result)

class TestCombineToolCentroid(unittest.TestCase):

    def test_join_two_pc_imzML_def_param(self):
        # get data paths
        input_data = get_wdir(r"testdata\pc.imzML")
        input_data2 = get_wdir(r"testdata\pc.imzML")

        output = get_wdir(r"tempfiles\pc")

        # convert data
        combine_datasets_imzml([input_data, input_data2], output)

        # expected result
        result = output + "_combined.imzML"

        self.assertTrue(os.path.isfile(result))

        # check if m2aia parses new file
        I = ImzMLReader(result)

        # cleanup temp files
        if delete_output() == True:
            os.remove(result)

    def test_join_two_pc_imzML_user_param(self):
        # get data paths
        input_data = get_wdir(r"testdata\pc.imzML")
        input_data2 = get_wdir(r"testdata\pc.imzML")

        output = get_wdir(r"tempfiles\pc")

        # convert data
        combine_datasets_imzml([input_data, input_data2], output, norm_method="TIC", padding= 5)

        # expected result
        result = output + "_combined.imzML"

        self.assertTrue(os.path.isfile(result))

        # check if m2aia parses new file
        I = ImzMLReader(result)

        # cleanup temp files
        if delete_output() == True:
            os.remove(result)

    def test_join_two_pc_imzML_polarity_overwrite(self):
        # get data paths
        input_data = get_wdir(r"testdata\pc.imzML")
        input_data2 = get_wdir(r"testdata\pc.imzML")

        output = get_wdir(r"tempfiles\pc")

        # convert data
        combine_datasets_imzml([input_data, input_data2], output, norm_method="TIC", padding=5, overwrite_polarity="negative")

        # expected result
        result = output + "_combined.imzML"

        self.assertTrue(os.path.isfile(result))

        # check if m2aia parses new file
        I = ImzMLReader(result)

        # cleanup temp files
        if delete_output() == True:
            os.remove(result)

    def test_join_two_pc_imzML_xcols(self):
        # get data paths
        input_data = get_wdir(r"testdata\pc.imzML")
        input_data2 = get_wdir(r"testdata\pc.imzML")
        input_data3 = get_wdir(r"testdata\pc.imzML")
        input_data4 = get_wdir(r"testdata\pc.imzML")
        input_data5 = get_wdir(r"testdata\pc.imzML")

        output = get_wdir(r"tempfiles\pc")

        # convert data
        combine_datasets_imzml([input_data,
                                input_data2,
                                input_data3,
                                input_data4,
                                input_data5], output, norm_method="TIC", padding=5, x_cols=3)

        # expected result
        result = output + "_combined.imzML"
        result2 = output + "_pixel_transform_matrix.tsv"

        self.assertTrue(os.path.isfile(result))
        self.assertTrue(os.path.isfile(result2))

        # check if m2aia parses new file
        I = ImzMLReader(result)

        # cleanup temp files
        if delete_output() == True:
            os.remove(result)
            os.remove(result2)


    def test_join_cc_pc_imzML_def_param(self):
        # get data paths
        input_data = get_wdir(r"testdata\pc.imzML")
        input_data2 = get_wdir(r"testdata\cc.imzML")

        output = get_wdir(r"tempfiles\pc")

        # convert data
        combine_datasets_imzml([input_data, input_data2], output)

        # expected result
        result = output + "_combined.imzML"

        self.assertTrue(os.path.isfile(result))

        # check if m2aia parses new file
        I = ImzMLReader(result)

        # cleanup temp files
        if delete_output() == True:
            os.remove(result)





if __name__ == "__main__":
    unittest.main()
