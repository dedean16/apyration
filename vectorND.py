#!/usr/bin/env python3
import numpy as np
from numpy.linalg import norm as norm


def unit(v):
    """Compute unit vector from vector."""
    normv = norm(v)
    return v / normv


def projection(v, w):
    """Compute vector projection of vector v onto vector w."""
    wunit = unit(w)
    return np.inner(v, wunit) * wunit


def rejection(v, w):
    """Compute vector rejection of vector v onto vector w."""
    return v - projection(v, w)
