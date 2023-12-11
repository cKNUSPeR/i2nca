
import m2aia as m2
from qctools.qctools import report_agnostic_qc, report_calibrant_qc, report_regions_qc
import webbrowser


if __name__ == "__main__":
    file_name = r"C:\Users\Jannik\Documents\Uni\Master_Biochem\4_Semester\QCdev\testfiles\metabolomics_small_mz_processed_centroid.imzML"
    I = m2.ImzMLReader(file_name)

    #pdf1 = report_agnostic_qc(I,
    #                   r"C:\Users\Jannik\Documents\Uni\Master_Biochem\4_Semester\QCdev\testfiles\metabolomics_small_mz_processed_centroid")

    #pdf2 = report_calibrant_qc(I,
    #                    r"C:\Users\Jannik\Documents\Uni\Master_Biochem\4_Semester\QCdev\testfiles\metabolomics_small_mz_processed_centroid",
    #                    r"C:\Users\Jannik\Documents\Uni\Master_Biochem\4_Semester\M2aia\data\exmpl_cont\calibrants_9AA.csv",
    #                    0.025, 50, 0.3)

    pdf3 = report_regions_qc(I,
                      r"C:\Users\Jannik\Documents\Uni\Master_Biochem\4_Semester\QCdev\testfiles\metabolomics_small_mz_processed_centroid",
                      r"C:\Users\Jannik\Documents\Uni\Master_Biochem\4_Semester\QCdev\testfiles\metabolomics_small_mz_annotated_regions.tsv")


    #file_name_2 = r"C:\Users\Jannik\Documents\Uni\Master_Biochem\4_Semester\QCdev\testfiles\metabolomics_small_mz_processed_centroid.imzML"
    #J = m2.ImzMLReader(file_name_2)

    #webbrowser.open(pdf1, new=2)
    #webbrowser.open(pdf2, new=2)
    webbrowser.open(pdf3, new=2)
