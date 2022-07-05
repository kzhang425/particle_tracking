# -*- coding: utf-8 -*-
"""
Miscellaneous Functions
Created on Mon June 20 19:29:16 2022

@author: kevi
"""

import numpy as np
from numba import jit


def distance(a, b):
    """

    Parameters
    ----------
    a : tuple
        First point
    b : tuple
        Second point
    Returns
    -------
    c : float
        The distance between the points.

    """

    c = np.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)
    return c


@jit(nopython=True)
def cross(r):
    """

    Parameters
    ----------
    r : int
        Radius of the cross matrix to generate.

    Returns
    -------
    mat
        The "kernel" or matrix that has the shape of a cross.
    """
    s = 2 * r + 1
    mat = np.empty([s, s])
    for i in range(s):
        for j in range(s):
            if i != r and j != r:
                mat[i, j] = 0
            else:
                mat[i, j] = 1
    return mat



def find_radius(start_point, mask):
    # y is pointing downwards as in typical array-indexing fashion.
    y0, x0 = start_point

    # Make sure to not go over the bounds of the mask:
    ylim, xlim = mask.shape

    # First start with the x coordinates to find points there. Find west point here.
    x = x0
    while mask[y0, x]:
        if (mask[y0, x-1] == False) or (x == 1):
            west = (x, y0)
            break
        x -= 1

    # Now find the east-most point.
    x = x0
    while mask[y0, x]:
        if (mask[y0, x+1] == False) or (x == xlim-2):
            east = (x, y0)
            break
        x += 1

    # Repeat the same procedure but in the other dimension, y.
    y = y0
    while mask[y, x0]:
        if (mask[y+1, x0] == False) or (y == ylim-2):
            south = (x0, y)
            break
        y += 1

    # Find the north-most point.
    y = y0
    while mask[y, x0]:
        if (mask[y-1, x0] == False) or (y == 1):
            north = (x0, y)
            break
        y -= 1

    # Having found all four points, connect north to south and east to west. Find the midpoints there.
    ns_mid = (north[1] + south[1]) / 2
    ew_mid = (west[0] + east[0]) / 2
    center = [ns_mid, ew_mid]  # in (y, x) format for ease of array indexing
    c = (ew_mid, ns_mid)  # Use this one for calculating radius

    # Now calculate "radius" with the center and the four points generated, averaging in the end.
    avg_dist = np.mean([distance(c, west), distance(c, east), distance(c, north), distance(c, south)])
    return center, avg_dist


