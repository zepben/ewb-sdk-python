#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from busbranch.data.creators import _create_per_length_sequence_impedance
from network_fixtures import create_terminal, create_terminals
from zepben.evolve import NetworkService, AcLineSegment, PowerTransformer, EquivalentBranch, EnergyConsumer, PowerElectronicsConnection, PowerTransformerEnd


def lv_equivalent_branch_network(has_equivalent_branch_impedance: bool) -> NetworkService:
    """
    line has negligible impedance

                        pec
                line    +
     pt + o +---------+ o + ec
          +
          eb
          +
          o
          +
          ec_eb
    """
    # Network
    network = NetworkService()

    # PowerTransformer
    pt = PowerTransformer(mrid="pt")
    network.add(pt)
    end1 = PowerTransformerEnd(mrid="end1", power_transformer=pt)
    pt.add_end(end1)
    network.add(end1)
    end2 = PowerTransformerEnd(mrid="end2", power_transformer=pt)
    pt.add_end(end2)
    network.add(end2)

    pt_t = create_terminal(network, pt)
    end2.terminal = pt_t

    # AcLineSegment
    plsi = _create_per_length_sequence_impedance(0.0)
    network.add(plsi)
    line = AcLineSegment(mrid="line", length=0.0, per_length_sequence_impedance=plsi)
    network.add(line)
    line_terminals = create_terminals(network, line, 2)

    network.connect_terminals(pt_t, line_terminals[0])

    # EquivalentBranch
    eb = EquivalentBranch(mrid="eb")

    if has_equivalent_branch_impedance:
        eb.r = 1.0
        eb.x = 1.0

    network.add(eb)
    eb_terminals = create_terminals(network, eb, 2)

    network.connect_by_mrid(eb_terminals[0], pt_t.connectivity_node.mrid)

    # EnergyConsumer
    ec = EnergyConsumer(mrid="ec", name="ec", p=0.0, q=0.0)
    network.add(ec)
    ec_t = create_terminal(network, ec)

    network.connect_terminals(line_terminals[1], ec_t)

    ec_eb = EnergyConsumer(mrid="ec_eb", name="ec_eb", p=0.0, q=0.0)
    network.add(ec_eb)
    ec_eb_t = create_terminal(network, ec_eb)

    network.connect_terminals(ec_eb_t, eb_terminals[1])

    # PowerElectronicsConnection
    pec = PowerElectronicsConnection(mrid="pec")
    network.add(pec)
    pec_t = create_terminal(network, pec)

    network.connect_by_mrid(pec_t, line_terminals[1].connectivity_node.mrid)

    return network
