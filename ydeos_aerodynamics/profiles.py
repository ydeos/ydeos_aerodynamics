# coding: utf-8

r"""Wind profiles (i.e. variation of wind speed with altitude)."""

from math import log


def power_law(wind_speed_known: float,
              height_reference: float,
              height: float,
              alpha: float = 0.11) -> float:
    r"""Wind profile power law.

    wind_speed_known : The measured wind speed at height_reference
    height_reference : The height at which the wind speed
                       has been measured or is known
    height : The height at which we want to determine the wind speed
    alpha : float, optional (default is 0.11)
        stability related exponent, aka Hellman exponent
        A value of 0.11 is recommended over open water
        A value of 0.143 (1/7) is recommended over land

        Unstable air above open water surface: 0.06
        Neutral air above open water surface: 0.10
        Unstable air above flat open coast: 0.11
        Neutral air above flat open coast: 0.16
        Stable air above open water surface: 0.27
        Unstable air above human inhabited areas: 0.27
        Neutral air above human inhabited areas: 0.34
        Stable air above flat open coast: 0.40
        Stable air above human inhabited areas: 0.60

    Returns the wind speed at height

    References
    ----------
    https://en.wikipedia.org/wiki/Wind_profile_power_law

    """
    if wind_speed_known < 0.:
        raise ValueError("Wind speed known should be positive or zero")
    if height_reference <= 0.:
        raise ValueError("Height reference should be strictly positive")
    if height < 0.:
        raise ValueError("Height should be positive or zero")
    if alpha <= 0.:
        raise ValueError("alpha must be strictly positive")
    return wind_speed_known * (height / height_reference)**alpha


def logarithmic(wind_speed_known: float,
                height_reference: float,
                height: float,
                roughness_length: float = 0.0002) -> float:
    r"""Logarithmic wind profile.

    wind_speed_known : The measured wind speed at height_reference
    height_reference : The height at which the wind speed
                       has been measured or is known
    height : The height at which we want to determine the wind speed
    roughness_length : float, optional
                              (default is 0.0002,
                              roughness for water surfaces: seas and Lakes)
        Roughness length
        0.0002 m : Water surfaces: seas and Lakes
        0.0024 m : Open terrain with smooth surface,
                   e.g. concrete, airport runways, mown grass etc.
        0.03 m : Open agricultural land without fences and hedges;
                 maybe some far apart buildings and very gentle hills
        0.055 m : Agricultural land with a few buildings and 8 m high hedges
                  separated by more than 1 km
        0.1 m : Agricultural land with a few buildings
                and 8 m high hedges separated by approx. 500 m
        0.2 m : Agricultural land with many trees, bushes and plants,
                or 8 m high hedges separated by approx. 250 m
        0.4 m : Towns, villages, agricultural land with many or high hedges,
                forests and very rough and uneven terrain
        0.6 m : Large towns with high buildings
        1.6 m : Large cities with high buildings and skyscrapers

    Returns the wind speed at height

    References
    ----------
    http://wind-data.ch/tools/profile.php?lng=en

    """
    if wind_speed_known < 0.:
        raise ValueError("Wind speed known should be positive or zero")
    if height_reference <= 0.:
        raise ValueError("Height reference should be strictly positive")
    if height <= 0.:
        raise ValueError("Height should be strictly positive")
    if roughness_length <= 0.:
        raise ValueError("Roughness length must be strictly positive")
    return wind_speed_known * log(height / roughness_length) / log(height_reference / roughness_length)
