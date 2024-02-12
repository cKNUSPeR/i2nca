import unittest
import os as os

from m2aia import ImzMLReader
from i2nca import report_agnostic_qc


def get_wdir(rel_path:str):
    return str(os.path.join(os.getcwd(), rel_path))

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
        os.remove(result)

if __name__ == "__main__":
    unittest.main()
