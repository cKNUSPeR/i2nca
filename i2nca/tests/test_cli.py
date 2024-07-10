import unittest
import os as os
import subprocess as subprocess

from i2nca import report_agnostic_qc, report_calibrant_qc, report_regions_qc


def get_wdir(rel_path: str):
    return str(os.path.join(os.getcwd(), rel_path))


def delete_output():
    return False


class TestCLI_QC(unittest.TestCase):

    def test_agnostic_qc_cli(self):
        # dependant on machine and env
        executable = r"C:\Users\Jannik\.conda\envs\QCdev\python.exe"

        # denendant on machinene and built
        cli = r"C:\Users\Jannik\Documents\Uni\Master_Biochem\4_Semester\QCdev\src\i2nca\i2nca\workflows\CLI\agnostic_qc_cli.py"

        input_dir = get_wdir(r"testdata\cc.imzML")
        output_dir = get_wdir(r"tempfiles\cc")
        #input_dir = r"C:\Users\Jannik\Documents\Uni\Master_Biochem\4_Semester\QCdev\src\i2nca\i2nca\tests\testdata\cc.imzML"
        #output_dir = r"C:\Users\Jannik\Documents\Uni\Master_Biochem\4_Semester\QCdev\src\i2nca\i2nca\tests\tempfiles\empty"

        # prepare the command
        command = [executable, cli,input_dir,output_dir]
        # run in shell
        subprocess.run(command)

        #check expected result
        result = output_dir + "_agnostic_QC.pdf"

        # assert file building
        self.assertTrue(os.path.isfile(result))

        # cleanup temp files
        if delete_output() == True:
            os.remove(result)

    def test_calibrant_qc_cli(self):
        # dependant on machine and env
        executable = r"C:\Users\Jannik\.conda\envs\QCdev\python.exe"

        # denendant on machinene and built
        cli = r"C:\Users\Jannik\Documents\Uni\Master_Biochem\4_Semester\QCdev\src\i2nca\i2nca\workflows\CLI\agnostic_qc_cli.py"

        input_dir = get_wdir(r"testdata\cc.imzML")
        output_dir = get_wdir(r"tempfiles\cc")
        calibrants_dir = get_wdir(r"testdata\calibrant.csv")

        # optinal parameters
        ppm = "5"
        sample_size = "1"

        # prepare the command
        command = [executable, cli,
                   "--ppm", ppm, "--sample_size", sample_size,
                   input_dir, output_dir, calibrants_dir]
        # run in shell
        subprocess.run(command)

        # check expected result
        result = output_dir + "_calibrant_QC.pdf"

        # assert file building
        self.assertTrue(os.path.isfile(result))

        # cleanup temp files
        if delete_output() == True:
            os.remove(result)

    def test_region_qc_cli(self):
        # dependant on machine and env
        executable = r"C:\Users\Jannik\.conda\envs\QCdev\python.exe"

        # denendant on machinene and built
        cli = r"C:\Users\Jannik\Documents\Uni\Master_Biochem\4_Semester\QCdev\src\i2nca\i2nca\workflows\CLI\region_qc_cli.py"

        input_dir = get_wdir(r"testdata\cc.imzML")
        output_dir = get_wdir(r"tempfiles\cc")
        region_dir = get_wdir(r"testdata\regions.tsv")

        # optinal parameters

        # prepare the command
        command = [executable, cli, input_dir, output_dir, region_dir]
        # run in shell
        subprocess.run(command)

        # check expected result
        result = output_dir + "_region_QC.pdf"

        # assert file building
        self.assertTrue(os.path.isfile(result))

        # cleanup temp files
        if delete_output() == True:
            os.remove(result)



