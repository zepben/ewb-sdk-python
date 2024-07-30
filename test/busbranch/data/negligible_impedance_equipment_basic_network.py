#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from busbranch.data.creators import _create_per_length_sequence_impedance
from network_fixtures import create_terminal, create_terminals
from zepben.evolve import NetworkService, AcLineSegment


def negligible_impedance_equipment_basic_network(nie_constructor) -> NetworkService:
    """
    all same psli

                               | a5
                               +
                               | a4
      a0           a1    a2    |      a3
     ----+ nie1 +----+------ nie2 -----------+

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

    # NegligibleImpedanceEquipment1
    nie1 = nie_constructor("nie1")
    network.add(nie1)
    nie1_ts = create_terminals(network, nie1, 2)

    network.connect_terminals(a0_t, nie1_ts[0])

    # AcLineSegment1
    a1 = AcLineSegment(mrid="a1", length=0.0, per_length_sequence_impedance=plsi)
    network.add(a1)
    a1_ts = create_terminals(network, a1, 2)

    network.connect_terminals(nie1_ts[1], a1_ts[0])

    # AcLineSegment2
    a2 = AcLineSegment(mrid="a2", length=2.0, per_length_sequence_impedance=plsi)
    network.add(a2)
    a2_ts = create_terminals(network, a2, 2)

    network.connect_terminals(a1_ts[1], a2_ts[0])

    # NegligibleImpedanceEquipment2
    nie2 = nie_constructor("nie2")
    network.add(nie2)
    nie2_ts = create_terminals(network, nie2, 3)

    network.connect_terminals(a2_ts[1], nie2_ts[0])

    # AcLineSegment3
    a3 = AcLineSegment(mrid="a3", length=3.0, per_length_sequence_impedance=plsi)
    network.add(a3)
    a3_ts = create_terminals(network, a3, 2)

    network.connect_terminals(nie2_ts[1], a3_ts[0])

    # AcLineSegment4
    a4 = AcLineSegment(mrid="a4", length=4.0, per_length_sequence_impedance=plsi)
    network.add(a4)
    a4_ts = create_terminals(network, a4, 2)

    network.connect_terminals(nie2_ts[2], a4_ts[0])

    # AcLineSegment5
    a5 = AcLineSegment(mrid="a5", length=5.0, per_length_sequence_impedance=plsi)
    network.add(a5)
    a5_t = create_terminal(network, a5)

    network.connect_terminals(a4_ts[1], a5_t)

    return network
