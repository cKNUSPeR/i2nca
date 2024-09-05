import unittest
import os as os

from m2aia import ImzMLReader
from i2nca import report_agnostic_qc, report_calibrant_qc, report_regions_qc


def get_wdir(rel_path:str):
    return str(os.path.join(os.getcwd(), rel_path))


def delete_output():
    return False


class TestAgnosticQC(unittest.TestCase):
        
    def test_agnostic_qc_on_pp_imzml(self):

        input = get_wdir(r"testdata\pp.imzML")
        output = get_wdir(r"tempfiles\pp")

        # parse dataset
        I = ImzMLReader(input)
        # report QC
        report_agnostic_qc(I, output)

        # expected result
        result = output + "_agnostic_QC.pdf"

        # assert file building
        self.assertTrue(os.path.isfile(result))

        # cleanup temp files
        if delete_output() == True: 
            os.remove(result)

    def test_agnostic_qc_on_cp_imzml(self):

        input = get_wdir(r"testdata\cp.imzML")
        output = get_wdir(r"tempfiles\cp")

        # parse dataset
        I = ImzMLReader(input)
        # report QC
        report_agnostic_qc(I, output)

        # expected result
        result = output + "_agnostic_QC.pdf"

        # assert file building
        self.assertTrue(os.path.isfile(result))

        # cleanup temp files
        if delete_output() == True: 
            os.remove(result)

    def test_agnostic_qc_on_pc_imzml(self):

        input = get_wdir(r"testdata\pc.imzML")
        output = get_wdir(r"tempfiles\pc")

        # parse dataset
        I = ImzMLReader(input)
        # report QC
        report_agnostic_qc(I, output)

        # expected result
        result = output + "_agnostic_QC.pdf"

        # assert file building
        self.assertTrue(os.path.isfile(result))

        # cleanup temp files
        if delete_output() == True: 
            os.remove(result)

    def test_agnostic_qc_on_cc_imzml(self):

        input = get_wdir(r"testdata\cc.imzML")
        output = get_wdir(r"tempfiles\cc")

        # parse dataset
        I = ImzMLReader(input)
        # report QC
        report_agnostic_qc(I, output)

        # expected result
        result = output + "_agnostic_QC.pdf"

        # assert file building
        self.assertTrue(os.path.isfile(result))

        # cleanup temp files
        if delete_output() == True: 
            os.remove(result)

    def test_agnostic_qc_on_joined_imzml(self):

        input = get_wdir(r"testdata\joined_file.imzML")
        output = get_wdir(r"tempfiles\joined_file")

        # parse dataset
        I = ImzMLReader(input)
        # report QC
        report_agnostic_qc(I, output)

        # expected result
        result = output + "_agnostic_QC.pdf"

        # assert file building
        self.assertTrue(os.path.isfile(result))

        # cleanup temp files
        if delete_output() == True:
            os.remove(result)

