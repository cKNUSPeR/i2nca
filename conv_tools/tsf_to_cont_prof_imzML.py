# -*- coding: utf-8 -*-
"""Test program using Python wrapper for timsdata.dll to read tsf (spectrum) data"""
# this script converts .tsf data into profile processed imzML files
import sys, tsfdata, sqlite3
import numpy as np
from pyimzml.ImzMLWriter import ImzMLWriter
import random as rnd
import statistics as stat
from typing import Optional
from datetime import datetime
import m2aia as m
import matplotlib.pyplot as plt

def get_batch_from_tsf(tsffile_superdir: str):
    # setting up of sqlite reader
    tsf = tsfdata.TsfData(tsffile_superdir)
    conn = tsf.conn

    # Get total spectrum count:
    q = conn.execute("SELECT COUNT(*) FROM Frames")
    row = q.fetchone()
    n = row[0]

    # create the small sample list (100 pixels)
    batch_size = 100
    randomlist = rnd.sample(range(0, n), batch_size)


    # get length of each pixel
    mz_length = []
    for id in randomlist:
        intensities = tsf.readProfileSpectrum(id)
        mz = tsf.indexToMz(id, list(range(len(intensities))))
        mz_length.append(len(mz))

    # check if there are any pixels that do not fit the max length (or are otherwise sparce)
    max_mz_bins = max(mz_length)
    print(max_mz_bins)
    remover = []
    for i, mz in enumerate(mz_length):
        if mz != max_mz_bins:
            remover.append(i)

    # cleanup invalid pixels
    for i in remover:
        randomlist.pop(i)
        mz_length.pop(i)
    # return of nested list with m
    return mz_length, randomlist
    
    
        

def convert_tsf_to_cont_prof_imzml(tsffile_superdir: str,
                                   output_dir: Optional[str] = None
                                   ) -> str:
    """
        Converts tsf composite file to imzML.
        Assumes tsf file as processed profile spectra.
        Converts the profile spectra on the fly to centroids by manual cutoff.

        Parameters:
            tsffile_superdir (str): File path to folder that stores analysis.tsf file.
            output_dir (Opt): File path for output. in same folder as tsf if not specified.


        Returns:
           (str): imzML File directory
           also imzML file

        """
    # specification of output imzML file location and file extension
    if output_dir is None:
        output_dir = tsffile_superdir
    output_file = output_dir + "\\conv_output_cont_profile.imzML"
    
 
    # setting up of sqlite reader
    tsf = tsfdata.TsfData(tsffile_superdir)
    conn = tsf.conn

    # Get total spectrum count:
    q = conn.execute("SELECT COUNT(*) FROM Frames")
    row = q.fetchone()
    n = row[0]

    # create the small sample list (100 pixels)
    batch_size = 100
    randomlist = rnd.sample(range(0, n), batch_size)


    # get length of each pixel
    mz_length = []
    for id in randomlist:
        intensities = tsf.readProfileSpectrum(id)
        mz = tsf.indexToMz(id, list(range(len(intensities))))
        mz_length.append(len(mz))

    # check if there are any pixels that do not fit the max length (or are otherwise sparce)
    max_mz_bins = max(mz_length)
    print(max_mz_bins)
    remover = []
    for i, mz in enumerate(mz_length):
        if mz != max_mz_bins:
            remover.append(i)

    # cleanup invalid pixels
    for i in remover:
        randomlist.pop(i)
        mz_length.pop(i)

    print(f'pixels remaining for instrument bin calculation: {len(randomlist)} of {batch_size}.')

    # collect them in symmetric numpy array (mz_collector)
    intensities = tsf.readProfileSpectrum(randomlist[0])
    mz = tsf.indexToMz(randomlist[0], list(range(len(intensities))))
    mz_collector = mz


    for id in randomlist[1:]:
        intensities = tsf.readProfileSpectrum(id)
        mz = tsf.indexToMz(id, list(range(len(intensities))))
        mz_collector = np.vstack((mz_collector, mz))

    # transpose the array
    mz_collector = mz_collector.T

    aligned_mass = np.array([])
    for mass in mz_collector:
        aligned_mass = np.append(aligned_mass, [stat.mean(mass)], axis=0)

    len_aligned_mass = len(aligned_mass)


    # readout of polarity, defensive
    polarity_scan= conn.execute(f"SELECT Polarity FROM Frames").fetchone()[0]
    if polarity_scan == "+":
        polarity = "positive"
    elif polarity_scan == "-":
        polarity = "negative"
    else:
        raise ValueError("Polarity was not defined.")

    # get the pixel size, is assumed to be square
    spot_size = conn.execute(f"SELECT SpotSize FROM MaldiFrameLaserInfo").fetchone()[0]
    spot_size = str(int(spot_size))

    # writing of the imzML file, based on pyimzML
    with ImzMLWriter(output_file,
                    polarity=polarity,
                    mz_dtype= np.float64,
                    #intensity_dtype=np.uintc,
                    mode='continuous',
                    spec_type='profile',
                    # the laser movement param are taken from scilslab export
                    scan_direction='top_down',
                    line_scan_direction='line_right_left',
                    scan_pattern='meandering',
                    scan_type='horizontal_line',
                    # preinstalled pixel sizes TODO get correct ones
                    pixel_size_x=spot_size,
                    pixel_size_y=spot_size,
                    ) as w:
        # tsf data is 1-indexed
        for id in range(1, n+1):
            # gene
            intensities = tsf.readProfileSpectrum(id)
            length = len(intensities)
            mz = tsf.indexToMz(id, list(range(length)))

            x_pos = conn.execute(f"SELECT XIndexPos FROM MaldiFrameInfo WHERE Frame={id}").fetchone()[0]
            y_pos = conn.execute(f"SELECT YIndexPos FROM MaldiFrameInfo WHERE Frame={id}").fetchone()[0]
            pos = (x_pos,y_pos)

            # writing with pyimzML
            if length == len_aligned_mass:
                w.addSpectrum(aligned_mass, intensities, pos)
            else:
                print(f"Sparce pixel at {id}")
            if (id%100)== 0:
                print(f"pixels {id}/{n} written.")
    return output_file

