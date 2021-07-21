#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List

from pytest import fixture

from test.network_fixtures import create_terminal, create_terminals
from zepben.evolve import NetworkService, AcLineSegment, PerLengthSequenceImpedance, \
    PowerTransformer, PowerTransformerEnd, Breaker, BaseVoltage, OverheadWireInfo, PowerTransformerInfo, EnergyConsumer, EnergySource, \
    PowerElectronicsConnection, Junction
from zepben.evolve.services.network.network import connect


@fixture()
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


@fixture()
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


@fixture()
def single_branch_common_lines_network(request) -> NetworkService:
    """
      acls1     acls2     acls3            acls4     acls5 
     --------+---------+---------+  sw  +---------+--------
    |           psli1            |      |  psli2  | psli3 |
    """
    # Network
    network = NetworkService()
    sw_is_open = request.param or False

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


@fixture()
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


@fixture()
def negligible_impedance_equipment_basic_network(request) -> NetworkService:
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

    nie_constructor = request.param

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


@fixture()
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


def _create_per_length_sequence_impedance(i: float) -> PerLengthSequenceImpedance:
    return PerLengthSequenceImpedance(mrid=f"plsi{i}", r=i, x=i, bch=i, gch=i, r0=i, x0=i, b0ch=i, g0ch=i)


def _create_transformer_ends(tx: PowerTransformer, voltages: List[int] = None) -> List[PowerTransformerEnd]:
    if voltages is None:
        voltages = [11000, 415]

    ends = []
    for i in range(0, len(voltages)):
        end = PowerTransformerEnd(mrid=f"{tx.mrid}_e{i + 1}", power_transformer=tx, rated_u=voltages[i])
        terminal = tx.get_terminal_by_sn(i + 1)

        if terminal is None:
            raise ValueError(f"No terminal found to attach transformer end {end.mrid} in power transformer {tx.mrid}")

        tx.add_end(end)
        end.terminal = terminal
        ends.append(end)

    return ends
