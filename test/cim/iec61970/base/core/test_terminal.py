#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import builds, sampled_from, integers

from cim.cim_creators import MIN_32_BIT_INTEGER, MAX_32_BIT_INTEGER
from cim.iec61970.base.core.test_ac_dc_terminal import ac_dc_terminal_kwargs, verify_ac_dc_terminal_constructor_default, \
    verify_ac_dc_terminal_constructor_kwargs, verify_ac_dc_terminal_constructor_args, ac_dc_terminal_args
from util import mrid_strategy
from zepben.ewb import Terminal, ConnectivityNode, ConductingEquipment, PhaseCode, generate_id, NetworkService, Junction
from zepben.ewb.services.network.tracing.feeder.feeder_direction import FeederDirection

terminal_kwargs = {
    **ac_dc_terminal_kwargs,
    "conducting_equipment": builds(ConductingEquipment, mrid=mrid_strategy),
    "phases": sampled_from(PhaseCode),
    "sequence_number": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    "normal_feeder_direction": sampled_from(FeederDirection),
    "current_feeder_direction": sampled_from(FeederDirection),
    "connectivity_node": builds(ConnectivityNode, mrid=mrid_strategy)
}

# noinspection PyArgumentList
terminal_args = [
    *ac_dc_terminal_args,
    ConductingEquipment(mrid=generate_id()),
    PhaseCode.XYN,
    1,
    FeederDirection.UPSTREAM,
    FeederDirection.DOWNSTREAM,
    ConnectivityNode(mrid=generate_id())
]


def test_terminal_constructor_default():
    t = Terminal(mrid=generate_id())

    verify_ac_dc_terminal_constructor_default(t)
    assert not t.conducting_equipment
    assert t.phases == PhaseCode.ABC
    assert t.sequence_number == 0
    assert t.normal_feeder_direction == FeederDirection.NONE
    assert t.current_feeder_direction == FeederDirection.NONE
    assert t.normal_phases._phase_status_internal == 0
    assert t.current_phases._phase_status_internal == 0
    assert not t.connectivity_node


@given(**terminal_kwargs)
def test_terminal_constructor_kwargs(conducting_equipment, phases, sequence_number, normal_feeder_direction, current_feeder_direction,
                                     connectivity_node, **kwargs):
    t = Terminal(conducting_equipment=conducting_equipment,
                 phases=phases,
                 sequence_number=sequence_number,
                 normal_feeder_direction=normal_feeder_direction,
                 current_feeder_direction=current_feeder_direction,
                 connectivity_node=connectivity_node,
                 **kwargs)

    verify_ac_dc_terminal_constructor_kwargs(t, **kwargs)
    assert t.conducting_equipment == conducting_equipment
    assert t.phases == phases
    assert t.sequence_number == sequence_number
    assert t.normal_feeder_direction == normal_feeder_direction
    assert t.current_feeder_direction == current_feeder_direction
    assert t.connectivity_node == connectivity_node


def test_terminal_constructor_args():
    t = Terminal(*terminal_args)

    verify_ac_dc_terminal_constructor_args(t)
    expected_args = [
        t.conducting_equipment,
        t.phases,
        t.sequence_number,
        t.normal_feeder_direction,
        t.current_feeder_direction,
        t.connectivity_node
    ]
    assert (terminal_args[-len(expected_args):] == expected_args)


def test_connectivity():
    terminal = Terminal(mrid=generate_id())
    connectivity_node = ConnectivityNode(mrid=generate_id())

    assert terminal.connectivity_node is None
    assert terminal.connectivity_node_id is None
    assert terminal.connected == False

    terminal.connect(connectivity_node)

    assert terminal.connectivity_node == connectivity_node
    assert terminal.connectivity_node_id is connectivity_node.mrid
    assert terminal.connected == True

    terminal.disconnect()

    assert terminal.connectivity_node is None
    assert terminal.connectivity_node_id is None
    assert terminal.connected == False


def test_connected_terminals():
    terminal1 = Terminal(mrid=generate_id())
    terminal2 = Terminal(mrid=generate_id())
    terminal3 = Terminal(mrid=generate_id())
    network_service = NetworkService()

    assert list(terminal1.connected_terminals()) == []

    network_service.connect(terminal1, "cn1")
    assert list(terminal1.connected_terminals()) == []

    network_service.connect(terminal2, "cn1")
    assert list(terminal1.connected_terminals()) == [terminal2]

    network_service.connect(terminal3, "cn1")
    assert list(terminal1.connected_terminals()) == [terminal2, terminal3]


def test_other_terminals():
    terminal1 = Terminal(mrid=generate_id())
    terminal2 = Terminal(mrid=generate_id())
    terminal3 = Terminal(mrid=generate_id())
    ce = Junction(mrid=generate_id())

    assert list(terminal1.other_terminals()) == []

    ce.add_terminal(terminal1)
    assert list(terminal1.other_terminals()) == []

    ce.add_terminal(terminal2)
    assert list(terminal1.other_terminals()) == [terminal2]

    ce.add_terminal(terminal3)
    assert list(terminal1.other_terminals()) == [terminal2, terminal3]


def test_normal_and_current_phases_are_different_statuses():
    terminal = Terminal(mrid=generate_id())

    assert terminal.normal_phases is not terminal.current_phases
