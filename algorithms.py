# -*- coding: utf-8 -*-
"""
Algorithms
Created on Thu May 19 08:15:16 2022

@author: kevi
"""

import numpy as np
from parameters import parameters
import cv2
import matplotlib.pyplot as plt

# Dictionary of parameters right here
params = parameters()


def generate_histogram(img, z=3):
    a_frame = img
    max_intensity = np.max(a_frame)
    print('Max intensity: ' + str(max_intensity))
    stdev = np.std(a_frame, axis=None)
    mean = np.mean(a_frame, axis=None)
    min = mean - (z*stdev)
    max = mean + (z*stdev)
    a = cv2.calcHist(a_frame, channels=[0], mask=None, 
                     histSize=[params['histBins']], ranges=[min, max])
    a = np.array(a.T[0])
    b = np.linspace(min, max, params['histBins'])
    plt.bar(b, a, width=max_intensity/params['histBins'], edgecolor='black', color='purple')
    plt.xlabel('Intensity')
    plt.ylabel('Pixel Count')
    plt.show()
    return a


def calc_histogram(img, show_plot=False):
    """

    Parameters
    ----------
    img : Image or NumPy array
        This function takes an image for histogram analysis.

    Returns
    -------
    for_processing : array-like
        Returns a histogram with bins corresponding to values between 0 and 
        predetermined z value away from the mean (defined in parameters).
    bins : array
        Returns the bin values from 0 to the max

    """
    max_intensity = np.max(img)
    z_val = params['histSTD']
    max_range = np.mean(img) + z_val*np.std(img)
    for_processing = cv2.calcHist(img, channels=[0], mask=None,
                                  histSize=[params['histBins']], 
                                  ranges=[0, max_range])
    bins = np.linspace(0, max_range, params['histBins'])
    for_processing = np.array(for_processing.T[0])
    for_processing[0] = 0 # First peak big because of background
    if show_plot:
        fig, ax = plt.subplots()
        ax.bar(bins, for_processing, 
               width=max_range/params['histBins'], 
               edgecolor='black', color='purple')
        plt.show()
        return for_processing, bins, fig
    else:
        return for_processing, bins


def hist_analysis(hist):
    """

    Inspired by Pystachio algorithm, all credit goes to their work.

    Parameters
    ----------
    hist : array
        Inputs an array that represents the histogram of interest.

    Returns
    -------
    width : float
        The width of the first notable peak in histogram, measured in bins
    extreme_val : int
        Where the extreme value can be found, at index of histogram

    """
    elements = hist.shape[0]
    level = params['histLevel']
    data = hist / np.max(hist) # Normalize histogram data
    indices = range(0, elements)
    N = hist.shape[0] - 1 # Limit that any index can take
    if hist[0] < level:
        center = np.argmax(hist)
    else:
        center = np.argmin(hist)
    extreme_val = indices[center]
    for e in indices[:-1]:
        if (np.sign(data[e] - level) != np.sign(data[e + 1] - level)) and e < indices[-1]:
            lead_i = e
            break
    ratio_lead = (level - data[lead_i])/(data[lead_i + 1] - data[lead_i])
    lead_index = indices[lead_i] + ratio_lead * (indices[lead_i + 1] - indices[lead_i])
    
    # Now we find the trailing index using the established "center" variable
    for e in indices[center:-1]:
        if np.sign(data[e] - level) != np.sign(data[e + 1] - level) and e < indices[-1]:
            trail_i = e
            break
    width = trail_i - lead_i
    return width, extreme_val


def local_max(img):
    y = img.shape[0]
    x = img.shape[1]
    k_size = params['localMaxKernel']



    