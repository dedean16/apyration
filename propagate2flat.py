def propagate2flat(r_0, theta_0, d, D):
    """Description pending ;)."""
    import numpy as np

    r_1 = r_0 + np.tan(theta_0)*d
    z_1 = d
    theta_n = theta_0
    theta_z = 0

    if D < 2*r_1:
        print('The ray is out of bounds for your optical component')

    return z_1, r_1, theta_n, theta_z
