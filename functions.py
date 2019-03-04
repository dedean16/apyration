#!/usr/bin/env python3
from math import tan, sin, asin, cos, sqrt
import warnings
from numpy.polynomial import Polynomial
import numpy as np


def focal_length(n, r1, r2, d):
    return ((n - 1) * (1 / r1 - 1 / r2 + ((n - 1) * d) / (n * r1 * r2))) ** -1


def principal_plane_h1(f, n, d, r2):
    return -f * (n - 1) * d / (r2 * n)


def principal_plane_h2(f, n, d, r1):
    return -f * (n - 1) * d / (r1 * n)


def coddington_shape_factor(r1, r2):
    return (r2 + r1) / (r2 - r1)


def minimum_coma_condition(n, object_distance, img_distance):
    sigma = ((2 * n ** 2 - n - 1) / (n + 1))
    if object_distance is not None:
        sigma = sigma * ((object_distance - img_distance) / (object_distance + img_distance))
    return sigma


# Graphical functions only
def lens_curvature(component_diameter, lens_center, interface_radius, array_length=30):
    y_axis = np.linspace(-component_diameter / 2, component_diameter / 2, array_length)
    x_axis = [lens_center + interface_radius - sqrt(interface_radius**2 - y**2) * interface_radius/abs(interface_radius)
              for y in y_axis]
    return {"x": x_axis, "y": y_axis}


def focal_length_plane(lens_position, h2, f, component_size):
    return {"x": [lens_position + h2 + f, lens_position + h2 + f], "y": [-component_size / 2, component_size / 2]}


def snells_old(ray_angle=0.0, normal_angle=0.0, index_left=1, index_right=1):
    """"
    Returns the angle w.r.t. the optical axis after encountering an interface, given the angle of the ray to the normal
    of the surface, the angle of the surface normal to the optical axis, and the left and right indices of refraction
    """
    return asin(sin(ray_angle)*index_left/index_right) + normal_angle


def propagate2flat_old(initial_y, initial_angle, distance_to_interface, component_diameter, suppress=False):
    """"
    Returns the x,y coordinates, angle to surface normal and the angle of the normal to the optical axis, given the
    initial y coordinate, angle of the ray w.r.t. the normal, distance from the interface, and component diameter.
    """
    end_y = initial_y + tan(initial_angle) * distance_to_interface
    if not suppress:
        if abs(2*end_y) > component_diameter:
            warnings.warn("The ray is out of bounds for your optical component.")
    return {
        "x": distance_to_interface,
        "y": end_y,
        "ray_angle": initial_angle,
        "normal_angle": 0
    }


def propagate2spherical_old(initial_y, initial_angle, distance_to_interface, component_diameter, interface_radius):
    poly_coefficients = Polynomial([
        initial_y**2 + 2*distance_to_interface*interface_radius + distance_to_interface**2,
        2*initial_y*tan(initial_angle) - 2*interface_radius - 2*distance_to_interface,
        1 + tan(initial_angle)**2
    ])
    roots = poly_coefficients.roots()
    if interface_radius > 0:
        end_x = min(roots)
    else:
        end_x = max(roots)
    end_y = initial_y + end_x*tan(initial_angle)
    normal_angle = -asin(end_y/interface_radius)
    ray_angle = -normal_angle + initial_angle

    if abs(2*end_y) > component_diameter:
        warnings.warn("The ray is out of bounds for your optical component.")
    return {
        "x": end_x,
        "y": end_y,
        "ray_angle": ray_angle,
        "normal_angle": normal_angle
    }
