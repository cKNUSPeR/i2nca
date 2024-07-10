from i2nca.qctools.dependencies import *

from i2nca.qctools.utils import evaluate_formats, get_polarity, evaluate_polarity, get_pixsize, parse_regionfile


# tools sample file generation

def split_dataset_imzml(file_path,
                        roi_path: str,
                        output_path: Optional[str] = None
                        ) -> str:
    """
    Top-level sample file producer.
    A small imzML file with a predefined numer of pixels is generated.
    The file type remains unchanged.

    Parameters
    ----------
    file_path : string
        Path of imzML file.
    roi_path:
        Path to ROI annotation.
    output_path : string ,optional
        Path to filename where the output file should be built.
        If ommitted, the file_path is used.


    Returns
    -------
    output_file : str
      File path as string of succesfully converted imzML file.
    """

    # only use quadratic values. Square root is calcualted.


    if output_path is None:
        output_path = file_path[:-6]

    # parse imzml file
    Image = m2.ImzMLReader(file_path)

    # get data format
    format_flags = evaluate_formats(Image.GetSpectrumType())

    # get the defined regions
    region_table, region_image, nr_regions = parse_regionfile(roi_path, "annotation", Image)

    region_table = make_bb_boxes(region_table, Image.GetIndexArray(), nr_regions)


    if format_flags["profile"] and format_flags["processed"]:
        return write_grouped_imzml(Image, output_path,
                                   "profile", "processed",
                                   region_table, nr_regions)

    elif format_flags["profile"] and format_flags["continuous"]:
        return write_grouped_imzml(Image, output_path,
                                   "profile", "continuous",
                                   region_table, nr_regions)

    elif format_flags["centroid"] and format_flags["processed"]:
        return write_grouped_imzml(Image, output_path,
                                   "centroid", "processed",
                                   region_table, nr_regions)

    elif format_flags["centroid"] and format_flags["continuous"]:
        return write_grouped_imzml(Image, output_path,
                                   "centroid", "continuous",
                                   region_table, nr_regions)
    else:
        raise ValueError(
            "The loaded file has an undefined spectrum or alignment type."
            "\n Please check for accessions 'MS:1000128' or 'MS:1000127'"
            "\n Please check for accessions 'IMS:1000030' or 'IMS:1000031'")



def write_grouped_imzml(Image,
                        output_dir: str,
                        spectrum_type: str,
                        alignment_type: str,
                        annotation_df,
                        group_index):
    """
    Writer for any imzml files within m2aia to their respective format.


    Parameters:
        Image:
            parsed izML file (by m2aia or equvalent object that emulates the methods)
        output_path : string ,optional
            Path to filename where the output file should be built.
            If ommitted, the file_path is used.
        spectrum_type: string
            The spectrum type. Either 'profile' or 'centroid'.
        alignment_type: string
            The alignment type. Either 'processed' or 'continuous'.
        sample_size: interget
            The number of pixels that are written in the new snippet dataset
        scattered : bool, optional
            Determines if random number of pixels are randomly distributed over image or grouped as one block
            If ommitted, True is used.


    Returns:
       (str): imzML File path,
       additionally, imzML file is written there

        """


    # specification of output imzML file location and file extension
    output_file = output_dir + "_data_snippet.imzML"


    # get the polarity
    polarity = get_polarity(evaluate_polarity(Image))

    # get the pixel size
    pix_size = get_pixsize(Image)

    for group in range(1, group_index + 1):

        # get the group
        grouped_rows = annotation_df[annotation_df["annotation_values"] == group]

        # single out the name
        output_file = output_dir + str(grouped_rows.iloc[0]["annotation"]) + ".imzML"

        #get the index values as list
        index_list = grouped_rows['index'].tolist()

        # writing of the imzML file, based on pyimzML
        with ImzMLWriter(output_file,
                         polarity=polarity,
                         mz_dtype=np.float32,
                         # intensity_dtype=np.uintc,
                         mode=alignment_type,
                         spec_type=spectrum_type,
                         pixel_size_x=pix_size,
                         pixel_size_y=pix_size,
                         # the laser movement param are adapted to TTF presets
                         scan_direction='top_down',
                         line_scan_direction='line_right_left',
                         scan_pattern='meandering',
                         scan_type='horizontal_line',
                         ) as w:
            # m2aia is 0-indexed
            for id in index_list:
                #
                mz, intensities = Image.GetSpectrum(id)
                rw = grouped_rows.loc[grouped_rows['index'] == id]
                xyz_pos = [rw["new_x"].values[0], rw["new_y"].values[0]]

                # image offset (m2aia5.1 quirk, persistent up to 5.10)
                img_offset = 1
                # offset needs to be added fro 1-based indexing of xyz system
                pos = (xyz_pos[0] + img_offset, xyz_pos[1] + img_offset)

                # writing with pyimzML

                w.addSpectrum(mz, intensities, pos)

                # progress print statement
                # if (id % 100) == 0:
                #    print(f"pixels {id}/{n} written.")




def make_bb_boxes(df, index_image, group_index):
    """Helper function to find the new x-y coordinates of the annotaion_df by the annotated group."""
    df["new_x"] = 0
    df["new_y"] = 0

    for group in range(1,group_index+1):
        grouped_rows = df[df["annotation_values"] == group]
        x_offset = min(grouped_rows["x"])
        y_offset = min(grouped_rows["y"])

        grouped_rows["new_x"] = grouped_rows["x"] - x_offset
        grouped_rows["new_y"] = grouped_rows["y"] - y_offset

        df.update(grouped_rows)

    # query the index position
    df["index"] = df.apply(lambda rows: index_image[0,rows["y"],rows["x"]], axis=1)

    return df


if __name__ == "__main__":
    cut_by_roi_imzml(r"C:\Users\Jannik\Documents\Uni\Master_Biochem\4_Semester\QCdev\src\i2nca\i2nca\tests\tempfiles\pc_combined.imzML",
                     r"C:\Users\Jannik\Documents\Uni\Master_Biochem\4_Semester\QCdev\src\i2nca\i2nca\tests\tempfiles\pc_no_annoannotated_regions.tsv",
                     r"C:\Users\Jannik\Documents\Uni\Master_Biochem\4_Semester\QCdev\src\i2nca\i2nca\tests\tempfiles\ROI_")

