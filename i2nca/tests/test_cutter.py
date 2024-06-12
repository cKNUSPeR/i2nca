import os as os
import unittest

from m2aia import ImzMLReader

from i2nca import cut_dataset_imzml


def get_wdir(rel_path: str):
    return str(os.path.join(os.getcwd(), rel_path))


def delete_output():
    return False


class TestCutToolCentroid(unittest.TestCase):

    def test_cut_pc_imzML_with_roi(self):
        # get data paths
        input_data = get_wdir(r"testdata\combined_pc.imzML")
        input_roi = get_wdir(r"testdata\combined_pc_roi.tsv")

        output = get_wdir(r"tempfiles\ROI_")

        # convert data
        cut_dataset_imzml(input_data, input_roi, output)

        # expected result
        result1 = output + "A.imzML"
        result2 = output + "B.imzML"

        self.assertTrue(os.path.isfile(result1))
        self.assertTrue(os.path.isfile(result2))

        # check if m2aia parses new file
        I = ImzMLReader(result1)
        I = ImzMLReader(result2)

        # cleanup temp files
        if delete_output() == True:
            os.remove(result1)
            os.remove(result2)

    def test_cut_pp_imzML_with_region(self):
        # get data paths
        input_data = get_wdir(r"testdata\pp.imzML")
        input_roi = get_wdir(r"testdata\regions.tsv")

        output = get_wdir(r"tempfiles\ROI_")

        # convert data
        cut_dataset_imzml(input_data, input_roi, output)

        # expected result
        result1 = output + "1.imzML"
        result2 = output + "2.imzML"
        result3 = output + "3.imzML"

        self.assertTrue(os.path.isfile(result1))
        self.assertTrue(os.path.isfile(result2))
        self.assertTrue(os.path.isfile(result3))

        # check if m2aia parses new file
        I = ImzMLReader(result1)
        I = ImzMLReader(result2)
        I = ImzMLReader(result3)

        # cleanup temp files
        if delete_output() == True:
            os.remove(result1)
            os.remove(result2)
            os.remove(result3)


if __name__ == "__main__":
    unittest.main()
