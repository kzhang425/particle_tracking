# -*- coding: utf-8 -*-
"""
Image Data Info
Created on Wed May 18 11:27:42 2022

@author: kevi
"""
import skimage.io as skio
import numpy as np
import matplotlib.pyplot as plt
from skimage.filters import gaussian
import imageio
import skimage.morphology as morph
from skimage.morphology import disk

# Basic functions
def i_range(img):
    return np.min(img), np.max(img)

# Classes
class ImageData:
    
    def __init__(self, imgs=None):
        self.raw_data = imgs
        self.max_intensity = np.max(self.raw_data)
        if imgs is not None:
            self.frame_count = imgs.shape[0]
        
    def read(self, filename):
        self.raw_data = skio.imread(filename)
        self.max_intensity = np.max(self.raw_data)
        self.frame_count = self.raw_data.shape[0]
        
    def write(self, filename):
        """

        Parameters
        ----------
        filename : string
            Name of file to export to.

        """
        if self.raw_data is not None:
            imageio.mimwrite(filename, self.raw_data)
        else:
            print('No image exists.')
            return 0
        
    def frame(self, i):
        return self.raw_data[i, :, :]

    def dimensions(self):
        z, y, x = self.raw_data.shape
        print('Frame Dimensions: ' + str(x) + ' pixels wide and ' + str(y) + ' pixels tall')
        print('There are ' + str(z) + ' frames in the movie')
        return x, y, z
    
    def gauss_filter(self, Gaussian_sigma=1, image_data=True):
        """
        Parameters
        ----------
        Gaussian_sigma : TYPE, optional
            This determines the strength of blurring. The default is 1.
        image_data : TYPE, optional
            This parameter makes the output another ImageData. The default is True.

        Returns
        -------
        imgs_after : TYPE
            Another ImageData object by default or the NumPy array if image_data is False.

        """
        imgs_after = []
        for img in self.raw_data:
            imgs_after.append(gaussian(img, sigma=Gaussian_sigma))
        imgs_after = np.array(imgs_after)
        if image_data:
            return ImageData(imgs_after)
        else:
            return imgs_after
        
    def top_hat(self, disk_size=1, image_data=True):
        t_imgs = []
        footprint = disk(disk_size)
        for img in self.raw_data:
            t_imgs.append(morph.white_tophat(img, footprint))
        t_imgs = np.array(t_imgs)
        if image_data:
            return ImageData(t_imgs)
        else:
            return t_imgs
        
        