def convert_imzML_to_cont_prof_imzml(imzML_filename: str,
                                   output_dir: Optional[str] = None
                                   ) -> str:
    """
        Converts tsf composite file to imzML.
        Assumes tsf file as processed profile spectra.
        Converts the profile spectra on the fly to centroids by manual cutoff.

        Parameters:
            tsffile_superdir (str): File path to folder that stores analysis.tsf file.
            output_dir (Opt): File path for output. in same folder as tsf if not specified.


        Returns:
           (str): imzML File directory
           also imzML file

        """
    # specification of output imzML file location and file extension
    if output_dir is None:
        output_dir = imzML_filename[:-6]
    output_file = output_dir + "_conv_output_cont_profile.imzML"
    
    # setting up of  reader
    I = m.ImzMLReader(imzML_filename)
    I.Execute()
    
    # Get total spectrum count:
    n = I.GetNumberOfSpectra()

    # create the small sample list (100 pixels)
    batch_size = 100
    randomlist = rnd.sample(range(0, n), batch_size)

    # get length of each pixel
    mz_length = []
    for id in randomlist:
        mz, intensities = I.GetSpectrum(id)
        mz_length.append(len(mz))

    # check if there are any pixels that do not fit the max length (or are otherwise sparce)
    max_mz_bins = max(mz_length)
    print("maximum discrete bins in spectrum: ", max_mz_bins)
    remover = []
    for i, mz in enumerate(mz_length):
        if mz != max_mz_bins:
            remover.append(i) 
        
    # cleanup invalid pixels
    randomlist = [ele for i, ele in enumerate(randomlist) if ele not in remover]
    print(f'pixels remaining for instrument bin calculation: {len(randomlist)} of {batch_size}.')

    # collect them in symmetric numpy array (mz_collector)
    mz, intensities = I.GetSpectrum(randomlist[0])
    mz_collector = mz


    for id in randomlist[1:]:
        mz, intensities = I.GetSpectrum(id)
        mz_collector = np.vstack((mz_collector, mz))

    # transpose the array
    mz_collector = mz_collector.T

    # align the masses to their mean
    aligned_mass = np.array([])
    for mass in mz_collector:
        aligned_mass = np.append(aligned_mass, [stat.mean(mass)], axis=0)

    len_aligned_mass = len(aligned_mass)


    # readout of polarity, defensive
    """polarity_scan= conn.execute(f"SELECT Polarity FROM Frames").fetchone()[0]
    if polarity_scan == "+":
        polarity = "positive"
    elif polarity_scan == "-":
        polarity = "negative"
    else:
        raise ValueError("Polarity was not defined.")"""

    # get the pixel size, is assumed to be square
    """spot_size = conn.execute(f"SELECT SpotSize FROM MaldiFrameLaserInfo").fetchone()[0]
    spot_size = str(int(spot_size))"""
    # writing of the imzML file, based on pyimzML
    with ImzMLWriter(output_file,
                    polarity="positive",
                    mz_dtype= np.float64,
                    #intensity_dtype=np.uintc,
                    mode='continuous',
                    spec_type='profile',
                    # the laser movement param are taken from scilslab export
                    scan_direction='top_down',
                    line_scan_direction='line_right_left',
                    scan_pattern='meandering',
                    scan_type='horizontal_line',
                    # preinstalled pixel sizes TODO get correct ones
                    pixel_size_x="20",
                    pixel_size_y="20",
                    ) as w:
        # tsf data is 1-indexed
        for id in range(0, n):
            # gene
            mz, intensities = I.GetSpectrum(id)
            length = len(intensities)
            xyz_pos = I.GetSpectrumPosition(id)
            pos = (xyz_pos[0],xyz_pos[1])

            # writing with pyimzML
            if length == len_aligned_mass:
                w.addSpectrum(aligned_mass, intensities, pos)
            else:
                print(f"Sparce pixel at {id}")
            if (id%100)== 0:
                print(f"pixels {id}/{n} written.")
    return output_file


