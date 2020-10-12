# coding: utf-8

r"""Air characteristics"""

import numpy as np
from scipy.interpolate import PchipInterpolator

temperatures = np.array([-50, 0, 20, 40, 60, 80, 100])
densities_air = np.array([1.534, 1.293, 1.205, 1.127, 1.067, 1.000, 0.946])
kinematic_viscosities_air = np.array([9.55e-6, 13.30e-6, 15.11e-6, 16.97e-6, 18.90e-6, 20.94e-6, 23.06e-6])

RHO_AIR_20C = 1.205


def density_air(temperature: float) -> float:
    r"""Air density as a function of temperature

    temperature : The temperature in degrees celsius

    Returns the density in kg/m**3

    """
    density_interpolator = PchipInterpolator(temperatures, densities_air, extrapolate=False)
    return density_interpolator(temperature)


def kinematic_viscosity_air(temperature: float) -> float:
    r"""Air kinematic viscosity as a function of temperature

    temperature : The temperature in degrees celsius

    Returns the kinematic viscosity in m**2/s

    """
    kinematic_viscosity_interpolator = PchipInterpolator(temperatures, kinematic_viscosities_air, extrapolate=False)
    return kinematic_viscosity_interpolator(temperature)
