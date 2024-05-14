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



class test_CLI_conv(unittest.TestCase):


    def test_pp_conv_cli_full_param(self):
        # dependant on machine and env
        executable = r"C:\Users\Jannik\.conda\envs\QCdev\python.exe"

        # denendant on machinene and built
        cli = r"C:\Users\Jannik\Documents\Uni\Master_Biochem\4_Semester\QCdev\src\i2nca\i2nca\workflows\CLI\processed_profile_cli.py"

        input_dir = get_wdir(r"testdata\pp.imzML")
        output_dir = get_wdir(r"tempfiles\pp")

        # optinal parameters
        cov = "1"
        bsl = "Median"
        bsl_hws = "20"
        nor ="RMS"
        smo ="Gaussian"
        smo_hws = "3"
        itr = "Log2"

        # prepare the command
        command = [executable, cli,
                   "--cov", cov,
                   "--bsl", bsl,
                   "--bsl_hws", bsl_hws,
                   "--nor", nor,
                   "--smo", smo,
                   "--smo_hws", smo_hws,
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

    def test_pp_conv_cli_minimal(self):
        # dependant on machine and env
        executable = r"C:\Users\Jannik\.conda\envs\QCdev\python.exe"

        # denendant on machinene and built
        cli = r"C:\Users\Jannik\Documents\Uni\Master_Biochem\4_Semester\QCdev\src\i2nca\i2nca\workflows\CLI\processed_profile_cli.py"

        input_dir = get_wdir(r"testdata\pp.imzML")
        output_dir = get_wdir(r"tempfiles\pp")

        # optinal parameters
        """cov = "1"
        bsl = "Median"
        bsl_hws = "20"
        nor = "RMS"
        smo = "Gaussian"
        smo_hws = "3"
        itr = "Log2" """

        # prepare the command
        command = [executable, cli,
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