#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from busbranch.data.creators import _create_per_length_sequence_impedance
from network_fixtures import create_terminal, create_terminals
from zepben.evolve import NetworkService, AcLineSegment, EnergyConsumer, PowerElectronicsConnection


def end_of_branch_multiple_ec_pec() -> NetworkService:
    """
    all same plsi
                                pec1
                              +
        a1          a2       /
     +---------+---------+ o + ec
                            \
                             +
                              pec2
    """
    # Network
    network = NetworkService()

    # PerLineSequenceImpedance
    plsi1 = _create_per_length_sequence_impedance(1.0)
    network.add(plsi1)

    # AcLineSegment1
    a1 = AcLineSegment(mrid="a1", length=1.0, per_length_sequence_impedance=plsi1)
    network.add(a1)
    a1_terminals = create_terminals(network, a1, 2)

    # AcLineSegment2
    a2 = AcLineSegment(mrid="a2", length=2.0, per_length_sequence_impedance=plsi1)
    network.add(a2)
    a2_terminals = create_terminals(network, a2, 2)

    network.connect_terminals(a1_terminals[1], a2_terminals[0])

    # Load
    ec = EnergyConsumer(mrid="ec", name="ec", p=100000., q=50000.)
    network.add(ec)
    ec_t = create_terminal(network, ec)

    network.connect_terminals(a2_terminals[1], ec_t)

    # PowerElectronicsConnection
    pec1 = PowerElectronicsConnection(mrid="pec1")
    network.add(pec1)
    pec1_t = create_terminal(network, pec1)
    pec1_t.mrid = "pec1_t1"

    network.connect_by_mrid(pec1_t, a2_terminals[1].connectivity_node.mrid)

    pec2 = PowerElectronicsConnection(mrid="pec2")
    network.add(pec2)
    pec2_t = create_terminal(network, pec2)
    pec2_t.mrid = "pec2_t1"

    network.connect_by_mrid(pec2_t, a2_terminals[1].connectivity_node.mrid)

    return network