class TestCalibrantQC(unittest.TestCase):

    def test_calibrant_qc_on_pp_imzml_user_param(self):

        input = get_wdir(r"testdata\pp.imzML")
        calibrants = get_wdir(r"testdata\calibrant.csv")
        output = get_wdir(r"tempfiles\pp")

        # parse dataset
        I = ImzMLReader(input)
        # report QC
        report_calibrant_qc(I, output, calibrants, 50, 0.33)

        # expected result
        result = output + "_calibrant_QC.pdf"

        # assert file building
        self.assertTrue(os.path.isfile(result))

        # cleanup temp files
        if delete_output() == True: 
            os.remove(result)

    def test_calibrant_qc_on_pp_imzml_def_param(self):

        input = get_wdir(r"testdata\pp.imzML")
        calibrants = get_wdir(r"testdata\calibrant.csv")
        output = get_wdir(r"tempfiles\pp_def")

        # parse dataset
        I = ImzMLReader(input)
        # report QC
        report_calibrant_qc(I, output, calibrants, 50)

        # expected result
        result = output + "_calibrant_QC.pdf"

        # assert file building
        self.assertTrue(os.path.isfile(result))

        # cleanup temp files
        if delete_output() == True: 
            os.remove(result)

    def test_calibrant_qc_on_cp_imzml_user_param(self):
        input = get_wdir(r"testdata\cp.imzML")
        calibrants = get_wdir(r"testdata\calibrant.csv")
        output = get_wdir(r"tempfiles\cp")

        # parse dataset
        I = ImzMLReader(input)
        # report QC
        report_calibrant_qc(I, output, calibrants, 50, 0.33)

        # expected result
        result = output + "_calibrant_QC.pdf"

        # assert file building
        self.assertTrue(os.path.isfile(result))

        # cleanup temp files
        if delete_output() == True: 
            os.remove(result)

    def test_calibrant_qc_on_cp_imzml_def_param(self):
        input = get_wdir(r"testdata\cp.imzML")
        calibrants = get_wdir(r"testdata\calibrant.csv")
        output = get_wdir(r"tempfiles\cp_def")

        # parse dataset
        I = ImzMLReader(input)
        # report QC
        report_calibrant_qc(I, output, calibrants, 50)

        # expected result
        result = output + "_calibrant_QC.pdf"

        # assert file building
        self.assertTrue(os.path.isfile(result))

        # cleanup temp files
        if delete_output() == True: 
            os.remove(result)

    def test_calibrant_qc_on_pc_imzml_user_param(self):
        input = get_wdir(r"testdata\pc.imzML")
        calibrants = get_wdir(r"testdata\calibrant.csv")
        output = get_wdir(r"tempfiles\pc")

        # parse dataset
        I = ImzMLReader(input)
        # report QC
        report_calibrant_qc(I, output, calibrants, 50, 0.33)

        # expected result
        result = output + "_calibrant_QC.pdf"

        # assert file building
        self.assertTrue(os.path.isfile(result))

        # cleanup temp files
        if delete_output() == True: 
            os.remove(result)

    def test_calibrant_qc_on_pc_imzml_def_param(self):
        input = get_wdir(r"testdata\pc.imzML")
        calibrants = get_wdir(r"testdata\calibrant.csv")
        output = get_wdir(r"tempfiles\pc_def")

        # parse dataset
        I = ImzMLReader(input)
        # report QC
        report_calibrant_qc(I, output, calibrants, 50)

        # expected result
        result = output + "_calibrant_QC.pdf"

        # assert file building
        self.assertTrue(os.path.isfile(result))

        # cleanup temp files
        if delete_output() == True: 
            os.remove(result)

    def test_calibrant_qc_on_cc_imzml_user_param(self):
        input = get_wdir(r"testdata\cc.imzML")
        calibrants = get_wdir(r"testdata\calibrant.csv")
        output = get_wdir(r"tempfiles\cc")

        # parse dataset
        I = ImzMLReader(input)
        # report QC
        report_calibrant_qc(I, output, calibrants, 50, 1)

        # expected result
        result = output + "_calibrant_QC.pdf"

        # assert file building
        self.assertTrue(os.path.isfile(result))

        # cleanup temp files
        if delete_output() == True:
             os.remove(result)

    def test_calibrant_qc_on_cc_imzml_def_param(self):
        input = get_wdir(r"testdata\cc.imzML")
        calibrants = get_wdir(r"testdata\calibrant.csv")
        output = get_wdir(r"tempfiles\cc_def")

        # parse dataset
        I = ImzMLReader(input)
        # report QC
        report_calibrant_qc(I, output, calibrants, 50)

        # expected result
        result = output + "_calibrant_QC.pdf"

        # assert file building
        self.assertTrue(os.path.isfile(result))

        # cleanup temp files
        if delete_output() == True: 
            os.remove(result)

    def test_calibrant_qc_on_combined_pc_imzml_user_param(self):
        input = get_wdir(r"testdata\combined_pc.imzML")
        calibrants = get_wdir(r"testdata\calibrant.csv")
        output = get_wdir(r"tempfiles\combined_pc")

        # parse dataset
        I = ImzMLReader(input)
        # report QC
        report_calibrant_qc(I, output, calibrants, 50, 0.33)

        # expected result
        result = output + "_calibrant_QC.pdf"

        # assert file building
        self.assertTrue(os.path.isfile(result))

        # cleanup temp files
        if delete_output() == True:
             os.remove(result)

class TestRegionQC(unittest.TestCase):

    def test_region_qc_on_cc_imzml_no_anno(self):
        input = get_wdir(r"testdata\cc.imzML")
        output = get_wdir(r"tempfiles\cc")

        # parse dataset
        I = ImzMLReader(input)
        # report QC
        report_regions_qc(I, output)

        # expected result
        result = output + "_region_QC.pdf"

        # assert file building
        self.assertTrue(os.path.isfile(result))

        # cleanup temp files
        if delete_output() == True:
            os.remove(result)

    def test_region_qc_on_cc_imzml_with_anno(self):
        input = get_wdir(r"testdata\pp.imzML")
        output = get_wdir(r"tempfiles\pp_w_anno")
        region_file = get_wdir(r"testdata\regions.tsv")

        # parse dataset
        I = ImzMLReader(input)
        # report
        report_regions_qc(I, output, region_file)

        # expected result
        result = output + "_region_QC.pdf"

        # assert file building
        self.assertTrue(os.path.isfile(result))

        # cleanup temp files
        if delete_output() == True:
            os.remove(result)

    def test_region_qc_on_combined_pc_imzml_with_anno(self):
        input = get_wdir(r"testdata\combined_pc.imzML")
        output = get_wdir(r"tempfiles\combined_pc_w_anno")
        region_file = get_wdir(r"testdata\combined_pc_roi.tsv")

        # parse dataset
        I = ImzMLReader(input)
        # report
        report_regions_qc(I, output, region_file)

        # expected result
        result = output + "_region_QC.pdf"

        # assert file building
        self.assertTrue(os.path.isfile(result))

        # cleanup temp files
        if delete_output() == True:
            os.remove(result)

if __name__ == "__main__":
    unittest.main()
