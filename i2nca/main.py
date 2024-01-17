
import m2aia as m2
from qctools.qctools import report_agnostic_qc, report_calibrant_qc, report_regions_qc
import webbrowser


if __name__ == "__main__":

    #file_name = r"C:\Users\Jannik\Documents\Uni\Master_Biochem\4_Semester\QCdev\testfiles\metabolomics_small_mz_processed_centroid.imzML"
    file_name = r"C:\Users\Jannik\Documents\Uni\Master_Biochem\4_Semester\M2aia\data\exmpl_cont\conv_output_centroided.imzML"

    I = m2.ImzMLReader(file_name)

    # pdf1 = report_agnostic_qc(I,
    #                    file_name[:-6])
    # webbrowser.open(pdf1, new=2)
    #
    # pdf2 = report_calibrant_qc(I,
    #                     file_name[:-6],
    #                    r'C:\Users\Jannik\Documents\Uni\Master_Biochem\4_Semester\M2aia\data\exmpl_cont\calibrants_9AA.csv',
    #                     50, 0.3)
    # webbrowser.open(pdf2, new=2)

    pdf3 = report_regions_qc(I,
                      file_name[:-6],
                      #r"C:\Users\Jannik\Documents\Uni\Master_Biochem\4_Semester\QCdev\testfiles\metabolomics_small_mz_annotated_regions.tsv")
                      r"C:\Users\Jannik\Documents\Uni\Master_Biochem\4_Semester\M2aia\data\exmpl_cont\kidney_annotated_regions.tsv")
    webbrowser.open(pdf3, new=2)


    #file_name = r"C:\Users\Jannik\Documents\Uni\Master_Biochem\4_Semester\M2aia\data\exmpl_cont\conv_output_centroided.imzML"
    #J = m2.ImzMLReader(file_name_2)




