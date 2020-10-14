#!/usr/bin/env python
# coding: utf-8

r"""Tests for the profile.py module"""

import pytest

from ydeos_aerodynamics.profiles import power_law, logarithmic


def test_power_law():
    r"""Power-law wind profile test."""
    wind_speed_0m = power_law(wind_speed_known=20., height_reference=10., height=0.)
    assert wind_speed_0m == 0.

    wind_speed_10m = power_law(wind_speed_known=20., height_reference=10., height=10.)
    assert wind_speed_10m == 20.

    wind_speed_20m = power_law(wind_speed_known=20., height_reference=10., height=20.)
    assert wind_speed_20m > wind_speed_10m


def test_power_law_wrong_input():
    r"""Wrong parameters for the power law."""
    with pytest.raises(ValueError):
        power_law(wind_speed_known=-20., height_reference=10., height=0.)
    with pytest.raises(ValueError):
        power_law(wind_speed_known=20., height_reference=-10., height=0.)
    with pytest.raises(ValueError):
        power_law(wind_speed_known=20.,
                  height_reference=10.,
                  height=0.,
                  alpha=0.)


def test_power_law_negative_height():
    r"""Power-law wind profile test."""
    with pytest.raises(ValueError):
        _ = power_law(wind_speed_known=20., height_reference=10., height=-1.)


def test_logarithmic():
    r"""Logarithmic wind profile test."""
    wind_speed_10m = logarithmic(wind_speed_known=20., height_reference=10., height=10.)
    assert wind_speed_10m == 20.

    wind_speed_20m = logarithmic(wind_speed_known=20., height_reference=10., height=20.)
    assert wind_speed_20m > wind_speed_10m


def test_logarithmic_zero_height():
    r"""logarithmic wind profile test at zero height."""
    with pytest.raises(ValueError):
        logarithmic(wind_speed_known=20., height_reference=10., height=0.)


def test_logarithmic_negative_height():
    r"""logarithmic wind profile test at negative height."""
    with pytest.raises(ValueError):
        logarithmic(wind_speed_known=20., height_reference=10., height=-1.)


def test_logarithmic_wrong_input():
    r"""Bad input for the logarithmic profile."""
    with pytest.raises(ValueError):
        logarithmic(wind_speed_known=-20., height_reference=10., height=1.)
    with pytest.raises(ValueError):
        logarithmic(wind_speed_known=20., height_reference=-10., height=1.)
    with pytest.raises(ValueError):
        logarithmic(wind_speed_known=20.,
                    height_reference=10.,
                    height=1.,
                    roughness_length=0.)
