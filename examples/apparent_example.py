#!/usr/bin/env python
# coding: utf-8

r"""Example use of apparent.py.

Given true wind angle and speed, find the apparent wind angle and speed.
Plot it.

"""

from wind_triangle import display_wind_triangle

from ydeos_aerodynamics.apparent import apparent_wind

true_wind_speed = 10
true_wind_angle = -60  # positive on starboard tack
boatspeed = 5

apparent_wind_speed_dict = apparent_wind(true_wind_speed,
                                         true_wind_angle,
                                         boatspeed,
                                         heel_angle=0.,
                                         check_heel_angle=True)
apparent_wind_speed, apparent_wind_angle = \
    apparent_wind_speed_dict["speed"], apparent_wind_speed_dict["angle"]

display_wind_triangle(true_wind_speed,
                      true_wind_angle,
                      apparent_wind_speed,
                      apparent_wind_angle,
                      boatspeed)
