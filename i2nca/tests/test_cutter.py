import os as os
import unittest

from m2aia import ImzMLReader

from i2nca import cut_dataset_imzml, combine_datasets_imzml


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


    # for later update
    """def test_join_cc_pc_imzML_def_param(self):
        # get data paths
        input_data = get_wdir(r"testdata\pc.imzML")
        input_data2 = get_wdir(r"testdata\cc.imzML")

        output = get_wdir(r"tempfiles\pc")

        # convert data
        combine_datasets_imzml([input_data, input_data2], output)

        # expected result
        result1 = output + "_combined.imzML"
        result2 = output + "_pixel_transform_matrix.tsv"

        self.assertTrue(os.path.isfile(result1))
        self.assertTrue(os.path.isfile(result2))

        # read and replace the header to fit to the cutter
        with open(result2, 'r') as file:
            content = file.readlines()
        # Modify the header
        content[0] = 'old_x\told_y\tannotation\tx\ty\n'
        # Write the modified content back to the file
        with open(result2, 'w') as file:
            file.writelines(content)

        # convert data
        cut_dataset_imzml(result1, result2, output)


        # cleanup temp files
        if delete_output() == True:
            os.remove(result1)
            """


if __name__ == "__main__":
    unittest.main()
