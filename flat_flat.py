#!/usr/bin/env python3
from functions import *
from config_plot import *
from config_general import *
import matplotlib.pyplot as plt
import numpy


for ray in numpy.linspace(-5, 2, RAYS):
    result1 = propagate2flat(ray, INITIAL_ANGLE, FIRST_INTERFACE, COMPONENT_DIAMETER)
    theta2 = snells(ray_angle=result1["ray_angle"], normal_angle=result1["normal_angle"],
                    index_left=VACUUM_REFRACTIVE_INDEX, index_right=MATERIAL_REFRACTIVE_INDEX)
    result2 = propagate2flat(result1["y"], theta2, SECOND_INTERFACE-result1["x"], COMPONENT_DIAMETER)
    theta3 = snells(ray_angle=result2["ray_angle"], normal_angle=result2["normal_angle"],
                    index_left=MATERIAL_REFRACTIVE_INDEX, index_right=VACUUM_REFRACTIVE_INDEX)
    result3 = propagate2flat(result2["y"], theta3, END-result1["x"]-result2["x"], COMPONENT_DIAMETER, suppress=True)

    plt.plot([0, result1["x"], result1["x"] + result2["x"], result1["x"] + result2["x"] + result3["x"]],
             [ray, result1["y"], result2["y"], result3["y"]],
             PLOT_RAY_COLOR, linewidth=PLOT_LINE_WIDTH)


plt.plot([0, END], [0, 0], PLOT_CONSTRUCTION)
plt.plot([FIRST_INTERFACE, FIRST_INTERFACE], [-COMPONENT_DIAMETER/2, COMPONENT_DIAMETER/2], PLOT_CONSTRUCTION)
plt.plot([SECOND_INTERFACE, SECOND_INTERFACE], [-COMPONENT_DIAMETER/2, COMPONENT_DIAMETER/2], PLOT_CONSTRUCTION)
plt.show()