if __name__ == "__main__":
    print(datetime.now())
    print("File succesfully generated at: ",
          convert_imzML_to_cont_prof_imzml("D:\\wittej\\data\\testdata\\conv_output_profile.imzML",
                                           "D:\\wittej\\data\\testdata")
    )
    print(datetime.now())


def imzML_check_spacing(imzML_filename: str) -> np.ndarray:
 # setting up of  reader
    I = m.ImzMLReader(imzML_filename)
    I.Execute()
    
    # Get total spectrum count:
    n = I.GetNumberOfSpectra()

    # create the small sample list (100 pixels)
    batch_size = 100
    randomlist = rnd.sample(range(0, n), batch_size)

    # instance and collect mass values from the small batch
    first_mz, _ = I.GetSpectrum(0)
    len_first_mz = len(first_mz)
    processed_collector = first_mz

    for id in randomlist: 
        mz, _ = I.GetSpectrum(id)
        # assumes that the instrument makes same amount of data points in each pixel
        if len_first_mz == len(mz):
            processed_collector = np.vstack((processed_collector,mz))

    processed_collector = processed_collector.T # transpose to easily access each group of masses 

    dpoint_mean = tuple() # collector for mean mz value of each pseudo-bin
    dpoint_spread = tuple() # collector of the standard variation within each pseudo-bin

    # iterate to get the means and the bin-spreads
    for row in processed_collector:
        dpoint_mean += (stat.mean(row),)
        dpoint_spread += (stat.stdev(row),)

    dpoint_mean = np.asarray(dpoint_mean)
    dpoint_spread = np.asarray(dpoint_spread)
    dbin_spread = np.diff(dpoint_mean) # calculation of inter-bin step size 

    fig = plt.figure(figsize=[7,5])
    ax = plt.subplot(111)

    ax.set_title('Comparison of aquisition-based binning')
    ax.set_xlabel('mz of each pseudo-bin')
    ax.set_ylabel('mz deviation')

    ax.grid(visible=True, c='lightgray', ls="--")

    ax.plot(dpoint_mean[:-1], dbin_spread, color='g',zorder=-1, 
            label=f"Stepsize between \neach pseudo-bin \nmedian: {stat.median(dbin_spread):.6f}")
    
    ax.plot(dpoint_mean, dpoint_spread, color='r',zorder=-1, 
            label=f"standard deviation \nwithin each pseudo-bin \nmedian: {stat.median(dpoint_spread):.6f}")
    

    ax.legend()
    plt.show()

    return dpoint_mean


