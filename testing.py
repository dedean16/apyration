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
from matplotlib.pyplot import cm
from matplotlib.mlab import griddata


def grid(x, y, z, resX=100, resY=100):
    "Convert 3 column data to matplotlib grid"
    xi = np.linspace(min(x), max(x), resX)
    yi = np.linspace(min(y), max(y), resY)
    Z = griddata(x, y, z, xi, yi, interp='linear')
    X, Y = np.meshgrid(xi, yi)
    return X, Y, Z


PLOT_RAY_TRACE = False

rays = input_beam(z=FIRST_INTERFACE, diameter=5, angle=pi/6, rays=101)

FIRST_LENS_RADIUS = 10
SECOND_LENS_RADIUS = -10
ray_paths = two_interface_system(rays=rays, first_interface=FIRST_INTERFACE,
                                 r1=FIRST_LENS_RADIUS, r2=SECOND_LENS_RADIUS,
                                 n_lens=MATERIAL_REFRACTIVE_INDEX, d_lens=THICKNESS_LENS)
END = 30

if True:
    # plt.figure(1)
    ray_container = {"x": [], "y": [], "z": [], "c": []}
    for r in ray_paths:
        ray_container["x"].append(r[0][-1])
        ray_container["y"].append(r[1][-1])
        ray_container["z"].append(r[2][-1])
        ray_container["c"].append(r[3])
        # noinspection PyUnresolvedReferences
        # plt.plot(r[0][-1], r[1][-1], 'o', color=cm.tab10(r[3]), markersize=4)
    # plt.scatter(x=ray_container["x"], y=ray_container["y"], c=ray_container["c"], cmap='tab10')
    

    # Create a contour plot
    plt.figure(3)
    X, Y, C = grid(ray_container["x"], ray_container["y"], ray_container["c"])
    plt.axes(aspect='equal')
    plt.contourf(X, Y, C)
    plt.colorbar()
    plt.title('Comatic circles')
    plt.xlabel('X')
    plt.ylabel('Y')

print('pause')

if PLOT_RAY_TRACE:
    plt.figure(2)
    ax = plt.axes(projection='3d')
    ax.set_xlabel('x')
    ax.set_ylabel('z')
    ax.set_zlabel('y')
    ax.set_xlim(-END/2, END/2)
    ax.set_ylim(0, END)
    ax.set_zlim(-END/2, END/2)
    ray_container2 = {"x": [], "y": [], "z": [], "c": []}
    for r in ray_paths:
        ray_container2["x"].append(r[0])
        ray_container2["y"].append(r[1])
        ray_container2["z"].append(r[2])
        ray_container2["c"].append(r[3])
    for r in ray_paths:
        ax.plot3D(r[0], r[2], r[1], PLOT_RAY_COLOR, linewidth=PLOT_LINE_WIDTH)
    # Plot Lens
    Rring = 4
    vertex_count = 36
    L1 = lens_surface(FIRST_INTERFACE, FIRST_LENS_RADIUS, Rring, vertex_count)
    ax.plot_surface(L1['x'], L1['z'], L1['y'], color='xkcd:sky blue', alpha=0.5)
    L2 = lens_surface(FIRST_INTERFACE+THICKNESS_LENS, SECOND_LENS_RADIUS, Rring, vertex_count)
    ax.plot_surface(L2['x'], L2['z'], L2['y'], color='xkcd:sky blue', alpha=0.5)
    ax.plot3D([0, 0, 0], [0, END, 0], PLOT_CONSTRUCTION)


rbeam, xzone, yzone, rzone = compute_coma(ray_container, Nzones=30)
plt.figure(4)
plt.plot(rbeam**3, yzone-yzone[0], '.-')
# plt.plot(rbeam**3, rzone, '.-')


plt.show()

print("pause")
