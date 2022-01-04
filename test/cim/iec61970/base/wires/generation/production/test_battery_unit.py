#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import integers, sampled_from, data

from test.cim.test_common_two_way_connections import check_power_electronics_unit_two_way_link_test, set_up_power_electronics_unit_two_way_link_test
from test.cim.common_testing_functions import verify
from test.cim.iec61970.base.wires.generation.production.test_power_electronics_unit import power_electronics_unit_kwargs, \
    verify_power_electronics_unit_constructor_default, verify_power_electronics_unit_constructor_kwargs, verify_power_electronics_unit_constructor_args, \
    power_electronics_unit_args
from test.cim.cim_creators import MAX_32_BIT_INTEGER
from zepben.evolve import BatteryUnit, BatteryStateKind
from zepben.evolve.model.cim.iec61970.base.wires.create_wires_components import create_battery_unit

battery_unit_kwargs = {
    **power_electronics_unit_kwargs,
    "battery_state": sampled_from(BatteryStateKind),
    "rated_e": integers(min_value=0, max_value=MAX_32_BIT_INTEGER),
    "stored_e": integers(min_value=0, max_value=MAX_32_BIT_INTEGER),
}

battery_unit_args = [*power_electronics_unit_args, BatteryStateKind.full, 1, 2]


def test_battery_unit_constructor_default():
    bu = BatteryUnit()
    bu2 = create_battery_unit()
    verify_default_battery_unit_constructor(bu)
    verify_default_battery_unit_constructor(bu2)


def verify_default_battery_unit_constructor(bu):
    verify_power_electronics_unit_constructor_default(bu)
    assert bu.battery_state == BatteryStateKind.UNKNOWN
    assert bu.rated_e is None
    assert bu.stored_e is None


# noinspection PyShadowingNames
@given(data())
def test_battery_unit_constructor_kwargs(data):
    verify(
        [BatteryUnit, create_battery_unit],
        data, battery_unit_kwargs, verify_battery_unit_values
    )


def verify_battery_unit_values(bu, battery_state, rated_e, stored_e, **kwargs):
    verify_power_electronics_unit_constructor_kwargs(bu, **kwargs)
    assert bu.battery_state == battery_state
    assert bu.rated_e == rated_e
    assert bu.stored_e == stored_e


def test_battery_unit_constructor_args():
    bu = BatteryUnit(*battery_unit_args)

    verify_power_electronics_unit_constructor_args(bu)
    assert bu.battery_state == battery_unit_args[-3]
    assert bu.rated_e == battery_unit_args[-2]
    assert bu.stored_e == battery_unit_args[-1]


def test_auto_two_way_connections_for_battery_unit_constructor():
    up, ec, opr, f, pec = set_up_power_electronics_unit_two_way_link_test()
    bu = create_battery_unit(usage_points=[up], equipment_containers=[ec], operational_restrictions=[opr], current_feeders=[f],
                             power_electronics_connection=pec)
    check_power_electronics_unit_two_way_link_test(bu, up, ec, opr, f, pec)
