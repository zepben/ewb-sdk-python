#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import pytest
from hypothesis import given
from hypothesis.strategies import builds

from cim.private_collection_validator import validate_unordered
from util import mrid_strategy
from zepben.ewb import AcLineSegment, generate_id, SinglePhaseKind, OverheadWireInfo
from zepben.ewb.model.cim.iec61970.base.wires.ac_line_segment_phase import AcLineSegmentPhase
from zepben.ewb.model.cim.iec61970.base.wires.per_length_sequence_impedance import PerLengthSequenceImpedance

from cim.iec61970.base.wires.test_conductor import verify_conductor_constructor_default, \
    verify_conductor_constructor_kwargs, verify_conductor_constructor_args, conductor_kwargs, conductor_args
from zepben.ewb.model.cim.iec61970.base.wires.per_length_phase_impedance import PerLengthPhaseImpedance

ac_line_segment_kwargs = {
    **conductor_kwargs,
    "per_length_impedance": builds(PerLengthSequenceImpedance, mrid=mrid_strategy)
}

ac_line_segment_args = [*conductor_args, PerLengthSequenceImpedance(mrid=generate_id())]


def test_ac_line_segment_constructor_default():
    als = AcLineSegment(mrid=generate_id())

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
    acls = AcLineSegment(mrid=generate_id())
    plpi = PerLengthPhaseImpedance(mrid=generate_id())
    plsi = PerLengthSequenceImpedance(mrid=generate_id())

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


def test_supports_different_phase():
    acls = AcLineSegment(mrid=generate_id())
    (phase1 := AcLineSegmentPhase(mrid=generate_id())).phase = SinglePhaseKind.A
    (phase2 := AcLineSegmentPhase(mrid=generate_id())).phase = SinglePhaseKind.B
    (phase3 := AcLineSegmentPhase(mrid=generate_id())).phase = SinglePhaseKind.C
    (phase4 := AcLineSegmentPhase(mrid=generate_id())).phase = SinglePhaseKind.N

    acls.add_phase(phase1)
    acls.add_phase(phase2)
    acls.add_phase(phase3)
    acls.add_phase(phase4)

    assert acls.num_phases() == 4
    assert [phase1, phase2, phase3, phase4] == list(acls.phases)


def test_assigns_ac_line_segment_to_phase_if_missing():
    acls = AcLineSegment(mrid=generate_id())
    phase = AcLineSegmentPhase(mrid=generate_id())

    acls.add_phase(phase)
    assert phase.ac_line_segment == acls


def test_rejects_ac_line_segment_phase_with_wrong_ac_line_segment():
    acls1 = AcLineSegment(mrid=generate_id())
    acls2 = AcLineSegment(mrid=generate_id())
    (phase := AcLineSegmentPhase(mrid=generate_id())).ac_line_segment = acls2

    with pytest.raises(ValueError):
        acls1.add_phase(phase)


def test_ac_line_segment_phases():
    validate_unordered(
        AcLineSegment,
        lambda mrid: AcLineSegmentPhase(mrid),
        AcLineSegment.phases,
        AcLineSegment.num_phases,
        AcLineSegment.get_phase,
        AcLineSegment.add_phase,
        AcLineSegment.remove_phase,
        AcLineSegment.clear_phases
    )


def test_retrieves_wire_info_for_phase():
    wi = OverheadWireInfo(mrid=generate_id())
    (acls := AcLineSegment(mrid=generate_id())).wire_info = wi
    wiA = OverheadWireInfo(mrid=generate_id())
    wiB = OverheadWireInfo(mrid=generate_id())
    wiC = OverheadWireInfo(mrid=generate_id())
    acls.add_phase(AcLineSegmentPhase(mrid=generate_id(), ac_line_segment=acls, phase=SinglePhaseKind.A, asset_info=wiA))
    acls.add_phase(AcLineSegmentPhase(mrid=generate_id(), ac_line_segment=acls, phase=SinglePhaseKind.B, asset_info=wiB))
    acls.add_phase(AcLineSegmentPhase(mrid=generate_id(), ac_line_segment=acls, phase=SinglePhaseKind.C, asset_info=wiC))

    assert acls.wire_info_for_phase(SinglePhaseKind.A) == wiA
    assert acls.wire_info_for_phase(SinglePhaseKind.B) == wiB
    assert acls.wire_info_for_phase(SinglePhaseKind.C) == wiC
    assert acls.wire_info_for_phase(SinglePhaseKind.N) == wi
    assert acls.wire_info_for_phase(SinglePhaseKind.NONE) == wi
    assert acls.wire_info_for_phase(SinglePhaseKind.INVALID) == wi
    assert acls.wire_info_for_phase(SinglePhaseKind.X) == wi
    assert acls.wire_info_for_phase(SinglePhaseKind.Y) == wi
    assert acls.wire_info_for_phase(SinglePhaseKind.s1) == wi
    assert acls.wire_info_for_phase(SinglePhaseKind.s2) == wi
