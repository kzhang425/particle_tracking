# -*- coding: utf-8 -*-
"""
Parameters for calculating diffusion coefficient
Created on Wed May 18 22:53:50 2022

@author: kevi
"""


def parameters():
    settings = {
        'doGaussian': True,
        'gaussianSigma': 3,  # Sigma for gaussian blurring
        'kernelRadius': 5,  # Disc kernel size
        'histBins': 48,  # How many bins to calculate for histogram
        'localMaxKernel': 1,  # How wide is the kernel used to find the centers of the particles (radius)
        'histSTD': 2,  # Standard deviations to use when plotting histogram
        'peakTolerance': 0,
        'histLevel': 0.5,
        'imageThreshold': 0.5
        }
    return settings
