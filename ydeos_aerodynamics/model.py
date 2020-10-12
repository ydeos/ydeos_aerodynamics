# coding: utf-8

r"""Aerodynamic forces model based on the ORC 2013 model

TODO
  kpp
  eqn. [39] of ORC VPP 2013 (currently not taken into account)
  forward shift of CE at attached apparent wind angles (cf. Marchaj + see pdfs)

"""

from typing import Tuple, List
import warnings
from math import sqrt, cos, sin, radians, pi
from scipy import interpolate
from ydeos_aerodynamics.air import RHO_AIR_20C
from ydeos_aerodynamics.force import Force
from ydeos_aerodynamics.apparent import apparent_wind_angle, apparent_wind_speed


# Sail forces coefficients

class _Interpolant(object):
    """Interpolable object (for sail coefficients)"""

    def __init__(self, x: List[float], y: List[float]):
        """
        x : A 1-D array of monotonically increasing real values.
        y : A 1-D array of the same size as x

        """
        assert len(x) == len(y)
        self._x = x
        self._y = y
        # self._interpolant = interpolate.UnivariateSpline(x, y, s=0)
        # self._interpolant = interpolate.Rbf(x, y, function='thin_plate', smooth=0.)

        # Piecewise Cubic Hermite Interpolating Polynomial
        self._interpolant = interpolate.PchipInterpolator(x, y)

        # self._interpolant = interpolate.InterpolatedUnivariateSpline(x, y, k=1)

    def __call__(self, val: float) -> float:
        if self._x[-1] >= val >= self._x[0]:
            return self._interpolant(val)
        else:
            return 0


