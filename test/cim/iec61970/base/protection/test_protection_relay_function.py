#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis.strategies import floats, sampled_from, booleans, lists, builds, text

from cim.cim_creators import FLOAT_MIN, FLOAT_MAX, ALPHANUM, TEXT_MAX_SIZE, boolean_or_none
from cim.iec61970.base.core.test_power_system_resource import power_system_resource_kwargs, verify_power_system_resource_constructor_default, \
    verify_power_system_resource_constructor_kwargs, verify_power_system_resource_constructor_args, power_system_resource_args
from cim.private_collection_validator import validate_unordered, validate_ordered_other
from cim.property_validator import validate_property_accessor
from util import mrid_strategy
from zepben.ewb import ProtectionKind, PowerDirectionKind, ProtectedSwitch, ProtectionRelayFunction, RelayInfo, ProtectionRelayScheme, RelaySetting, Sensor, \
    UnitSymbol, unit_symbol_from_id, generate_id

protection_relay_function_kwargs = {
    **power_system_resource_kwargs,
    "model": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
    "reclosing": boolean_or_none(),
    "relay_delay_time": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "protection_kind": sampled_from(ProtectionKind),
    "directable": booleans(),
    "power_direction": sampled_from(PowerDirectionKind),
    "sensors": lists(builds(Sensor, mrid=mrid_strategy), max_size=2),
    "protected_switches": lists(builds(ProtectedSwitch, mrid=mrid_strategy), max_size=2),
    "schemes": lists(builds(ProtectionRelayScheme, mrid=mrid_strategy), max_size=2),
    "time_limits": lists(floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX), min_size=4, max_size=4),
    "thresholds": lists(builds(RelaySetting, unit_symbol=sampled_from(UnitSymbol), value=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
                               name=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE)), min_size=4, max_size=4),
}

protection_relay_function_args = [
    *power_system_resource_args,
    "model_string",
    False,
    1.1,
    ProtectionKind.JG,
    True,
    PowerDirectionKind.FORWARD,
    [Sensor(mrid=generate_id())],
    [ProtectedSwitch(mrid=generate_id())],
    [ProtectionRelayScheme(mrid=generate_id())],
    [2.2, 3.3],
    [RelaySetting(unit_symbol=UnitSymbol.METRES, value=1.1, name="rs1"), RelaySetting(unit_symbol=UnitSymbol.GYPERS, value=2.2, name="rs2")]
]


def verify_protection_relay_function_constructor_default(prf: ProtectionRelayFunction):
    verify_power_system_resource_constructor_default(prf)
    assert prf.model is None
    assert prf.reclosing is None
    assert prf.relay_delay_time is None
    assert prf.protection_kind is ProtectionKind.UNKNOWN
    assert prf.directable is None
    assert prf.power_direction == PowerDirectionKind.UNKNOWN
    assert len(list(prf.sensors)) == 0
    assert len(list(prf.protected_switches)) == 0
    assert len(list(prf.time_limits)) == 0
    assert len(list(prf.thresholds)) == 0


def verify_protection_relay_function_constructor_kwargs(
    prf: ProtectionRelayFunction,
    model,
    reclosing,
    relay_delay_time,
    protection_kind,
    directable,
    power_direction,
    sensors,
    protected_switches,
    schemes,
    time_limits,
    thresholds,
    **kwargs
):
    verify_power_system_resource_constructor_kwargs(prf, **kwargs)
    assert prf.model == model
    assert prf.reclosing == reclosing
    assert prf.relay_delay_time == relay_delay_time
    assert prf.protection_kind == protection_kind
    assert prf.directable == directable
    assert prf.power_direction == power_direction
    assert list(prf.sensors) == sensors
    assert list(prf.protected_switches) == protected_switches
    assert list(prf.schemes) == schemes
    assert list(prf.time_limits) == time_limits
    assert list(prf.thresholds) == thresholds


def verify_protection_relay_function_constructor_args(prf: ProtectionRelayFunction):
    verify_power_system_resource_constructor_args(prf)
    assert protection_relay_function_args[-11:] == [
        prf.model,
        prf.reclosing,
        prf.relay_delay_time,
        prf.protection_kind,
        prf.directable,
        prf.power_direction,
        list(prf.sensors),
        list(prf.protected_switches),
        list(prf.schemes),
        list(prf.time_limits),
        list(prf.thresholds)
    ]


def test_sensors_collection():
    validate_unordered(
        ProtectionRelayFunction,
        lambda mrid: Sensor(mrid),
        ProtectionRelayFunction.sensors,
        ProtectionRelayFunction.num_sensors,
        ProtectionRelayFunction.get_sensor,
        ProtectionRelayFunction.add_sensor,
        ProtectionRelayFunction.remove_sensor,
        ProtectionRelayFunction.clear_sensors
    )


def test_protected_switches_collection():
    validate_unordered(
        ProtectionRelayFunction,
        lambda mrid: ProtectedSwitch(mrid),
        ProtectionRelayFunction.protected_switches,
        ProtectionRelayFunction.num_protected_switches,
        ProtectionRelayFunction.get_protected_switch,
        ProtectionRelayFunction.add_protected_switch,
        ProtectionRelayFunction.remove_protected_switch,
        ProtectionRelayFunction.clear_protected_switches
    )


def test_scheme_collection():
    validate_unordered(
        ProtectionRelayFunction,
        lambda mrid: ProtectionRelayScheme(mrid),
        ProtectionRelayFunction.schemes,
        ProtectionRelayFunction.num_schemes,
        ProtectionRelayFunction.get_scheme,
        ProtectionRelayFunction.add_scheme,
        ProtectionRelayFunction.remove_scheme,
        ProtectionRelayFunction.clear_schemes
    )


def test_time_limits_collection():
    validate_ordered_other(
        ProtectionRelayFunction,
        lambda i: float(i),
        ProtectionRelayFunction.time_limits,
        ProtectionRelayFunction.num_time_limits,
        ProtectionRelayFunction.get_time_limit,
        ProtectionRelayFunction.for_each_time_limit,
        ProtectionRelayFunction.add_time_limit,
        ProtectionRelayFunction.add_time_limit,
        ProtectionRelayFunction.remove_time_limit,
        ProtectionRelayFunction.remove_time_limit_at,
        ProtectionRelayFunction.clear_time_limits
    )


def test_thresholds_collection():
    validate_ordered_other(
        ProtectionRelayFunction,
        lambda i: RelaySetting(unit_symbol_from_id(i), int(i), str(i)),
        ProtectionRelayFunction.thresholds,
        ProtectionRelayFunction.num_thresholds,
        ProtectionRelayFunction.get_threshold,
        ProtectionRelayFunction.for_each_threshold,
        ProtectionRelayFunction.add_threshold,
        ProtectionRelayFunction.add_threshold,
        ProtectionRelayFunction.remove_threshold,
        ProtectionRelayFunction.remove_threshold_at,
        ProtectionRelayFunction.clear_thresholds
    )


def test_relay_info_accessor():
    validate_property_accessor(ProtectionRelayFunction, RelayInfo, ProtectionRelayFunction.relay_info)
