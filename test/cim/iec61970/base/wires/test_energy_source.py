#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import builds, lists, floats, booleans

from cim.collection_validator import validate_collection_unordered
from cim.iec61970.base.wires.test_energy_connection import verify_energy_connection_constructor_default, \
    verify_energy_connection_constructor_kwargs, verify_energy_connection_constructor_args, energy_connection_kwargs, energy_connection_args
from cim.cim_creators import FLOAT_MIN, FLOAT_MAX
from zepben.evolve import EnergySource, EnergySourcePhase

energy_source_kwargs = {
    **energy_connection_kwargs,
    "energy_source_phases": lists(builds(EnergySourcePhase)),
    "active_power": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "reactive_power": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "voltage_angle": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "voltage_magnitude": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "p_max": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "p_min": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "r": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "r0": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "rn": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "x": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "x0": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "xn": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "is_external_grid": booleans(),
    "r_min": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "rn_min": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "r0_min": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "x_min": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "xn_min": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "x0_min": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "r_max": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "rn_max": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "r0_max": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "x_max": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "xn_max": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "x0_max": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)
}

energy_source_args = [*energy_connection_args, [EnergySourcePhase()], 1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9, 10.01, 11.11, 12.21, True,
                      13.31, 14.41, 15.51, 16.61, 17.71, 18.81, 19.91, 20.02, 21.12, 22.22, 23.32, 24.42]


def test_energy_source_constructor_default():
    es = EnergySource()

    verify_energy_connection_constructor_default(es)
    assert not list(es.phases)
    assert es.active_power is None
    assert es.reactive_power is None
    assert es.voltage_angle is None
    assert es.voltage_magnitude is None
    assert es.p_max is None
    assert es.p_min is None
    assert es.r is None
    assert es.r0 is None
    assert es.rn is None
    assert es.x is None
    assert es.x0 is None
    assert es.xn is None
    assert es.is_external_grid is False
    assert es.r_min is None
    assert es.rn_min is None
    assert es.r0_min is None
    assert es.x_min is None
    assert es.xn_min is None
    assert es.x0_min is None
    assert es.r_max is None
    assert es.rn_max is None
    assert es.r0_max is None
    assert es.x_max is None
    assert es.xn_max is None
    assert es.x0_max is None


@given(**energy_source_kwargs)
def test_energy_source_constructor_kwargs(energy_source_phases, active_power, reactive_power, voltage_angle, voltage_magnitude, p_max, p_min,
                                          r, r0, rn, x, x0, xn, is_external_grid, r_min, rn_min, r0_min, x_min, xn_min, x0_min,
                                          r_max, rn_max, r0_max, x_max, xn_max, x0_max, **kwargs):
    es = EnergySource(energy_source_phases=energy_source_phases,
                      active_power=active_power,
                      reactive_power=reactive_power,
                      voltage_angle=voltage_angle,
                      voltage_magnitude=voltage_magnitude,
                      p_max=p_max,
                      p_min=p_min,
                      r=r,
                      r0=r0,
                      rn=rn,
                      x=x,
                      x0=x0,
                      xn=xn,
                      is_external_grid=is_external_grid,
                      r_min=r_min,
                      rn_min=rn_min,
                      r0_min=r0_min,
                      x_min=x_min,
                      xn_min=xn_min,
                      x0_min=x0_min,
                      r_max=r_max,
                      rn_max=rn_max,
                      r0_max=r0_max,
                      x_max=x_max,
                      xn_max=xn_max,
                      x0_max=x0_max,
                      **kwargs)

    verify_energy_connection_constructor_kwargs(es, **kwargs)
    assert list(es.phases) == energy_source_phases
    assert es.active_power == active_power
    assert es.reactive_power == reactive_power
    assert es.voltage_angle == voltage_angle
    assert es.voltage_magnitude == voltage_magnitude
    assert es.p_max == p_max
    assert es.p_min == p_min
    assert es.r == r
    assert es.r0 == r0
    assert es.rn == rn
    assert es.x == x
    assert es.x0 == x0
    assert es.xn == xn
    assert es.is_external_grid == is_external_grid
    assert es.r_min == r_min
    assert es.rn_min == rn_min
    assert es.r0_min == r0_min
    assert es.x_min == x_min
    assert es.xn_min == xn_min
    assert es.x0_min == x0_min
    assert es.r_max == r_max
    assert es.rn_max == rn_max
    assert es.r0_max == r0_max
    assert es.x_max == x_max
    assert es.xn_max == xn_max
    assert es.x0_max == x0_max


def test_energy_source_constructor_args():
    es = EnergySource(*energy_source_args)

    verify_energy_connection_constructor_args(es)
    assert list(es.phases) == energy_source_args[-26]
    assert es.active_power == energy_source_args[-25]
    assert es.reactive_power == energy_source_args[-24]
    assert es.voltage_angle == energy_source_args[-23]
    assert es.voltage_magnitude == energy_source_args[-22]
    assert es.p_max == energy_source_args[-21]
    assert es.p_min == energy_source_args[-20]
    assert es.r == energy_source_args[-19]
    assert es.r0 == energy_source_args[-18]
    assert es.rn == energy_source_args[-17]
    assert es.x == energy_source_args[-16]
    assert es.x0 == energy_source_args[-15]
    assert es.xn == energy_source_args[-14]
    assert es.is_external_grid == energy_source_args[-13]
    assert es.r_min == energy_source_args[-12]
    assert es.rn_min == energy_source_args[-11]
    assert es.r0_min == energy_source_args[-10]
    assert es.x_min == energy_source_args[-9]
    assert es.xn_min == energy_source_args[-8]
    assert es.x0_min == energy_source_args[-7]
    assert es.r_max == energy_source_args[-6]
    assert es.rn_max == energy_source_args[-5]
    assert es.r0_max == energy_source_args[-4]
    assert es.x_max == energy_source_args[-3]
    assert es.xn_max == energy_source_args[-2]
    assert es.x0_max == energy_source_args[-1]


def test_phases_collection():
    validate_collection_unordered(EnergySource,
                                  lambda mrid, _: EnergySourcePhase(mrid),
                                  EnergySource.num_phases,
                                  EnergySource.get_phase,
                                  EnergySource.phases,
                                  EnergySource.add_phase,
                                  EnergySource.remove_phase,
                                  EnergySource.clear_phases)
