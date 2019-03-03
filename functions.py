from math import tan, sin, asin, sqrt
import warnings
from numpy.polynomial import Polynomial
import numpy


def snells(ray_angle=0.0, normal_angle=0.0, index_left=1, index_right=1):
    """"
    Returns the angle w.r.t. the optical axis after encountering an interface, given the angle of the ray to the normal
    of the surface, the angle of the surface normal to the optical axis, and the left and right indices of refraction
    """
    return asin(sin(ray_angle)*index_left/index_right) + normal_angle


def propagate2flat(initial_y, initial_angle, distance_to_interface, component_diameter, suppress=False):
    """"
    Returns the x,y coordinates, angle to surface normal and the angle of the normal to the optical axis, given the
    initial y coordinate, angle of the ray w.r.t. the normal, distance from the interface, and component diameter.
    """
    end_y = initial_y + tan(initial_angle) * distance_to_interface
    if not suppress:
        if 2*end_y > component_diameter:
            warnings.warn("The ray is out of bounds for your optical component.")
    return {
        "x": distance_to_interface,
        "y": end_y,
        "ray_angle": initial_angle,
        "normal_angle": 0
    }


def propagate2spherical(initial_y, initial_angle, distance_to_interface, component_diameter, interface_radius):
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

    if 2*end_y > component_diameter:
        warnings.warn("The ray is out of bounds for your optical component.")
    return {
        "x": end_x,
        "y": end_y,
        "ray_angle": ray_angle,
        "normal_angle": normal_angle
    }


def lens_curvature(component_diameter, lens_center, interface_radius, array_length=30):
    y_axis = numpy.linspace(-component_diameter / 2, component_diameter / 2, array_length)
    x_axis = [lens_center + interface_radius - sqrt(interface_radius**2 - y**2) * interface_radius/abs(interface_radius)
              for y in y_axis]
    return {"x": x_axis, "y": y_axis}
