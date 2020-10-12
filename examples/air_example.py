#!/usr/bin/env python
# coding: utf-8

r"""example use of air"""

from ydeos_aerodynamics.air import density_air, kinematic_viscosity_air

# difference between air density at 0° and 35° in percent
# The density increases by 13% from 35°C to 0°C.
# The forces on the sails therefore also increase by 13%.
print(100 * (density_air(temperature=0) - density_air(temperature=35)) / density_air(temperature=35))

# kinematic viscosity
# The kinematic viscosity decreases by 20% from 35°C to 0°C
# (For the same dimension and speed,
# the Reynolds number is higher at 0°C than at 35°C)
print(100 * (kinematic_viscosity_air(temperature=0) - kinematic_viscosity_air(temperature=35)) / kinematic_viscosity_air(temperature=35))
