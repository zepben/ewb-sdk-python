#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given

from cim.fill_fields import ac_line_segment_phase_kwargs
from cim.iec61970.base.core.test_power_system_resource import verify_power_system_resource_constructor_default, verify_power_system_resource_constructor_kwargs, \
    verify_power_system_resource_constructor_args, power_system_resource_args
from zepben.ewb import generate_id, AcLineSegment, SinglePhaseKind
from zepben.ewb.model.cim.iec61970.base.wires.ac_line_segment_phase import AcLineSegmentPhase

ac_line_segment_phase_args = [*power_system_resource_args, SinglePhaseKind.A, 0, AcLineSegment(mrid=generate_id())]


def test_ac_line_segment_phase_constructor_default():
    als = AcLineSegmentPhase(mrid=generate_id())

    verify_power_system_resource_constructor_default(als)
    assert als.phase == SinglePhaseKind.X
    assert not als.sequence_number
    assert not als.ac_line_segment


@given(**ac_line_segment_phase_kwargs())
def test_ac_line_segment_phase_constructor_kwargs(phase, sequence_number, ac_line_segment, **kwargs):
    als = AcLineSegmentPhase(
        phase=phase,
        sequence_number=sequence_number,
        ac_line_segment=ac_line_segment,
        **kwargs
    )

    verify_power_system_resource_constructor_kwargs(als, **kwargs)
    assert als.phase == phase
    assert als.sequence_number == sequence_number
    assert als.ac_line_segment == ac_line_segment


def test_ac_line_segment_phase_constructor_args():
    als = AcLineSegmentPhase(*ac_line_segment_phase_args)

    verify_power_system_resource_constructor_args(als)
    assert ac_line_segment_phase_args[-3:] == [
        als.phase,
        als.sequence_number,
        als.ac_line_segment,
    ]
