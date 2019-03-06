#!/usr/bin/env python3
"""Ray propagation and refraction functions in 3D."""

import numpy as np
from numpy.linalg import norm
from vectorND import rejection, unit
from functions import *



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


def propagate2surf3D(A, k, z, Rsphere, Rring):
    """
    Propagate light ray along z-axis to surface perpendicular to z.

    Input:
    A       Starting position of ray. (x,y,z).
    k       Directional unit vector of ray. (kx, ky, kz). Must have nonzero
            z-component.
    z       Position of surface on z axis. (scalar).
    Rsphere Radius of spherical surface. If Rsphere=0, a flat surface will be
            used. (scalar).
    Rring   Radius indicating the size of the lens. Rays outside this radius
            shall not pass! (scalar).

    Output:
    B       Arrival position of ray at surface. (x,y,z)
    N       Surface normal unit vector. (Nx, Ny, Nz).
    """
    zdist = z - A[2]                # Compute relative distance to front

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


def input_beam(z, diameter, angle, rays=20):
    center_position = np.array([0, -z*tan(angle), 0])
    diameter = diameter*1.01
    beam_radius = diameter/2
    step_size = diameter/rays
    xy = np.mgrid[-beam_radius+center_position[0]:beam_radius+center_position[0]+step_size:step_size,
                  -beam_radius+center_position[1]:beam_radius+center_position[1]+step_size:step_size]
    return [
        (np.array([xy[0][x][y], xy[1][x][y], center_position[2]]),
         np.array([0, sin(angle), cos(angle)]),
         sqrt((xy[0][x][y]-center_position[0]) ** 2 + (xy[1][x][y]-center_position[1]) ** 2) / beam_radius)
        for x in range(0, rays) for y in range(0, rays)
        if ((xy[0][x][y]-center_position[0]) ** 2 + (xy[1][x][y]-center_position[1]) ** 2) < beam_radius ** 2
    ]


def two_interface_system(rays, r1, r2, n_lens, d_lens, first_interface):
    f = focal_length(n=n_lens, r1=r1, r2=r2, d=d_lens)
    h2 = principal_plane_h2(f=f, n=n_lens, d=d_lens, r1=r1)
    ray_paths = []
    for ray in rays:
        interface1 = propagate2surf3D(A=ray[0], k=ray[1], z=first_interface, Rsphere=r1, Rring=None)
        k2 = snellsvec(k_in=ray[1], N=interface1[1], n_in=1, n_out=n_lens)
        interface2 = propagate2surf3D(A=interface1[0], k=k2, z=first_interface+d_lens, Rsphere=r2, Rring=None)
        k3 = snellsvec(k_in=k2, N=interface2[1], n_in=n_lens, n_out=1)
        interface3 = propagate2surf3D(A=interface2[0], k=k3, z=first_interface+d_lens+h2 + f, Rsphere=0, Rring=None)
        r = [
            [ray[0][0], interface1[0][0], interface2[0][0], interface3[0][0]],
            [ray[0][1], interface1[0][1], interface2[0][1], interface3[0][1]],
            [ray[0][2], interface1[0][2], interface2[0][2], interface3[0][2]],
            ray[2]
        ]
        ray_paths.append(r)
    return ray_paths


def find_ray_crossing(A1, k1, A2, k2):
    """Find position where two rays are closest together."""
    # Find parameter s with closest distance in xy-plane.
    # From Wolfram Mathematica, I derived this:  d/ds sqrt(Dx^2 + Dy^2) == 0 -> s=...
    s = (-(A1[0]*k1[0]) + A2[0]*k1[0] - A1[0]*k2[0] + A2[0]*k2[0] - A1[1]*k1[1]
         + A2[1]*k1[1] - A1[1]*k2[1] + A2[1]*k2[1]) / (k1[0]**2 + 2*k1[0]*k2[0]
                                                       + k2[0]**2 + k1[1]**2 +
                                                       2*k1[1]*k2[1] + k2[1]**2
                                                      + 1e-20)
    B = (A1 + k1*s + A2 + k2*s) / 2             # Compute midpoint of ray crossing
    return B
