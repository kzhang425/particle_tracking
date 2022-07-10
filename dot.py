# -*- coding: utf-8 -*-
"""
Dot class
Created on Thursday June 16 10:11 2022

@author: kevi
"""

import numpy as np


class Dot:
    def __init__(self):
        self.x = []
        self.y = []
        self.radii = []
        self.intensity = []
        self.times = []
        self.active = True

    def add(self, array):
        """

        Parameters
        ----------
        array : list or 1-D array
            A list containing frame, row, column, radius, and intensity in that order.

        Returns
        -------
        None
            None
        """
        f, y, x, r, i = array
        self.times.append(f)
        self.x.append(x)
        self.y.append(y)
        self.radii.append(r)
        self.intensity.append(i)

    def last_entry(self):
        """

        Returns
        -------
        Array
            An array of the most recent parameters passed into the struct.
        """
        return np.array([self.times[-1],
                         self.y[-1],
                         self.x[-1],
                         self.radii[-1],
                         self.intensity[-1]])

