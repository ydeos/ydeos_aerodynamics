#!/usr/bin/env python
# coding: utf-8

r"""Tests for the windage.py module"""

import pytest

from ydeos_aerodynamics.windage import windage_hull, windage_mast_with_sail


def test_windage_hull_negative_freeboard():
    r"""Negative freeboard average"""
    with pytest.raises(ValueError):
        windage_hull(tws=10., twa=45., boatspeed=0., heel_angle=0., freeboard_average=-0.07, loa=1.0, beam_max=0.2)


def test_windage_hull_zero_speed_x_force_negative():
    r"""Zero speed"""
    force = windage_hull(tws=10., twa=45., boatspeed=0., heel_angle=0., freeboard_average=0.07, loa=1.0, beam_max=0.2)
    assert force.fx < 0

    force = windage_hull(tws=10., twa=-45., boatspeed=0., heel_angle=0., freeboard_average=0.07, loa=1.0, beam_max=0.2)
    assert force.fx < 0


def test_windage_hull_zero_speed_stbd_y_force_positive():
    r"""Zero speed, starboard tack"""
    force_stb = windage_hull(tws=10., twa=45., boatspeed=0., heel_angle=0., freeboard_average=0.07, loa=1.0,
                             beam_max=0.2)
    assert force_stb.fy > 0


def test_windage_hull_zero_speed_port_y_force_negative():
    r"""Zero speed, port tack"""
    force_port = windage_hull(tws=10., twa=-45., boatspeed=0., heel_angle=0., freeboard_average=0.07, loa=1.0,
                              beam_max=0.2)
    assert force_port.fy < 0


def test_windage_hull_square_downwind_running():
    r"""Windage of hull running downwind"""
    force = windage_hull(tws=10., twa=180., boatspeed=5., heel_angle=0., freeboard_average=0.07, loa=1.0, beam_max=0.2)
    assert force.fx > 0

# Mast windage


def test_windage_mast_with_sail_exceptions():
    r"""Wrong input cases"""
    with pytest.raises(ValueError):
        windage_mast_with_sail(tws=10., twa=45., boatspeed=2., heel_angle=10., trim_angle=0., mast_x=0.5,
                               mast_z_bottom=-0.07, mast_z_top=1.7, mast_front_area=0.017, mast_side_area=0.017)
    with pytest.raises(ValueError):
        windage_mast_with_sail(tws=10., twa=45., boatspeed=2., heel_angle=10., trim_angle=0., mast_x=0.5,
                               mast_z_bottom=0.07, mast_z_top=1.7, mast_front_area=-0.017, mast_side_area=0.017)


def test_windage_mast_with_sail_stbd_upwind():
    r"""Upwind on starboard tack"""
    force = windage_mast_with_sail(tws=10., twa=45., boatspeed=2., heel_angle=10., trim_angle=0., mast_x=0.5,
                                   mast_z_bottom=0.07, mast_z_top=1.7, mast_front_area=0.017, mast_side_area=0.017)

    assert force.fx < 0
    assert force.fy > 0
    assert force.py > 0

    force_neg_heel = windage_mast_with_sail(tws=10., twa=45., boatspeed=2., heel_angle=-10., trim_angle=0., mast_x=0.5,
                                            mast_z_bottom=0.07, mast_z_top=1.7, mast_front_area=0.017,
                                            mast_side_area=0.017)
    assert force_neg_heel.py < 0


def test_windage_mast_with_sail_port_upwind():
    r"""Upwind on port tack"""
    force = windage_mast_with_sail(tws=10., twa=-45., boatspeed=2., heel_angle=10., trim_angle=0., mast_x=0.5,
                                   mast_z_bottom=0.07, mast_z_top=1.7, mast_front_area=0.017, mast_side_area=0.017)

    assert force.fx < 0
    assert force.fy < 0
    assert force.py < 0

    force_neg_heel = windage_mast_with_sail(tws=10., twa=-45., boatspeed=2., heel_angle=-10., trim_angle=0., mast_x=0.5,
                                            mast_z_bottom=0.07, mast_z_top=1.7, mast_front_area=0.017,
                                            mast_side_area=0.017)
    assert force_neg_heel.py > 0


def test_windage_mast_with_sail_stbd_downwind():
    r"""Downwind on port tack"""
    force = windage_mast_with_sail(tws=10., twa=165., boatspeed=2., heel_angle=0., trim_angle=0., mast_x=0.5,
                                   mast_z_bottom=0.07, mast_z_top=1.7, mast_front_area=0.017, mast_side_area=0.017)
    assert force.fx > 0
    assert force.fy > 0


def test_windage_mast_with_sail_port_downwind():
    r"""Downwind on port tack"""
    force = windage_mast_with_sail(tws=10., twa=-165., boatspeed=2., heel_angle=0., trim_angle=0., mast_x=0.5,
                                   mast_z_bottom=0.07, mast_z_top=1.7, mast_front_area=0.017, mast_side_area=0.017)
    assert force.fx > 0
    assert force.fy < 0


def test_windage_mast_ce_position():
    r"""Centre of effort position tests, with 30° of heel and 60° of heel

    y position of force application at 30° should be the same as z position
    of application at 60° of heel

    """
    force = windage_mast_with_sail(tws=10., twa=45., boatspeed=2., heel_angle=30., trim_angle=0., mast_x=0.5,
                                   mast_z_bottom=0.07, mast_z_top=1.7, mast_front_area=0.017, mast_side_area=0.017)
    value = ((1.7 + 0.07) / 2.) / 2.
    assert value - 1e-6 <= force.py <= value + 1e-6

    force = windage_mast_with_sail(tws=10., twa=45., boatspeed=2., heel_angle=60., trim_angle=0., mast_x=0.5,
                                   mast_z_bottom=0.07, mast_z_top=1.7, mast_front_area=0.017, mast_side_area=0.017)
    assert value - 1e-6 <= force.pz <= value + 1e-6


def test_windage_mast_with_trim_angle():
    r"""Trim angle influence tests"""
    # bow up
    force_stb = windage_mast_with_sail(tws=10., twa=45., boatspeed=2., heel_angle=30., trim_angle=5., mast_x=0.5,
                                       mast_z_bottom=0.07, mast_z_top=1.7, mast_front_area=0.017, mast_side_area=0.017)
    assert force_stb.fx < 0.5
    force_por = windage_mast_with_sail(tws=10., twa=-45., boatspeed=2., heel_angle=30., trim_angle=5.,   mast_x=0.5,
                                       mast_z_bottom=0.07, mast_z_top=1.7, mast_front_area=0.017,  mast_side_area=0.017)
    assert force_por.fx < 0.5

    # bow dow
    force_stb = windage_mast_with_sail(tws=10., twa=45., boatspeed=2., heel_angle=30.,  trim_angle=-5.,   mast_x=0.5,
                                       mast_z_bottom=0.07,  mast_z_top=1.7,    mast_front_area=0.017,
                                       mast_side_area=0.017)
    assert force_stb.px > 0.5
    force_por = windage_mast_with_sail(tws=10., twa=-45., boatspeed=2., heel_angle=30., trim_angle=-5.,  mast_x=0.5,
                                       mast_z_bottom=0.07,  mast_z_top=1.7,  mast_front_area=0.017,
                                       mast_side_area=0.017)
    assert force_por.px > 0.5
