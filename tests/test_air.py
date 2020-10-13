#!/usr/bin/env python
# coding: utf-8

r"""tests for the air.py module."""

import math

from ydeos_aerodynamics.air import density_air, densities_air, \
    kinematic_viscosity_air, kinematic_viscosities_air, temperatures


def test_temperature_bounds():
    r"""Temperature bounds.

    Check that the values at each end of the temperature range
    are equal to the specified values

    """
    assert density_air(temperature=max(temperatures)) == min(densities_air)
    assert density_air(temperature=min(temperatures)) == max(densities_air)

    assert (kinematic_viscosity_air(temperature=max(temperatures)) ==
            max(kinematic_viscosities_air))
    assert (kinematic_viscosity_air(temperature=min(temperatures)) ==
            min(kinematic_viscosities_air))


def test_wrong_temperature():
    r"""Wrong temperature.

    Check that the values returned for a temperature that is outside
    of the temperature definition range are NaN

    """
    assert math.isnan(density_air(temperature=max(temperatures) + 1e-6))
    assert math.isnan(density_air(temperature=min(temperatures) - 1e-6))

    assert math.isnan(kinematic_viscosity_air(temperature=max(temperatures) + 1e-6))
    assert math.isnan(kinematic_viscosity_air(temperature=min(temperatures) - 1e-6))
