from tsf_to_imzML_converter import convert_tsf_to_proc_prof_imzml
from tsf_to_centroid_imzML_converter import convert_tsf_to_proc_cent_imzml
from datetime import datetime


print(datetime.now())
 
print("File succesfully generated at: ",
      convert_tsf_to_proc_cent_imzml("D:\\wittej\\data\\testdata",
                                     "D:\\wittej\\data\\testdata",
                                     20)
)

print(datetime.now())

print("File succesfully generated at: ",
      convert_tsf_to_proc_prof_imzml("D:\\wittej\\data\\testdata",
                                     "D:\\wittej\\data\\testdata")
)

print(datetime.now())