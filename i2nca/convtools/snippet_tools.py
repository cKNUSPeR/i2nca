from i2nca.qctools.dependencies import *

from i2nca.qctools.utils import evaluate_formats, get_polarity, evaluate_polarity, get_pixsize


# tools sample file generation

def convert_data_to_snippet_imzml(file_path,
                                  output_path: Optional[str] = None,
                                  snippet_size: int = 25,
                                  scattered: Optional[bool] = True ) -> str:
    """
    Top-level sample file producer.
    A small imzML file with a predefined numer of pixels is generated.
    The file type remains unchanged.

    Parameters
    ----------
    file_path : string
        Path of imzML file.
    output_path : string ,optional
        Path to filename where the output file should be built.
        If ommitted, the file_path is used.
    snippet_size : int, optional
        The number of pixels that are written in the new snippet dataset.
        If ommitted, 25  pixels are returned
    scattered : bool, optional
        Determines if random number of pixels are randomly distributed over image or grouped as one block.
        If ommitted, True is used.

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

    if format_flags["profile"] and format_flags["processed"]:
        return write_snippet_imzml(Image, output_path,
                                   "profile", "processed",
                                   snippet_size, scattered)

    elif format_flags["profile"] and format_flags["continuous"]:
        return write_snippet_imzml(Image, output_path,
                                   "profile", "continuous",
                                   snippet_size, scattered)

    elif format_flags["centroid"] and format_flags["processed"]:
        return write_snippet_imzml(Image, output_path,
                                   "centroid", "processed",
                                   snippet_size, scattered)

    elif format_flags["centroid"] and format_flags["continuous"]:
        return write_snippet_imzml(Image, output_path,
                                   "centroid", "continuous",
                                   snippet_size, scattered)
    else:
        raise ValueError(
            "The loaded file has an undefined spectrum or alignment type."
            "\n Please check for accessions 'MS:1000128' or 'MS:1000127'"
            "\n Please check for accessions 'IMS:1000030' or 'IMS:1000031'")


def write_snippet_imzml(Image,
                        output_dir: str,
                        spectrum_type: str,
                        alignment_type: str,
                        sample_size: int,
                        scattered: bool) -> str:
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
    output_file = output_dir + "_conv_output_proc_profile.imzML"

    # Get total spectrum count:
    n = Image.GetNumberOfSpectra()

    # get the polarity
    polarity = get_polarity(evaluate_polarity(Image))

    # get the pixel size
    pix_size = get_pixsize(Image)

    if scattered != True:
        begin = rnd.randint(0, n)
        subsample_indices = list(range(begin, begin + n))
    # get the index of subsamples as list
    else:
        subsample_indices = rnd.sample(range(0, n), sample_size)

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
        for id in subsample_indices:
            #
            mz, intensities = Image.GetSpectrum(id)

            xyz_pos = Image.GetSpectrumPosition(id)

            # image offset (m2aia5.1 quirk, persistent up to 5.10)
            img_offset = 1
            # offset needs to be added fro 1-based indexing of xyz system
            pos = (xyz_pos[0] + img_offset, xyz_pos[1] + img_offset)

            # writing with pyimzML

            w.addSpectrum(mz, intensities, pos)

            # progress print statement
            # if (id % 100) == 0:
            #    print(f"pixels {id}/{n} written.")
    return output_file
