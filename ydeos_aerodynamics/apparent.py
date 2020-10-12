# coding: utf-8

r"""Apparent wind from true"""

from typing import Dict
from math import cos, sin, radians, degrees, atan, sqrt


def apparent_wind_angle(true_wind_speed: float,
                        true_wind_angle: float,
                        boatspeed: float,
                        heel_angle: float = 0.,
                        check_heel_angle: bool = False) -> float:
    r"""Apparent wind angle from true wind, boat speed and heel angle.

    true_wind_speed : true wind speed [m/s], must be >= 0
    true_wind_angle : true wind angle [degrees], must be between -180 and 180
                      positive on starboard tack, negative on port tack
    boatspeed : [m/s] can be positive (forward motion) or negative(backwards motion)
    heel_angle : the heel angle [degrees], must be between -90 and 90
                 positive when the boat heels to leeward and
                 negative when the boat heels to windward
    check_heel_angle : Should the heel angle be checked for validity
                       The apparent_wind_speed() function may be used
                       by a solver that cannot deal with a ValueError
                       and should realize by itself that it is going in the
                       wrong direction to find a solution.
                       A ValueError might break a solver's logic and it should
                       be possible to disable the check on the heel angle.

    Returns the apparent wind angle [degrees]
            the apparent wind angle must be between -180 and 180.
            the apparent wind angle is positive on starboard tack, negative on port tack.
            the true wind angle and the apparent wind angle always have the same sign.

    Raises
    ------
    ValueError
        if true_wind_speed is negative
        if true_wind_angle is smaller than -180 or greater than 180
        if the computed apparent wind angle is smaller than -180 or greater than 180

    """
    if true_wind_speed < 0.:
        raise ValueError("The true wind speed must be positive")
    if true_wind_angle < -180. or true_wind_angle > 180.:
        raise ValueError("The true wind angle must be between -180 and 180")
    if check_heel_angle is True:
        if heel_angle < -90. or heel_angle > 90.:
            raise ValueError("Unrealistic heel angle")

    sign = true_wind_angle / abs(true_wind_angle) if true_wind_angle != 0. else 0.

    if (true_wind_speed * cos(radians(abs(true_wind_angle)))) + boatspeed == 0.:
        awa = 0.
    else:
        awa = degrees(atan(true_wind_speed *
                           sin(radians(abs(true_wind_angle))) *
                           cos(radians(heel_angle)) /
                           (true_wind_speed *
                            cos(radians(abs(true_wind_angle))) + boatspeed)))

    # math.atan will return a negative angle for awa between 90 and 180
    if awa < 0:
        awa += 180.

    if awa < -180. or awa > 180.:
        raise ValueError('The apparent wind angle must be between -180 and 180')

    return awa * sign


def apparent_wind_speed(true_wind_speed: float,
                        true_wind_angle: float,
                        boatspeed: float,
                        heel_angle: float = 0.,
                        check_heel_angle: bool = False) -> float:
    r"""Compute the apparent wind speed from true wind, boat speed and heel angle.

    true_wind_speed : true wind speed [m/s], must be >= 0
    true_wind_angle : true wind angle [degrees], must be between -180 and 180
                      true wind angle is positive on starboard tack, negative on port tack
    boatspeed : [m/s] can be positive (forward motion) or negative(backwards motion)
    heel_angle : [degrees], must be between -90 and 90
                 positive when the boat heels to leeward
                 negative when the boat heels to windward
    check_heel_angle : Should the heel angle be checked for validity
                       The apparent_wind_speed() function may be used by
                       a solver that cannot deal with a ValueError
                       and should realize by itself that it is going in
                       the wrong direction to find a solution.
                       A ValueError might break a solver's logic and it
                       should be possible to disable the check on
                       the heel angle.

    Returns the apparent wind speed [m/s] (is always positive or zero)

    Raises
    ------
    ValueError
        if true_wind_speed is negative
        if true_wind_angle is smaller than -180 or greater than 180
        if heel_angle is smaller than -90 or greater than 90 and check_heel_angle is True

    """
    if true_wind_speed < 0.:
        raise ValueError('The true wind speed must be positive')
    if true_wind_angle < -180. or true_wind_angle > 180.:
        raise ValueError('The true wind angle must be between -180 and 180')
    if check_heel_angle is True:
        if heel_angle < -90. or heel_angle > 90.:
            raise ValueError("Unrealistic heel angle")

    return sqrt((true_wind_speed * sin(radians(true_wind_angle)) * cos(radians(heel_angle))) ** 2 +
                (true_wind_speed * cos(radians(true_wind_angle)) + boatspeed) ** 2)


def apparent_wind(true_wind_speed: float,
                  true_wind_angle: float,
                  boatspeed: float,
                  heel_angle: float = 0.,
                  check_heel_angle: bool = False) -> Dict[str, float]:
    r"""Compute the apparent wind from true wind, boat speed and heel angle.

    true_wind_speed : true wind speed [m/s], must be >= 0
    true_wind_angle : true wind angle [degrees], must be between -180 and 180
                      true wind angle is positive on starboard tack, negative on port tack
    boatspeed : [m/s] can be positive (forward motion) or negative(backwards motion)
    heel_angle : [degrees], must be between -90 and 90
                 positive when the boat heels to leeward
                 negative when the boat heels to windward
    check_heel_angle : Should the heel angle be checked for validity
                       The apparent_wind_speed() function may be used by a
                       solver that cannot deal with a ValueError
                       and should realize by itself that it is going in the
                       wrong direction to find a solution.
                       A ValueError might break a solver's logic and it
                       should be possible to disable the check on
                       the heel angle.

    """
    return {"speed": apparent_wind_speed(true_wind_speed,
                                         true_wind_angle,
                                         boatspeed,
                                         heel_angle,
                                         check_heel_angle),
            "angle": apparent_wind_angle(true_wind_speed,
                                         true_wind_angle,
                                         boatspeed,
                                         heel_angle,
                                         check_heel_angle)}