class test_CLI_conv_pp(unittest.TestCase):


    def test_pp_conv_cli_full_param(self):
        # dependant on machine and env
        executable = r"C:\Users\Jannik\.conda\envs\QCdev\python.exe"

        # denendant on machinene and built
        cli = r"C:\Users\Jannik\Documents\Uni\Master_Biochem\4_Semester\QCdev\src\i2nca\i2nca\workflows\CLI\processed_profile_cli.py"

        input_dir = get_wdir(r"testdata\pp.imzML")
        output_dir = get_wdir(r"tempfiles\pp")
        method = "fixed_bins"
        cov = "1"
        ppm = "10"

        # optinal parameters
        bsl = "Median"
        bsl_hws = "20"
        nor ="RMS"
        smo ="Gaussian"
        smo_hws = "3"
        itr = "Log2"

        # prepare the command
        command = [executable, cli,
                   "--cov", cov,
                   "--acc", ppm,
                   "--bsl", bsl,
                   "--bsl_hws", bsl_hws,
                   "--nor", nor,
                   "--smo", smo,
                   "--smo_hws", smo_hws,
                   "--itr", itr,
                   input_dir, output_dir,
                   method]
        # run in shell
        subprocess.run(command)

        # check expected result
        result = output_dir + "_conv_output_cont_profile.imzML"

        # assert file building
        self.assertTrue(os.path.isfile(result))

        # cleanup temp files
        if delete_output() == True:
            os.remove(result)

    def test_pp_conv_cli_minimal_alignment(self):
        # dependant on machine and env
        executable = r"C:\Users\Jannik\.conda\envs\QCdev\python.exe"

        # denendant on machinene and built
        cli = r"C:\Users\Jannik\Documents\Uni\Master_Biochem\4_Semester\QCdev\src\i2nca\i2nca\workflows\CLI\processed_profile_cli.py"

        input_dir = get_wdir(r"testdata\pp.imzML")
        output_dir = get_wdir(r"tempfiles\pp")
        input_dir = get_wdir(r"testdata\pp.imzML")
        output_dir = get_wdir(r"tempfiles\pp")
        method = "fixed_alignment"
        cov = "1"

        # optinal parameters

        # prepare the command
        command = [executable, cli,
                   "--cov", cov,
                   input_dir, output_dir,
                   method]
        # run in shell
        subprocess.run(command)

        # check expected result
        result = output_dir + "_conv_output_cont_profile.imzML"

        # assert file building
        self.assertTrue(os.path.isfile(result))

        # cleanup temp files
        if delete_output() == True:
            os.remove(result)

    def test_pp_conv_cli_minimal_bins(self):
        # dependant on machine and env
        executable = r"C:\Users\Jannik\.conda\envs\QCdev\python.exe"

        # denendant on machinene and built
        cli = r"C:\Users\Jannik\Documents\Uni\Master_Biochem\4_Semester\QCdev\src\i2nca\i2nca\workflows\CLI\processed_profile_cli.py"

        input_dir = get_wdir(r"testdata\pp.imzML")
        output_dir = get_wdir(r"tempfiles\pp")
        input_dir = get_wdir(r"testdata\pp.imzML")
        output_dir = get_wdir(r"tempfiles\pp")
        method = "fixed_bins"
        ppm = "200"

        # optinal parameters

        # prepare the command
        command = [executable, cli,
                   "--acc", ppm,
                   input_dir, output_dir,
                   method]
        # run in shell
        subprocess.run(command)

        # check expected result
        result = output_dir + "_conv_output_cont_profile.imzML"

        # assert file building
        self.assertTrue(os.path.isfile(result))

        # cleanup temp files
        if delete_output() == True:
            os.remove(result)

    def test_pp_conv_cli_mixed(self):
        # dependant on machine and env
        executable = r"C:\Users\Jannik\.conda\envs\QCdev\python.exe"

        # denendant on machinene and built
        cli = r"C:\Users\Jannik\Documents\Uni\Master_Biochem\4_Semester\QCdev\src\i2nca\i2nca\workflows\CLI\processed_profile_cli.py"

        input_dir = get_wdir(r"testdata\pp.imzML")
        output_dir = get_wdir(r"tempfiles\pp")
        cov = "1"

        # optinal parameters
        itr = "Log2"

        # prepare the command
        command = [executable, cli,
                   "--cov", cov,
                   "--itr", itr,
                   input_dir, output_dir]
        # run in shell
        subprocess.run(command)

        # check expected result
        result = output_dir + "_conv_output_cont_profile.imzML"

        # assert file building
        self.assertTrue(os.path.isfile(result))

        # cleanup temp files
        if delete_output() == True:
            os.remove(result)


class test_CLI_conv_prof(unittest.TestCase):

    def test_pc_conv_cli_set_find_peaks_full_param(self):
        # dependant on machine and env
        executable = r"C:\Users\Jannik\.conda\envs\QCdev\python.exe"

        # denendant on machinene and built
        cli = r"C:\Users\Jannik\Documents\Uni\Master_Biochem\4_Semester\QCdev\src\i2nca\i2nca\workflows\CLI\profile_2_centroid_cli.py"

        input_dir = get_wdir(r"testdata\pp.imzML")
        output_dir = get_wdir(r"tempfiles\test")
        method = "set_find_peaks"

        # optinal parameters
        fp_hei = "10"
        fp_thr = "2"
        fp_dis = "1"
        fp_pro = "0.5"
        fp_wid = "2"
        fp_wlen = "1"
        fp_rhei = "1"
        fp_pla = "1"

        # prepare the command
        command = [executable, cli,
                   "--fp_hei", fp_hei,
                   "--fp_thr", fp_thr,
                   "--fp_dis", fp_dis,
                   "--fp_pro", fp_pro,
                   "--fp_wid", fp_wid,
                   "--fp_wlen", fp_wlen,
                   "--fp_rhei", fp_rhei,
                   "--fp_pla", fp_pla,
                   input_dir, output_dir,
                   method]
        # run in shell
        subprocess.run(command)

        # check expected result
        result = output_dir + "_conv_output_proc_centroid.imzML"

        # assert file building
        self.assertTrue(os.path.isfile(result))

        # cleanup temp files
        if delete_output() == True:
            os.remove(result)

    # add the find_peaks_cwt method