def tsf_check_spacing(tsf_dir: str) -> np.ndarray:

     # setting up of sqlite reader
    tsf = tsfdata.TsfData(tsf_dir)
    conn = tsf.conn

    # Get total spectrum count:
    q = conn.execute("SELECT COUNT(*) FROM Frames")
    row = q.fetchone()
    n = row[0]

    # create the small sample list (100 pixels)
    batch_size = 100
    randomlist = rnd.sample(range(1, n), batch_size)

    # instance and collect mass values from the small batch
    first_mz = tsf.indexToMz(1, list(range(len(tsf.readProfileSpectrum(1))))) # retruns an ndarray
    len_first_mz = len(first_mz)
    processed_collector = first_mz

    for id in randomlist: 
        mz = tsf.indexToMz(id, list(range(len(tsf.readProfileSpectrum(id)))))
        # assumes that the instrument makes same amount of data points in each pixel
        if len_first_mz == len(mz):
            processed_collector = np.vstack((processed_collector,mz))

    processed_collector = processed_collector.T # transpose to easily access each group of masses 

    dpoint_mean = tuple() # collector for mean mz value of each pseudo-bin
    dpoint_spread = tuple() # collector of the standard variation within each pseudo-bin

    # iterate to get the means and the bin-spreads
    for row in processed_collector:
        dpoint_mean += (stat.mean(row),)
        dpoint_spread += (stat.stdev(row),)

    dpoint_mean = np.asarray(dpoint_mean)
    dpoint_spread = np.asarray(dpoint_spread)
    dbin_spread = np.diff(dpoint_mean) # calculation of inter-bin step size 

    fig = plt.figure(figsize=[7,5])
    ax = plt.subplot(111)

    ax.set_title('Comparison of aquisition-based binning')
    ax.set_xlabel('mz of each pseudo-bin')
    ax.set_ylabel('mz deviation')

    ax.grid(visible=True, c='lightgray', ls="--")

    ax.plot(dpoint_mean[:-1], dbin_spread, color='g',zorder=-1, 
            label=f"Stepsize between \neach pseudo-bin \nmedian: {stat.median(dbin_spread):.6f}")
    
    ax.plot(dpoint_mean, dpoint_spread, color='r',zorder=-1, 
            label=f"standard deviation \nwithin each pseudo-bin \nmedian: {stat.median(dpoint_spread):.6f}")
    

    ax.legend()
    plt.show()

    return dpoint_mean

