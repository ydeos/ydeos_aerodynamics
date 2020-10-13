#!/usr/bin/env python
# coding: utf-8

r"""Example use of true.py.

Given apparent wind angle and speed, find the true wind angle and speed.
Plot it.

"""

from ydeos_aerodynamics.true import true_wind

from wind_triangle import display_wind_triangle

apparent_wind_speed = 20.
apparent_wind_angle = 110.  # positive on starboard tack
boatspeed = 10.


true_wind_speed_dict = true_wind(apparent_wind_speed,
                                 apparent_wind_angle,
                                 boatspeed)
true_wind_speed, true_wind_angle = \
    true_wind_speed_dict["speed"], true_wind_speed_dict["angle"]

display_wind_triangle(true_wind_speed,
                      true_wind_angle,
                      apparent_wind_speed,
                      apparent_wind_angle,
                      boatspeed)
