#!/usr/bin/env python3
"""Compute and plot coma dependence on focal length."""
import numpy as np
from config_plot import *
from config_general import *
from functions import compute_coma, focal_length, coddington_shape_factor
import matplotlib.pyplot as plt
from functions3D import input_beam, two_interface_system
from matplotlib.pyplot import cm

# Variable arrays
codd_opt = 0.8
Nvars = 20
theta = np.pi/12
Rlens1 = [np.linspace(5, 30, Nvars), np.linspace(10, 60, Nvars), np.zeros(Nvars),
          np.linspace(5, 33, Nvars)]
Rlens2 = [np.zeros(Nvars), -np.linspace(10, 60, Nvars), -np.linspace(5, 30, Nvars)]

Rlens2.append( Rlens1[-1] * (codd_opt+1)/(codd_opt-1) )

# Initialization
fs = []                         # Focal lengths
coddington = []                 # Coddington shape factors
rbeams = []
yzones = []
comayr3s = []

# Computation loop
for i in range(len(Rlens1)):
    fs.append([])
    coddington.append([])
    rbeams.append([])
    yzones.append([])
    comayr3s.append([])

    for iR in range(Nvars):
        rays = input_beam(z=FIRST_INTERFACE, diameter=4, angle=theta, rays=60)

        # Compute ray paths
        ray_paths = two_interface_system(rays=rays, first_interface=FIRST_INTERFACE,
                                         r1=Rlens1[i][iR], r2=Rlens2[i][iR],
                                         n_lens=MATERIAL_REFRACTIVE_INDEX,
                                         d_lens=THICKNESS_LENS, offset=0)

        # Save relevant variables
        ray_container = {"x": [], "y": [], "z": [], "c": []}
        for r in ray_paths:
            ray_container["x"].append(r[0][-1])
            ray_container["y"].append(r[1][-1])
            ray_container["c"].append(r[3])
        
        # Quantify coma
        rbeam, xzone, yzone, rzone = compute_coma(ray_container, Nzones=30)
        rbeams[i].append(rbeam)
        yzones[i].append(yzone)

        comayr3 = (yzone[-1] - yzone[0]) / (rbeam[-1]**3 - rbeam[0]**3)
        comayr3s[i].append(comayr3)

        # Compute focal length and Coddington shape factor
        fs[i].append(focal_length(MATERIAL_REFRACTIVE_INDEX, Rlens1[i][iR], Rlens2[i][iR],
                               THICKNESS_LENS))
        coddington[i].append(coddington_shape_factor(Rlens1[i][iR], Rlens2[i][iR]))

        print('Radii:', Rlens1[i][iR], Rlens2[i][iR], 'Coddington:', coddington[i][-1])

    # Let's get plotting!
    plt.plot(fs[i], comayr3s[i], '.-', label=f"CSF={coddington[i][0]}")

plt.title(rf'Coma Strength | $\theta={theta:.2f}$ | n={MATERIAL_REFRACTIVE_INDEX}')
plt.xlabel('focal length')
plt.ylabel('coma strength')
plt.legend()
plt.show()
