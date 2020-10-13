#!/usr/bin/env python
# coding: utf-8

r"""Weibull wind speed distribution example."""

import matplotlib.pyplot as plt

from ydeos_aerodynamics.distribution import plot_weibull, weibull_mean


l_ = 14
k_ = 1.65
to_ = 5 * l_

f, a = plot_weibull(to_x=to_, lambda_=l_, k=k_)
plt.show()
print("Theoretical average : %.3f" % weibull_mean(lambda_=l_, k=k_))
