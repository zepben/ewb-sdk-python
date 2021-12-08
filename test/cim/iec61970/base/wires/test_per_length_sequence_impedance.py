#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import floats

from test.cim.extract_testing_args import extract_testing_args
from test.cim.iec61970.base.wires.test_per_length_impedance import verify_per_length_impedance_constructor_default, \
    verify_per_length_impedance_constructor_kwargs, verify_per_length_impedance_constructor_args, per_length_impedance_kwargs, per_length_impedance_args
from test.cim.cim_creators import FLOAT_MIN, FLOAT_MAX
from zepben.evolve import PerLengthSequenceImpedance
from zepben.evolve.model.cim.iec61970.base.wires.create_wires_components import create_per_length_sequence_impedance

per_length_sequence_impedance_kwargs = {
    **per_length_impedance_kwargs,
    "r": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "x": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "bch": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "gch": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "r0": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "x0": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "b0ch": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "g0ch": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)
}

per_length_sequence_impedance_args = [*per_length_impedance_args, 1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8]


def test_per_length_sequence_impedance_constructor_default():
    plsi = PerLengthSequenceImpedance()
    plsi2 = create_per_length_sequence_impedance()
    validate_default_per_length_sequence_impedance_constructor(plsi)
    validate_default_per_length_sequence_impedance_constructor(plsi2)


def validate_default_per_length_sequence_impedance_constructor(plsi):
    verify_per_length_impedance_constructor_default(plsi)
    assert plsi.r is None
    assert plsi.x is None
    assert plsi.bch is None
    assert plsi.gch is None
    assert plsi.r0 is None
    assert plsi.x0 is None
    assert plsi.b0ch is None
    assert plsi.g0ch is None


@given(**per_length_sequence_impedance_kwargs)
def test_per_length_sequence_impedance_constructor_kwargs(r, x, bch, gch, r0, x0, b0ch, g0ch, **kwargs):
    args = extract_testing_args(locals())
    plsi = PerLengthSequenceImpedance(**args, ** kwargs)
    validate_per_length_sequence_impedance_values(plsi, **args, ** kwargs)


@given(**per_length_sequence_impedance_kwargs)
def test_per_length_sequence_impedance_creator(r, x, bch, gch, r0, x0, b0ch, g0ch, **kwargs):
    args = extract_testing_args(locals())
    plsi = create_per_length_sequence_impedance(**args, ** kwargs)
    validate_per_length_sequence_impedance_values(plsi, **args, ** kwargs)


def validate_per_length_sequence_impedance_values(plsi, r, x, bch, gch, r0, x0, b0ch, g0ch, **kwargs):
    verify_per_length_impedance_constructor_kwargs(plsi, **kwargs)
    assert plsi.r == r
    assert plsi.x == x
    assert plsi.bch == bch
    assert plsi.gch == gch
    assert plsi.r0 == r0
    assert plsi.x0 == x0
    assert plsi.b0ch == b0ch
    assert plsi.g0ch == g0ch


def test_per_length_sequence_impedance_constructor_args():
    # noinspection PyArgumentList
    plsi = PerLengthSequenceImpedance(*per_length_sequence_impedance_args)

    verify_per_length_impedance_constructor_args(plsi)
    assert plsi.r == per_length_sequence_impedance_args[-8]
    assert plsi.x == per_length_sequence_impedance_args[-7]
    assert plsi.bch == per_length_sequence_impedance_args[-6]
    assert plsi.gch == per_length_sequence_impedance_args[-5]
    assert plsi.r0 == per_length_sequence_impedance_args[-4]
    assert plsi.x0 == per_length_sequence_impedance_args[-3]
    assert plsi.b0ch == per_length_sequence_impedance_args[-2]
    assert plsi.g0ch == per_length_sequence_impedance_args[-1]
