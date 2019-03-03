#!/usr/bin/env python3


def propagate2sph(r_0, theta_0, d, D, R):
    """
    Propagate light to a spherical surface.

    Input:
    ...
    """
    import numpy as np

    a = 1 + np.tan(theta_0)**2
    b = 2*r_0*np.tan(theta_0)-2*R-2*d
    c = r_0**2+2*d*R+d**2

    if R > 0:
        z_1 = np.min(np.roots([a, b, c]))  # what?
    else:
        z_1 = np.max(np.roots([a, b, c]))

    r_1 = r_0 + z_1 * np.tan(theta_0)
    theta_z = -np.asin(r_1/R)
    theta_n = -theta_z + theta_0

    if D < 2*r_1:
        print('The ray is out of bounds for your optical component')

    return z_1, r_1, theta_n, theta_z
