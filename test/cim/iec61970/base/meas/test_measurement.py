#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from hypothesis.strategies import text, builds, sampled_from

from cim.iec61970.base.core.test_identified_object import identified_object_kwargs, verify_identified_object_constructor_default, \
    verify_identified_object_constructor_kwargs, verify_identified_object_constructor_args, identified_object_args
from cim.cim_creators import ALPHANUM, TEXT_MAX_SIZE
from zepben.evolve import Measurement, RemoteSource, PhaseCode, UnitSymbol

measurement_kwargs = {
    **identified_object_kwargs,
    "power_system_resource_mrid": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
    "remote_source": builds(RemoteSource),
    "terminal_mrid": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
    "phases": sampled_from(PhaseCode),
    "unit_symbol": sampled_from(UnitSymbol)
}

measurement_args = [*identified_object_args, "a", RemoteSource(), "b", PhaseCode.XYN, UnitSymbol.A]


def verify_measurement_constructor_default(m: Measurement):
    verify_identified_object_constructor_default(m)
    assert not m.power_system_resource_mrid
    assert not m.remote_source
    assert not m.terminal_mrid
    assert m.phases == PhaseCode.ABC
    assert m.unit_symbol == UnitSymbol.NONE


def verify_measurement_constructor_kwargs(m: Measurement, power_system_resource_mrid, remote_source, terminal_mrid, phases, unit_symbol, **kwargs):
    verify_identified_object_constructor_kwargs(m, **kwargs)
    assert m.power_system_resource_mrid == power_system_resource_mrid
    assert m.remote_source == remote_source
    assert m.terminal_mrid == terminal_mrid
    assert m.phases == phases
    assert m.unit_symbol == unit_symbol


def verify_measurement_constructor_args(m: Measurement):
    verify_identified_object_constructor_args(m)
    assert m.power_system_resource_mrid == measurement_args[-5]
    assert m.remote_source == measurement_args[-4]
    assert m.terminal_mrid == measurement_args[-3]
    assert m.phases == measurement_args[-2]
    assert m.unit_symbol == measurement_args[-1]
