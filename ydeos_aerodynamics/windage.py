# coding: utf-8

r"""Windage

# **** DOUBTS ****
# kx value for RectBivariateSpline

"""

from math import sin, cos, radians
import numpy as np
from scipy.interpolate import RectBivariateSpline, UnivariateSpline
from ydeos_aerodynamics.air import RHO_AIR_20C
from ydeos_aerodynamics.force import Force
from ydeos_aerodynamics.apparent import apparent_wind_angle, apparent_wind_speed


def windage_hull(tws: float,
                 twa: float,
                 boatspeed: float,
                 heel_angle: float,
                 freeboard_average: float,
                 loa: float,
                 beam_max: float,
                 rho_air: float = RHO_AIR_20C) -> Force:
    r"""Hull windage

    tws : true wind speed [m/s], positive
    twa : true wind angle [degrees], between -180 and 180
    boatspeed : [m/s]
    heel_angle : [degrees], between -90 and 90
    freeboard_average : Freeboard height average of the hull [m], must be >= 0
    loa : overall length of the hull [m], must be >= 0
    beam_max : maximum beam of the hull[m], must be >= 0
    rho_air : air density [kg/m**3], must be >= 0

    Logic summary
    -------------
    ORC 2013 p44
    @ AWA = 0°
        Zce = 0.66 * ( FBAV + B*sin(phi))
        Cd = 0.68
        A_ref = FBAV * B
    @AWA = 90°
        Zce = 0.66 * ( FBAV + B*sin(phi))
        Cd = 0.68
        A_ref = f(HSA, phi)
    @AWA = 180° -> idem 0°

    Returns a Force object, representing the hull windage,
    The x-coordinate of the point of application is loa/2

    """
    if freeboard_average <= 0.:
        raise ValueError("freeboard_average must be strictly positive")
    if loa <= 0.:
        raise ValueError("loa must be strictly positive")
    if beam_max <= 0.:
        raise ValueError("beam_max must be strictly positive")
    if rho_air <= 0.:
        raise ValueError("rho_air must be strictly positive")

    half_deck_surface = (loa * beam_max * 0.7) / 2.
    hull_side_area_upright = loa * freeboard_average

    # Build a 2D interpolable surface
    awas = [0., 90., 180.]
    heel_angle_samples = [0., 10., 20., 30., 40., 50., 60., 70., 80., 90.]
    arefs = []
    for awa in awas:
        values = []
        for heel_angle in heel_angle_samples:
            if awa != 90.:
                values.append(freeboard_average * beam_max)
            else:
                values.append(hull_side_area_upright +
                              half_deck_surface * sin(radians(heel_angle)))
        arefs.append(values)
    arefs = np.array(arefs)
    aref_interpolant = RectBivariateSpline(awas,
                                           heel_angle_samples,
                                           arefs,
                                           kx=1)

    awa = apparent_wind_angle(tws, twa, boatspeed, heel_angle=0.)
    aws = apparent_wind_speed(tws, twa, boatspeed, heel_angle=0.)

    z_ce = 0.66 * (freeboard_average + beam_max * sin(radians(heel_angle)))

    # aref = aref_interpolant.ev(abs(awa), abs(heel_angle))[0]
    aref = aref_interpolant.ev(abs(awa), abs(heel_angle))

    c_drag = 0.68
    drag = 0.5 * rho_air * c_drag * aref * aws ** 2

    # back = drag * cos(radians(awa))

    # positive with awa  positive (stbd), negative on port
    # side = drag * sin(radians(awa))

    return Force(-drag * cos(radians(awa)), drag * sin(radians(awa)), 0, loa / 2., 0., z_ce)


def windage_mast_with_sail(tws: float,
                           twa: float,
                           boatspeed: float,
                           heel_angle: float,
                           trim_angle: float,
                           mast_x: float,
                           mast_z_bottom: float,
                           mast_z_top: float,
                           mast_front_area: float,
                           mast_side_area: float,
                           rho_air: float = RHO_AIR_20C) -> Force:
    r"""Calculates the force caused by the windage of the mast

    tws : true wind speed [m/s], positive
    twa : true wind angle [degrees], between -180 and 180
    boatspeed : [m/s]
    heel_angle : [degrees], between -90 and 90
    trim_angle : [degrees], bow up is positive. If not provided, the default value is 0.
    mast_x : mast x position
    mast_z_bottom : Altitude of the lowest part of the mast that is
                    exposed to the wind.
                    Must be > 0.
    mast_z_top : Altitude of the highest part of the mast that is
                 exposed to the wind.
                 Must be > 0.
    mast_front_area : Frontal area of the mast [m**2] that is
                      exposed to the wind.
                      Must be >= 0.
    mast_side_area : Lateral area of the mast [m**2] that is
                     exposed to the wind.
                     Must be >= 0.
    rho_air : air density [kg/m**3], must be >= 0

    Logic summary
    -------------
    ORC 2013 p44

    Returns a Force object, representing the hull windage.
    The x-coordinate of the point of application is mast_x

    """
    if mast_z_bottom <= 0.:
        raise ValueError("mast_z_bottom must be strictly positive")
    if mast_z_top <= 0.:
        raise ValueError("mast_z_top must be strictly positive")
    if mast_z_top <= mast_z_bottom:
        raise ValueError("mast_z_top must be strictly above mast_z_bottom")
    if mast_front_area <= 0.:
        raise ValueError("mast_front_area must be strictly positive")
    if mast_side_area <= 0.:
        raise ValueError("mast_side_area must be strictly positive")
    if rho_air <= 0.:
        raise ValueError("rho_air must be strictly positive")

    # The upright centre of effort is always at the same altitude.
    upright_centre_of_effort_altitude = (mast_z_bottom + mast_z_top) / 2.

    # Build a 1D interpolable object
    awas = [0., 90., 180.]
    s_times_c_drag = []
    for awa in awas:
        if awa != 90.:
            s_times_c_drag.append(0.4 * mast_front_area)
        else:
            s_times_c_drag.append(0.6 * mast_side_area)
    s_times_c_drag_interpolant = UnivariateSpline(awas, s_times_c_drag, k=2, s=0)

    if twa == 0.:
        sign = 0.
    else:
        sign = twa / abs(twa) if boatspeed != 0. else 0.

    awa = apparent_wind_angle(tws, twa, boatspeed, heel_angle=0.)
    aws = apparent_wind_speed(tws, twa, boatspeed, heel_angle=0.)

    drag = 0.5 * rho_air * s_times_c_drag_interpolant(abs(awa)) * aws ** 2

    x_force = -drag * cos(radians(awa))

    # positive with awa  positive (stbd), negative on port
    y_force = drag * sin(radians(awa))

    return Force(x_force, y_force, 0,
                 mast_x - upright_centre_of_effort_altitude * sin(radians(trim_angle)),
                 upright_centre_of_effort_altitude * sin(radians(heel_angle)) * sign,
                 upright_centre_of_effort_altitude * cos(radians(heel_angle)))
