#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import integers, builds, lists, floats

from cim.collection_validator import validate_collection_unordered
from cim.iec61970.base.wires.test_regulating_cond_eq import verify_regulating_cond_eq_constructor_default, \
    verify_regulating_cond_eq_constructor_kwargs, verify_regulating_cond_eq_constructor_args, regulating_cond_eq_kwargs, regulating_cond_eq_args
from cim_creators import MIN_32_BIT_INTEGER, MAX_32_BIT_INTEGER, FLOAT_MIN, FLOAT_MAX
from zepben.evolve import PowerElectronicsUnit, PowerElectronicsConnectionPhase, BatteryUnit, PowerElectronicsConnection

power_electronics_connection_kwargs = {
    **regulating_cond_eq_kwargs,
    "max_i_fault": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    "p": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "q": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "max_q": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "min_q": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "rated_s": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    "rated_u": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    "power_electronics_units": lists(builds(BatteryUnit), max_size=2),
    "power_electronics_connection_phases": lists(builds(PowerElectronicsConnectionPhase), max_size=2)
}

power_electronics_connection_args = [*regulating_cond_eq_args, 1, 2.2, 3.3, 4.4, 5.5, 6, 7, [BatteryUnit(), BatteryUnit()],
                                     [PowerElectronicsConnectionPhase(), PowerElectronicsConnectionPhase()]]


def test_power_electronics_connection_constructor_default():
    pec = PowerElectronicsConnection()

    verify_regulating_cond_eq_constructor_default(pec)
    assert pec.max_i_fault == 0
    assert pec.p == 0.0
    assert pec.q == 0.0
    assert pec.max_q == 0.0
    assert pec.min_q == 0.0
    assert pec.rated_s == 0
    assert pec.rated_u == 0
    assert not list(pec.units)
    assert not list(pec.phases)


@given(**power_electronics_connection_kwargs)
def test_power_electronics_connection_constructor_kwargs(max_i_fault, p, q, max_q, min_q, rated_s, rated_u, power_electronics_units,
                                                         power_electronics_connection_phases, **kwargs):
    pec = PowerElectronicsConnection(max_i_fault=max_i_fault, p=p, q=q, max_q=max_q, min_q=min_q, rated_s=rated_s, rated_u=rated_u,
                                     power_electronics_units=power_electronics_units,
                                     power_electronics_connection_phases=power_electronics_connection_phases, **kwargs)

    verify_regulating_cond_eq_constructor_kwargs(pec, **kwargs)
    assert pec.max_i_fault == max_i_fault
    assert pec.p == p
    assert pec.q == q
    assert pec.max_q == max_q
    assert pec.min_q == min_q
    assert pec.rated_s == rated_s
    assert pec.rated_u == rated_u
    assert list(pec.units) == power_electronics_units
    assert list(pec.phases) == power_electronics_connection_phases


def test_power_electronics_connection_constructor_args():
    pec = PowerElectronicsConnection(*power_electronics_connection_args)

    verify_regulating_cond_eq_constructor_args(pec)
    assert pec.max_i_fault == power_electronics_connection_args[-9]
    assert pec.p == power_electronics_connection_args[-8]
    assert pec.q == power_electronics_connection_args[-7]
    assert pec.max_q == power_electronics_connection_args[-6]
    assert pec.min_q == power_electronics_connection_args[-5]
    assert pec.rated_s == power_electronics_connection_args[-4]
    assert pec.rated_u == power_electronics_connection_args[-3]
    assert list(pec.units) == power_electronics_connection_args[-2]
    assert list(pec.phases) == power_electronics_connection_args[-1]


def test_power_electronics_units_collection():
    validate_collection_unordered(PowerElectronicsConnection,
                                  lambda mrid, _: PowerElectronicsUnit(mrid),
                                  PowerElectronicsConnection.num_units,
                                  PowerElectronicsConnection.get_unit,
                                  PowerElectronicsConnection.units,
                                  PowerElectronicsConnection.add_unit,
                                  PowerElectronicsConnection.remove_unit,
                                  PowerElectronicsConnection.clear_units)


def test_power_electronics_connection_phases_collection():
    # noinspection PyArgumentList
    validate_collection_unordered(PowerElectronicsConnection,
                                  lambda mrid, _: PowerElectronicsConnectionPhase(mrid),
                                  PowerElectronicsConnection.num_phases,
                                  PowerElectronicsConnection.get_phase,
                                  PowerElectronicsConnection.phases,
                                  PowerElectronicsConnection.add_phase,
                                  PowerElectronicsConnection.remove_phase,
                                  PowerElectronicsConnection.clear_phases)
