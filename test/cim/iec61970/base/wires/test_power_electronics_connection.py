#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from collections import OrderedDict

from hypothesis import given, seed
from hypothesis.strategies import lists, integers, floats

from test.cim.collection_validator import validate_collection_unordered
from test.cim_creators import powerelectronicsconnection, powersystemresource, batteryunit, powerelectronicsconnectionphase, MAX_32_BIT_INTEGER, FLOAT_MAX, \
    FLOAT_MIN, regulatingcondeq
from zepben.evolve import PowerElectronicsConnection, BatteryUnit, PowerElectronicsConnectionPhase, SinglePhaseKind

from test.cim.constructor_validation import *

pec_kwargs = {**rce_kwargs, "power_electronics_units": lists(builds(BatteryUnit), max_size=2),
              "power_electronics_connection_phases": lists(builds(PowerElectronicsConnectionPhase), max_size=2),
              "max_i_fault": integers(min_value=0, max_value=MAX_32_BIT_INTEGER),
              "max_q": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
              "min_q": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
              "p": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
              "q": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
              "rated_s": integers(min_value=0, max_value=MAX_32_BIT_INTEGER),
              "rated_u": integers(min_value=0, max_value=MAX_32_BIT_INTEGER)}

pec_args = (*rce_args, 1, 2.0, 3.0, 4.0, 5.0, 6, 7, [BatteryUnit("test_bu")], [PowerElectronicsConnectionPhase("test_pecphase")])


@given(**pec_kwargs)
def test_pec_constructor_kwargs(max_i_fault, p, q, max_q, min_q, rated_s, rated_u, power_electronics_units, power_electronics_connection_phases, **kwargs):
    pec = PowerElectronicsConnection(max_i_fault=max_i_fault, p=p, q=q, max_q=max_q, min_q=min_q, rated_s=rated_s, rated_u=rated_u,
                                     power_electronics_units=power_electronics_units, power_electronics_connection_phases=power_electronics_connection_phases)
    assert pec.max_i_fault == max_i_fault
    assert pec.p == p
    assert pec.q == q
    assert pec.max_q == max_q
    assert pec.min_q == min_q
    assert pec.rated_s == rated_s
    assert pec.rated_u == rated_u
    assert [u for u in pec.units] == power_electronics_units
    assert [p for p in pec.phases] == power_electronics_connection_phases

    verify_regulating_cond_eq_constructor(clazz=PowerElectronicsConnection, **kwargs)


def test_pec_constructor_args():
    pec = PowerElectronicsConnection(*pec_args)
    assert pec.max_i_fault == 1
    assert pec.p == 2.0
    assert pec.q == 3.0
    assert pec.max_q == 4.0
    assert pec.min_q == 5.0
    assert pec.rated_s == 6
    assert pec.rated_u == 7
    assert pec._power_electronics_units == pec_args[-2]
    assert pec._power_electronics_connection_phases == pec_args[-1]
    verify_rce_args(pec)


def test_power_electronics_units_collection():
    validate_collection_unordered(PowerElectronicsConnection,
                                  lambda mrid, _: PowerElectronicsUnit(mrid),
                                  PowerElectronicsConnection.num_units,
                                  PowerElectronicsConnection.get_unit,
                                  lambda it: PowerElectronicsConnection.units.fget(it),
                                  PowerElectronicsConnection.add_unit,
                                  PowerElectronicsConnection.remove_unit,
                                  PowerElectronicsConnection.clear_units)


def test_power_electronics_connection_phases_collection():
    validate_collection_unordered(PowerElectronicsConnection,
                                  lambda mrid, _: PowerElectronicsConnectionPhase(mrid),
                                  PowerElectronicsConnection.num_phases,
                                  PowerElectronicsConnection.get_phase,
                                  lambda it: PowerElectronicsConnection.phases.fget(it),
                                  PowerElectronicsConnection.add_phase,
                                  PowerElectronicsConnection.remove_phase,
                                  PowerElectronicsConnection.clear_phases)
