#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from hypothesis import given
from hypothesis.strategies import builds, floats, data

from test.cim.common_testing_functions import verify
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
    verify_default_ratio_tap_changer_constructor(rtc)
    verify_default_ratio_tap_changer_constructor(rtc2)


def verify_default_ratio_tap_changer_constructor(rtc):
    verify_tap_changer_constructor_default(rtc)
    assert not rtc.transformer_end
    assert rtc.step_voltage_increment is None


# noinspection PyShadowingNames
@given(data())
def test_ratio_tap_changer_constructor_kwargs(data):
    verify(
        [RatioTapChanger, create_ratio_tap_changer],
        data, ratio_tap_changer_kwargs, verify_ratio_tap_changer_constructor_values
    )


def verify_ratio_tap_changer_constructor_values(rtc, transformer_end, step_voltage_increment, **kwargs):
    verify_tap_changer_constructor_kwargs(rtc, **kwargs)
    assert rtc.transformer_end == transformer_end
    assert rtc.step_voltage_increment == step_voltage_increment


def test_ratio_tap_changer_constructor_args():
    rtc = RatioTapChanger(*ratio_tap_changer_args)

    verify_tap_changer_constructor_args(rtc)
    assert rtc.transformer_end == ratio_tap_changer_args[-2]
    assert rtc.step_voltage_increment == ratio_tap_changer_args[-1]


def test_auto_two_way_connections_for_ratio_tap_changer_constructor():
    te = TransformerEnd()
    rtc = create_ratio_tap_changer(transformer_end=te)

    assert te.ratio_tap_changer == rtc
