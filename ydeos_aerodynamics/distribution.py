# coding: utf-8

r"""Wind speeds statistical distribution.

Follows a Weibull distribution law

lambda is the scale (linked to average wind speed)

k is the shape of the distribution.
A small value for k signifies very variable winds,
    while constant winds are characterized by a higher k

lambda typical values
---------------------
inland : 3-4 m/s or 6-8 knts
average : 4-5 m/s or 8-10knts
windy place near coast : 5-7 m/s or 10-14 knts

Beware than statistics may tale nighttime wind speeds into account,
    normally pulling the average down

k typical values
----------------
Typical ranges from 1.2 to 2.1?
average value around 1.65
1.15 in turbulent urban areas
As high as 3 or 4 for tropical trade winds

"""

from typing import Tuple
from math import exp
import numpy as np
from scipy.special import gamma
import matplotlib.pyplot as plt
from matplotlib.pyplot import Figure, Axes


def weibull_pdf(x: float, lambda_: float = 1, k: float = 1.65) -> float:
    r"""Probability distribution function."""
    if x < 0:
        return 0
    return (k / lambda_) * (x / lambda_)**(k - 1) * exp(-(x / lambda_)**k)


def weibull_cdf(x: float, lambda_: float = 1, k: float = 1.65) -> float:
    r"""Cumulative distribution function."""
    if x < 0:
        return 0
    return 1 - exp(-(x / lambda_)**k)


def weibull_mean(lambda_: float = 1, k: float = 1.65) -> float:
    r"""Mean value."""
    return lambda_ * gamma(1 + 1 / k)


def plot_weibull(to_x: float = 3,
                 lambda_: float = 1,
                 k: float = 1.65,
                 samples: int = 100,
                 show_pdf: bool = True,
                 show_cdf: bool = False,
                 show_random_samples: bool = True,
                 samples_info: bool = False) -> Tuple[Figure, Axes]:
    r"""Plot the Weibull distribution."""
    figure, axes = plt.subplots()
    xs = np.linspace(0, to_x, samples, endpoint=True)

    if show_pdf:
        ys = [weibull_pdf(x, lambda_, k) for x in xs]
        axes.plot(xs, ys, c="BLUE")

    if show_cdf:
        ys = [weibull_cdf(x, lambda_, k) for x in xs]
        axes.plot(xs, ys, c="ORANGE")

    if show_random_samples:
        nb_samples = int(1e5)
        random_samples = weibull_random_samples(nb_samples=nb_samples,
                                                lambda_=lambda_,
                                                k=k,
                                                samples_info=samples_info)
        # ax.hist(random_samples, bins=100, normed=True, color="gray")
        axes.hist(random_samples, bins=100, color="gray")

    axes.set_title(f"Weibull distribution\nlambda={lambda_:.3f}, k={k:.3f} "
                   f"- Mean (theory) : {weibull_mean(lambda_, k):.3f}")
    axes.set_xlim(left=0)
    # Intentionally not setting an upper limit
    # Will be inferred by the max of samples values
    axes.grid()

    return figure, axes


def weibull_random_samples(nb_samples: int = 10000,
                           lambda_: float = 1,
                           k: float = 1.65,
                           samples_info: bool = False) -> np.ndarray:
    r"""Generate random samples."""
    random_samples = np.random.weibull(k, nb_samples)
    random_samples *= lambda_  # horizontal scaling
    if samples_info:
        print("Random samples avg : %.3f "
              "on %i samples" % (np.average(random_samples), nb_samples))
        print("Random samples max : %.3f" % np.max(random_samples))
        print("Random samples min : %.3f" % np.min(random_samples))
    return random_samples
