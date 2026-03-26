#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given

from cim.fill_fields import ratio_tap_changer_kwargs
from cim.iec61970.base.wires.test_tap_changer import verify_tap_changer_constructor_default, \
    verify_tap_changer_constructor_kwargs, verify_tap_changer_constructor_args, tap_changer_args, assume_step_values
from zepben.ewb import generate_id
from zepben.ewb.model.cim.iec61970.base.wires.ratio_tap_changer import RatioTapChanger
from zepben.ewb.model.cim.iec61970.base.wires.transformer_end import TransformerEnd

ratio_tap_changer_args = [*tap_changer_args, TransformerEnd(mrid=generate_id()), 1.1]


def test_ratio_tap_changer_constructor_default():
    rtc = RatioTapChanger(mrid=generate_id())

    verify_tap_changer_constructor_default(rtc)
    assert not rtc.transformer_end
    assert rtc.step_voltage_increment is None


@given(**ratio_tap_changer_kwargs())
def test_ratio_tap_changer_constructor_kwargs(transformer_end, step_voltage_increment, **kwargs):
    assume_step_values(kwargs["high_step"], kwargs["low_step"], kwargs["neutral_step"], kwargs["normal_step"], kwargs["step"])

    rtc = RatioTapChanger(transformer_end=transformer_end, step_voltage_increment=step_voltage_increment, **kwargs)

    verify_tap_changer_constructor_kwargs(rtc, **kwargs)
    assert rtc.transformer_end == transformer_end
    assert rtc.step_voltage_increment == step_voltage_increment


def test_ratio_tap_changer_constructor_args():
    rtc = RatioTapChanger(*ratio_tap_changer_args)

    verify_tap_changer_constructor_args(rtc)
    assert ratio_tap_changer_args[-2:] == [
        rtc.transformer_end,
        rtc.step_voltage_increment
    ]
