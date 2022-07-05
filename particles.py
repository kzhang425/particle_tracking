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
        self.img = None
        self.frame = frame
        
    
    def read(self, image_data, frame, confirm=False):
        img = image_data.frame(frame)
        self.img = img
        self.frame = frame
        if confirm:
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
        blur_img = blur_img - np.min(blur_img)
        self.blurred = blur_img
        hist, bins = al.calc_histogram(self.blurred, False)
        threshold = al.triangle_threshold(hist, bins)
        footprint = mph.disk(params['kernelRadius'])
        custom_mask = blur_img > threshold
        bool_mask = mph.white_tophat(custom_mask, footprint)
        self.mask = bool_mask
        self.filtered_img = bool_mask * blur_img


        # Use iterative algorithm to determine local maxima and filter out those in the background.
        self.peak_list = al.local_max(self.filtered_img, bool_mask)

        # Use the list of local maxima to calculate particle centers, radii, and intensity.
        some_data = al.find_radii(self.filtered_img, self.mask, self.peak_list)

        # Add which frame the data belongs to for ease of identification and modularization.
        full_particle_data = []
        for row in some_data:
            line = [self.frame, row[0], row[1], row[2], row[3]]
            full_particle_data.append(line)

        self.particle_data = np.array(full_particle_data)

