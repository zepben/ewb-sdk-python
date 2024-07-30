#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import builds

from cim.iec61970.base.wires.test_conductor import verify_conductor_constructor_default, \
    verify_conductor_constructor_kwargs, verify_conductor_constructor_args, conductor_kwargs, conductor_args
from zepben.evolve import AcLineSegment, PerLengthSequenceImpedance

ac_line_segment_kwargs = {
    **conductor_kwargs,
    "per_length_sequence_impedance": builds(PerLengthSequenceImpedance)
}

ac_line_segment_args = [*conductor_args, PerLengthSequenceImpedance()]


def test_ac_line_segment_constructor_default():
    als = AcLineSegment()

    verify_conductor_constructor_default(als)
    assert not als.per_length_sequence_impedance


@given(**ac_line_segment_kwargs)
def test_ac_line_segment_constructor_kwargs(per_length_sequence_impedance, **kwargs):
    als = AcLineSegment(per_length_sequence_impedance=per_length_sequence_impedance, **kwargs)

    verify_conductor_constructor_kwargs(als, **kwargs)
    assert als.per_length_sequence_impedance == per_length_sequence_impedance


def test_ac_line_segment_constructor_args():
    als = AcLineSegment(*ac_line_segment_args)

    verify_conductor_constructor_args(als)
    assert als.per_length_sequence_impedance == ac_line_segment_args[-1]
