# -*- coding: utf-8 -*-
"""
Spot finder
Created on Wed May 18 21:27:50 2022

@author: kevi
"""
# Note that this class only applies to a single frame

import numpy as np
import matplotlib.pyplot as plt
from parameters import parameters
from skimage.filters import gaussian
import skimage.morphology as mph
from images import *
import algorithms as al
import cv2

params = parameters()


class Particles:
    def __init__(self, frame=None):
        self.coords = None
        self.custom_mask = None
        self.filtered_img = None
        self.img_no_background = None
        self.img = None
        self.frame = frame
        
    
    def read(self, image_data, frame):
        img = image_data.frame(frame)
        self.img = img
        self.frame = frame
        print("ImageData frame saved as Particles object.")
        return img
        
    def a_histogram(self, z=3):
        """

        Parameters
        ----------
        z : float, optional
            How many standard deviations away to view. The default is 3.

        Returns
        -------
        None.

        """
        a_frame = self.img
        stdev = np.std(a_frame, axis=None)
        mean = np.mean(a_frame, axis=None)
        min = mean - (z*stdev)
        max = mean + (z*stdev)
        a = cv2.calcHist(a_frame, channels=[0], mask=None, 
                         histSize=[params['histBins']], ranges=[min, max])
        a = np.array(a.T[0])
        b = np.linspace(min, max, params['histBins'])
        plt.bar(b, a, width=1, edgecolor='black', color='purple')
        plt.xlabel('Intensity')
        plt.ylabel('Pixel Count')
        plt.show()


    def find_particles(self):
        """

        Parameters
        ----------
        self : Numpy Array
            Takes the frame of the Particles object.

        Returns
        -------
        coords : Numpy Array
            An array containing the array indices of particle centers.

        """

        # Optional Gaussian blur, but highly recommended.
        if params['doGaussian']:
            blur_img = gaussian(self.img, params['gaussianSigma'], preserve_range=True)
        else:
            blur_img = self.img
        footprint = mph.disk(params['kernelRadius'])
        th_img = mph.white_tophat(blur_img, footprint)

        # For compatibility, the image is turned into a float32 so skimage can still process it.
        self.filtered_img = th_img.astype(np.float32)
        self.custom_mask = self.filtered_img > params['imageThreshold']

        # Set background to zero by multiplication with binary mask.
        img_no_background = blur_img * self.custom_mask
        self.img_no_background = img_no_background.astype(np.float32)

        # Use iterative algorithm to determine local maxima and filter out those in the background.
        self.coords = al.local_max(self.img_no_background, self.custom_mask)

