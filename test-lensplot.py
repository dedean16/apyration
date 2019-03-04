import numpy as np
from functions3D import *
from vectorND import *
from functions3D import *
from geometry3D import lens_surface, lens_thickness
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig2 = plt.figure()
ax = fig2.add_subplot(111, projection='3d')

z0 = 2
Rsphere = 8
Rring = 2
vertex_count = 36

L1 = lens_surface(z0, Rsphere, Rring, vertex_count)
ax.plot_surface(L1['x'], L1['z'], L1['y'], color='xkcd:sky blue', alpha=0.5)

# Surfaces must be slightly separated to prevent rendering glitches
z2 = z0 + lens_thickness(Rsphere, Rring) + 1e-6
L2 = lens_surface(z2, 0, Rring, vertex_count)
ax.plot_surface(L2['x'], L2['z'], L2['y'], color='xkcd:sky blue', alpha=0.5)

ax.set_ylim([1, 3])
plt.show()
