#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from test.busbranch.data.creators import _create_transformer_ends
from test.network_fixtures import create_terminal, create_terminals
from zepben.evolve import NetworkService, AcLineSegment, PerLengthSequenceImpedance, PowerTransformer, BaseVoltage, OverheadWireInfo, PowerTransformerInfo, \
    EnergyConsumer, EnergySource, PowerElectronicsConnection


def simple_node_breaker_network() -> NetworkService:
    # Network
    network = NetworkService()

    # BaseVoltages
    bv_hv: BaseVoltage = BaseVoltage(mrid="20kV", nominal_voltage=20000, name="20kV")
    bv_lv: BaseVoltage = BaseVoltage(mrid="415V", nominal_voltage=400, name="415V")
    network.add(bv_hv)
    network.add(bv_lv)

    # PerLengthSequenceImpedance
    plsi = PerLengthSequenceImpedance(mrid="plsi", r=0.642 / 1000, x=0.083 / 1000)
    network.add(plsi)

    # WireInfo
    wire_info = OverheadWireInfo(mrid="wire_info", rated_current=0.142 * 1000)
    network.add(wire_info)

    # PowerTransformerInfo
    pt_info = PowerTransformerInfo(mrid="pt_info")
    network.add(pt_info)

    # EnergySource
    es = EnergySource(mrid="grid_connection", name="Grid Connection", voltage_magnitude=1.02 * bv_hv.nominal_voltage)
    es.base_voltage = bv_hv
    network.add(es)
    es_t = create_terminal(network, es)

    # Transformer
    tx = PowerTransformer(mrid="transformer", name="Transformer")
    tx.asset_info = pt_info
    network.add(tx)
    tx_terminals = create_terminals(network, tx, 2)

    ends = _create_transformer_ends(tx, [20000, 400])
    for end in ends:
        network.add(end)

    network.connect_terminals(tx_terminals[0], es_t)

    # Line
    line = AcLineSegment(mrid="line", name="Line", length=100.0, per_length_sequence_impedance=plsi)
    line.asset_info = wire_info
    line.base_voltage = bv_lv
    network.add(line)
    line_terminals = create_terminals(network, line, 2)

    network.connect_terminals(tx_terminals[1], line_terminals[0])

    # Load
    ec = EnergyConsumer(mrid="load", name="Load", p=100000., q=50000.)
    ec.base_voltage = bv_lv
    network.add(ec)
    ec_t = create_terminal(network, ec)

    network.connect_terminals(line_terminals[1], ec_t)

    # PowerElectronicsConnection
    pec = PowerElectronicsConnection(mrid="pec")
    pec.base_voltage = bv_lv
    network.add(pec)
    pec_t = create_terminal(network, pec)
    pec_t.mrid = "pec_t1"

    network.connect_by_mrid(pec_t, line_terminals[1].connectivity_node.mrid)

    return network
