#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis.strategies import floats, booleans, builds, integers

from test.cim.iec61970.base.core.test_identified_object import identified_object_kwargs, verify_identified_object_constructor_default, \
    verify_identified_object_constructor_kwargs, verify_identified_object_constructor_args, identified_object_args
from test.cim.cim_creators import FLOAT_MIN, FLOAT_MAX, MIN_32_BIT_INTEGER, MAX_32_BIT_INTEGER
from zepben.evolve import TransformerEnd, RatioTapChanger, Terminal, BaseVoltage, TransformerStarImpedance

transformer_end_kwargs = {
    **identified_object_kwargs,
    "grounded": booleans(),
    "r_ground": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "x_ground": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "ratio_tap_changer": builds(RatioTapChanger),
    "terminal": builds(Terminal),
    "base_voltage": builds(BaseVoltage),
    "end_number": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    "star_impedance": builds(TransformerStarImpedance)
}

transformer_end_args = [*identified_object_args, True, 1.1, 2.2, RatioTapChanger(), Terminal(), BaseVoltage(), 3, TransformerStarImpedance()]


def verify_transformer_end_constructor_default(te: TransformerEnd):
    verify_identified_object_constructor_default(te)
    assert not te.grounded
    assert te.r_ground is None
    assert te.x_ground is None
    assert not te.ratio_tap_changer
    assert not te.terminal
    assert not te.base_voltage
    assert te.end_number == 0
    assert not te.star_impedance


def verify_transformer_end_constructor_kwargs(te: TransformerEnd, grounded, r_ground, x_ground, ratio_tap_changer, terminal, base_voltage, end_number,
                                              star_impedance, **kwargs):
    verify_identified_object_constructor_kwargs(te, **kwargs)
    assert te.grounded == grounded
    assert te.r_ground == r_ground
    assert te.x_ground == x_ground
    assert te.ratio_tap_changer == ratio_tap_changer
    assert te.terminal == terminal
    assert te.base_voltage == base_voltage
    assert te.end_number == end_number
    assert te.star_impedance == star_impedance


def verify_transformer_end_constructor_args(te: TransformerEnd):
    verify_identified_object_constructor_args(te)
    assert te.grounded == transformer_end_args[-8]
    assert te.r_ground == transformer_end_args[-7]
    assert te.x_ground == transformer_end_args[-6]
    assert te.ratio_tap_changer == transformer_end_args[-5]
    assert te.terminal == transformer_end_args[-4]
    assert te.base_voltage == transformer_end_args[-3]
    assert te.end_number == transformer_end_args[-2]
    assert te.star_impedance == transformer_end_args[-1]


def verify_transformer_end_creator(te: TransformerEnd, grounded, r_ground, x_ground, ratio_tap_changer, terminal, base_voltage, end_number,
                                   star_impedance, **kwargs):
    verify_identified_object_constructor_kwargs(te, **kwargs)
    assert te.grounded == grounded
    assert te.r_ground == r_ground
    assert te.x_ground == x_ground
    assert te.ratio_tap_changer == ratio_tap_changer
    assert te.terminal == terminal
    assert te.base_voltage == base_voltage
    # Compensate for automatic two way connection in the creator
    if end_number == 0:
        assert te.end_number == end_number+1
    else:
        assert te.end_number == end_number
    assert te.star_impedance == star_impedance
