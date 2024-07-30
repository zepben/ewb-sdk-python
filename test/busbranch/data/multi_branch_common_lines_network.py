#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from busbranch.data.creators import _create_per_length_sequence_impedance
from network_fixtures import create_terminal, create_terminals
from zepben.evolve import NetworkService, AcLineSegment
from zepben.evolve.services.network.network_service import connect


def multi_branch_common_lines_network() -> NetworkService:
    """
    all same psli

                     | a7
                     +
                     | a6
      a0    a1   a2  |        a4    a5
     ----+----+------+-----+-----+-----+
                       a3  |
                           | a8

    """
    # Network
    network = NetworkService()

    # PerLineSequenceImpedance
    plsi = _create_per_length_sequence_impedance(1.0)
    network.add(plsi)

    # AcLineSegment0
    a0 = AcLineSegment(mrid="a0", length=0.0, per_length_sequence_impedance=plsi)
    network.add(a0)
    a0_t = create_terminal(network, a0)

    # AcLineSegment1
    a1 = AcLineSegment(mrid="a1", length=1.0, per_length_sequence_impedance=plsi)
    network.add(a1)
    a1_ts = create_terminals(network, a1, 2)

    network.connect_terminals(a0_t, a1_ts[0])

    # AcLineSegment2
    a2 = AcLineSegment(mrid="a2", length=2.0, per_length_sequence_impedance=plsi)
    network.add(a2)
    a2_ts = create_terminals(network, a2, 2)

    network.connect_terminals(a1_ts[1], a2_ts[0])

    # AcLineSegment3
    a3 = AcLineSegment(mrid="a3", length=3.0, per_length_sequence_impedance=plsi)
    network.add(a3)
    a3_ts = create_terminals(network, a3, 2)

    network.connect_terminals(a2_ts[1], a3_ts[0])

    # AcLineSegment4
    a4 = AcLineSegment(mrid="a4", length=4.0, per_length_sequence_impedance=plsi)
    network.add(a4)
    a4_ts = create_terminals(network, a4, 2)

    network.connect_terminals(a3_ts[1], a4_ts[0])

    # AcLineSegment5
    a5 = AcLineSegment(mrid="a5", length=5.0, per_length_sequence_impedance=plsi)
    network.add(a5)
    a5_ts = create_terminals(network, a5, 2)

    network.connect_terminals(a4_ts[1], a5_ts[0])

    # AcLineSegment6
    a6 = AcLineSegment(mrid="a6", length=6.0, per_length_sequence_impedance=plsi)
    network.add(a6)
    a6_ts = create_terminals(network, a6, 2)

    connect(a6_ts[0], a2_ts[1].connectivity_node)

    # AcLineSegment7
    a7 = AcLineSegment(mrid="a7", length=7.0, per_length_sequence_impedance=plsi)
    network.add(a7)
    a7_t = create_terminal(network, a7)

    network.connect_terminals(a6_ts[1], a7_t)

    # AcLineSegment8
    a8 = AcLineSegment(mrid="a8", length=8.0, per_length_sequence_impedance=plsi)
    network.add(a8)
    a8_t = create_terminal(network, a8)

    connect(a8_t, a3_ts[1].connectivity_node)

    return network
