#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import builds, data

from test.cim.test_common_two_way_connections import set_up_conducting_equipment_two_way_link_test, check_conducting_equipment_two_way_link_test
from test.cim.common_testing_functions import verify
from test.cim.iec61970.base.wires.test_conductor import verify_conductor_constructor_default, \
    verify_conductor_constructor_kwargs, verify_conductor_constructor_args, conductor_kwargs, conductor_args
from zepben.evolve import AcLineSegment, PerLengthSequenceImpedance
from zepben.evolve.model.cim.iec61970.base.wires.create_wires_components import create_ac_line_segment

ac_line_segment_kwargs = {
    **conductor_kwargs,
    "per_length_sequence_impedance": builds(PerLengthSequenceImpedance)
}

ac_line_segment_args = [*conductor_args, PerLengthSequenceImpedance()]


def test_ac_line_segment_constructor_default():
    als = AcLineSegment()
    als2 = create_ac_line_segment()
    verify_default_ac_line_segment_constructor(als)
    verify_default_ac_line_segment_constructor(als2)


def verify_default_ac_line_segment_constructor(als):
    verify_conductor_constructor_default(als)
    assert not als.per_length_sequence_impedance


# noinspection PyShadowingNames
@given(data())
def test_ac_line_segment_constructor_kwargs(data):
    verify(
        [AcLineSegment, create_ac_line_segment],
        data, ac_line_segment_kwargs, verify_ac_line_segment_values
    )


def verify_ac_line_segment_values(als, per_length_sequence_impedance, **kwargs):
    verify_conductor_constructor_kwargs(als, **kwargs)
    assert als.per_length_sequence_impedance == per_length_sequence_impedance


def test_ac_line_segment_constructor_args():
    als = AcLineSegment(*ac_line_segment_args)

    verify_conductor_constructor_args(als)
    assert als.per_length_sequence_impedance == ac_line_segment_args[-1]


def test_auto_two_way_connections_for_ac_line_segment_constructor():
    up, ec, opr, f, t = set_up_conducting_equipment_two_way_link_test()
    als = create_ac_line_segment(usage_points=[up], equipment_containers=[ec], operational_restrictions=[opr], current_feeders=[f], terminals=[t])
    check_conducting_equipment_two_way_link_test(als, up, ec, opr, f, t)
