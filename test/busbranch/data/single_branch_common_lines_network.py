#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from busbranch.data.creators import _create_per_length_sequence_impedance
from network_fixtures import create_terminal, create_terminals
from zepben.evolve import NetworkService, AcLineSegment, Breaker


def single_branch_common_lines_network(sw_is_open: bool) -> NetworkService:
    """
      acls1     acls2     acls3            acls4     acls5
     --------+---------+---------+  sw  +---------+--------
    |           psli1            |      |  psli2  | psli3 |
    """
    # Network
    network = NetworkService()

    # PerLineSequenceImpedance
    plsi1 = _create_per_length_sequence_impedance(1.0)
    plsi2 = _create_per_length_sequence_impedance(2.0)
    plsi3 = _create_per_length_sequence_impedance(3.0)
    network.add(plsi1)
    network.add(plsi2)
    network.add(plsi3)

    # AcLineSegment1
    acls1 = AcLineSegment(mrid="acls1", length=1.0, per_length_sequence_impedance=plsi1)
    network.add(acls1)
    acls1_t = create_terminal(network, acls1)

    # AcLineSegment2
    acls2 = AcLineSegment(mrid="acls2", length=2.0, per_length_sequence_impedance=plsi1)
    network.add(acls2)
    acls2_terminals = create_terminals(network, acls2, 2)

    network.connect_terminals(acls1_t, acls2_terminals[0])

    # AcLineSegment3
    acls3 = AcLineSegment(mrid="acls3", length=3.0, per_length_sequence_impedance=plsi1)
    network.add(acls3)
    acls3_terminals = create_terminals(network, acls3, 2)

    network.connect_terminals(acls2_terminals[1], acls3_terminals[0])

    # SW
    sw = Breaker(mrid="sw")
    sw.set_open(sw_is_open)
    sw.set_normally_open(sw_is_open)
    network.add(sw)
    sw_terminals = create_terminals(network, sw, 2)
    network.connect_terminals(acls3_terminals[1], sw_terminals[0])

    # AcLineSegment4
    acls4 = AcLineSegment(mrid="acls4", length=4.0, per_length_sequence_impedance=plsi2)
    network.add(acls4)
    acls4_terminals = create_terminals(network, acls4, 2)

    network.connect_terminals(sw_terminals[1], acls4_terminals[0])

    # AcLineSegment5
    acls5 = AcLineSegment(mrid="acls5", length=5.0, per_length_sequence_impedance=plsi3)
    network.add(acls5)
    acls5_t = create_terminal(network, acls5)

    network.connect_terminals(acls4_terminals[1], acls5_t)

    return network