class test_CLI_conv_proc_cent(unittest.TestCase):

    def test_cc_conv_cli_bins_200(self):
        # dependant on machine and env
        executable = r"C:\Users\Jannik\.conda\envs\QCdev\python.exe"

        # denendant on machinene and built
        cli = r"C:\Users\Jannik\Documents\Uni\Master_Biochem\4_Semester\QCdev\src\i2nca\i2nca\workflows\CLI\pc_2_cc_cli.py"

        input_dir = get_wdir(r"testdata\pc.imzML")
        output_dir = get_wdir(r"tempfiles\cc")
        method = "fixed"

        # optinal parameters
        acc = "200"

        # prepare the command
        command = [executable, cli,
                   "--acc", acc,
                   input_dir, output_dir,
                   method]
        # run in shell
        subprocess.run(command)

        # check expected result
        result = output_dir + "_conv_output_cont_centroid.imzML"

        # assert file building
        self.assertTrue(os.path.isfile(result))

        # cleanup temp files
        if delete_output() == True:
            os.remove(result)

    def test_cc_conv_cli_unique(self):
        # dependant on machine and env
        executable = r"C:\Users\Jannik\.conda\envs\QCdev\python.exe"

        # denendant on machinene and built
        cli = r"C:\Users\Jannik\Documents\Uni\Master_Biochem\4_Semester\QCdev\src\i2nca\i2nca\workflows\CLI\pc_2_cc_cli.py"

        input_dir = get_wdir(r"testdata\pc.imzML")
        output_dir = get_wdir(r"tempfiles\cc")
        method = "unique"

        # optinal parameters
        acc = "200"


        # prepare the command
        command = [executable, cli,
                   "--acc", acc,
                   input_dir, output_dir,
                   method]
        # run in shell
        subprocess.run(command)

        # check expected result
        result = output_dir + "_conv_output_cont_centroid.imzML"

        # assert file building
        self.assertTrue(os.path.isfile(result))

        # cleanup temp files
        if delete_output() == True:
            os.remove(result)


class test_CLI_joiner(unittest.TestCase):

    def test_4_joins_no_Args(self):
        # dependant on machine and env
        executable = r"C:\Users\Jannik\.conda\envs\QCdev\python.exe"

        # denendant on machinene and built
        cli = r"C:\Users\Jannik\Documents\Uni\Master_Biochem\4_Semester\QCdev\src\i2nca\i2nca\workflows\CLI\file_joiner_cli.py"

        input_dir = get_wdir(r"testdata\cc.imzML")
        output_dir = get_wdir(r"tempfiles\joined")

        # prepare the command
        command = [executable, cli,
                   output_dir,
                   input_dir, input_dir, input_dir, input_dir]

        # run in shell
        subprocess.run(command)

        # check expected result
        result = output_dir + "_combined.imzML"

        # assert file building
        self.assertTrue(os.path.isfile(result))

        # cleanup temp files
        if delete_output() == True:
            os.remove(result)

    def test_4_joins_all_Args(self):
        # dependant on machine and env
        executable = r"C:\Users\Jannik\.conda\envs\QCdev\python.exe"

        # denendant on machinene and built
        cli = r"C:\Users\Jannik\Documents\Uni\Master_Biochem\4_Semester\QCdev\src\i2nca\i2nca\workflows\CLI\file_joiner_cli.py"

        input_dir = get_wdir(r"testdata\cc.imzML")
        output_dir = get_wdir(r"tempfiles\joined")

        norm = "RMS"
        pad = "2"
        cols = "3"
        polarity = "negative"

        # prepare the command
        command = [executable, cli,
                   "--nor", norm,
                   "--pad",pad,
                   "--col",cols,
                   "--pol",polarity,
                   output_dir,
                   input_dir, input_dir, input_dir, input_dir]

        # run in shell
        subprocess.run(command)

        # check expected result
        result = output_dir + "_combined.imzML"

        # assert file building
        self.assertTrue(os.path.isfile(result))

        # cleanup temp files
        if delete_output() == True:
            os.remove(result)

class test_CLI_cutter(unittest.TestCase):

    def test_cutter(self):
        # dependant on machine and env
        executable = r"C:\Users\Jannik\.conda\envs\QCdev\python.exe"

        # denendant on machinene and built
        cli = r"C:\Users\Jannik\Documents\Uni\Master_Biochem\4_Semester\QCdev\src\i2nca\i2nca\workflows\CLI\file_cutter_cli.py"

        input_data = get_wdir(r"testdata\combined_pc.imzML")
        input_roi = get_wdir(r"testdata\combined_pc_roi.tsv")

        output_dir = get_wdir(r"tempfiles\ROI_")

        # prepare the command
        command = [executable, cli,
                   input_data, input_roi, output_dir]

        # run in shell
        subprocess.run(command)

        # expected result
        result1 = output_dir + "A.imzML"
        result2 = output_dir + "B.imzML"

        self.assertTrue(os.path.isfile(result1))
        self.assertTrue(os.path.isfile(result2))

        # cleanup temp files
        if delete_output() == True:
            os.remove(result1)
            os.remove(result2)


class test_CLI_version(unittest.TestCase):

    def test_get_version(self):
        # dependant on machine and env
        executable = r"C:\Users\Jannik\.conda\envs\QCdev\python.exe"

        # independant off machinene
        com = r"i2nca_version"


        # prepare the command
        command = [executable, com]

        # run in shell
        subprocess.run(command)