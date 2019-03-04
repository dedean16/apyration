#!/usr/bin/env python3
from functions import *
from config_plot import *
from config_general import *
from math import pi
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from functions3D import *


rays = input_beam(center_position=np.array([0, -3, 0]), diameter=5, angle=pi/24, rays=21)


FIRST_LENS_RADIUS = 10
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

plt.show()


print("pause")
