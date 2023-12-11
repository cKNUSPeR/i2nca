import numpy as np
import m2aia as m2
import matplotlib.pyplot as plt
from i2nca.qctools.utils import mask_bad_image, make_index_image

file_name = r"C:\Users\Jannik\Documents\Uni\Master_Biochem\4_Semester\M2aia\data\exmpl_cont\conv_output_centroided.imzML"
I = m2.ImzMLReader(file_name)

im_stats = [a for a in range(0,1400)]

im = mask_bad_image(im_stats, im_stats, make_index_image(I))

print(max(im.flatten()))