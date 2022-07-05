# -*- coding: utf-8 -*-
"""
Diffusion_coefficient v3
Created on Wed May 18 12:53:16 2022

@author: kevi
"""
import numpy as np
import images
import particles
import pandas as pd

filename = 'Single_molecule_moving.tif'
data = images.ImageData()
data.read(filename)
print("Data is read. Processing...")
part = particles.Particles()
part.read(data, 0)
part.find_particles()
data_array = part.particle_data
for i in range(1, data.frame_count):
    part = particles.Particles()
    part.read(data, i)
    part.find_particles()
    data_array = np.vstack((data_array, part.particle_data))

print("Calculations done. Writing data to csv file...")
column_names = ["Frame", "Row", "Column", "Radius", "Peak Intensity"]
df = pd.DataFrame(data=data_array,
                  columns=column_names)
df.to_csv("particle_data.csv")
print("Successfully exported particle data.")