class ImsAeroModelCoefficients(object):
    """Build aerodynamic model coefficient interpolable objects"""

    # MAIN
    main_cl = _Interpolant([0.0, 12.0, 13.0, 15.0, 20.0, 30.0, 60.0, 90.0, 120.0, 170.0],
                           [0.0, 1.45, 1.45, 1.45, 1.43, 1.40, 1.28, 0.90, 0.60, 0.0])
    main_cd = _Interpolant([20.0, 60.0, 90.0, 120.0, 150.0, 176.0, 177.0, 178.0, 179.0, 180.0],
                           [0.0, 0.10, 0.30, 0.66, 1.10, 1.20, 1.20, 1.20, 1.20, 1.20])

    # MAIN_HIGH (ORC 2013)
    main_high_cl = _Interpolant([0., 7., 9., 12., 28., 60., 90., 120., 150., 180.],
                                [0.000, 0.948, 1.138, 1.250, 1.427, 1.269, 1.125, 0.838, 0.296, -0.112])
    main_high_cd = _Interpolant([0., 7., 9., 12., 28., 60., 90., 120., 150., 180.],
                                [0.034, 0.017, 0.015, 0.015, 0.026, 0.113, 0.383, 0.969, 1.316, 1.345])

    # MAIN_LOW (ORC 2013)
    main_low_cl = _Interpolant([0., 7., 9., 12., 28., 60., 90., 120., 150., 180.],
                               [0.000, 0.862, 1.052, 1.164, 1.347, 1.239, 1.125, 0.838, 0.296, -0.112])
    main_low_cd = _Interpolant([0., 7., 9., 12., 28., 60., 90., 120., 150., 180.],
                               [0.043, 0.026, 0.023, 0.023, 0.033, 0.113, 0.383, 0.969, 1.316, 1.345])

    # JIB
    jib_cl = _Interpolant([8.0, 19.0, 20.0, 21.0, 40.0, 50.0, 60.0, 80.0, 100.0, 150.0],
                          [0.0, 1.44, 1.45, 1.45, 1.43, 1.41, 1.25, 0.78, 0.40, 0.0])
    jib_cd = _Interpolant([16.0, 28.0, 40.0, 60.0, 80.0, 100.0, 120.0, 140.0, 160.0, 180.0],
                          [0.0, 0.10, 0.20, 0.35, 0.56, 0.73, 0.83, 0.92, 0.96, 0.90])

    # JIB_HIGH (ORC 2013)
    jib_high_cl = _Interpolant([7., 15., 20., 27., 50., 60., 100., 150., 180.],
                               [0.000, 1.100, 1.475, 1.500, 1.430, 1.250, 0.400, 0.000, -0.100])
    jib_high_cd = _Interpolant([7., 15., 20., 27., 50., 60., 100., 150., 180.],
                               [0.050, 0.032, 0.031, 0.037, 0.250, 0.350, 0.730, 0.950, 0.900])

    # JIB_LOW (ORC 2013)
    jib_low_cl = _Interpolant([7., 15., 20., 27., 50., 60., 100., 150., 180.],
                              [0.000, 1.000, 1.375, 1.450, 1.430, 1.250, 0.400, 0.000, -0.100])
    jib_low_cd = _Interpolant([7., 15., 20., 27., 50., 60., 100., 150., 180.],
                              [0.050, 0.032, 0.031, 0.037, 0.250, 0.350, 0.730, 0.950, 0.900])

    # BOOMED JIB
    # boomed_jib_cl = _Interpolant([ 8.0, 19.0, 20.0, 21.0, 40.0, 50.0, 60.0, 80.0, 100.0, 170.0 ],
    #                                  [ 0.0,  1.44, 1.45, 1.45, 1.43, 1.41, 1.30, 1.00,  0.70,  0.0 ])
    boomed_jib_cl = _Interpolant([7., 15., 20., 27., 50., 60., 100., 160., 180.],
                                 [0.000, 1.000, 1.375, 1.450, 1.430, 1.250 * 1.05, 0.400 * 1.3, 0.000, -0.100])
    # boomed_jib_cd = _Interpolant([ 16.0, 28.0, 40.0, 60.0, 80.0, 100.0, 120.0, 140.0, 160.0, 180.0 ],
    #                                  [ 0.0,   0.03, 0.06, 0.12, 0.25,  0.45,  0.70,  0.92,  1.05,  1.10 ])
    boomed_jib_cd = _Interpolant([7., 15., 20., 27., 50., 60., 100., 150., 180.],
                                 [0.050, 0.032, 0.031, 0.037, 0.250, 0.350, 0.730 * 1.1, 0.950 * 1.2, 0.900 * 1.3])

    # SPINNAKER
    spi_cl = _Interpolant([28.0, 41.0, 60.0, 80.0, 100.0, 120.0, 140.0, 160.0, 170.0, 180.0],
                          [0.0, 1.15, 1.70, 1.62, 1.40, 1.00, 0.65, 0.32, 0.16, 0.0])
    spi_cd = _Interpolant([28.0, 41.0, 60.0, 80.0, 100.0, 120.0, 140.0, 160.0, 170.0, 180.0],
                          [0.10, 0.20, 0.43, 0.80, 1.00, 1.08, 1.12, 1.10, 1.10, 1.10])

    # S_SPINNAKER (ORC 2013)
    S_spinnaker_cl = _Interpolant([28., 41., 50., 60., 67., 75., 100., 115., 130., 150., 180.],
                                  [0.000, 0.978, 1.241, 1.454, 1.456, 1.437, 1.190, 0.951, 0.706, 0.425, 0.000])
    S_spinnaker_cd = _Interpolant([28., 41., 50., 60., 67., 75., 100., 115., 130., 150., 180.],
                                  [0.213, 0.321, 0.425, 0.587, 0.598, 0.619, 0.850, 0.911, 0.935, 0.935, 0.935])

    # A_SPINNAKER ON CENTRELINE (ORC 2013)
    A_spinnaker_on_centreline_cl = _Interpolant([28., 41., 50., 60., 67., 75., 100., 115., 130., 150., 180.],
                                                [0.026, 1.018, 1.277, 1.471, 1.513, 1.444, 1.137, 0.829, 0.560, 0.250,
                                                 -0.120])
    A_spinnaker_on_centreline_cd = _Interpolant([28., 41., 50., 60., 67., 75., 100., 115., 130., 150., 180.],
                                                [0.191, 0.280, 0.366, 0.523, 0.448, 0.556, 0.757, 0.790, 0.776, 0.620,
                                                 0.400])

    # A_SPINNAKER ON POLE (ORC 2013)
    A_spinnaker_on_pole_cl = _Interpolant([28., 41., 50., 60., 67., 75., 100., 115., 130., 150., 180.],
                                          [0.085, 1.114, 1.360, 1.513, 1.548, 1.479, 1.207, 0.956, 0.706, 0.425, 0.000])
    A_spinnaker_on_pole_cd = _Interpolant([28., 41., 50., 60., 67., 75., 100., 115., 130., 150., 180.],
                                          [0.170, 0.238, 0.306, 0.459, 0.392, 0.493, 0.791, 0.894, 0.936,  0.936,
                                           0.936])

    # CODE_ZERO (ORC 2013)
    code_zero_cl = _Interpolant([7., 19., 26., 35., 42., 53., 70., 100., 120., 150., 180.],
                                [0.000, 1.000, 1.785, 2.150, 2.200, 1.900, 1.450, 0.800, 0.450, 0.150, -0.070])
    code_zero_cd = _Interpolant([7., 19., 26., 35., 42., 53., 70., 100., 120., 150., 180.],
                                [0.065, 0.045, 0.065, 0.080, 0.140, 0.280, 0.470, 0.740, 0.850, 0.820, 0.720])

    @staticmethod
    def coefficient(sail_type: str, awa: float) -> Tuple[float, float]:
        """Return the values (cl,cd) of the aero coefficients for a given sail type and apparent wind angle"""
        cl, cd = ImsAeroModelCoefficients.coefficient_interp(sail_type)
        return cl(awa), cd(awa)

    @staticmethod
    def coefficient_interp(sail_type: str) -> Tuple[_Interpolant, _Interpolant]:
        """Get a tuple of interpolable objects representing the lift and drag coefficients for the given sail type"""
        try:
            return (getattr(ImsAeroModelCoefficients, sail_type + '_cl'),
                    getattr(ImsAeroModelCoefficients, sail_type + '_cd'))
        except AttributeError:
            raise ValueError('Unknown sail type')


