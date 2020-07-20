# -*- coding: utf-8 -*-
"""Testing re-orientation in shearflow."""
import os

import numpy as np

import matplotlib.pyplot as plt
from fiberpy.constants import COMPS
from fiberpy.orientation import get_zhang_aspect_ratio, rsc_ode
from matplotlib import cm
from scipy.integrate import odeint

dark2 = cm.get_cmap("Dark2", 7)

ar = get_zhang_aspect_ratio(4.431135)
xi = (ar ** 2 - 1) / (ar ** 2 + 1)
G = 1.0


def L(t):
    """Velocity gradient."""
    return np.array([[0.0, 0.0, 0.0], [G, 0.0, 0.0], [0.0, 0.0, 0.0]])


# load simulation data
data_list = []
rootdir = "data/volfrac1"
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        if file == "A.csv":
            name = os.path.join(subdir, file)
            data_list.append(np.loadtxt(name, delimiter=","))
data = np.array(data_list)

# Compute mean values of simulation result at given times t.
t = np.nanmean(data[:, :, 0], axis=0)
mean = np.nanmean(data[:, :, 1:10], axis=0)
std = np.std(data[:, :, 1:10], axis=0)

A0 = data[0, 0, 1:10]
t = data[0, :, 0]

A_ref = odeint(rsc_ode, A0.ravel(), t, args=(xi, L, 0.001, 1.0))

subplots = ["A11", "A22", "A33", "A12"]

legend_list = ["SPH simulation %d" % i for i in range(len(data_list))]
legend_list.append("Mean")
legend_list.append("RSC")

plt.figure(figsize=(12, 3))
for j, c in enumerate(subplots):
    i = COMPS[c]
    plt.subplot("14" + str(j + 1))
    for d in range(len(data_list)):
        plt.plot(G * t, data[d, :, i + 1], color=dark2(d), alpha=0.3)
    plt.plot(G * t, mean[:, i], color=dark2(d+1))
    plt.plot(G * t, A_ref[:, i], color=dark2(d+2))
    plt.xlabel("Strains")
    plt.title(c)
    plt.ylim([-(i % 2), 1])

    if j == 2:
        plt.legend(legend_list)

plt.tight_layout()
plt.show()