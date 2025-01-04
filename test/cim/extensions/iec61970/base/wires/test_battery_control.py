#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import floats, sampled_from

from cim.cim_creators import FLOAT_MIN, FLOAT_MAX
from cim.iec61970.base.wires.test_regulating_control import regulating_control_kwargs, regulating_control_args, verify_regulating_control_constructor_default, \
    verify_regulating_control_constructor_kwargs, verify_regulating_control_constructor_args
from zepben.evolve import BatteryControl, BatteryControlMode

battery_control_kwargs = {
    **regulating_control_kwargs,
    "charging_rate": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "discharging_rate": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "reserve_percent": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "control_mode": sampled_from(BatteryControlMode),
}

battery_control_args = [*regulating_control_args, 1.1, 2.2, 3.3, BatteryControlMode.time]


def test_battery_control_constructor_default():
    bc = BatteryControl()

    verify_regulating_control_constructor_default(bc)

    assert bc.charging_rate is None
    assert bc.discharging_rate is None
    assert bc.reserve_percent is None
    assert bc.control_mode is BatteryControlMode.UNKNOWN


@given(**battery_control_kwargs)
def test_battery_control_constructor_kwargs(charging_rate, discharging_rate, reserve_percent, control_mode, **kwargs):
    bc = BatteryControl(
        charging_rate=charging_rate,
        discharging_rate=discharging_rate,
        reserve_percent=reserve_percent,
        control_mode=control_mode,
        **kwargs
    )

    verify_regulating_control_constructor_kwargs(bc, **kwargs)
    assert bc.charging_rate == charging_rate
    assert bc.discharging_rate == discharging_rate
    assert bc.reserve_percent == reserve_percent
    assert bc.control_mode == control_mode


def test_battery_control_constructor_args():
    bc = BatteryControl(*battery_control_args)

    verify_regulating_control_constructor_args(bc)
    assert battery_control_args[-4:] == [
        bc.charging_rate,
        bc.discharging_rate,
        bc.reserve_percent,
        bc.control_mode
    ]
