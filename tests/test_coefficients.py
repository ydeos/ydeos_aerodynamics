# !/usr/bin/env python
# coding: utf-8

r"""Tests for the coefficients.py module"""

import pytest

from ydeos_aerodynamics.model import ImsAeroModelCoefficients


def test_exceptions():
    r"""Test a request for an unknown sail type"""
    with pytest.raises(ValueError):
        ImsAeroModelCoefficients.coefficient_interp('unknown_sail_type')


def test_calls():
    r"""Test a normal successful code"""
    cl, cd = ImsAeroModelCoefficients.coefficient('jib', awa=50.)
    assert cl > 0
    assert cd > 0


def test_shitty_calls():
    r"""Test coefficients are 0 outside of the 0 - 180 degrees range"""
    cl, cd = ImsAeroModelCoefficients.coefficient('jib', awa=-1.)

    assert cl == 0
    assert cd == 0

    cl, cd = ImsAeroModelCoefficients.coefficient('jib', awa=181.)

    assert cl == 0
    assert cd == 0
