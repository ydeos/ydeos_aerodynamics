#!/usr/bin/env python
# coding: utf-8

r"""Tests for the apparent.py module"""

import math

import pytest

from ydeos_aerodynamics.apparent import apparent_wind_angle, apparent_wind_speed


# apparent_wind_angle() tests


def test_awa_negative_tws():
    r"""Negative true wind speed, should raise a ValueError"""
    with pytest.raises(ValueError):
        apparent_wind_angle(true_wind_speed=-1., true_wind_angle=45., boatspeed=0.)


def test_awa_twa_lt_minus180():
    r"""true wind angle lower than -180, should raise a ValueError"""
    with pytest.raises(ValueError):
        apparent_wind_angle(true_wind_speed=1., true_wind_angle=-181., boatspeed=0.)


def test_awa_twa_gt_180():
    r"""true wind angle higher than 180, should raise a ValueError"""
    with pytest.raises(ValueError):
        apparent_wind_angle(true_wind_speed=1., true_wind_angle=181., boatspeed=0.)


def test_awa_zero_boatspeed_twa():
    r"""At zero speed, the true wind angle and
    the apparent wind angle should be equal"""
    awa_zero_boatspeed_1 = apparent_wind_angle(true_wind_speed=10., true_wind_angle=45., boatspeed=0.)
    assert awa_zero_boatspeed_1 == 45.

    awa_zero_boatspeed_2 = apparent_wind_angle(true_wind_speed=10., true_wind_angle=-165., boatspeed=0.)
    expected_value, atol = -165., 1e-6
    assert expected_value - atol <= awa_zero_boatspeed_2 <= expected_value + atol

    # (tws*math.cos(twa * to_rad))+speed is 0
    awa_zero_boatspeed_3 = apparent_wind_angle(true_wind_speed=10., true_wind_angle=90., boatspeed=0.)
    assert awa_zero_boatspeed_3 == 90.


def test_awa_known_values():
    r"""Known values"""
    awa_reaching_same_speed_as_tws = apparent_wind_angle(true_wind_speed=10., true_wind_angle=90., boatspeed=10.)
    assert awa_reaching_same_speed_as_tws == 45.

    awa_almost_downwind = apparent_wind_angle(true_wind_speed=10., true_wind_angle=170., boatspeed=1.)
    expected_value, atol = 168.896520756, 1e-6
    assert expected_value - atol <= awa_almost_downwind <= expected_value + atol


def test_awa_known_values_going_backwards():
    r"""Known values going backwards"""
    awa_backwards_reaching_same_speed_as_tws = apparent_wind_angle(
        true_wind_speed=10., true_wind_angle=90.,
        boatspeed=-10.)
    assert awa_backwards_reaching_same_speed_as_tws == 135.

    # Head to wind, going backwards at the same speed as true_wind_speed
    awa_head_to_wind_no_apparent = apparent_wind_angle(true_wind_speed=10., true_wind_angle=0., boatspeed=-10.)
    assert awa_head_to_wind_no_apparent == 0.


def test_awa_opposite_heel_angles():
    r"""Opposite heel angles should result in the same apparent wind angle"""
    awa_heeled_40_degrees = apparent_wind_angle(true_wind_speed=10., true_wind_angle=120., boatspeed=3., heel_angle=40.)
    awa_counterheeled_40_degrees = apparent_wind_angle(true_wind_speed=10., true_wind_angle=120., boatspeed=3.,
                                                       heel_angle=-40.)
    assert awa_heeled_40_degrees == awa_counterheeled_40_degrees


def test_awa_90_degrees_heel():
    r""" Boat at 90° heel"""
    awa_heeled_90_degrees_1 = apparent_wind_angle(true_wind_speed=10., true_wind_angle=75., boatspeed=3.,
                                                  heel_angle=90.)
    expected_value, atol = 0., 1e-6
    assert expected_value - atol <= awa_heeled_90_degrees_1 <= expected_value + atol

    awa_heeled_90_degrees_2 = apparent_wind_angle(true_wind_speed=10., true_wind_angle=90., boatspeed=3.,
                                                  heel_angle=90.)
    expected_value, atol = 0., 1e-6
    assert expected_value - atol <= awa_heeled_90_degrees_2 <= expected_value + atol


# apparent_wind_speed() tests


def test_aws_negative_tws():
    r"""Negative true wind speed, should raise a ValueError"""
    with pytest.raises(ValueError):
        apparent_wind_speed(true_wind_speed=-1., true_wind_angle=45., boatspeed=0.)


def test_aws_twa_lt_minus180():
    r"""true wind angle lower than -180, should raise a ValueError"""
    with pytest.raises(ValueError):
        apparent_wind_speed(true_wind_speed=1., true_wind_angle=-181., boatspeed=0.)


def test_aws_twa_gt_180():
    r"""true wind angle higher than 180, should raise a ValueError"""
    with pytest.raises(ValueError):
        apparent_wind_speed(true_wind_speed=1., true_wind_angle=181., boatspeed=0.)


def test_aws_known_values():
    r"""Known or easily determined values"""
    aws_head_to_wind = apparent_wind_speed(true_wind_speed=10., true_wind_angle=0., boatspeed=10.)
    assert aws_head_to_wind == 20.

    # fully downwind
    aws_downwind = apparent_wind_speed(true_wind_speed=10., true_wind_angle=180., boatspeed=3.)
    assert aws_downwind == 7.

    # 90° reach at the same speed as true_wind_speed
    aws_reaching_same_boatspeed_as_tws = apparent_wind_speed(true_wind_speed=10., true_wind_angle=90., boatspeed=10.)
    assert aws_reaching_same_boatspeed_as_tws == 10 * math.sqrt(2.)


def test_aws_known_values_going_backwards():
    r"""Known values going backwards"""
    aws_going_backwards_head_to_wind = apparent_wind_speed(true_wind_speed=10., true_wind_angle=0., boatspeed=-10.)
    assert aws_going_backwards_head_to_wind == 0.


def test_aws_opposite_twa():
    r"""Opposite twas"""
    aws_beating_on_starboard = apparent_wind_speed(true_wind_speed=10., true_wind_angle=45., boatspeed=3.)
    aws_beating_on_port = apparent_wind_speed(true_wind_speed=10., true_wind_angle=-45., boatspeed=3.)
    assert aws_beating_on_starboard == aws_beating_on_port
