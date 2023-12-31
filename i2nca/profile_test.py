
import m2aia as m2
from qctools.qctools import report_agnostic_qc, report_calibrant_qc, report_regions_qc


if __name__ == "__main__":
    file_name = r"C:\Users\Jannik\Documents\Uni\Master_Biochem\4_Semester\QCdev\testfiles\metabolomics_small_mz_continuous_profile.imzML"
    I = m2.ImzMLReader(file_name)

    report_agnostic_qc(I,
                       r"C:\Users\Jannik\Documents\Uni\Master_Biochem\4_Semester\QCdev\testfiles\metabolomics_small_mz_continuous_profile")

    report_calibrant_qc(I,
                        r"C:\Users\Jannik\Documents\Uni\Master_Biochem\4_Semester\QCdev\testfiles\metabolomics_small_mz_continuous_profile",
                        r"C:\Users\Jannik\Documents\Uni\Master_Biochem\4_Semester\M2aia\data\exmpl_cont\calibrants_9AA.csv",
                        0.025, 50, 0.3)

    report_regions_qc(I,
                      r"C:\Users\Jannik\Documents\Uni\Master_Biochem\4_Semester\QCdev\testfiles\metabolomics_small_mz_continuous_profile")



