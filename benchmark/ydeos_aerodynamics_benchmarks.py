#!/usr/bin/env python3
# coding: utf-8

r"""Benchmarking of the aerodynamics functions."""

from ydeos_benchmark.benchmark import run_benchmark_simple

from ydeos_aerodynamics.air import density_air, kinematic_viscosity_air
from ydeos_aerodynamics.apparent import apparent_wind_angle, \
    apparent_wind_speed, apparent_wind
from ydeos_aerodynamics.true import true_wind_angle, true_wind_speed, true_wind
from ydeos_aerodynamics.profiles import power_law, logarithmic
from ydeos_aerodynamics.distribution import weibull_pdf, weibull_cdf, \
    weibull_mean, weibull_random_samples
from ydeos_aerodynamics.windage import windage_hull, windage_mast_with_sail
from ydeos_aerodynamics.model import ImsAeroModelCoefficients, aero_force

# List of functions to benchmark
to_profile = (
    (density_air, [21], {}),
    (kinematic_viscosity_air, [22], {}),
    #
    (apparent_wind_angle, [10., 45., 2.], {}),
    (apparent_wind_speed, [10., 45., 2.], {}),
    (apparent_wind, [10., 45., 2.], {}),
    (true_wind_angle, [10., 45., 2.], {}),
    (true_wind_speed, [10., 45., 2.], {}),
    (true_wind, [10., 45., 2.], {}),
    #
    (power_law, [10., 10., 20.], {}),
    (logarithmic, [10., 10., 20.], {}),
    #
    (weibull_pdf, [1.], {}),
    (weibull_cdf, [1.], {}),
    (weibull_mean, [], {}),
    (weibull_random_samples, [], {}),
    #
    (windage_hull, [10., 45., 2., 0., 0.1, 1., 0.2], {}),
    (windage_mast_with_sail, [10., 45., 2., 0., 1., 0.5, 0.1, 1.2, 0.05, 0.05],{}),
    #
    # centre of effort not benchmarked -> only basic operations
    #
    (ImsAeroModelCoefficients.coefficient_interp, ["main"], {}),
    (ImsAeroModelCoefficients.coefficient, ["main", 45.], {}),
    #
    (aero_force, [10., 45., 2., 0., 0.,
                  "main", 0.3, (1., 2., 3.),
                  "jib", 0.2, (1., 2., 3.),
                  1.6], {}),)


if __name__ == "__main__":
    NB_TIMES = 1000
    run_benchmark_simple(to_profile, n_times=NB_TIMES)
    # run_benchmark_complete(to_profile, n_times=NB_TIMES, save_results=True)
