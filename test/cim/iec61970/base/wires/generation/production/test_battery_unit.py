#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import integers, sampled_from

from cim.cim_creators import MAX_32_BIT_INTEGER
from cim.iec61970.base.wires.generation.production.test_power_electronics_unit import power_electronics_unit_kwargs, \
    verify_power_electronics_unit_constructor_default, verify_power_electronics_unit_constructor_kwargs, verify_power_electronics_unit_constructor_args, \
    power_electronics_unit_args
from cim.private_collection_validator import validate_unordered_1234567890
from zepben.evolve import BatteryUnit, BatteryStateKind
from zepben.evolve.model.cim.extensions.iec61970.base.wires.battery_control import BatteryControl

battery_unit_kwargs = {
    **power_electronics_unit_kwargs,
    "battery_state": sampled_from(BatteryStateKind),
    "rated_e": integers(min_value=0, max_value=MAX_32_BIT_INTEGER),
    "stored_e": integers(min_value=0, max_value=MAX_32_BIT_INTEGER),
}

battery_unit_args = [*power_electronics_unit_args, BatteryStateKind.full, 1, 2]


def test_battery_unit_constructor_default():
    b = BatteryUnit()

    verify_power_electronics_unit_constructor_default(b)
    assert b.battery_state == BatteryStateKind.UNKNOWN
    assert b.rated_e is None
    assert b.stored_e is None


@given(**battery_unit_kwargs)
def test_battery_unit_constructor_kwargs(battery_state, rated_e, stored_e, **kwargs):
    b = BatteryUnit(
        battery_state=battery_state,
        rated_e=rated_e,
        stored_e=stored_e,
        **kwargs
    )

    verify_power_electronics_unit_constructor_kwargs(b, **kwargs)
    assert b.battery_state == battery_state
    assert b.rated_e == rated_e
    assert b.stored_e == stored_e


def test_battery_unit_constructor_args():
    b = BatteryUnit(*battery_unit_args)

    verify_power_electronics_unit_constructor_args(b)
    assert battery_unit_args[-3:] == [
        b.battery_state,
        b.rated_e,
        b.stored_e
    ]


def test_battery_control_collection():
    validate_unordered_1234567890(
        BatteryUnit,
        lambda mrid: BatteryControl(mrid),
        BatteryUnit.battery_controls,
        BatteryUnit.num_battery_controls,
        BatteryUnit.get_battery_control,
        BatteryUnit.add_battery_control,
        BatteryUnit.remove_battery_control,
        BatteryUnit.clear_battery_controls
    )
