import m2aia as m2
from i2nca.convtools.conv_tools import convert_pp_to_pp_imzml

filepath = r"C:\Users\Jannik\Documents\Uni\Master_Biochem\4_Semester\M2aia\S042_Processed_imzML\S042_Processed.imzML"
I = m2.ImzMLReader(filepath)

outfile = r"C:\Users\Jannik\Documents\Uni\Master_Biochem\4_Semester\M2aia\S042_Processed_imzML\S042_out_pp"
out_path = convert_pp_to_pp_imzml(file_path=filepath, output_path=outfile)
print(out_path)

J= m2.ImzMLReader(out_path)
