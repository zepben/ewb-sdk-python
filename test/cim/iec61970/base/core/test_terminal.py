#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import builds, sampled_from, integers

from cim.iec61970.base.core.test_ac_dc_terminal import ac_dc_terminal_kwargs, verify_ac_dc_terminal_constructor_default, \
    verify_ac_dc_terminal_constructor_kwargs, verify_ac_dc_terminal_constructor_args, ac_dc_terminal_args
from cim.cim_creators import MIN_32_BIT_INTEGER, MAX_32_BIT_INTEGER
from zepben.evolve import Terminal, ConnectivityNode, TracedPhases, ConductingEquipment, PhaseCode
from zepben.evolve.services.network.tracing.feeder.feeder_direction import FeederDirection

terminal_kwargs = {
    **ac_dc_terminal_kwargs,
    "conducting_equipment": builds(ConductingEquipment),
    "phases": sampled_from(PhaseCode),
    "sequence_number": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    "normal_feeder_direction": sampled_from(FeederDirection),
    "current_feeder_direction": sampled_from(FeederDirection),
    "traced_phases": builds(TracedPhases),
    "connectivity_node": builds(ConnectivityNode)
}

# noinspection PyArgumentList
terminal_args = [*ac_dc_terminal_args, ConductingEquipment(), PhaseCode.XYN, 1, FeederDirection.UPSTREAM, FeederDirection.DOWNSTREAM, TracedPhases(1),
                 ConnectivityNode()]


def test_terminal_constructor_default():
    t = Terminal()

    verify_ac_dc_terminal_constructor_default(t)
    assert not t.conducting_equipment
    assert t.phases == PhaseCode.ABC
    assert t.sequence_number == 0
    assert t.normal_feeder_direction == FeederDirection.NONE
    assert t.current_feeder_direction == FeederDirection.NONE
    assert t.traced_phases == TracedPhases()
    assert not t.connectivity_node


@given(**terminal_kwargs)
def test_terminal_constructor_kwargs(conducting_equipment, phases, sequence_number, normal_feeder_direction, current_feeder_direction, traced_phases,
                                     connectivity_node, **kwargs):
    t = Terminal(conducting_equipment=conducting_equipment,
                 phases=phases,
                 sequence_number=sequence_number,
                 normal_feeder_direction=normal_feeder_direction,
                 current_feeder_direction=current_feeder_direction,
                 traced_phases=traced_phases,
                 connectivity_node=connectivity_node,
                 **kwargs)

    verify_ac_dc_terminal_constructor_kwargs(t, **kwargs)
    assert t.conducting_equipment == conducting_equipment
    assert t.phases == phases
    assert t.sequence_number == sequence_number
    assert t.normal_feeder_direction == normal_feeder_direction
    assert t.current_feeder_direction == current_feeder_direction
    assert t.traced_phases == traced_phases
    assert t.connectivity_node == connectivity_node


def test_terminal_constructor_args():
    t = Terminal(*terminal_args)

    verify_ac_dc_terminal_constructor_args(t)
    assert t.conducting_equipment == terminal_args[-7]
    assert t.phases == terminal_args[-6]
    assert t.sequence_number == terminal_args[-5]
    assert t.normal_feeder_direction == terminal_args[-4]
    assert t.current_feeder_direction == terminal_args[-3]
    assert t.traced_phases == terminal_args[-2]
    assert t.connectivity_node == terminal_args[-1]
