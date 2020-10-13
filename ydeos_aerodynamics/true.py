# coding: utf-8

r"""True wind from apparent.

http://www.sailnet.com/forums/general-discussion-sailing-related/50411-apparent-wind-formula.html

"""

from typing import Dict
from math import cos, sin, radians, degrees, atan, sqrt


def true_wind_angle(apparent_wind_speed: float,
                    apparent_wind_angle: float,
                    boatspeed: float,
                    heel_angle: float = 0.) -> float:
    r"""True wind angle from apparent wind, boat speed and heel angle.

    Parameters
    ----------
    apparent_wind_speed : apparent wind speed [m/s], must be >= 0
    apparent_wind_angle : apparent wind angle [degrees],
                          must be between -180 and 180
                          positive on starboard tack, negative on port tack
    boatspeed : [m/s], positive (forward motion) or negative(backwards motion)
    heel_angle : [degrees], must be between -90 and 90
                 positive when the boat heels to leeward
                 negative when the boat heels to windward

    Returns the true wind angle [degrees]
            the true wind angle must be between -180 and 180.
            the true wind angle is:
            - positive on starboard tack,
            - negative on port tack.
            the true wind angle and the apparent wind angle
            always have the same sign.

    Raises
    ------
    ValueError
        if apparent_wind_speed is negative
        if apparent_wind_angle is smaller than -180 or greater than 180
        if the computed true wind angle is smaller than -180 or greater than 180

    """
    if apparent_wind_speed < 0.:
        raise ValueError("The apparent wind speed must be positive")
    if apparent_wind_angle < -180. or apparent_wind_angle > 180.:
        raise ValueError("The apparent wind angle must be between -180 and 180")
    if heel_angle < -89. or heel_angle > 89.:
        raise ValueError("Cannot compute the true wind from a boat heeled"
                         "more than 89 degrees")

    sign = apparent_wind_angle / abs(apparent_wind_angle) if apparent_wind_angle != 0. else 0.
    apparent_wind_angle = abs(apparent_wind_angle)
    apparent_wind_angle /= cos(radians(heel_angle))
    y = 90. - apparent_wind_angle
    a = apparent_wind_speed * cos(radians(y))
    bb = apparent_wind_speed * sin(radians(y))
    b = bb - boatspeed

    return sign * (90. - degrees(atan(b / a))) if a != 0. else 0.


def true_wind_speed(apparent_wind_speed: float,
                    apparent_wind_angle: float,
                    boatspeed: float,
                    heel_angle: float = 0.) -> float:
    r"""Apparent wind speed from true wind, boat speed and heel angle.

    Parameters
    ----------
    apparent_wind_speed : apparent wind speed [m/s], must be >= 0
    apparent_wind_angle : apparent wind angle [degrees],
                          must be between -180 and 180
                          apparent wind angle is:
                          - positive on starboard tack
                          - negative on port tack
    boatspeed : [m/s], positive (forward motion) or negative(backwards motion)
    heel_angle : [degrees], must be between -90 and 90
                 positive when the boat heels to leeward
                 negative when the boat heels to windward

    Returns the true wind speed [m/s] (is always positive or zero)

    Raises
    ------
    ValueError
        if apparent_wind_speed is negative
        if apparent_wind_angle smaller than -180 or greater than 180

    """
    if apparent_wind_speed < 0.:
        raise ValueError('The apparent wind speed must be positive')
    if apparent_wind_angle < -180. or apparent_wind_angle > 180.:
        raise ValueError('The apparent wind angle must be between -180 and 180')
    if heel_angle < -89. or heel_angle > 89.:
        raise ValueError("Cannot compute the true wind from a boat"
                         "heeled more than 89 degrees")
    apparent_wind_angle = abs(apparent_wind_angle)
    apparent_wind_angle /= cos(radians(heel_angle))
    y = 90. - apparent_wind_angle
    a = apparent_wind_speed * cos(radians(y))
    bb = apparent_wind_speed * sin(radians(y))
    b = bb - boatspeed
    return sqrt(a * a + b * b)


def true_wind(apparent_wind_speed: float,
              apparent_wind_angle: float,
              boatspeed: float,
              heel_angle: float = 0.) -> Dict[str, float]:
    r"""Compute the apparent wind from true wind, boat speed and heel angle.

    apparent_wind_speed : [m/s], must be >= 0
    apparent_wind_angle : [degrees], must be between -180 and 180
                          apparent wind angle is:
                          - positive on starboard tack
                          - negative on port tack
    boatspeed : [m/s], positive (forward motion) or negative(backwards motion)
    heel_angle : [degrees], must be between -90 and 90
                 positive when the boat heels to leeward
                 negative when the boat heels to windward

    """
    return {"speed": true_wind_speed(apparent_wind_speed,
                                     apparent_wind_angle,
                                     boatspeed,
                                     heel_angle),
            "angle": true_wind_angle(apparent_wind_speed,
                                     apparent_wind_angle,
                                     boatspeed,
                                     heel_angle)}
