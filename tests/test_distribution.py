# !/usr/bin/env python
# coding: utf-8

r"""Tests for the distribution.py module"""

import numpy as np

from ydeos_aerodynamics.distribution import weibull_pdf, weibull_cdf, \
    weibull_mean, plot_weibull, weibull_random_samples


def test_weibull_pdf():
    r"""Test the probability distribution function"""
    assert weibull_pdf(1.) == 0.6070010779328798


def test_weibull_cdf():
    r"""Test the cumulative probability distribution function"""
    assert weibull_cdf(1.) == 0.6321205588285577
    for v in [float(x) for x in range(1, 100)]:
        assert weibull_pdf(v) < weibull_cdf(v)


def test_weibull_mean():
    r"""test the mean value"""
    assert weibull_mean() == 0.8942122621661722
    epsilon = 1e-3
    for v in [float(x) for x in range(1, 100)]:
        assert weibull_mean(v) < weibull_mean(v + epsilon)


def test_plot_weibull():
    r"""Just make sure it works"""
    fig, ax = plot_weibull()
    assert fig is not None
    assert ax is not None


def test_weibull_ransom_samples():
    r"""Just make sure it works"""
    samples = weibull_random_samples()
    assert isinstance(samples, np.ndarray)
