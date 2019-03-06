#!/usr/bin/env python3
from config_general import *
from functions import *
from functions3D import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.mlab import griddata

ITERATIONS = 10


r0 = np.linspace(0, 0, ITERATIONS)
r1 = np.linspace(10, 100, ITERATIONS)
r2 = np.linspace(20, 110, ITERATIONS)


def lens_radii(lens_shape):
    if lens_shape == -2:
        lzip = list(zip(-r2, -r1))
    elif lens_shape == -1:
        lzip = list(zip(r0, -r1))
    elif lens_shape == 1:
        lzip = list(zip(r1, r0))
    elif lens_shape == 2:
        lzip = list(zip(r1, r2))
    else:
        lzip = list(zip(r1, -r1))
    return lzip


table = []
for r in lens_radii(-1):
    table.append({"f": focal_length(n=MATERIAL_REFRACTIVE_INDEX, r1=r[0], r2=r[1], d=THICKNESS_LENS),
                  "r1": r[0], "r2": r[1] })
for t in table:
    print(t)


rays = input_beam(z=FIRST_INTERFACE, diameter=BEAM_DIAMETER, angle=ANGLE, rays=RAYS_SCATTER)

ray_paths = two_interface_system(rays=rays, first_interface=FIRST_INTERFACE,
                                 r1=FIRST_LENS_RADIUS, r2=SECOND_LENS_RADIUS,
                                 n_lens=MATERIAL_REFRACTIVE_INDEX, d_lens=THICKNESS_LENS)
plt.figure(f"{FIRST_LENS_RADIUS}-{SECOND_LENS_RADIUS}")
ray_container = {"x": [], "y": [], "z": [], "c": []}
for r in ray_paths:
    ray_container["x"].append(r[0][-1])
    ray_container["y"].append(r[1][-1])
    ray_container["c"].append(r[3])
plt.axes(aspect='equal')
plt.scatter(x=ray_container["x"], y=ray_container["y"], c=ray_container["c"], cmap='tab10', s=0.1)


# Create a contour plot
plt.figure(f"{FIRST_LENS_RADIUS}-{SECOND_LENS_RADIUS}-contour")
X, Y, C = grid(ray_container["x"], ray_container["y"], ray_container["c"])
plt.axes(aspect='equal')
plt.contourf(X, Y, C, levels=10, cmap='tab10')
# plt.colorbar()
plt.title('Comatic circles')
plt.xlabel('X')
plt.ylabel('Y')
plt.show()




print('pause')
