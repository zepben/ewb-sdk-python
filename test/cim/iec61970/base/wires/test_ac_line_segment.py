#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import builds
from zepben.ewb import AcLineSegment
from zepben.ewb.model.cim.iec61970.base.wires.per_length_sequence_impedance import PerLengthSequenceImpedance

from cim.iec61970.base.wires.test_conductor import verify_conductor_constructor_default, \
    verify_conductor_constructor_kwargs, verify_conductor_constructor_args, conductor_kwargs, conductor_args
from zepben.ewb.model.cim.iec61970.base.wires.per_length_phase_impedance import PerLengthPhaseImpedance

ac_line_segment_kwargs = {
    **conductor_kwargs,
    "per_length_impedance": builds(PerLengthSequenceImpedance)
}

ac_line_segment_args = [*conductor_args, PerLengthSequenceImpedance()]


def test_ac_line_segment_constructor_default():
    als = AcLineSegment()

    verify_conductor_constructor_default(als)
    assert not als.per_length_impedance
    assert not als.per_length_sequence_impedance
    assert not als.per_length_phase_impedance


@given(**ac_line_segment_kwargs)
def test_ac_line_segment_constructor_kwargs(per_length_impedance, **kwargs):
    als = AcLineSegment(per_length_impedance=per_length_impedance, **kwargs)

    verify_conductor_constructor_kwargs(als, **kwargs)
    assert als.per_length_impedance == per_length_impedance
    assert als.per_length_sequence_impedance == per_length_impedance
    assert als.per_length_phase_impedance != per_length_impedance


def test_ac_line_segment_constructor_args():
    als = AcLineSegment(*ac_line_segment_args)

    verify_conductor_constructor_args(als)
    assert ac_line_segment_args[-1:] == [
        als.per_length_impedance
    ]


def test_properties():
    acls = AcLineSegment()
    plpi = PerLengthPhaseImpedance()
    plsi = PerLengthSequenceImpedance()

    acls.per_length_phase_impedance = plpi
    assert acls.per_length_impedance == plpi
    assert acls.per_length_phase_impedance == plpi
    assert acls.per_length_sequence_impedance is None

    acls.per_length_phase_impedance = None
    assert acls.per_length_impedance is None
    assert acls.per_length_phase_impedance is None
    assert acls.per_length_sequence_impedance is None

    acls.per_length_sequence_impedance = plsi
    assert acls.per_length_impedance == plsi
    assert acls.per_length_phase_impedance is None
    assert acls.per_length_sequence_impedance == plsi

    acls.per_length_sequence_impedance = None
    assert acls.per_length_impedance is None
    assert acls.per_length_phase_impedance is None
    assert acls.per_length_sequence_impedance is None
