#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from hypothesis import given
from hypothesis.strategies import builds, floats

from cim import extract_testing_args
from test.cim.iec61970.base.wires.test_tap_changer import verify_tap_changer_constructor_default, \
    verify_tap_changer_constructor_kwargs, verify_tap_changer_constructor_args, tap_changer_kwargs, tap_changer_args, assume_step_values
from test.cim.cim_creators import FLOAT_MIN, FLOAT_MAX
from zepben.evolve import RatioTapChanger, TransformerEnd
from zepben.evolve.model.cim.iec61970.base.wires.create_wires_components import create_ratio_tap_changer

ratio_tap_changer_kwargs = {
    **tap_changer_kwargs,
    "transformer_end": builds(TransformerEnd),
    "step_voltage_increment": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)
}

ratio_tap_changer_args = [*tap_changer_args, TransformerEnd(), 1.1]


def test_ratio_tap_changer_constructor_default():
    rtc = RatioTapChanger()
    rtc2 = create_ratio_tap_changer()
    validate_default_ratio_tap_changer_constructor(rtc)
    validate_default_ratio_tap_changer_constructor(rtc2)


def validate_default_ratio_tap_changer_constructor(rtc):
    verify_tap_changer_constructor_default(rtc)
    assert not rtc.transformer_end
    assert rtc.step_voltage_increment is None


@given(**ratio_tap_changer_kwargs)
def test_ratio_tap_changer_constructor_kwargs(transformer_end, step_voltage_increment, **kwargs):
    args = extract_testing_args(locals())
    assume_step_values(kwargs["high_step"], kwargs["low_step"], kwargs["neutral_step"], kwargs["normal_step"], kwargs["step"])

    rtc = RatioTapChanger(**args, **kwargs)
    validate_ratio_tap_changer_constructor_values(rtc, **args, **kwargs)


@given(**ratio_tap_changer_kwargs)
def test_ratio_tap_changer_creator(transformer_end, step_voltage_increment, **kwargs):
    args = extract_testing_args(locals())
    assume_step_values(kwargs["high_step"], kwargs["low_step"], kwargs["neutral_step"], kwargs["normal_step"], kwargs["step"])

    rtc = create_ratio_tap_changer(**args, **kwargs)
    validate_ratio_tap_changer_constructor_values(rtc, **args, **kwargs)


def validate_ratio_tap_changer_constructor_values(rtc, transformer_end, step_voltage_increment, **kwargs):
    verify_tap_changer_constructor_kwargs(rtc, **kwargs)
    assert rtc.transformer_end == transformer_end
    assert rtc.step_voltage_increment == step_voltage_increment


def test_ratio_tap_changer_constructor_args():
    rtc = RatioTapChanger(*ratio_tap_changer_args)

    verify_tap_changer_constructor_args(rtc)
    assert rtc.transformer_end == ratio_tap_changer_args[-2]
    assert rtc.step_voltage_increment == ratio_tap_changer_args[-1]
