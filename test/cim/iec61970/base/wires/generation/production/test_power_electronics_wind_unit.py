#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given

from test.cim.test_common_two_way_connections import set_up_power_electronics_unit_two_way_link_test, check_power_electronics_unit_two_way_link_test
from test.cim.iec61970.base.wires.generation.production.test_power_electronics_unit import power_electronics_unit_kwargs, \
    verify_power_electronics_unit_constructor_default, verify_power_electronics_unit_constructor_kwargs, verify_power_electronics_unit_constructor_args, \
    power_electronics_unit_args
from zepben.evolve import PowerElectronicsWindUnit
from zepben.evolve.model.cim.iec61970.base.wires.create_wires_components import create_power_electronics_wind_unit

power_electronics_wind_unit_kwargs = power_electronics_unit_kwargs
power_electronics_wind_unit_args = power_electronics_unit_args


def test_power_electronics_wind_unit_constructor_default():
    verify_power_electronics_unit_constructor_default(PowerElectronicsWindUnit())
    verify_power_electronics_unit_constructor_default(create_power_electronics_wind_unit())


@given(**power_electronics_wind_unit_kwargs)
def test_power_electronics_wind_unit_constructor_kwargs(**kwargs):
    verify_power_electronics_unit_constructor_kwargs(PowerElectronicsWindUnit(**kwargs), **kwargs)


@given(**power_electronics_wind_unit_kwargs)
def test_power_electronics_wind_unit_creator(**kwargs):
    verify_power_electronics_unit_constructor_kwargs(create_power_electronics_wind_unit(**kwargs), **kwargs)


def test_power_electronics_wind_unit_constructor_args():
    verify_power_electronics_unit_constructor_args(PowerElectronicsWindUnit(*power_electronics_wind_unit_args))


# noinspection SpellCheckingInspection
def test_auto_two_way_connections_for_power_electronics_wind_unit_constructor():
    up, ec, opr, f, pec = set_up_power_electronics_unit_two_way_link_test()
    pewu = create_power_electronics_wind_unit(usage_points=[up], equipment_containers=[ec], operational_restrictions=[opr], current_feeders=[f],
                                              power_electronics_connection=pec)
    check_power_electronics_unit_two_way_link_test(pewu, up, ec, opr, f, pec)
