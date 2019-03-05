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


rays = input_beam(center_position=np.array([0, -3, 0]), diameter=5, angle=pi/24, rays=7)


FIRST_LENS_RADIUS = 5
SECOND_LENS_RADIUS = -10
ray_paths = two_interface_system(rays=rays, first_interface=FIRST_INTERFACE,
                                 r1=FIRST_LENS_RADIUS, r2=SECOND_LENS_RADIUS,
                                 n_lens=MATERIAL_REFRACTIVE_INDEX, d_lens=THICKNESS_LENS)

# ax = plt.axes(projection='3d')
# # ax.set_xlim(-15, 15)
# # ax.set_ylim(0, 30)
# # ax.set_zlim(-15, 15)
# ax.set_xlabel('x')
# ax.set_ylabel('z')
# ax.set_zlabel('y')
# for r in ray_paths:
#     ax.plot3D(r[0], r[2], r[1], PLOT_RAY_COLOR, linewidth=PLOT_LINE_WIDTH)
# plt.show()


plt.figure(1)
for r in ray_paths:
    plt.plot(r[0][-1], r[1][-1], 'o', color=[0, r[3], r[3]])
plt.figure(2)
ax = plt.axes(projection='3d')
ax.set_xlabel('x')
ax.set_ylabel('z')
ax.set_zlabel('y')
for r in ray_paths:
    ax.plot3D(r[0], r[2], r[1], PLOT_RAY_COLOR, linewidth=PLOT_LINE_WIDTH)

# Plot Lens
Rring = 3
vertex_count = 36

L1 = lens_surface(FIRST_INTERFACE, FIRST_LENS_RADIUS, Rring, vertex_count)
ax.plot_surface(L1['x'], L1['z'], L1['y'], color='xkcd:sky blue', alpha=0.5)

# # Surfaces must be slightly separated to prevent rendering glitches
# z2 = FIRST_INTERFACE + lens_thickness(Rsphere, Rring) + 1e-6
# L2 = lens_surface(z2, 0, Rring, vertex_count)
# ax.plot_surface(L2['x'], L2['z'], L2['y'], color='xkcd:sky blue', alpha=0.5)

zdlim = np.diff(ax.get_zlim())
ax.set_xlim((-zdlim/2, zdlim/2))

plt.show()


print("pause")
