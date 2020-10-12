#!/usr/bin/env python
# coding: utf-8

r"""example use of profile.py"""

import matplotlib.pyplot as plt
import numpy as np

from ydeos_aerodynamics.profiles import power_law, logarithmic

max_height = 30.
ref_height = 30.

heights = np.arange(0.01, max_height, 0.01)

wind_speeds_power_law_0_11 = [power_law(wind_speed_known=10.,
                                        height_reference=ref_height,
                                        height=h,
                                        alpha=0.11)
                              for h in heights]
wind_speeds_power_law_0_06 = [power_law(wind_speed_known=10.,
                                        height_reference=ref_height,
                                        height=h,
                                        alpha=0.06)
                              for h in heights]

wind_speeds_loga_0_0002 = [logarithmic(wind_speed_known=10.,
                                       height_reference=ref_height,
                                       height=h,
                                       roughness_length=0.0002)
                           for h in heights]
wind_speeds_loga_0_055 = [logarithmic(wind_speed_known=10.,
                                      height_reference=ref_height,
                                      height=h,
                                      roughness_length=0.055)
                          for h in heights]

w, h = plt.figaspect(3.)
f = plt.figure(figsize=(w, h), facecolor="white")
# ax = f.add_subplot(111, axisbg='white')
ax = f.add_subplot(111, facecolor='white')
# plt.axis("equal")
plt.xlabel("Wind speed")
plt.ylabel("Height")
ax.set_ylim([0., max_height])
ax.grid(True)


ax.plot(wind_speeds_power_law_0_11, heights, color="b", label="power law, alpha=0.11")
ax.plot(wind_speeds_power_law_0_06, heights, color="r", label="power law, alpha=0.06")
ax.plot(wind_speeds_loga_0_0002, heights, color="black", label="logarithmic, roughness=0.0002 m")
ax.plot(wind_speeds_loga_0_055, heights, color="black", linestyle="--", label="logarithmic, roughness=0.055 m")
plt.legend(loc="upper right", fontsize=10)
plt.show()
