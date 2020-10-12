#!/usr/bin/env python
# -*- coding: utf-8 -*-

r"""Tests for the aero_model_orc2013_like.py module"""

import pytest

from ydeos_aerodynamics.model import aero_force


def test_aero_model_exceptions():
    r"""negative mainsail area"""
    with pytest.raises(ValueError):
        aero_force(tws=10.,
                   twa=45.,
                   boatspeed=2.,
                   heel_angle=10.,
                   trim_angle=0.,
                   mainsail_type='main',
                   mainsail_area=-0.3,
                   mainsail_coe=(0.4, 0., 0.68),
                   frontsail_type='jib',
                   frontsail_area=0.2,
                   frontsail_coe=(0.8, 0., 0.45),
                   rig_z_max=1.7)


def test_aero_model_stbd_upwind():
    r"""Check the force on starboard tack, upwind"""
    force = aero_force(tws=10.,
                       twa=45.,
                       boatspeed=2.,
                       heel_angle=10.,
                       trim_angle=0.,
                       mainsail_type='main',
                       mainsail_area=0.3,
                       mainsail_coe=(0.4, 0., 0.68),
                       frontsail_type='jib',
                       frontsail_area=0.2,
                       frontsail_coe=(0.8, 0., 0.45),
                       rig_z_max=1.7)

    assert force.fx > 0
    assert force.fy > 0
    assert force.fz < 0
    assert force.py > 0


def test_aero_model_stbd_upwind_going_backwards():
    r"""Check the force on starboard tack, upwind, going backwards"""
    force = aero_force(tws=10.,
                       twa=45.,
                       boatspeed=-2.,
                       heel_angle=10.,
                       trim_angle=0.,
                       mainsail_type='main',
                       mainsail_area=0.3,
                       mainsail_coe=(0.4, 0., 0.68),
                       frontsail_type='jib',
                       frontsail_area=0.2,
                       frontsail_coe=(0.8, 0., 0.45),
                       rig_z_max=1.7)

    assert force.fx > 0
    assert force.fy > 0
    assert force.fz < 0
    assert force.py > 0


def test_aero_model_stbd_upwind_heeled_to_windward():
    r"""Check the force on starboard tack, upwind, negative heel"""
    force = aero_force(tws=10.,
                       twa=45.,
                       boatspeed=2.,
                       heel_angle=-10.,
                       trim_angle=0.,
                       mainsail_type='main',
                       mainsail_area=0.3,
                       mainsail_coe=(0.4, 0., 0.68),
                       frontsail_type='jib',
                       frontsail_area=0.2,
                       frontsail_coe=(0.8, 0., 0.45),
                       rig_z_max=1.7)

    assert force.fx > 0
    assert force.fy > 0
    assert force.fz > 0
    assert force.py < 0


def test_aero_model_port_upwind():
    r"""Check the force on port tack, upwind"""
    force = aero_force(tws=10.,
                       twa=-45.,
                       boatspeed=2.,
                       heel_angle=10.,
                       trim_angle=0.,
                       mainsail_type='main',
                       mainsail_area=0.3,
                       mainsail_coe=(0.4, 0., 0.68),
                       frontsail_type='jib',
                       frontsail_area=0.2,
                       frontsail_coe=(0.8, 0., 0.45),
                       rig_z_max=1.7)
    x_force = force.fx
    y_force = force.fy

    y_poa = force.py

    assert x_force > 0
    assert y_force < 0
    assert y_poa < 0


def test_twa_symmetry():
    r"""Check the force symmetry, for 2 opposite twa"""
    force_stb = aero_force(tws=10.,
                           twa=45.,
                           boatspeed=2.,
                           heel_angle=10.,
                           trim_angle=0.,
                           mainsail_type='main',
                           mainsail_area=0.3,
                           mainsail_coe=(0.4, 0., 0.68),
                           frontsail_type='jib',
                           frontsail_area=0.2,
                           frontsail_coe=(0.8, 0., 0.45),
                           rig_z_max=1.7)
    force_port = aero_force(tws=10.,
                            twa=-45.,
                            boatspeed=2.,
                            heel_angle=10.,
                            trim_angle=0.,
                            mainsail_type='main',
                            mainsail_area=0.3,
                            mainsail_coe=(0.4, 0., 0.68),
                            frontsail_type='jib',
                            frontsail_area=0.2,
                            frontsail_coe=(0.8, 0., 0.45),
                            rig_z_max=1.7)
    assert force_stb.fx == force_port.fx
    assert force_stb.fy == -force_port.fy
    assert force_stb.py == -force_port.py
