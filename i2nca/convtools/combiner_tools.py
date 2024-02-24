import numpy as np

from i2nca.qctools.dependencies import *

from i2nca.qctools.utils import evaluate_formats, evaluate_image_corners, evaluate_polarity, get_polarity, get_pixsize


def combine_datasets_imzml(path_list: list[str],
                           output_path: Optional[str] = None,
                           norm_method: str = "RMS",
                           padding: int = 20) -> str:
    """
    Top-level joiner of different imzML files.
    Only files with the same spectral type can be joined.
    The output is a processed imzML.

    This converter does not explicitly change files.
    Converts all read data to float32 arrays.

    Parameters
    ----------
    path_list : list[string]
        List of paths  to the imzML files.
    output_path : string ,optional
        Path to filename where the output file should be built.
        If ommitted, the file path of the first element in the list is used.
    norm_method : string
        Normalization method applied to each individual dataset before joining.
        If ommitted, the Root Mean Square Normalization is used.
    padding : integer
        The free pixels that are added in x dim between combined datasets.
        If ommited, a space of 20 pixels is insterted.

    Returns
    -------
    output_file : str
      File path as string of succesfully converted imzML file.
    """

    # return singe datasets
    if len(path_list) == 1:
        return path_list[0]

    # chack empty path
    if output_path is None:
        output_path = path_list[0][:-6]

    output_file = output_path + "_combined.imzML"

    # parse imzml files
    image_array = [m2.ImzMLReader(file_path, normalization=norm_method) for file_path in path_list]

    # get spectral types
    type_array = [evaluate_formats(Image.GetSpectrumType()) for Image in image_array]

    # check the spectral typing of the first element
    if type_array[0]["centroid"] == True:
        spectrum_type = "centroid"
    else:
        spectrum_type = "profile"

    for image_type in type_array:
        if image_type[spectrum_type] != True:
            raise ValueError("Not all files for combination are provided as centroid spectra."
                             "\n Please check for accessions 'MS:1000128' or 'MS:1000127'"
                                 )



    # get polarity array
    polarity_array = [get_polarity(evaluate_polarity(Image)) for Image in image_array]

    first_polarity = polarity_array[0]

    for polarity in polarity_array:
        if  polarity != first_polarity:
            raise ValueError("Not all files have the same polarity."
                             "They cannot be combined"
                                 )

    # get pixel size array
    pix_array = [get_pixsize(Image) for Image in image_array]

    first_pix = pix_array[0]

    for pix in pix_array:
        if pix != first_pix:
            raise ValueError("Not all files have the same pixel size. "
                             "They cannot be combined"
                             )

    # else: # implicit check on profile data
    #     for image_type in type_array:
    #
    #         if image_type["profile"] != True:
    #             raise ValueError("Not all files for combination are provided as profile spectra."
    #                              "\n Please check for accessions 'MS:1000128' or 'MS:1000127'"
    #                              )


    # image corners at [0]:x_min, [1]:x_max, [2]:y_min, [3]:y_max
    image_corner_data = np.zeros((4, len(image_array) ))

    # get all the image corner dat,a
    for i, Image in enumerate(image_array):
        x_lims, y_lims = evaluate_image_corners(Image.GetMaskArray()[0])
        image_corner_data[0][i],image_corner_data[1][i]  = x_lims
        image_corner_data[2][i],image_corner_data[3][i]  = x_lims

    # array for image offsets ([0]: x offset and [1]:y offset)
    image_offsets = np.zeros((2, len(image_array) ))

    for i in range(0, len(image_array)):
        if i == 0:
            image_offsets[0][i], image_offsets[1][i] = (0-image_corner_data[0][0], 0-image_corner_data[0][0])
        else:
            # offset of xmax from prev (xmax of ori and added offset),
            prev_img_max_padded = image_corner_data[1][i-1] + image_offsets[0][i-1] + padding
            image_offsets[0][i], image_offsets[1][i] = (prev_img_max_padded - image_corner_data[0][0], 0 - image_corner_data[0][0])

        # write all the files:

        with ImzMLWriter(output_file,
                         polarity=first_polarity,
                         mz_dtype=np.float32,
                         # intensity_dtype=np.uintc,
                         mode="processed",
                         spec_type=spectrum_type,
                         pixel_size_x=first_pix,
                         pixel_size_y=first_pix,
                         # the laser movement param are adapted to TTF presets
                         scan_direction='top_down',
                         line_scan_direction='line_right_left',
                         scan_pattern='meandering',
                         scan_type='horizontal_line',
                         ) as w:
            for i, Image in enumerate(image_array):

                # Get total spectrum count:
                n = Image.GetNumberOfSpectra()

                # m2aia is 0-indexed
                for id in range(0, n):
                    #
                    mz, intensities = Image.GetSpectrum(id)

                    xyz_pos = Image.GetSpectrumPosition(id)

                    # image offset (m2aia5.1 quirk, persistent up to 5.10)
                    img_offset = 1
                    # offset needs to be added fro 1-based indexing of xyz system and real offset
                    pos = (xyz_pos[0] + img_offset + image_offsets[0][i], xyz_pos[1] + img_offset + image_offsets[1][i])

                    # writing with pyimzML

                    w.addSpectrum(mz, intensities, pos)
    return output_file

