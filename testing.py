#!/usr/bin/env python3
from functions import *
import numpy as np
from math import pi
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


rays = input_beam(center_position=np.array([0, 0, 0]), diameter=8, angle=pi/4, rays=11)

xrays = [[r[0][0], r[1][0]] for r in rays]
yrays = [[r[0][1], r[1][1]] for r in rays]
zrays = [[r[0][2], r[1][2]] for r in rays]

fig = plt.figure()
ax = plt.axes(projection='3d')

for ray in rays:
    ax.plot3D([ray[0][0], ray[1][0]+ray[0][0]], [ray[0][1], ray[1][1]+ray[0][1]], [ray[0][2], ray[1][2]+ray[0][2]])
plt.show()


print("pause")
