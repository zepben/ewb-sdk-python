#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import integers, sampled_from

from test.cim.constructor_validation import peu_kwargs, verify_peu_args, verify_power_electronics_unit_constructor, peu_args
from test.cim_creators import MAX_32_BIT_INTEGER, MIN_32_BIT_INTEGER
from zepben.evolve import PowerElectronicsUnit, BatteryUnit, BatteryStateKind, PhotoVoltaicUnit, PowerElectronicsWindUnit

battery_kwargs = {**peu_kwargs, "battery_state": sampled_from(BatteryStateKind),
                  "rated_e": integers(min_value=0, max_value=MAX_32_BIT_INTEGER),
                  "stored_e": integers(min_value=0, max_value=MAX_32_BIT_INTEGER),
                  }

battery_args = (*peu_args, BatteryStateKind.charging, 1000, 2000)

pv_kwargs = peu_kwargs

pv_args = peu_args

pewu_kwargs = peu_kwargs

pewu_args = peu_args


@given(**peu_kwargs)
def test_power_electronics_unit_constructor_kwargs(power_electronics_connection, max_p, min_p, **kwargs):
    verify_power_electronics_unit_constructor(PowerElectronicsUnit, power_electronics_connection, max_p, min_p, **kwargs)


def test_power_electronics_unit_constructor_args():
    verify_peu_args(PowerElectronicsUnit(*peu_args))


@given(**battery_kwargs)
def test_battery_unit_constructor_kwargs(battery_state, rated_e, stored_e, **kwargs):
    battery = BatteryUnit(battery_state=battery_state, rated_e=rated_e, stored_e=stored_e)
    assert battery.battery_state == battery_state
    assert battery.rated_e == rated_e
    assert battery.stored_e == stored_e
    verify_power_electronics_unit_constructor(BatteryUnit, **kwargs)


def test_battery_unit_constructor_args():
    bu = BatteryUnit(*battery_args)
    assert bu.battery_state == BatteryStateKind.charging
    assert bu.rated_e == 1000
    assert bu.stored_e == 2000
    verify_peu_args(bu)


@given(**pewu_kwargs)
def test_power_electronics_wind_unit_constructor_kwargs(**kwargs):
    verify_power_electronics_unit_constructor(PowerElectronicsWindUnit, **kwargs)


def test_power_electronics_wind_unit_constructor_args():
    verify_peu_args(PowerElectronicsWindUnit(*pewu_args))


@given(**pv_kwargs)
def test_photo_voltaic_unit_constructor_kwargs(**kwargs):
    verify_power_electronics_unit_constructor(PhotoVoltaicUnit, **kwargs)


def test_photo_voltaic_unit_constructor_args():
    verify_peu_args(PhotoVoltaicUnit(*pv_args))
