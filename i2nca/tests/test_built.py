import unittest
import os as os
import subprocess as subprocess
import i2nca as i2

def get_wdir(rel_path: str):
    return str(os.path.join(os.getcwd(), rel_path))

def delete_output():
    return True


class TestVersion(unittest.TestCase):

    def test_version_number(self):
       vs = i2.get_version()

       self.assertTrue(type(vs)==str)

       print("Current i2nca version is:", vs)