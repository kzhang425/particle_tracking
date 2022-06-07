# -*- coding: utf-8 -*-
"""
Parameters for calculating diffusion coefficient
Created on Wed May 18 22:53:50 2022

@author: kevi
"""


def parameters():
    settings = {
        'doGaussian': True,
        'gaussianSigma': 3,
        'kernelRadius': 3,
        'histBins': 48,
        'localMaxKernel': 1,
        'histSTD': 2,
        'peakTolerance': 0,
        'histLevel': 0.5
        }
    return settings