#

def aero_force(tws: float, twa: float, boatspeed: float, heel_angle: float, trim_angle: float,
               mainsail_type: str, mainsail_area: float, mainsail_coe: Tuple[float, float, float],
               frontsail_type: str, frontsail_area: float, frontsail_coe: Tuple[float, float, float],
               rig_z_max: float, flat: float = 1.0, fractionality: float = 0.8, overlap: float = 1.1,
               roach: float = 0.2, rho_air: float = RHO_AIR_20C) -> Force:
    r"""Aero force inspired by ORC 2013 model

    tws : true wind speed [m/s], positive
    twa : true wind angle [degrees], between -180 and 180
    boatspeed : [m/s]
    heel_angle : [degrees], between -90 and 90
    trim_angle : [degrees], bow up is positive. Used to shift the X position of the centre of effort when the boat
                 has trim angle.
    mainsail_type : The type of mainsail, has to be an entry of the coefficients
    mainsail_area: [m**2], must be > 0.
    mainsail_coe : Represents the x, y, z coordinates of the mainsail centre of effort
    frontsail_type : The type of frontsail, has to be an entry of the coefficients
    frontsail_area : [m**2], must be > 0.
    frontsail_coe : Represents the x, y, z coordinates of the frontsail centre of effort
    rig_z_max : mainsail head z or avg (mainsail head z, frontsail head z) if frontsail head z > mainsail head z
    flat : FLAT parameter, between 0 and 1. Realistic values are between 0.6 and 1.0
    fractionality : Icurrent/(Pcurrent+BAS). Realistic values are between 0.6 and 1.0
    overlap : LPGcurrent/J, Realistic values are between 0.7 and 2.0
    roach : Mainsail Area /(P x E / 2) -1
    rho_air : air density [kg/m**3], must be >= 0

    """
    # errors
    if mainsail_area < 0.:
        raise ValueError("mainsail_area must be positive or zero")
    if frontsail_area < 0.:
        raise ValueError("frontsail_area must be positive or zero")
    if not (0 <= flat <= 1. or flat > 1.):
        raise ValueError("wrong flat value")
    if not (0 <= fractionality <= 1.):
        raise ValueError("wrong fractionality value")
    if overlap < 0.:
        raise ValueError("overlap must be positive or zero")
    if roach < -1.:
        raise ValueError("roach must be greater than -1 or -1")
    if rho_air <= 0.:
        raise ValueError("rho_air must be strictly positive")

    # warnings
    if flat < 0.6:
        warnings.warn('flat realistic values are between 0.6 and 1.0')
    if fractionality < 0.6:
        warnings.warn('fractionality realistic values are between 0.6 and 1.0')
    if overlap < 0.7 or overlap > 2.0:
        warnings.warn('overlap realistic values are between 0.7 and 2.0')
    if roach < -0.2 or roach > 2.0:
        warnings.warn('roach realistic values are between -0.2 and 2.0')

    mainsail_c_lift, mainsail_c_drag = ImsAeroModelCoefficients.coefficient_interp(mainsail_type)
    frontsail_c_lift, frontsail_c_drag = ImsAeroModelCoefficients.coefficient_interp(frontsail_type)

    twa_sign = twa / abs(twa) if twa != 0. else 0.

    # phi_up = phi_up(heel_angle)

    awa_phi_up = apparent_wind_angle(tws, abs(twa), boatspeed, phi_up(heel_angle))
    # aws_phi_up = apparent_wind_speed(tws, abs(twa), boatspeed, phi_up(heel_angle))
    awa = apparent_wind_angle(tws, abs(twa), boatspeed, heel_angle)
    aws = apparent_wind_speed(tws, abs(twa), boatspeed, heel_angle)

    reference_area = mainsail_area + frontsail_area

    # Global Cl max
    cl_max = (mainsail_c_lift(awa_phi_up) * (mainsail_area / reference_area)
              + frontsail_c_lift(awa_phi_up) * (frontsail_area / reference_area))

    # Global Cd
    cdp = (mainsail_c_drag(awa_phi_up) * (mainsail_area / reference_area)
           + frontsail_c_drag(awa_phi_up) * (frontsail_area / reference_area))

    # Centre of effort coordinates
    x_coe_main = mainsail_coe[0]
    x_coe_front = frontsail_coe[0]

    z_coe_main = mainsail_coe[2]
    z_coe_front = frontsail_coe[2]

    # TODO: shift of x position with awa (cf. marchaj.)
    # base it on z_max and sail areas to get an idea of chord length
    if (cl_max ** 2 + cdp ** 2) == 0:
        x_coe = x_coe_main * (mainsail_area / reference_area) + x_coe_front * (frontsail_area / reference_area)
        z_coe = z_coe_main * (mainsail_area / reference_area) + z_coe_front * (frontsail_area / reference_area)
    else:
        x_coe = x_coe_main \
                * (mainsail_area / reference_area) \
                * (sqrt((mainsail_c_lift(awa_phi_up)) ** 2 +
                        (mainsail_c_drag(awa_phi_up)) ** 2) /
                   sqrt(cl_max ** 2 + cdp ** 2)) \
                + \
                x_coe_front \
                * (frontsail_area / reference_area) \
                * (sqrt((frontsail_c_lift(awa_phi_up)) ** 2 +
                        (frontsail_c_drag(awa_phi_up)) ** 2) /
                   sqrt(cl_max ** 2 + cdp ** 2))

        z_coe = z_coe_main * (mainsail_area / reference_area) \
            * (sqrt((mainsail_c_lift(awa_phi_up)) ** 2 +
                    (mainsail_c_drag(awa_phi_up)) ** 2) /
                sqrt(cl_max ** 2 + cdp ** 2)) + \
            z_coe_front * (frontsail_area / reference_area) \
            * (sqrt((frontsail_c_lift(awa_phi_up)) ** 2 +
                    (frontsail_c_drag(awa_phi_up)) ** 2) /
               sqrt(cl_max ** 2 + cdp ** 2))

    z_coe_twist = z_coe * twist(flat, fractionality)

    # Quadratic parasite drag
    # <TO BE COMPLETED> - KPP page 47 ORC VPP 2013 ????
    kpp = 0.

    # Effective rig height
    eff_span_corr = effective_span_correction(roach, fractionality, overlap)

    # THIS IS AN APPROXIMATION -> see eqn. [39] of ORC VPP 2013
    cheff = eff_span_corr

    heff = rig_z_max * cheff

    # GF : changed heff to heff**2
    c_e = kpp + (reference_area / (pi * heff ** 2))
    # 1 / pi*AR -> AR = heff**2/Area

    c_drag_sails = cdp + c_e * cl_max ** 2 * flat ** 2
    c_lift = cl_max * flat

    c_r = c_lift * sin(radians(awa)) - c_drag_sails * cos(radians(awa))
    c_h = c_lift * cos(radians(awa)) + c_drag_sails * sin(radians(awa))

    # Forces in boat coordinates
    driving_force = 0.5 * c_r * rho_air * reference_area * aws ** 2
    heeling_force = 0.5 * c_h * rho_air * reference_area * aws ** 2

    # force = Force([driving_force*(1 + flat * 0.0001)
    #  workaround to avoid having flat 0.6 as best downwind sails trim
    return Force(driving_force,
                 twa_sign * heeling_force * cos(radians(heel_angle)),
                 - heeling_force * sin(radians(heel_angle)),
                 x_coe - z_coe_twist * sin(radians(trim_angle)),
                 twa_sign * z_coe_twist * sin(radians(heel_angle)),
                 z_coe_twist * cos(radians(heel_angle)))  # TODO: X position


def effective_span_correction(roach: float, fractionality: float, overlap: float) -> float:
    """ORC 2013 eqn. [38]"""
    return 1.1 + 0.08 * (roach - 0.2) + 0.5 * (0.68 + +0.31 * fractionality + 0.075 * overlap - 1.10)


def phi_up(phi: float) -> float:
    """Correction for the heel_angle used to interpolate the coefficient curves.
    Defined on p49 (eqn. [43]) of ORC VPP documentation 2013

    In the VPP as the yacht heels the apparent wind angle seen 
    by the sails reduces, but on the water the crew have traveler and jib 
    lead controls that permit adjustment of angle of attack. 
    To reflect this the PHI_UP function modifies the heel angle 
    that is used in the calculation of the 
    apparent wind angle at which the collective curves of lift and drag 
    coefficient are evaluated. 
    """
    return 10 * (phi / 30.) ** 2


def twist(flat: float, fractionality: float) -> float:
    """Corrector for COE height defined on p50 (eqn. [44]) of ORC VPP documentation 2013"""
    return 1. - 0.203 * (1. - flat) - 0.451 * (1. - flat) * (1. - fractionality)
