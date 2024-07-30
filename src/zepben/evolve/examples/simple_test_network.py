#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
__all__ = ["simple_test_network"]

from typing import List

from zepben.evolve import NetworkService, BaseVoltage, PerLengthSequenceImpedance, OverheadWireInfo, \
    PowerTransformerInfo, PhaseCode, EnergySourcePhase, EnergySource, PowerTransformer, PowerTransformerEnd, Terminal, \
    ConductingEquipment, EnergyConsumer, AcLineSegment, PositionPoint, Location


async def simple_test_network() -> NetworkService:
    # Network
    network = NetworkService()

    # BaseVoltages
    bv_hv: BaseVoltage = BaseVoltage(mrid="20kV", nominal_voltage=20000, name="20kV")
    bv_lv: BaseVoltage = BaseVoltage(mrid="415V", nominal_voltage=400, name="415V")
    network.add(bv_hv)
    network.add(bv_lv)
    point1 = PositionPoint(x_position=149.12791965570293, y_position=-35.277592101000934)
    point2 = PositionPoint(x_position=149.12779472660375, y_position=-35.278183862759285)
    point3 = PositionPoint(x_position=149.12840360920450, y_position=-35.277171304657690)

    loc1 = Location().add_point(point1)
    loc2 = Location().add_point(point2)
    loc3 = Location().add_point(point3)

    # PerLengthSequenceImpedance
    plsi = PerLengthSequenceImpedance(
        mrid="psli",
        r=0.642 / 1000,
        x=0.083 / 1000
    )
    network.add(plsi)

    # WireInfo
    wire_info = OverheadWireInfo(
        mrid="wire_info",
        rated_current=0.142 * 1000
    )
    network.add(wire_info)

    # PowerTransformerInfo
    pt_info = PowerTransformerInfo(
        mrid="pt_info"
    )
    network.add(pt_info)

    # EnergySource
    energy_source_phases = []
    for sp in PhaseCode.ABC.single_phases:
        esp = EnergySourcePhase()
        esp.phase = sp
        energy_source_phases.append(esp)
        network.add(esp)
    es = EnergySource(
        mrid="grid_connection",
        name="Grid Connection",
        voltage_magnitude=1.02 * bv_hv.nominal_voltage,
        energy_source_phases=energy_source_phases,
        location=loc1
    )

    es.base_voltage = bv_hv
    network.add(es)
    es_t = _create_terminal(es)
    network.add(es_t)

    # Transformer
    tx = PowerTransformer(mrid="transformer", name="Transformer", location=loc1)
    tx.asset_info = pt_info
    tx_terminals = _create_terminals(tx, [PhaseCode.ABC, PhaseCode.ABN])
    for t in tx_terminals:
        network.add(t)
    network.add(tx)

    ends = _create_transformer_ends(tx, [20000, 400])
    for end in ends:
        network.add(end)

    network.connect_terminals(tx_terminals[0], es_t)

    # Line
    line_location = Location().add_point(point2).add_point(point3)
    network.add(line_location)
    line = AcLineSegment(mrid="line", name="Line", length=100.0, per_length_sequence_impedance=plsi,
                         location=line_location)
    line.asset_info = wire_info
    line.base_voltage = bv_lv
    line_terminals = _create_terminals(line)
    for t in line_terminals:
        network.add(t)
    network.add(line)

    network.connect_terminals(tx_terminals[1], line_terminals[0])

    # Load
    ec = EnergyConsumer(mrid="load", name="Load", p=100000., q=50000., location=loc3)
    ec.base_voltage = bv_lv
    network.add(ec)
    ec_t = _create_terminal(ec)
    network.add(ec_t)

    network.connect_terminals(line_terminals[1], ec_t)

    await network.set_phases()
    return network


def _create_terminal(ce: ConductingEquipment, phases: PhaseCode = PhaseCode.ABC) -> Terminal:
    return _create_terminals(ce, [phases])[0]


def _create_terminals(ce: ConductingEquipment, phases_per_term: List[PhaseCode] = None) -> List[Terminal]:
    if phases_per_term is None:
        phases_per_term = [PhaseCode.ABC, PhaseCode.ABC]

    terminals: List[Terminal] = []
    for i in range(0, len(phases_per_term)):
        terminal = Terminal(
            mrid=f"{ce.mrid}_t{i + 1}",
            conducting_equipment=ce,
            phases=phases_per_term[i],
            sequence_number=i + 1
        )
        ce.add_terminal(terminal)
        terminals.append(terminal)
    return terminals


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
