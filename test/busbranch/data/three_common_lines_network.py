#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from busbranch.data.creators import _create_per_length_sequence_impedance
from network_fixtures import create_terminal, create_terminals
from zepben.evolve import NetworkService, AcLineSegment, OverheadWireInfo, Junction


def three_common_lines_network() -> NetworkService:
    """
           acls1     acls2     acls3
     [j1]--------+---------+---------[j2]
        |           psli1            |
    """
    # Network
    network = NetworkService()

    # PerLineSequenceImpedance
    plsi1 = _create_per_length_sequence_impedance(1.0)
    wire_info = OverheadWireInfo(mrid="wire_info")
    network.add(plsi1)

    # Junction 1
    j1 = Junction(mrid="j1")
    network.add(j1)
    j1_t = create_terminal(network, j1)

    # AcLineSegment1
    acls1 = AcLineSegment(mrid="acls1", length=1.0, per_length_sequence_impedance=plsi1, asset_info=wire_info)
    network.add(acls1)
    acls1_terminals = create_terminals(network, acls1, 2)

    network.connect_terminals(j1_t, acls1_terminals[0])

    # AcLineSegment2
    acls2 = AcLineSegment(mrid="acls2", length=2.0, per_length_sequence_impedance=plsi1, asset_info=wire_info)
    network.add(acls2)
    acls2_terminals = create_terminals(network, acls2, 2)

    network.connect_terminals(acls1_terminals[1], acls2_terminals[0])

    # AcLineSegment3
    acls3 = AcLineSegment(mrid="acls3", length=3.0, per_length_sequence_impedance=plsi1, asset_info=wire_info)
    network.add(acls3)
    acls3_terminals = create_terminals(network, acls3, 2)

    network.connect_terminals(acls2_terminals[1], acls3_terminals[0])

    # Junction 2
    j2 = Junction(mrid="j2")
    network.add(j2)
    j2_t = create_terminal(network, j2)

    network.connect_terminals(acls3_terminals[1], j2_t)
    return network
