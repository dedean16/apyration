#!/usr/bin/env python3
import numpy as np
from functions import *
from config_plot import *
from config_general import *
from math import pi
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from geometry3D import lens_surface, lens_thickness
from functions3D import *


rays = input_beam(z=FIRST_INTERFACE, diameter=5, angle=pi/3, rays=11)


FIRST_LENS_RADIUS = 10
SECOND_LENS_RADIUS = -10
ray_paths = two_interface_system(rays=rays, first_interface=FIRST_INTERFACE,
                                 r1=FIRST_LENS_RADIUS, r2=SECOND_LENS_RADIUS,
                                 n_lens=MATERIAL_REFRACTIVE_INDEX, d_lens=THICKNESS_LENS)

END = 30

plt.figure(1)
for r in ray_paths:
    plt.plot(r[0][-1], r[1][-1], 'o', color=[0, r[3], r[3]])
plt.xlim([-END/2, END/2])
plt.ylim([0, END])

# plt.figure(2)
# ax = plt.axes(projection='3d')
# ax.set_xlabel('x')
# ax.set_ylabel('z')
# ax.set_zlabel('y')
# ax.set_xlim(-END/2, END/2)
# ax.set_ylim(0, END)
# ax.set_zlim(-END/2, END/2)
# for r in ray_paths:
#     ax.plot3D(r[0], r[2], r[1], PLOT_RAY_COLOR, linewidth=PLOT_LINE_WIDTH)
# # Plot Lens
# Rring = 4
# vertex_count = 36
# L1 = lens_surface(FIRST_INTERFACE, FIRST_LENS_RADIUS, Rring, vertex_count)
# ax.plot_surface(L1['x'], L1['z'], L1['y'], color='xkcd:sky blue', alpha=0.5)
# L2 = lens_surface(FIRST_INTERFACE+THICKNESS_LENS, SECOND_LENS_RADIUS, Rring, vertex_count)
# ax.plot_surface(L2['x'], L2['z'], L2['y'], color='xkcd:sky blue', alpha=0.5)
# ax.plot3D([0, 0, 0], [0, END, 0], PLOT_CONSTRUCTION)

plt.show()

print("pause")
