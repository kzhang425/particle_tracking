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
from numba import jit

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
    show_plot : Boolean
        Whether to return the matplotlib figure or not.
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
    for_processing, bins = np.histogram(img, bins=params['histBins'])
    # bins = np.linspace(0, max_range, params['histBins'])
    last_num = bins[-1]
    bins = bins[:-1]
    for_processing = np.array(for_processing)
    # for_processing[0] = 0  # First peak big because of background
    if show_plot:
        fig, ax = plt.subplots()
        ax.bar(bins, for_processing, 
               width=last_num/params['histBins'],
               edgecolor='black', color='purple')
        plt.show()
        return for_processing, bins, fig
    else:
        return for_processing, bins


def triangle_threshold(hist, bins):
    """

    Parameters
    ----------
    bins : NumPy array
        Input is a NumPy array representing the bins used in said histogram.
    hist : NumPy array
        Input is a NumPy array that represents a histogram to be analyzed via triangle thresholding.

    Returns
    -------

    """

    print("Finding threshold via triangle method...")

    # First find maximum of the entire histogram.
    x_max = bins[np.argmax(hist)]
    y_max = np.max(hist)
    x_base = bins[-1]

    # The y_base should not really change here. Baseline should generally be zero.
    y_base = 0

    # m1 is the slope of the first line, peak to baseline.
    m1 = (y_max - y_base) / (x_max - x_base)
    b1 = y_max - m1 * x_max

    # Make vectors that represent histogram values.
    x_bar = bins
    y_bar = m1 * x_bar + b1

    # Set the slope of the perpendicular line as "m2". This slope will not change from
    # each histogram point.
    m2 = -1/m1

    # Iterate through the points that start from the maximum of the histogram until the far end.
    # Note that the iterable here is an index and NOT the actual x value.
    max_dist = 0
    best_coords = None
    for i in range(np.argmax(hist), len(hist)):
        hist_point = [bins[i], hist[i]]
        b2 = hist[i] - m2 * bins[i]
        # Use the classic MATLAB way of solving linear equations
        A_mat = np.array([[m2, -1],
                          [m1, -1]])
        b_vec = np.array([[-b2],
                          [-b1]])
        intersection = np.matmul(np.linalg.inv(A_mat), b_vec)
        intersection = intersection.flatten()
        dist = (hist_point[0] - intersection[0]) ** 2 + (hist_point[1] - intersection[1]) ** 2
        if dist > max_dist:
            max_dist = dist
            best_coords = hist_point
    if best_coords is not None:
        return best_coords[0]
    else:
        print("Error: Best coordinates not found.")
        return 0



# def hist_analysis(hist):
#     """
#
#     Inspired by Pystachio algorithm, all credit goes to their work. Unfortunately it is not very
#     compatible with the other algorithms and code that are used for the rest of the project
#
#     Parameters
#     ----------
#     hist : array
#         Inputs an array that represents the histogram of interest.
#
#     Returns
#     -------
#     width : float
#         The width of the first notable peak in histogram, measured in bins
#     extreme_val : int
#         Where the extreme value can be found, at index of histogram
#
#     """
#     elements = hist.shape[0]
#     level = params['histLevel']
#     data = hist / np.max(hist) # Normalize histogram data
#     indices = range(0, elements)
#     N = hist.shape[0] - 1 # Limit that any index can take
#     if hist[0] < level:
#         center = np.argmax(hist)
#     else:
#         center = np.argmin(hist)
#     extreme_val = indices[center]
#     for e in indices[:-1]:
#         if (np.sign(data[e] - level) != np.sign(data[e + 1] - level)) and e < indices[-1]:
#             lead_i = e
#             break
#     ratio_lead = (level - data[lead_i])/(data[lead_i + 1] - data[lead_i])
#     lead_index = indices[lead_i] + ratio_lead * (indices[lead_i + 1] - indices[lead_i])
#
#     # Now we find the trailing index using the established "center" variable
#     for e in indices[center:-1]:
#         if np.sign(data[e] - level) != np.sign(data[e + 1] - level) and e < indices[-1]:
#             trail_i = e
#             break
#     width = trail_i - lead_i
#     return width, extreme_val


@jit(nopython=True)
def local_max(img, mask=None):
    """

    Parameters
    ----------
    img : array
        Input image to be analyzed for local maxima. Usually works best when denoised.

    mask : boolean array
        Boolean mask based on img and must have the same dimensions as img.

    Returns
    -------
    output : Numpy array
        An array containing the coordinates of the local maxima points.

    """
    y = img.shape[0]
    x = img.shape[1]
    max_list = []
    output = []
    print('Finding local maxima...')
    for i in range(1, y-1):
        for j in range(1, x-1):
            chunk = img[i-1:i+2, j-1:j+2]

            # Check if the pixel currently is the max of the neighborhood
            if np.argmax(chunk) == 4:
                max_list.append([i, j])
    if mask is not None:
        for i, j in max_list:
            if mask[i, j]:
                output.append([i, j])
    else:
        output = max_list
    return np.array(output)


def find_radii(img, points=None):
    if points is None:
        print("No points were given to calculate radii from.")
        return 0

