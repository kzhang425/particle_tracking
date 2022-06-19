# -*- coding: utf-8 -*-
"""
Parameters for calculating diffusion coefficient
Created on Wed May 18 22:53:50 2022

@author: kevi
"""


def parameters():
    settings = {
        # Whether to do a Gaussian blur in the beginning or not
        'doGaussian': True,
        'gaussianSigma': 2,  # Sigma for gaussian blurring
        'kernelRadius': 15,  # Disc kernel size for top hat transformation
        'histBins': 128,  # How many bins to calculate for histogram
        'histSTD': 2,  # Standard deviations to use when plotting histogram
        'peakTolerance': 0,
        'histLevel': 0.5,
        'imageThreshold': 5
        }
    return settings
