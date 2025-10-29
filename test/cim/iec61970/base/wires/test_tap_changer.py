#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import re

from hypothesis import assume
from hypothesis.strategies import floats, booleans, integers, builds
from pytest import raises
from zepben.ewb import TapChangerControl
from zepben.ewb.model.cim.iec61970.base.wires.tap_changer import TapChanger

from cim.cim_creators import MIN_32_BIT_INTEGER, MAX_32_BIT_INTEGER
from cim.iec61970.base.core.test_power_system_resource import power_system_resource_kwargs, verify_power_system_resource_constructor_default, \
    verify_power_system_resource_constructor_kwargs, verify_power_system_resource_constructor_args, power_system_resource_args

tap_changer_kwargs = {
    **power_system_resource_kwargs,
    "control_enabled": booleans(),
    "neutral_u": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    "tap_changer_control": builds(TapChangerControl),
    "high_step": integers(min_value=100, max_value=MAX_32_BIT_INTEGER),
    "low_step": integers(min_value=MIN_32_BIT_INTEGER, max_value=-100),
    "neutral_step": integers(min_value=-100, max_value=100),
    "normal_step": integers(min_value=-100, max_value=100),
    "step": floats(min_value=-100.0, max_value=100.0)
}

tap_changer_args = [*power_system_resource_args, False, 1, TapChangerControl(), 10, 2, 3, 4, 5.5]


def verify_tap_changer_constructor_default(tc: TapChanger):
    verify_power_system_resource_constructor_default(tc)
    assert tc.control_enabled is None
    assert tc.neutral_u is None
    assert tc.high_step is None
    assert tc.low_step is None
    assert tc.neutral_step is None
    assert tc.normal_step is None
    assert tc.step is None
    assert tc.tap_changer_control is None


def assume_step_values(high_step, low_step, neutral_step, normal_step, step):
    assume(high_step > low_step)
    assume(high_step >= neutral_step >= low_step)
    assume(high_step >= normal_step >= low_step)
    assume(high_step >= step >= low_step)


def verify_tap_changer_constructor_kwargs(tc: TapChanger, control_enabled, neutral_u, high_step, low_step, neutral_step, normal_step, step, tap_changer_control,
                                          **kwargs):
    assume_step_values(high_step, low_step, neutral_step, normal_step, step)

    verify_power_system_resource_constructor_kwargs(tc, **kwargs)
    assert tc.control_enabled == control_enabled
    assert tc.neutral_u == neutral_u
    assert tc.high_step == high_step
    assert tc.low_step == low_step
    assert tc.neutral_step == neutral_step
    assert tc.normal_step == normal_step
    assert tc.step == step
    assert tc.tap_changer_control == tap_changer_control


def verify_tap_changer_constructor_args(tc: TapChanger):
    verify_power_system_resource_constructor_args(tc)
    assert tap_changer_args[-8:] == [
        tc.control_enabled,
        tc.neutral_u,
        tc.tap_changer_control,
        tc.high_step,
        tc.low_step,
        tc.neutral_step,
        tc.normal_step,
        tc.step
    ]


# noinspection PyArgumentList
from pytest import mark
@mark.skip(reason="Args are deprecated")
def test_detected_invalid_steps_via_constructor_args():
    # args order: control_enabled, neutral_u, _high_step, _low_step, _neutral_step, _normal_step, _step

    with raises(ValueError, match=re.escape("High step [0] must be greater than low step [0]")):
        TapChanger(*power_system_resource_args, True, 100, TapChangerControl(), 0, 0, 0, 0, 0.0)
    with raises(ValueError, match=re.escape("Neutral step [2] must be between high step [1] and low step [0]")):
        TapChanger(*power_system_resource_args, True, 100, TapChangerControl(), 1, 0, 2, 0, 0.0)
    with raises(ValueError, match=re.escape("Normal step [2] must be between high step [1] and low step [0]")):
        TapChanger(*power_system_resource_args, True, 100, TapChangerControl(), 1, 0, 0, 2, 0.0)
    with raises(ValueError, match=re.escape("Step [1.1] must be between high step [1] and low step [0]")):
        TapChanger(*power_system_resource_args, True, 100, TapChangerControl(), 1, 0, 0, 0, 1.1)


def test_validates_step_changes():
    tc = TapChanger(high_step=1, low_step=0, neutral_step=0, normal_step=0, step=0.0)
    with raises(ValueError, match=re.escape("High step [0] must be greater than low step [0]")):
        tc.high_step = 0
    with raises(ValueError, match=re.escape("Low step [2] must be less than high step [1]")):
        tc.low_step = 2
    with raises(ValueError, match=re.escape("Neutral step [2] must be between high step [1] and low step [0]")):
        tc.neutral_step = 2
    with raises(ValueError, match=re.escape("Normal step [2] must be between high step [1] and low step [0]")):
        tc.normal_step = 2
    with raises(ValueError, match=re.escape("Step [1.1] must be between high step [1] and low step [0]")):
        tc.step = 1.1

    tc.high_step = 10
    with raises(ValueError, match=re.escape("New value would invalidate current step of [0.0]")):
        tc.low_step = 2

    tc.step = 10.0
    with raises(ValueError, match=re.escape("New value would invalidate current normal_step of [0]")):
        tc.low_step = 2

    tc.normal_step = 10
    with raises(ValueError, match=re.escape("New value would invalidate current neutral_step of [0]")):
        tc.low_step = 2

    tc.neutral_step = 10
    with raises(ValueError, match=re.escape("New value would invalidate current step of [10.0]")):
        tc.high_step = 1

    tc.step = 0
    with raises(ValueError, match=re.escape("New value would invalidate current normal_step of [10]")):
        tc.high_step = 2

    tc.normal_step = 0
    with raises(ValueError, match=re.escape("New value would invalidate current neutral_step of [10]")):
        tc.high_step = 2
