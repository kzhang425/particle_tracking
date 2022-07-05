import algorithms as al
import particles
import images
import numpy as np
import matplotlib.pyplot as plt
import misc
import time

filename = 'Single_molecule_moving.tif'
data = images.ImageData()
data.read(filename)
part = particles.Particles()
part.read(data, 0)
part.find_particles()

"""
This section is for histogram analysis
"""
# al.calc_histogram(part.blurred, True)
# plt.show()

"""
Now test the true center-finding algorithm
"""
print(part.particle_data)