def write_imzML_to_cont_prof_imzml(imzML_filename: str,
                                   ref_mz : np.ndarray,
                                   polarity: Optional[str] = "positive",
                                   pixel_size: Optional[str] = "20",
                                   output_dir: Optional[str] = None
                                   ) -> str:
    """
        Writer for continous profile imzml files within m2aia.

        Sparcity implementation:
        pixel is skipped if it does not fit the lenght requirement of the mz axis.

        
        Parameters:
            imzML_filename (str): File name of imzML file
            ref_mz(np.ndarray): An array containing the reference mz axis.
            polarity (Opt) : Polarity, either "positive" or "negative", not accessible in pym2aia
            pixel_size (Opt): pixel size of imaging run, currently not accessible in pym2aia
            output_dir (Opt): File path for output. in same folder as tsf if not specified.


        Returns:
           (str): imzML File path, 
           additionally, imzML file is written there

        """
    # specification of output imzML file location and file extension
    if output_dir is None:
        output_dir = imzML_filename[:-6]
    output_file = output_dir + "_conv_output_cont_profile.imzML"
    
    # setting up of  reader
    I = m.ImzMLReader(imzML_filename)
    I.Execute()

    # Get total spectrum count:
    n = I.GetNumberOfSpectra()
    len_ref_mz = len(ref_mz)

    # writing of the imzML file, based on pyimzML
    with ImzMLWriter(output_file,
                     # TODO get polarity from file
                    polarity=polarity,
                    mz_dtype= np.float64,
                    #intensity_dtype=np.uintc,
                    mode='continuous',
                    spec_type='profile',
                    # the laser movement param are taken from scilslab export for ttf
                    scan_direction='top_down',
                    line_scan_direction='line_right_left',
                    scan_pattern='meandering',
                    scan_type='horizontal_line',
                    # preinstalled pixel sizes TODO get correct ones
                    pixel_size_x="20",
                    pixel_size_y="20",
                    ) as w:
        
        # m2aia is 0-indexed
        for id in range(0, n):

            # 
            mz, intensities = I.GetSpectrum(id)
            length = len(intensities)

            xyz_pos = I.GetSpectrumPosition(id)
            pos = (xyz_pos[0],xyz_pos[1])

            # writing with pyimzML
            if length == len_ref_mz:
                w.addSpectrum(ref_mz, intensities, pos)
            else:
                print(f"Sparce pixel at {id}")

            if (id%100)== 0:
                print(f"pixels {id}/{n} written.")
    return output_file

def write_tsf_to_cont_prof_imzml(tsffile_superdir: str,
                                 ref_mz : np.ndarray,
                                 output_dir: Optional[str] = None
                                 ) -> str:
    
    # specification of output imzML file location and file extension
    if output_dir is None:
        output_dir = tsffile_superdir
    output_file = output_dir + "\\conv_output_cont_profile.imzML"
    
 
    # setting up of sqlite reader
    tsf = tsfdata.TsfData(tsffile_superdir)
    conn = tsf.conn

    # Get total spectrum count:
    q = conn.execute("SELECT COUNT(*) FROM Frames")
    row = q.fetchone()
    n = row[0]
    len_ref_mz = len(ref_mz)

    # readout of polarity, defensive
    polarity_scan= conn.execute(f"SELECT Polarity FROM Frames").fetchone()[0]
    if polarity_scan == "+":
        polarity = "positive"
    elif polarity_scan == "-":
        polarity = "negative"
    else:
        raise ValueError("Polarity was not defined.")

    # get the pixel size, is assumed to be square
    spot_size = conn.execute(f"SELECT SpotSize FROM MaldiFrameLaserInfo").fetchone()[0]
    spot_size = str(int(spot_size))
    
    # writing of the imzML file, based on pyimzML
    with ImzMLWriter(output_file,
                    polarity=polarity,
                    mz_dtype= np.float64,
                    #intensity_dtype=np.uintc,
                    mode='continuous',
                    spec_type='profile',
                    # the laser movement param are taken from scilslab export
                    scan_direction='top_down',
                    line_scan_direction='line_right_left',
                    scan_pattern='meandering',
                    scan_type='horizontal_line',
                    # preinstalled pixel sizes TODO get correct ones
                    pixel_size_x=spot_size,
                    pixel_size_y=spot_size,
                    ) as w:
        # tsf data is 1-indexed
        for id in range(1, n+1):
            # gene
            intensities = tsf.readProfileSpectrum(id)
            length = len(intensities)
            mz = tsf.indexToMz(id, list(range(length)))

            x_pos = conn.execute(f"SELECT XIndexPos FROM MaldiFrameInfo WHERE Frame={id}").fetchone()[0]
            y_pos = conn.execute(f"SELECT YIndexPos FROM MaldiFrameInfo WHERE Frame={id}").fetchone()[0]
            pos = (x_pos,y_pos)

            # writing with pyimzML
            if length == len_ref_mz:
                w.addSpectrum(ref_mz, intensities, pos)
            else:
                print(f"Sparce pixel at {id}")
            if (id%100)== 0:
                print(f"pixels {id}/{n} written.")
    return output_file

