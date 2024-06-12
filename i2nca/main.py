
import m2aia as m2
import matplotlib.pyplot as plt
from qctools.qc_tools import report_agnostic_qc, report_calibrant_qc, report_regions_qc
import webbrowser


if __name__ == "__main__":

    file_name = r"C:\Users\Jannik\Documents\Uni\Master_Biochem\4_Semester\QCdev\src\i2nca\i2nca\tests\testdata\cc.imzML"

    I = m2.ImzMLReader(file_name)

    fig = plt.figure(figsize=[7, 5])
    ax = plt.subplot(111)
    ax.set_title(
        f'Intensity of 78.959, "mz"] ± {50} ppm')
    ax.set_xlabel('x axis')
    ax.set_ylabel('y axis')

    im = ax.imshow(I.GetArray(78.959, tol=50)[0],
                   cmap="viridis")
    fig.show()

    print(I.GetArray(78.959, tol=50)[0])