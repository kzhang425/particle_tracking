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
from skimage.filters import gaussian, threshold_otsu
import skimage.morphology as mph
from images import *
import algorithms as al
import cv2

params = parameters()

class Particles:
    def __init__(self, num_par=0, frame=0):
        self.number = num_par
        self.frame = frame
        
    
    def read(self, image_data, frame):
        img = image_data.frame(frame)
        self.img = img
        self.frame = frame
        print("ImageData frame saved in Particle data.")
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
        if params['doGaussian'] == True:
            blur_img = gaussian(self.img, params['gaussianSigma'], preserve_range=True)
        else:
            blur_img = self.img
        footprint = mph.disk(params['kernelRadius'])
        th_img = mph.white_tophat(blur_img, footprint)
        self.denoised = th_img.astype(np.float32)
        