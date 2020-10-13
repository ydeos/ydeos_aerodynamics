#!/usr/bin/env python
# coding: utf-8

r"""Tests for the true.py module"""

import math

import pytest

from ydeos_aerodynamics.true import true_wind_angle, true_wind_speed, true_wind


# true_wind_angle() tests


def test_twa_negative_aws():
    r"""Negative apparent wind speed, should raise a ValueError"""
    with pytest.raises(ValueError):
        true_wind_angle(apparent_wind_speed=-1.,
                        apparent_wind_angle=45.,
                        boatspeed=0.)


def test_twa_awa_lt_minus180():
    r"""Apparent wind angle lower than -180, should raise a ValueError"""
    with pytest.raises(ValueError):
        true_wind_angle(apparent_wind_speed=1.,
                        apparent_wind_angle=-181.,
                        boatspeed=0.)


def test_twa_awa_gt_180():
    r"""Apparent wind angle higher than 180, should raise a ValueError"""
    with pytest.raises(ValueError):
        true_wind_angle(apparent_wind_speed=1.,
                        apparent_wind_angle=181.,
                        boatspeed=0.)


def test_twa_zero_boatspeed_awa():
    r"""At zero speed, the true wind angle
    and the apparent wind angle should be equal"""
    twa_zero_boatspeed_1 = true_wind_angle(apparent_wind_speed=10.,
                                           apparent_wind_angle=45.,
                                           boatspeed=0.)
    assert twa_zero_boatspeed_1 == 45.

    twa_zero_boatspeed_2 = true_wind_angle(apparent_wind_speed=10.,
                                           apparent_wind_angle=-165.,
                                           boatspeed=0.)
    expected_value, atol = -165., 1e-6
    assert expected_value - atol <= twa_zero_boatspeed_2 <= expected_value + atol

    twa_zero_boatspeed_3 = true_wind_angle(apparent_wind_speed=10.,
                                           apparent_wind_angle=90.,
                                           boatspeed=0.)
    assert twa_zero_boatspeed_3 == 90.


def test_twa_known_values():
    r"""Known values."""
    twa_reaching_same_speed_as_tws = \
        true_wind_angle(apparent_wind_speed=10. * math.sqrt(2.),
                        apparent_wind_angle=45.,
                        boatspeed=10.)
    expected_value, atol = 90., 1e-6
    assert expected_value - atol <= twa_reaching_same_speed_as_tws <= expected_value + atol


def test_twa_known_values_going_backwards():
    r"""Known values going backwards."""
    twa_backwards_reaching_same_speed_as_tws = \
        true_wind_angle(apparent_wind_speed=10. * math.sqrt(2.),
                        apparent_wind_angle=135.,
                        boatspeed=-10.)
    expected_value, atol = 90., 1e-6
    assert expected_value - atol <= twa_backwards_reaching_same_speed_as_tws <= expected_value + atol

    # Head to wind, going backwards at the same speed as true_wind_speed
    twa_head_to_wind_no_true = true_wind_angle(apparent_wind_speed=0.,
                                               apparent_wind_angle=0.,
                                               boatspeed=-10.)
    expected_value, atol = 0., 1e-6
    assert expected_value - atol <= twa_head_to_wind_no_true <= expected_value + atol


def test_twa_opposite_heel_angles():
    r"""Opposite heel angles should result in the same true wind angle"""
    twa_heeled_40_degrees = true_wind_angle(apparent_wind_speed=10.,
                                            apparent_wind_angle=120.,
                                            boatspeed=3.,
                                            heel_angle=40.)
    twa_counterheeled_40_degrees = true_wind_angle(apparent_wind_speed=10.,
                                                   apparent_wind_angle=120.,
                                                   boatspeed=3.,
                                                   heel_angle=-40.)
    assert twa_heeled_40_degrees == twa_counterheeled_40_degrees


def test_twa_90_degrees_heel():
    r""" Boat at 90° heel."""
    with pytest.raises(ValueError):
        true_wind_angle(apparent_wind_speed=10.,
                        apparent_wind_angle=75.,
                        boatspeed=3.,
                        heel_angle=90.)


# true_wind_speed() tests


def test_tws_negative_tws():
    r"""Negative apparent wind speed, should raise a ValueError."""
    with pytest.raises(ValueError):
        true_wind_speed(apparent_wind_speed=-1.,
                        apparent_wind_angle=45.,
                        boatspeed=0.)


def test_tws_twa_lt_minus180():
    r"""Apparent wind angle lower than -180, should raise a ValueError."""
    with pytest.raises(ValueError):
        true_wind_speed(apparent_wind_speed=1.,
                        apparent_wind_angle=-181.,
                        boatspeed=0.)


def test_tws_twa_gt_180():
    r"""Apparent wind angle higher than 180, should raise a ValueError."""
    with pytest.raises(ValueError):
        true_wind_speed(apparent_wind_speed=1.,
                        apparent_wind_angle=181.,
                        boatspeed=0.)


def test_tws_known_values():
    r"""Known or easily determined values."""
    tws_head_to_wind = true_wind_speed(apparent_wind_speed=10.,
                                       apparent_wind_angle=0.,
                                       boatspeed=10.)
    expected_value, atol = 0., 1e-6
    assert expected_value - atol <= tws_head_to_wind <= expected_value + atol

    # fully downwind
    tws_downwind = true_wind_speed(apparent_wind_speed=10.,
                                   apparent_wind_angle=180.,
                                   boatspeed=3.)
    assert tws_downwind == 13.

    # 90° reach at the same speed as true_wind_speed
    tws_reaching_same_boatspeed_as_tws = \
        true_wind_speed(apparent_wind_speed=10. * math.sqrt(2.),
                        apparent_wind_angle=45.,
                        boatspeed=10.)
    expected_value, atol = 10., 1e-6
    assert expected_value - atol <= tws_reaching_same_boatspeed_as_tws <= expected_value + atol


def test_tws_known_values_going_backwards():
    r"""Known values going backwards."""
    tws_going_backwards_head_to_wind = true_wind_speed(apparent_wind_speed=10.,
                                                       apparent_wind_angle=0.,
                                                       boatspeed=-10.)
    assert tws_going_backwards_head_to_wind == 20.


def test_tws_opposite_awa():
    r"""Opposite apparent wind angles."""
    tws_beating_on_starboard = true_wind_speed(apparent_wind_speed=10.,
                                               apparent_wind_angle=45.,
                                               boatspeed=3.)
    tws_beating_on_port = true_wind_speed(apparent_wind_speed=10.,
                                          apparent_wind_angle=-45.,
                                          boatspeed=3.)
    assert tws_beating_on_starboard == tws_beating_on_port


def test_symmetry():
    r"""Test symmetry by using opposite apparent wind angles."""
    true_wind_starboard = true_wind(apparent_wind_speed=10.,
                                    apparent_wind_angle=45.,
                                    boatspeed=3.)
    true_wind_port = true_wind(apparent_wind_speed=10.,
                               apparent_wind_angle=-45.,
                               boatspeed=3.)
    assert true_wind_port["speed"] == true_wind_starboard["speed"]
    assert true_wind_port["angle"] == -true_wind_starboard["angle"]
