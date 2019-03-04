#!/usr/bin/env python3
"""Functions for computing 3D surface vertices."""

import numpy as np


def lens_surface(z, Rsphere, Rring, vertex_count=32):
    """
    Compute x,y,z coordinates of flat or spherical surface.

    Input:
    z               Position of lens front on z-axis.
    Rsphere         Radius of spherical surface. (scalar). If 0, the a flat
                    circular.
                    surface will be used.
    Rring           Radius of lens component ring. (scalar).
    vertex_count    Numer of vertices in radial and tangential direction. For
                    circle only tangential. (integer).

    Output:
    x, y, z         Vertex coordinates. (2D numpy arrays).
    """
    if Rsphere == 0:                # Create flat circular surface
        r = np.array((0, Rring))
        t = np.linspace(0, 2*np.pi, vertex_count)
        x = np.outer(r, np.cos(t))
        y = np.outer(r, np.sin(t))
        z = z * np.ones(np.size(x))
    else:                           # Create spherical surface
        ringangle = np.arcsin(Rring / Rsphere)
        u = np.linspace(0, 2 * np.pi, vertex_count)
        v = np.linspace(0, ringangle, vertex_count)
        x = Rsphere * np.outer(np.cos(u), np.sin(v))
        y = Rsphere * np.outer(np.sin(u), np.sin(v))
        z = Rsphere * np.outer(np.ones(np.size(u)), np.cos(v)) + z + Rsphere

    return {"x": x, "y": y, "z": z}
