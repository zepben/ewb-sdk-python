#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import builds, lists, floats

from test.cim.collection_validator import validate_collection_unordered
from test.cim.iec61970.base.wires.test_energy_connection import verify_energy_connection_constructor_default, \
    verify_energy_connection_constructor_kwargs, verify_energy_connection_constructor_args, energy_connection_kwargs, energy_connection_args
from test.cim_creators import FLOAT_MIN, FLOAT_MAX
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
    "xn": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)
}

energy_source_args = [*energy_connection_args, [EnergySourcePhase()], 1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9, 10.01, 11.11, 12.21]


def test_energy_source_constructor_default():
    es = EnergySource()

    verify_energy_connection_constructor_default(es)
    assert not list(es.phases)
    assert es.active_power == 0.0
    assert es.reactive_power == 0.0
    assert es.voltage_angle == 0.0
    assert es.voltage_magnitude == 0.0
    assert es.p_max == 0.0
    assert es.p_min == 0.0
    assert es.r == 0.0
    assert es.r0 == 0.0
    assert es.rn == 0.0
    assert es.x == 0.0
    assert es.x0 == 0.0
    assert es.xn == 0.0


@given(**energy_source_kwargs)
def test_energy_source_constructor_kwargs(energy_source_phases, active_power, reactive_power, voltage_angle, voltage_magnitude, p_max, p_min,
                                          r, r0, rn, x, x0, xn, **kwargs):
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


def test_energy_source_constructor_args():
    es = EnergySource(*energy_source_args)

    verify_energy_connection_constructor_args(es)
    assert list(es.phases) == energy_source_args[-13]
    assert es.active_power == energy_source_args[-12]
    assert es.reactive_power == energy_source_args[-11]
    assert es.voltage_angle == energy_source_args[-10]
    assert es.voltage_magnitude == energy_source_args[-9]
    assert es.p_max == energy_source_args[-8]
    assert es.p_min == energy_source_args[-7]
    assert es.r == energy_source_args[-6]
    assert es.r0 == energy_source_args[-5]
    assert es.rn == energy_source_args[-4]
    assert es.x == energy_source_args[-3]
    assert es.x0 == energy_source_args[-2]
    assert es.xn == energy_source_args[-1]


def test_phases_collection():
    validate_collection_unordered(EnergySource,
                                  lambda mrid, _: EnergySourcePhase(mrid),
                                  EnergySource.num_phases,
                                  EnergySource.get_phase,
                                  EnergySource.phases,
                                  EnergySource.add_phase,
                                  EnergySource.remove_phase,
                                  EnergySource.clear_phases)
