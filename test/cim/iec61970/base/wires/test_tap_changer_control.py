#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import integers, floats

from cim.cim_creators import MIN_32_BIT_INTEGER, MAX_32_BIT_INTEGER, FLOAT_MIN, FLOAT_MAX, boolean_or_none
from cim.iec61970.base.wires.test_regulating_control import regulating_control_kwargs, regulating_control_args, verify_regulating_control_constructor_default, \
    verify_regulating_control_constructor_kwargs, verify_regulating_control_constructor_args
from zepben.evolve import TapChangerControl

tap_changer_control_kwargs = {
    **regulating_control_kwargs,
    "limit_voltage": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    "line_drop_compensation": boolean_or_none(),
    "line_drop_r": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "line_drop_x": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "reverse_line_drop_r": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "reverse_line_drop_x": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "forward_ldc_blocking": boolean_or_none(),
    "time_delay": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "co_generation_enabled": boolean_or_none()
}

tap_changer_control_args = [*regulating_control_args, 1, False, 2.2, 3.3, 4.4, 5.5, True, 6.6, False]


def test_tap_changer_control_constructor_default():
    tcc = TapChangerControl()

    verify_regulating_control_constructor_default(tcc)

    assert tcc.limit_voltage is None
    assert tcc.line_drop_compensation is None
    assert tcc.line_drop_r is None
    assert tcc.line_drop_x is None
    assert tcc.reverse_line_drop_r is None
    assert tcc.reverse_line_drop_x is None
    assert tcc.forward_ldc_blocking is None
    assert tcc.time_delay is None
    assert tcc.co_generation_enabled is None


@given(**tap_changer_control_kwargs)
def test_tap_changer_control_constructor_kwargs(
    limit_voltage,
    line_drop_compensation,
    line_drop_r,
    line_drop_x,
    reverse_line_drop_r,
    reverse_line_drop_x,
    forward_ldc_blocking,
    time_delay,
    co_generation_enabled,
    **kwargs):

    tcc = TapChangerControl(
        limit_voltage=limit_voltage,
        line_drop_compensation=line_drop_compensation,
        line_drop_r=line_drop_r,
        line_drop_x=line_drop_x,
        reverse_line_drop_r=reverse_line_drop_r,
        reverse_line_drop_x=reverse_line_drop_x,
        forward_ldc_blocking=forward_ldc_blocking,
        time_delay=time_delay,
        co_generation_enabled=co_generation_enabled,
        **kwargs
    )

    verify_regulating_control_constructor_kwargs(tcc, **kwargs)
    assert tcc.limit_voltage == limit_voltage
    assert tcc.line_drop_compensation == line_drop_compensation
    assert tcc.line_drop_r == line_drop_r
    assert tcc.line_drop_x == line_drop_x
    assert tcc.reverse_line_drop_r == reverse_line_drop_r
    assert tcc.reverse_line_drop_x == reverse_line_drop_x
    assert tcc.forward_ldc_blocking == forward_ldc_blocking
    assert tcc.time_delay == time_delay
    assert tcc.co_generation_enabled == co_generation_enabled

def test_tap_changer_control_constructor_args():
    tcc = TapChangerControl(*tap_changer_control_args)

    verify_regulating_control_constructor_args(tcc)
    assert tcc.limit_voltage == tap_changer_control_args[-9]
    assert tcc.line_drop_compensation == tap_changer_control_args[-8]
    assert tcc.line_drop_r == tap_changer_control_args[-7]
    assert tcc.line_drop_x == tap_changer_control_args[-6]
    assert tcc.reverse_line_drop_r == tap_changer_control_args[-5]
    assert tcc.reverse_line_drop_x == tap_changer_control_args[-4]
    assert tcc.forward_ldc_blocking == tap_changer_control_args[-3]
    assert tcc.time_delay == tap_changer_control_args[-2]
    assert tcc.co_generation_enabled == tap_changer_control_args[-1]
