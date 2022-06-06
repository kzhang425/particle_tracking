# -*- coding: utf-8 -*-
"""
Better Diffusion Coefficient
Created on Tue May 17 22:48:53 2022

@author: kevi
"""

import numpy as np
import skimage.io as skio
import matplotlib.pyplot as plt
import skimage.morphology as morph
import numba_functions as funs
import images


# Read in the file:
filename = 'Single_molecule_moving'
filetype = 'tif'
imgs = skio.imread(filename + '.' + filetype)

# Options
do_Gaussian = True # Do Gaussian or not
Gaussian_sigma = 1 # Higher means more blurring
kernel_size = 1 # For footprint in top hat transformation, takes longer for bigger kernel

# Filtering
if do_Gaussian:
    imgs_after = funs.Gauss_loop(imgs, Gaussian_sigma)
else:
        imgs_after = imgs
footprint = morph.disk(kernel_size)

t_imgs = []
for img in imgs_after:
    t_imgs.append(morph.white_tophat(img, footprint))
t_imgs = np.array(t_imgs)

# Testing/Visualization
plt.imshow(imgs[0, :, :])