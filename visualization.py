import algorithms as al
import particles
import images
import numpy as np
import matplotlib.pyplot as plt

filename = 'Single_molecule_moving.tif'
data = images.ImageData()
data.read(filename)
part = particles.Particles()
part.read(data, 0)
part.find_particles()
plt.imshow(part.filtered_img)
plt.show()


