
import m2aia as m2
from qctools.qc_tools import report_agnostic_qc, report_calibrant_qc, report_regions_qc
import webbrowser


if __name__ == "__main__":

    file_name = r"D:\data\Jannik\Files_for_minidata\proteo\proteomics_full_mz_processed_profile.imzML"

    I = m2.ImzMLReader(file_name)

    pdf1 = report_agnostic_qc(I,
                       file_name[:-6])
    webbrowser.open(pdf1, new=2)

    pdf2 = report_calibrant_qc(I,
                        file_name[:-6],
                        r"D:\data\Jannik\Files_for_minidata\proteo\calibrants_peptides.csv",
                        50, 1)
    webbrowser.open(pdf2, new=2)

    pdf3 = report_regions_qc(I,
                      file_name[:-6],
                      False)
                      #r"C:\Users\Jannik\Documents\Uni\Master_Biochem\4_Semester\M2aia\data\exmpl_cont\kidney_annotated_regions.tsv")
    webbrowser.open(pdf3, new=2)

