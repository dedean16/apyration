#!/usr/bin/env python3
from functions import *
from config_plot import *
from config_general import *
import matplotlib.pyplot as plt
import numpy


FIRST_LENS_RADIUS = 10
first_lens = lens_curvature(COMPONENT_DIAMETER, FIRST_INTERFACE, FIRST_LENS_RADIUS)
SECOND_LENS_RADIUS = -10
second_lens = lens_curvature(COMPONENT_DIAMETER, SECOND_INTERFACE, SECOND_LENS_RADIUS)


# Focal length
f = focal_length(n=MATERIAL_REFRACTIVE_INDEX, r1=FIRST_LENS_RADIUS, r2=SECOND_LENS_RADIUS, d=THICKNESS_LENS)
h2 = principal_plane_h2(f=f, n=MATERIAL_REFRACTIVE_INDEX, d=THICKNESS_LENS, r1=FIRST_LENS_RADIUS)


print(f, h2)
for ray in numpy.linspace(-3, -1, RAYS):
    result1 = propagate2spherical_old(ray, INITIAL_ANGLE, FIRST_INTERFACE, COMPONENT_DIAMETER, FIRST_LENS_RADIUS)
    theta2 = snells_old(ray_angle=result1["ray_angle"], normal_angle=result1["normal_angle"],
                        index_left=VACUUM_REFRACTIVE_INDEX, index_right=MATERIAL_REFRACTIVE_INDEX)
    result2 = propagate2spherical_old(result1["y"], theta2, SECOND_INTERFACE - result1["x"], COMPONENT_DIAMETER,
                                      SECOND_LENS_RADIUS)
    theta3 = snells_old(ray_angle=result2["ray_angle"], normal_angle=result2["normal_angle"],
                        index_left=MATERIAL_REFRACTIVE_INDEX, index_right=VACUUM_REFRACTIVE_INDEX)
    result3 = propagate2flat_old(result2["y"], theta3, END - result1["x"] - result2["x"], COMPONENT_DIAMETER, suppress=True)

    plt.plot([0, result1["x"], result1["x"] + result2["x"], result1["x"] + result2["x"] + result3["x"]],
             [ray, result1["y"], result2["y"], result3["y"]],
             PLOT_RAY_COLOR, linewidth=PLOT_LINE_WIDTH)


plt.plot([0, END], [0, 0], PLOT_CONSTRUCTION)
plt.plot(first_lens["x"], first_lens["y"], PLOT_CONSTRUCTION)
plt.plot(second_lens["x"], second_lens["y"], PLOT_CONSTRUCTION)
plt.plot([SECOND_INTERFACE + h2 + f, SECOND_INTERFACE + h2 + f],
         [-COMPONENT_DIAMETER / 2, COMPONENT_DIAMETER / 2], PLOT_CONSTRUCTION)
plt.show()


