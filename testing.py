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
f = (MATERIAL_REFRACTIVE_INDEX-1) * (1 / FIRST_LENS_RADIUS - 1 / SECOND_LENS_RADIUS +
                                     ((MATERIAL_REFRACTIVE_INDEX-1) * THICKNESS_LENS)
                                     / (MATERIAL_REFRACTIVE_INDEX*FIRST_LENS_RADIUS*SECOND_LENS_RADIUS))
f = f**-1
# Principal plane
h2 = -f * (MATERIAL_REFRACTIVE_INDEX-1) * THICKNESS_LENS / (FIRST_LENS_RADIUS*MATERIAL_REFRACTIVE_INDEX)


print(f, h2)
for ray in numpy.linspace(-2.5, -1, RAYS):
    result1 = propagate2spherical(ray, INITIAL_ANGLE, FIRST_INTERFACE, COMPONENT_DIAMETER, FIRST_LENS_RADIUS)
    theta2 = snells(ray_angle=result1["ray_angle"], normal_angle=result1["normal_angle"],
                    index_left=VACUUM_REFRACTIVE_INDEX, index_right=MATERIAL_REFRACTIVE_INDEX)
    result2 = propagate2spherical(result1["y"], theta2, SECOND_INTERFACE-result1["x"], COMPONENT_DIAMETER,
                                  SECOND_LENS_RADIUS)
    theta3 = snells(ray_angle=result2["ray_angle"], normal_angle=result2["normal_angle"],
                    index_left=MATERIAL_REFRACTIVE_INDEX, index_right=VACUUM_REFRACTIVE_INDEX)
    result3 = propagate2flat(result2["y"], theta3, END-result1["x"]-result2["x"], COMPONENT_DIAMETER, suppress=True)

    plt.plot([0, result1["x"], result1["x"] + result2["x"], result1["x"] + result2["x"] + result3["x"]],
             [ray, result1["y"], result2["y"], result3["y"]],
             PLOT_RAY_COLOR, linewidth=PLOT_LINE_WIDTH)


plt.plot([0, END], [0, 0], PLOT_CONSTRUCTION)
plt.plot(first_lens["x"], first_lens["y"], PLOT_CONSTRUCTION)
plt.plot(second_lens["x"], second_lens["y"], PLOT_CONSTRUCTION)
plt.plot([SECOND_INTERFACE + h2 + f, SECOND_INTERFACE + h2 + f],
         [-COMPONENT_DIAMETER / 2, COMPONENT_DIAMETER / 2], PLOT_CONSTRUCTION)
plt.show()


