# coding: utf-8

r"""Wind triangle plotting.

Used by some examples to plot the wind triangle

"""

from math import sin, cos, radians, atan, degrees

import numpy as np
import matplotlib.pyplot as plt


def display_wind_triangle(true_wind_speed: float,
                          true_wind_angle: float,
                          apparent_wind_speed: float,
                          apparent_wind_angle: float,
                          boatspeed: float) -> None:
    r"""Plot the wind triangle."""
    if true_wind_speed < 0 or apparent_wind_speed < 0:
        raise ValueError("Wind speeds must be positive")
    tw_color = "#08DDF1"
    aw_color = "#00B8FF"
    boatspeed_color = "#FF8840"

    true_wind_vec = np.array([[0., true_wind_speed, 0, -true_wind_speed]])

    bsp_orig_x = sin(radians(true_wind_angle)) * boatspeed
    bsp_orig_y = -cos(radians(true_wind_angle)) * boatspeed
    bsp_x = -sin(radians(true_wind_angle)) * boatspeed
    bsp_y = cos(radians(true_wind_angle)) * boatspeed
    boatspeed_vec = np.array([[bsp_orig_x, bsp_orig_y, bsp_x, bsp_y]])

    aw_orig_y = true_wind_speed
    aw_x = (sin(radians(true_wind_angle - apparent_wind_angle)) *
            apparent_wind_speed)
    aw_y = (-cos(radians(true_wind_angle - apparent_wind_angle)) *
            apparent_wind_speed)
    apparent_wind_vec = np.array([[0, aw_orig_y, aw_x, aw_y]])

    X, Y, U, V = zip(*true_wind_vec)
    A, B, C, D = zip(*boatspeed_vec)
    E, F, G, H = zip(*apparent_wind_vec)

    width, height = plt.figaspect(1.)
    f = plt.figure(figsize=(width, height), facecolor="white")

    ax = f.add_subplot(111, facecolor='white')
    plt.axis("equal")

    # hide the cartesian axes
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    ax.set_frame_on(False)  # outer frame

    # True wind
    ax.quiver(X, Y, U, V,
              angles='xy', scale_units='xy', scale=1, color=tw_color)
    ax.text(0.,
            true_wind_speed / 2.,
            f"tws={true_wind_speed:.2f}, twa={true_wind_angle:.2f}",
            size="small",
            color="black",
            rotation=90,
            horizontalalignment='center',
            verticalalignment='center')

    # Boatspeed
    ax.quiver(A, B, C, D,
              angles='xy', scale_units='xy', scale=1, color=boatspeed_color)
    ax.text(bsp_orig_x + bsp_x / 2.,
            bsp_orig_y + bsp_y / 2.,
            f"boatspeed={boatspeed}",
            size="small",
            color="black",
            rotation=degrees(atan(bsp_y / bsp_x)),
            horizontalalignment='center',
            verticalalignment='center')

    # Apparent wind
    ax.quiver(E, F, G, H,
              angles='xy', scale_units='xy', scale=1, color=aw_color)
    ax.text(aw_x / 2.,
            aw_orig_y + aw_y / 2.,
            f"aws={apparent_wind_speed:.2f}, awa={apparent_wind_angle:.2f}",
            size="small",
            color="black",
            rotation=degrees(atan(aw_y / aw_x)),
            horizontalalignment='center',
            verticalalignment='center')

    ax.set_xlim([-true_wind_speed, true_wind_speed])
    ax.set_ylim([-true_wind_speed, true_wind_speed])
    plt.draw()
    plt.show()
