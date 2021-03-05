from typing import List

from pytest import fixture
from zepben.evolve import PhaseCode, NetworkService, Terminal, ConductingEquipment, AcLineSegment, PerLengthSequenceImpedance, \
    PowerTransformer, PowerTransformerEnd, Breaker, BaseVoltage, OverheadWireInfo, PowerTransformerInfo, EnergyConsumer, EnergySource
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
    es_t = _create_terminal(es)
    network.add(es_t)

    # Transformer
    tx = PowerTransformer(mrid="transformer", name="Transformer")
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
    line = AcLineSegment(mrid="line", name="Line", length=100.0, per_length_sequence_impedance=plsi)
    line.asset_info = wire_info
    line.base_voltage = bv_lv
    line_terminals = _create_terminals(line)
    for t in line_terminals:
        network.add(t)
    network.add(line)

    network.connect_terminals(tx_terminals[1], line_terminals[0])

    # Load
    ec = EnergyConsumer(mrid="load", name="Load", p=100000., q=50000.)
    ec.base_voltage = bv_lv
    network.add(ec)
    ec_t = _create_terminal(ec)
    network.add(ec_t)

    network.connect_terminals(line_terminals[1], ec_t)

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
    a0_t = _create_terminal(a0)
    network.add(a0_t)
    network.add(a0)

    # AcLineSegment1
    a1 = AcLineSegment(mrid="a1", length=1.0, per_length_sequence_impedance=plsi)
    a1_ts = _create_terminals(a1)
    for t in a1_ts:
        network.add(t)
    network.add(a1)

    network.connect_terminals(a0_t, a1_ts[0])

    # AcLineSegment2
    a2 = AcLineSegment(mrid="a2", length=2.0, per_length_sequence_impedance=plsi)
    a2_ts = _create_terminals(a2)
    for t in a2_ts:
        network.add(t)
    network.add(a2)

    network.connect_terminals(a1_ts[1], a2_ts[0])

    # AcLineSegment3
    a3 = AcLineSegment(mrid="a3", length=3.0, per_length_sequence_impedance=plsi)
    a3_ts = _create_terminals(a3)
    for t in a3_ts:
        network.add(t)
    network.add(a3)

    network.connect_terminals(a2_ts[1], a3_ts[0])

    # AcLineSegment4
    a4 = AcLineSegment(mrid="a4", length=4.0, per_length_sequence_impedance=plsi)
    a4_ts = _create_terminals(a4)
    for t in a4_ts:
        network.add(t)
    network.add(a4)

    network.connect_terminals(a3_ts[1], a4_ts[0])

    # AcLineSegment5
    a5 = AcLineSegment(mrid="a5", length=5.0, per_length_sequence_impedance=plsi)
    a5_ts = _create_terminals(a5)
    for t in a5_ts:
        network.add(t)
    network.add(a5)

    network.connect_terminals(a4_ts[1], a5_ts[0])

    # AcLineSegment6
    a6 = AcLineSegment(mrid="a6", length=6.0, per_length_sequence_impedance=plsi)
    a6_ts = _create_terminals(a6)
    for t in a6_ts:
        network.add(t)
    network.add(a6)

    connect(a6_ts[0], a2_ts[1].connectivity_node)

    # AcLineSegment7
    a7 = AcLineSegment(mrid="a7", length=7.0, per_length_sequence_impedance=plsi)
    a7_t = _create_terminal(a7)
    network.add(a7_t)
    network.add(a7)

    network.connect_terminals(a6_ts[1], a7_t)

    # AcLineSegment8
    a8 = AcLineSegment(mrid="a8", length=8.0, per_length_sequence_impedance=plsi)
    a8_t = _create_terminal(a8)
    network.add(a8_t)
    network.add(a8)

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
    acls1_t = _create_terminal(acls1)
    network.add(acls1_t)
    network.add(acls1)

    # AcLineSegment2
    acls2 = AcLineSegment(mrid="acls2", length=2.0, per_length_sequence_impedance=plsi1)
    acls2_terminals = _create_terminals(acls2)
    for t in acls2_terminals:
        network.add(t)
    network.add(acls2)

    network.connect_terminals(acls1_t, acls2_terminals[0])

    # AcLineSegment3
    acls3 = AcLineSegment(mrid="acls3", length=3.0, per_length_sequence_impedance=plsi1)
    acls3_terminals = _create_terminals(acls3)
    for t in acls3_terminals:
        network.add(t)
    network.add(acls3)

    network.connect_terminals(acls2_terminals[1], acls3_terminals[0])

    # SW
    sw = Breaker(mrid="sw")
    sw.set_open(sw_is_open)
    sw.set_normally_open(sw_is_open)
    sw_terminals = _create_terminals(sw)
    for t in sw_terminals:
        network.add(t)
    network.add(sw)
    network.connect_terminals(acls3_terminals[1], sw_terminals[0])

    # AcLineSegment4
    acls4 = AcLineSegment(mrid="acls4", length=4.0, per_length_sequence_impedance=plsi2)
    acls4_terminals = _create_terminals(acls4)
    for t in acls4_terminals:
        network.add(t)
    network.add(acls4)

    network.connect_terminals(sw_terminals[1], acls4_terminals[0])

    # AcLineSegment5
    acls5 = AcLineSegment(mrid="acls5", length=5.0, per_length_sequence_impedance=plsi3)
    acls5_t = _create_terminal(acls5)
    network.add(acls5_t)
    network.add(acls5)

    network.connect_terminals(acls4_terminals[1], acls5_t)

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
    a0_t = _create_terminal(a0)
    network.add(a0_t)
    network.add(a0)

    # NegligibleImpedanceEquipment1
    nie1 = nie_constructor("nie1")
    nie1_ts = _create_terminals(nie1)
    network.add(nie1)
    for t in nie1_ts:
        network.add(t)

    network.connect_terminals(a0_t, nie1_ts[0])

    # AcLineSegment1
    a1 = AcLineSegment(mrid="a1", length=1.0, per_length_sequence_impedance=plsi)
    a1_ts = _create_terminals(a1)
    for t in a1_ts:
        network.add(t)
    network.add(a1)

    network.connect_terminals(nie1_ts[1], a1_ts[0])

    # AcLineSegment2
    a2 = AcLineSegment(mrid="a2", length=2.0, per_length_sequence_impedance=plsi)
    a2_ts = _create_terminals(a2)
    for t in a2_ts:
        network.add(t)
    network.add(a2)

    network.connect_terminals(a1_ts[1], a2_ts[0])

    # NegligibleImpedanceEquipment2
    nie2 = nie_constructor("nie2")
    nie2_ts = _create_terminals(nie2, [PhaseCode.ABC, PhaseCode.ABC, PhaseCode.ABC])
    network.add(nie2)
    for t in nie2_ts:
        network.add(t)

    network.connect_terminals(a2_ts[1], nie2_ts[0])

    # AcLineSegment3
    a3 = AcLineSegment(mrid="a3", length=3.0, per_length_sequence_impedance=plsi)
    a3_ts = _create_terminals(a3)
    for t in a3_ts:
        network.add(t)
    network.add(a3)

    network.connect_terminals(nie2_ts[1], a3_ts[0])

    # AcLineSegment4
    a4 = AcLineSegment(mrid="a4", length=4.0, per_length_sequence_impedance=plsi)
    a4_ts = _create_terminals(a4)
    for t in a4_ts:
        network.add(t)
    network.add(a4)

    network.connect_terminals(nie2_ts[2], a4_ts[0])

    # AcLineSegment5
    a5 = AcLineSegment(mrid="a5", length=5.0, per_length_sequence_impedance=plsi)
    a5_t = _create_terminal(a5)
    network.add(a5)
    network.add(a5_t)

    network.connect_terminals(a4_ts[1], a5_t)

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
