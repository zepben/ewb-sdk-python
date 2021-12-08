#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import floats, builds

from cim import extract_testing_args
from test.cim.iec61970.base.core.test_identified_object import identified_object_kwargs, verify_identified_object_constructor_default, \
    verify_identified_object_constructor_kwargs, verify_identified_object_constructor_args, identified_object_args
from test.cim.cim_creators import FLOAT_MIN, FLOAT_MAX
from zepben.evolve import TransformerStarImpedance, TransformerEndInfo
from zepben.evolve.model.cim.iec61970.base.wires.create_wires_components import create_transformer_star_impedance

transformer_star_impedance_kwargs = {
    **identified_object_kwargs,
    "r": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "r0": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "x": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "x0": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "transformer_end_info": builds(TransformerEndInfo)
}

transformer_star_impedance_args = [*identified_object_args, 1.1, 2.2, 3.3, 4.4, TransformerEndInfo()]


def test_transformer_star_impedance_constructor_default():
    tsi = TransformerStarImpedance()
    tsi2 = create_transformer_star_impedance()
    validate_default_transformer_star_impedance_constructor(tsi)
    validate_default_transformer_star_impedance_constructor(tsi2)


def validate_default_transformer_star_impedance_constructor(tsi):
    verify_identified_object_constructor_default(tsi)
    assert tsi.r == 0.0
    assert tsi.r0 == 0.0
    assert tsi.x == 0.0
    assert tsi.x0 == 0.0
    assert not tsi.transformer_end_info


@given(**transformer_star_impedance_kwargs)
def test_transformer_star_impedance_constructor_kwargs(r, r0, x, x0, transformer_end_info, **kwargs):
    args = extract_testing_args(locals())
    tsi = TransformerStarImpedance(**args, **kwargs)
    validate_transformer_star_impedance_values(tsi, **args, **kwargs)


@given(**transformer_star_impedance_kwargs)
def test_transformer_star_impedance_creator(r, r0, x, x0, transformer_end_info, **kwargs):
    args = extract_testing_args(locals())
    tsi = create_transformer_star_impedance(**args, **kwargs)
    validate_transformer_star_impedance_values(tsi, **args, **kwargs)


def validate_transformer_star_impedance_values(tsi, r, r0, x, x0, transformer_end_info, **kwargs):
    verify_identified_object_constructor_kwargs(tsi, **kwargs)
    assert tsi.r == r
    assert tsi.r0 == r0
    assert tsi.x == x
    assert tsi.x0 == x0
    assert tsi.transformer_end_info == transformer_end_info


def test_transformer_star_impedance_constructor_args():
    # noinspection PyArgumentList
    tsi = TransformerStarImpedance(*transformer_star_impedance_args)

    verify_identified_object_constructor_args(tsi)
    assert tsi.r == transformer_star_impedance_args[-5]
    assert tsi.r0 == transformer_star_impedance_args[-4]
    assert tsi.x == transformer_star_impedance_args[-3]
    assert tsi.x0 == transformer_star_impedance_args[-2]
    assert tsi.transformer_end_info == transformer_star_impedance_args[-1]
