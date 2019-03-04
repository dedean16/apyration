#!/usr/bin/env python3
"""Ray propagation and refraction functions in 3D."""

import numpy as np
from numpy.linalg import norm
from vectorND import rejection, unit


def snellsvec(k_in, N, n_in=1, n_out=1):
    """
    Compute direction vector of refracted ray.

    Input:
    k_in    Directional unit vector incoming ray
    N       Surface normal unit vector
    n_in    Refractive index incoming ray
    n_out   Refractive index outgoing ray

    Output:
    k_out   Directional unit vector outgoing ray
    """
    k_inrej = rejection(-k_in, N)       # Perpendicular component k_in
    k_outrej = -n_in/n_out * k_inrej    # Perpendicular component k_out
    k_out = k_outrej - N * np.sqrt(1 - norm(k_outrej)**2)

    return k_out


def propagate2surf3D(A, k, zdist, Rsphere, Rring):
    """
    Propagate light ray along z-axis to surface perpendicular to z.

    Input:
    A       Starting position of ray. (x,y,z).
    k       Directional unit vector of ray. (kx, ky, kz). Must have nonzero
            z-component.
    zdist   Distance to surface along z axis. (scalar).
    Rsphere Radius of spherical surface. If Rsphere=0, a flat surface will be
            used. (scalar).
    Rring   Radius indicating the size of the lens. Rays outside this radius
            shall not pass! (scalar).

    Output:
    B       Arrival position of ray at surface. (x,y,z)
    N       Surface normal unit vector. (Nx, Ny, Nz).
    """
    if Rsphere == 0:                # Flat surface
        B = A + k * zdist/k[2]      # Scale k to flat surface
        N = np.array((0, 0, -1))    # Surface normal of flat surface

    else:                           # Spherical surface
        # See: https://en.wikipedia.org/wiki/Line%E2%80%93sphere_intersection
        # Compute intermediate terms
        Csphere = np.array((0, 0, A[2]+zdist+Rsphere))  # Center of sphere
        ACsphere = A - Csphere                          # Center relative to A
        kinACsphere = np.inner(k, ACsphere)             # Inner product k,ACsph

        # Compute solutions to line-sphere intersection
        discriminant = np.sqrt(kinACsphere**2 - norm(ACsphere)**2
                               + Rsphere**2)            # Discriminant of ABCeq
        kdist1 = -kinACsphere + discriminant
        kdist2 = -kinACsphere - discriminant
        ksort = np.sort((kdist1, kdist2))

        if discriminant <= 0:                           # No solutions
            print('Warning: ray out of bounds!')
            return

        # Solutions must be forward
        if ksort[0] > 0:
            kdist = ksort[0]
        elif ksort[1] > 0:
            kdist = ksort[1]
        else:
            print('Warning: no intersection found in forward ray direction!')

        B = A + k * kdist                               # Solution for intersec
        N = unit(B - Csphere) * np.sign(Rsphere)        # Compute normal vector

    return B, N
