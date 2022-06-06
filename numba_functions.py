# -*- coding: utf-8 -*-
"""
Numba Functions to use
Created on Wed May 18 10:41:37 2022

@author: kevi
"""
from skimage.filters import gaussian
import numpy as np
from numba import jit

# Image filtering steps

def Gauss_loop(imgs, Gaussian_sigma):
    imgs_after = []
    for img in imgs:
        imgs_after.append(gaussian(img, sigma=Gaussian_sigma))
    imgs_after = np.array(imgs_after)
    return imgs_after