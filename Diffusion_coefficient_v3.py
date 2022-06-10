# -*- coding: utf-8 -*-
"""
Diffusion_coefficient v3
Created on Wed May 18 12:53:16 2022

@author: kevi
"""
import numpy as np
import images
import particles
import matplotlib.pyplot as plt
from images import ImageData
import algorithms as al

filename = 'Single_molecule_moving.tif'
data = images.ImageData()
data.read(filename)
part = particles.Particles()
part.read(data, 0)
part.find_particles()
plt.imshow(part.denoised)
# plt.imshow(part.custom_mask)
points = al.local_max(part.denoised, part.custom_mask)
plt.scatter(points[:, 1], points[:, 0], s=10, color='white')
plt.show()
print('ok')

