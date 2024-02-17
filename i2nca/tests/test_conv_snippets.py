import os as os
import unittest

from m2aia import ImzMLReader

from i2nca import convert_data_to_snippet_imzml


def get_wdir(rel_path: str):
    return str(os.path.join(os.getcwd(), rel_path))


def delete_output():
    return False


class TestConvToolsSnippetPP(unittest.TestCase):

    def test_snippet_pp_imzML_def_param(self):
        # get data paths
        input_data = get_wdir(r"testdata\pp.imzML")
        output = get_wdir(r"tempfiles\pp")

        # convert data
        convert_data_to_snippet_imzml(input_data, output)

        # expected result
        result = output + "_data_snippet.imzML"

        self.assertTrue(os.path.isfile(result))

        # check if m2aia parses new file
        I = ImzMLReader(result)

        # cleanup temp files
        if delete_output() == True:
            os.remove(result)

    def test_snippet_pp_imzML_scattered(self):
        # get data paths
        input_data = get_wdir(r"testdata\pp.imzML")
        output = get_wdir(r"tempfiles\pp")

        # convert data
        convert_data_to_snippet_imzml(input_data, output, 2, scattered=True)

        # expected result
        result = output + "_data_snippet.imzML"

        self.assertTrue(os.path.isfile(result))

        # check if m2aia parses new file
        I = ImzMLReader(result)

        # cleanup temp files
        if delete_output() == True:
            os.remove(result)

    def test_snippet_pp_imzML_no_scattered(self):
        # get data paths
        input_data = get_wdir(r"testdata\pp.imzML")
        output = get_wdir(r"tempfiles\pp")

        # convert data
        convert_data_to_snippet_imzml(input_data, output, 1, scattered=False)

        # expected result
        result = output + "_data_snippet.imzML"

        self.assertTrue(os.path.isfile(result))

        # check if m2aia parses new file
        I = ImzMLReader(result)

        # cleanup temp files
        if delete_output() == True:
            os.remove(result)


class TestConvToolsSnippetCP(unittest.TestCase):

    def test_snippet_cp_imzML_def_param(self):
        # get data paths
        input_data = get_wdir(r"testdata\cp.imzML")
        output = get_wdir(r"tempfiles\cp")

        # convert data
        convert_data_to_snippet_imzml(input_data, output)

        # expected result
        result = output + "_data_snippet.imzML"

        self.assertTrue(os.path.isfile(result))

        # check if m2aia parses new file
        I = ImzMLReader(result)

        # cleanup temp files
        if delete_output() == True:
            os.remove(result)

    def test_snippet_cp_imzML_scattered(self):
        # get data paths
        input_data = get_wdir(r"testdata\cp.imzML")
        output = get_wdir(r"tempfiles\cp")

        # convert data
        convert_data_to_snippet_imzml(input_data, output, 2, scattered=True)

        # expected result
        result = output + "_data_snippet.imzML"

        self.assertTrue(os.path.isfile(result))

        # check if m2aia parses new file
        I = ImzMLReader(result)

        # cleanup temp files
        if delete_output() == True:
            os.remove(result)

    def test_snippet_cp_imzML_no_scattered(self):
        # get data paths
        input_data = get_wdir(r"testdata\cp.imzML")
        output = get_wdir(r"tempfiles\cp")

        # convert data
        convert_data_to_snippet_imzml(input_data, output, 1, scattered=False)

        # expected result
        result = output + "_data_snippet.imzML"

        self.assertTrue(os.path.isfile(result))

        # check if m2aia parses new file
        I = ImzMLReader(result)

        # cleanup temp files
        if delete_output() == True:
            os.remove(result)


class TestConvToolsSnippetPC(unittest.TestCase):

    def test_snippet_pc_imzML_def_param(self):
        # get data paths
        input_data = get_wdir(r"testdata\pc.imzML")
        output = get_wdir(r"tempfiles\pc")

        # convert data
        convert_data_to_snippet_imzml(input_data, output)

        # expected result
        result = output + "_data_snippet.imzML"

        self.assertTrue(os.path.isfile(result))

        # check if m2aia parses new file
        I = ImzMLReader(result)

        # cleanup temp files
        if delete_output() == True:
            os.remove(result)

    def test_snippet_pc_imzML_scattered(self):
        # get data paths
        input_data = get_wdir(r"testdata\pc.imzML")
        output = get_wdir(r"tempfiles\pc")

        # convert data
        convert_data_to_snippet_imzml(input_data, output, 2, scattered=True)

        # expected result
        result = output + "_data_snippet.imzML"

        self.assertTrue(os.path.isfile(result))

        # check if m2aia parses new file
        I = ImzMLReader(result)

        # cleanup temp files
        if delete_output() == True:
            os.remove(result)

    def test_snippet_pc_imzML_no_scattered(self):
        # get data paths
        input_data = get_wdir(r"testdata\pc.imzML")
        output = get_wdir(r"tempfiles\pc")

        # convert data
        convert_data_to_snippet_imzml(input_data, output, 1, scattered=False)

        # expected result
        result = output + "_data_snippet.imzML"

        self.assertTrue(os.path.isfile(result))

        # check if m2aia parses new file
        I = ImzMLReader(result)

        # cleanup temp files
        if delete_output() == True:
            os.remove(result)


class TestConvToolsSnippetCC(unittest.TestCase):

    def test_snippet_cc_imzML_def_param(self):
        # get data paths
        input_data = get_wdir(r"testdata\cc.imzML")
        output = get_wdir(r"tempfiles\cc")

        # convert data
        convert_data_to_snippet_imzml(input_data, output)

        # expected result
        result = output + "_data_snippet.imzML"

        self.assertTrue(os.path.isfile(result))

        # check if m2aia parses new file
        I = ImzMLReader(result)

        # cleanup temp files
        if delete_output() == True:
            os.remove(result)

    def test_snippet_cc_imzML_scattered(self):
        # get data paths
        input_data = get_wdir(r"testdata\cc.imzML")
        output = get_wdir(r"tempfiles\cc")

        # convert data
        convert_data_to_snippet_imzml(input_data, output, 2, scattered=True)

        # expected result
        result = output + "_data_snippet.imzML"

        self.assertTrue(os.path.isfile(result))

        # check if m2aia parses new file
        I = ImzMLReader(result)

        # cleanup temp files
        if delete_output() == True:
            os.remove(result)

    def test_snippet_cc_imzML_no_scattered(self):
        # get data paths
        input_data = get_wdir(r"testdata\cc.imzML")
        output = get_wdir(r"tempfiles\cc")

        # convert data
        convert_data_to_snippet_imzml(input_data, output, 1, scattered=False)

        # expected result
        result = output + "_data_snippet.imzML"

        self.assertTrue(os.path.isfile(result))

        # check if m2aia parses new file
        I = ImzMLReader(result)

        # cleanup temp files
        if delete_output() == True:
            os.remove(result)


if __name__ == "__main__":
    unittest.main()
