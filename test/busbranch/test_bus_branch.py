#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Set, Union, FrozenSet, Tuple

import pytest

from zepben.evolve import ConnectivityNode, Junction, Disconnector, BusbarSection, Switch, Terminal, NetworkService, AcLineSegment, PerLengthSequenceImpedance, \
    WireInfo, PowerTransformer, EnergySource, EnergyConsumer, ConductingEquipment, create_bus_branch_model, PowerElectronicsConnection
from zepben.evolve.model.busbranch.bus_branch import _group_negligible_impedance_terminals, _group_common_ac_line_segment_terminals


def test_create_bus_branch_model_callbacks(simple_node_breaker_network):
    assert simple_node_breaker_network is not None

    plsi = simple_node_breaker_network.get("plsi")
    assert plsi is not None

    wire_info = simple_node_breaker_network.get("wire_info")
    assert wire_info is not None

    pt_info = simple_node_breaker_network.get("pt_info")
    assert pt_info is not None

    es = simple_node_breaker_network.get("grid_connection")
    assert es is not None

    pt = simple_node_breaker_network.get("transformer")
    assert pt is not None

    line = simple_node_breaker_network.get("line")
    assert line is not None

    ec = simple_node_breaker_network.get("load")
    assert ec is not None

    bus_args = set()
    branch_args = set()
    branch_type_args = set()
    transformer_args = set()
    transformer_type_args = set()
    source_args = set()
    consumer_args = set()
    pec_args = set()

    bb_model_network = "bb_model_network"

    def create_terminal_based_id(terminals: Union[Set[Terminal], FrozenSet[Terminal]]) -> str:
        return "_".join(sorted([t.mrid for t in terminals]))

    def create_bus_branch_network(n: NetworkService):
        return bb_model_network

    def create_bus(
            bus_branch_model: str,
            base_voltage: int,
            closed_switches: FrozenSet[ConductingEquipment],
            border_terminals: FrozenSet[Terminal],
            inner_terminals: FrozenSet[Terminal],
            node_breaker_model: NetworkService
    ) -> str:
        bus_args.add((bus_branch_model, base_voltage, closed_switches, border_terminals, inner_terminals, node_breaker_model))
        return create_terminal_based_id(border_terminals)

    def create_branch(
            bus_branch_model: str,
            line_busses: Tuple[str, str],
            length: float,
            line_type: str,
            common_lines: FrozenSet[AcLineSegment],
            border_terminals: FrozenSet[Terminal],
            inner_terminals: FrozenSet[Terminal],
            node_breaker_model: NetworkService
    ):
        branch_args.add((bus_branch_model, line_busses, length, line_type, common_lines, border_terminals, inner_terminals, node_breaker_model))

    def get_branch_type_id(per_length_sequence_impedance: PerLengthSequenceImpedance, wi: WireInfo, voltage: int) -> str:
        return wi.mrid + ":" + per_length_sequence_impedance.mrid

    def create_branch_type(bus_branch_model: str, per_length_sequence_impedance: PerLengthSequenceImpedance,
                           wi: WireInfo, voltage: int) -> str:
        branch_type_args.add((bus_branch_model, per_length_sequence_impedance, wire_info))
        return get_branch_type_id(per_length_sequence_impedance, wi, voltage)

    def create_transformer(bus_branch_model: str, pt: PowerTransformer, busses: Tuple[str, str],
                           pt_type: str, node_breaker_model: NetworkService):
        transformer_args.add((bus_branch_model, pt, busses, pt_type, node_breaker_model))

    def get_transformer_type_id(transformer: PowerTransformer) -> str:
        return transformer.mrid + "_type"

    def create_transformer_type(bus_branch_model: str, transformer: PowerTransformer) -> str:
        transformer_type_args.add((bus_branch_model, transformer))
        return get_transformer_type_id(transformer)

    def create_source(bus_branch_model: str, source: EnergySource, bus, node_breaker_model: NetworkService):
        source_args.add((bus_branch_model, source, bus, node_breaker_model))

    def create_consumer(bus_branch_model: str, consumer: EnergyConsumer, bus, node_breaker_model: NetworkService):
        consumer_args.add((bus_branch_model, consumer, bus, node_breaker_model))

    def create_power_electronics(bus_branch_model: str, power_electronics_connection: PowerElectronicsConnection, bus, node_breaker_model: NetworkService):
        pec_args.add((bus_branch_model, power_electronics_connection, bus, node_breaker_model))

    result = create_bus_branch_model(
        lambda: simple_node_breaker_network,
        create_bus_branch_network,
        create_bus,
        create_branch,
        create_branch_type,
        get_branch_type_id,
        create_transformer,
        create_transformer_type,
        get_transformer_type_id,
        create_source,
        create_consumer,
        create_power_electronics
    )

    assert result.was_successful is True

    # Validation
    # Bus
    _assert_are_equal(
        bus_args,
        {
            (bb_model_network, 400, frozenset(), frozenset({list(line.terminals)[0], list(pt.terminals)[1]}), frozenset(), simple_node_breaker_network),
            (bb_model_network, 400, frozenset(), frozenset({list(ec.terminals)[0], list(line.terminals)[1]}), frozenset(), simple_node_breaker_network),
            (bb_model_network, 20000, frozenset(), frozenset({list(es.terminals)[0], list(pt.terminals)[0]}), frozenset(), simple_node_breaker_network)
        }
    )

    # Branch
    _assert_are_equal(
        branch_args,
        {
            (
                bb_model_network,
                tuple((create_terminal_based_id(t.connectivity_node) for t in line.terminals)),
                100,
                "wire_info:plsi",
                frozenset({line}),
                frozenset({*line.terminals}),
                frozenset(),
                simple_node_breaker_network
            )
        }
    )

    # Branch Type
    _assert_are_equal(
        branch_type_args,
        {
            (bb_model_network, plsi, wire_info)
        }
    )

    # Transformer
    _assert_are_equal(
        transformer_args,
        {
            (
                bb_model_network,
                pt,
                tuple((create_terminal_based_id(t.connectivity_node) for t in pt.terminals)),
                "transformer_type",
                simple_node_breaker_network
            )
        }
    )

    # Transformer Type
    _assert_are_equal(
        transformer_type_args,
        {
            (bb_model_network, pt)
        }
    )

    # Source
    _assert_are_equal(
        source_args,
        {
            (
                bb_model_network,
                es,
                create_terminal_based_id(list(es.terminals)[0].connectivity_node),
                simple_node_breaker_network
            )
        }
    )

    # Consumer
    _assert_are_equal(
        consumer_args,
        {
            (
                bb_model_network,
                ec,
                create_terminal_based_id(list(ec.terminals)[0].connectivity_node),
                simple_node_breaker_network
            )
        }
    )

    # PowerElectronicsConnection
    _assert_are_equal(pec_args, set())


def test_create_bus_branch_model_callbacks_with_pec(simple_node_breaker_network_with_pec):
    assert simple_node_breaker_network_with_pec is not None

    plsi = simple_node_breaker_network_with_pec.get("plsi")
    assert plsi is not None

    wire_info = simple_node_breaker_network_with_pec.get("wire_info")
    assert wire_info is not None

    pt_info = simple_node_breaker_network_with_pec.get("pt_info")
    assert pt_info is not None

    es = simple_node_breaker_network_with_pec.get("grid_connection")
    assert es is not None

    pt = simple_node_breaker_network_with_pec.get("transformer")
    assert pt is not None

    line = simple_node_breaker_network_with_pec.get("line")
    assert line is not None

    ec = simple_node_breaker_network_with_pec.get("load")
    assert ec is not None

    pec = simple_node_breaker_network_with_pec.get("pec")
    assert pec is not None

    bus_args = set()
    branch_args = set()
    branch_type_args = set()
    transformer_args = set()
    transformer_type_args = set()
    source_args = set()
    consumer_args = set()
    pec_args = set()

    bb_model_network = "bb_model_network"

    def create_terminal_based_id(terminals: Union[Set[Terminal], FrozenSet[Terminal]]) -> str:
        return "_".join(sorted([t.mrid for t in terminals]))

    def create_bus_branch_network(n: NetworkService):
        return bb_model_network

    def create_bus(
            bus_branch_model: str,
            base_voltage: int,
            closed_switches: FrozenSet[ConductingEquipment],
            border_terminals: FrozenSet[Terminal],
            inner_terminals: FrozenSet[Terminal],
            node_breaker_model: NetworkService
    ) -> str:
        bus_args.add((bus_branch_model, base_voltage, closed_switches, border_terminals, inner_terminals, node_breaker_model))
        return create_terminal_based_id(border_terminals)

    def create_branch(
            bus_branch_model: str,
            line_busses: Tuple[str, str],
            length: float,
            line_type: str,
            common_lines: FrozenSet[AcLineSegment],
            border_terminals: FrozenSet[Terminal],
            inner_terminals: FrozenSet[Terminal],
            node_breaker_model: NetworkService
    ):
        branch_args.add((bus_branch_model, line_busses, length, line_type, common_lines, border_terminals, inner_terminals, node_breaker_model))

    def get_branch_type_id(per_length_sequence_impedance: PerLengthSequenceImpedance, wi: WireInfo, voltage: int) -> str:
        return wi.mrid + ":" + per_length_sequence_impedance.mrid

    def create_branch_type(bus_branch_model: str, per_length_sequence_impedance: PerLengthSequenceImpedance,
                           wi: WireInfo, voltage: int) -> str:
        branch_type_args.add((bus_branch_model, per_length_sequence_impedance, wire_info))
        return get_branch_type_id(per_length_sequence_impedance, wi, voltage)

    def create_transformer(bus_branch_model: str, pt: PowerTransformer, busses: Tuple[str, str],
                           pt_type: str, node_breaker_model: NetworkService):
        transformer_args.add((bus_branch_model, pt, busses, pt_type, node_breaker_model))

    def get_transformer_type_id(transformer: PowerTransformer) -> str:
        return transformer.mrid + "_type"

    def create_transformer_type(bus_branch_model: str, transformer: PowerTransformer) -> str:
        transformer_type_args.add((bus_branch_model, transformer))
        return get_transformer_type_id(transformer)

    def create_source(bus_branch_model: str, source: EnergySource, bus, node_breaker_model: NetworkService):
        source_args.add((bus_branch_model, source, bus, node_breaker_model))

    def create_consumer(bus_branch_model: str, consumer: EnergyConsumer, bus, node_breaker_model: NetworkService):
        consumer_args.add((bus_branch_model, consumer, bus, node_breaker_model))

    def create_power_electronics(bus_branch_model: str, power_electronics_connection: PowerElectronicsConnection, bus, node_breaker_model: NetworkService):
        pec_args.add((bus_branch_model, power_electronics_connection, bus, node_breaker_model))

    result = create_bus_branch_model(
        lambda: simple_node_breaker_network_with_pec,
        create_bus_branch_network,
        create_bus,
        create_branch,
        create_branch_type,
        get_branch_type_id,
        create_transformer,
        create_transformer_type,
        get_transformer_type_id,
        create_source,
        create_consumer,
        create_power_electronics
    )

    assert result.was_successful is True

    # Validation
    # Bus
    _assert_are_equal(
        bus_args,
        {
            (
                bb_model_network,
                400,
                frozenset(),
                frozenset({list(line.terminals)[0], list(pt.terminals)[1]}),
                frozenset(),
                simple_node_breaker_network_with_pec
            ),
            (
                bb_model_network,
                400,
                frozenset(),
                frozenset({list(ec.terminals)[0], list(line.terminals)[1], list(pec.terminals)[0]}),
                frozenset(),
                simple_node_breaker_network_with_pec
            ),
            (
                bb_model_network,
                20000,
                frozenset(),
                frozenset({list(es.terminals)[0], list(pt.terminals)[0]}),
                frozenset(),
                simple_node_breaker_network_with_pec
            )
        }
    )

    # Branch
    _assert_are_equal(
        branch_args,
        {
            (
                bb_model_network,
                tuple((create_terminal_based_id(t.connectivity_node) for t in line.terminals)),
                100,
                "wire_info:plsi",
                frozenset({line}),
                frozenset({*line.terminals}),
                frozenset(),
                simple_node_breaker_network_with_pec
            )
        }
    )

    # Branch Type
    _assert_are_equal(
        branch_type_args,
        {
            (bb_model_network, plsi, wire_info)
        }
    )

    # Transformer
    _assert_are_equal(
        transformer_args,
        {
            (
                bb_model_network,
                pt,
                tuple((create_terminal_based_id(t.connectivity_node) for t in pt.terminals)),
                "transformer_type",
                simple_node_breaker_network_with_pec
            )
        }
    )

    # Transformer Type
    _assert_are_equal(
        transformer_type_args,
        {
            (bb_model_network, pt)
        }
    )

    # Source
    _assert_are_equal(
        source_args,
        {
            (
                bb_model_network,
                es,
                create_terminal_based_id(list(es.terminals)[0].connectivity_node),
                simple_node_breaker_network_with_pec
            )
        }
    )

    # Consumer
    _assert_are_equal(
        consumer_args,
        {
            (
                bb_model_network,
                ec,
                create_terminal_based_id(list(ec.terminals)[0].connectivity_node),
                simple_node_breaker_network_with_pec
            )
        }
    )

    # PowerElectronicsConnection
    _assert_are_equal(
        pec_args,
        {
            (
                bb_model_network,
                pec,
                create_terminal_based_id(list(pec.terminals)[0].connectivity_node),
                simple_node_breaker_network_with_pec
            )
        }
    )


@pytest.mark.parametrize(
    'single_branch_common_lines_network',
    [False, True],
    indirect=True
)
def test_group_common_ac_line_segment_terminals_single_branch(single_branch_common_lines_network):
    assert single_branch_common_lines_network is not None

    acls1 = single_branch_common_lines_network.get("acls1")
    assert acls1 is not None
    acls2 = single_branch_common_lines_network.get("acls2")
    assert acls2 is not None
    acls3 = single_branch_common_lines_network.get("acls3")
    assert acls3 is not None
    acls4 = single_branch_common_lines_network.get("acls4")
    assert acls4 is not None
    acls5 = single_branch_common_lines_network.get("acls5")
    assert acls5 is not None

    # Validation
    # acls1, acls2, acls3
    for a in acls1, acls2, acls3:
        common_lines, inner_terms, border_terms = _group_common_ac_line_segment_terminals(a)
        _assert_are_equal(common_lines, {acls1, acls2, acls3})
        _assert_are_equal(inner_terms, {*acls1.terminals, *acls2.terminals, list(acls3.terminals)[0]})
        _assert_are_equal(border_terms, {list(acls3.terminals)[1]})

    # acls4
    common_lines, inner_terms, border_terms = _group_common_ac_line_segment_terminals(acls4)
    _assert_are_equal(common_lines, {acls4})
    _assert_are_equal(inner_terms, set())
    _assert_are_equal(border_terms, {*acls4.terminals})

    # acls5
    common_lines, inner_terms, border_terms = _group_common_ac_line_segment_terminals(acls5)
    _assert_are_equal(common_lines, {acls5})
    _assert_are_equal(inner_terms, set())
    _assert_are_equal(border_terms, {*acls5.terminals})


def test_group_common_ac_line_segment_terminals_multi_branch(multi_branch_common_lines_network):
    assert multi_branch_common_lines_network is not None

    a0 = multi_branch_common_lines_network.get("a0")
    assert a0 is not None
    a1 = multi_branch_common_lines_network.get("a1")
    assert a1 is not None
    a2 = multi_branch_common_lines_network.get("a2")
    assert a2 is not None
    a3 = multi_branch_common_lines_network.get("a3")
    assert a3 is not None
    a4 = multi_branch_common_lines_network.get("a4")
    assert a4 is not None
    a5 = multi_branch_common_lines_network.get("a5")
    assert a5 is not None
    a6 = multi_branch_common_lines_network.get("a6")
    assert a6 is not None
    a7 = multi_branch_common_lines_network.get("a7")
    assert a7 is not None
    a8 = multi_branch_common_lines_network.get("a8")
    assert a8 is not None

    # Validation
    # a0, a1, a2
    for a in a0, a1, a2:
        common_lines, inner_terms, border_terms = _group_common_ac_line_segment_terminals(a)
        _assert_are_equal(common_lines, {a0, a1, a2})
        _assert_are_equal(inner_terms, {list(a0.terminals)[0], *a1.terminals, list(a2.terminals)[0]})
        _assert_are_equal(border_terms, {list(a2.terminals)[1]})

    # a3
    common_lines, inner_terms, border_terms = _group_common_ac_line_segment_terminals(a3)
    _assert_are_equal(common_lines, {a3})
    _assert_are_equal(inner_terms, set())
    _assert_are_equal(border_terms, {*a3.terminals})

    # a4, a5
    for a in a4, a5:
        common_lines, inner_terms, border_terms = _group_common_ac_line_segment_terminals(a)
        _assert_are_equal(common_lines, {a4, a5})
        _assert_are_equal(inner_terms, {list(a4.terminals)[1], list(a5.terminals)[0]})
        _assert_are_equal(border_terms, {list(a4.terminals)[0], list(a5.terminals)[1]})

    # a6, a7
    for a in a6, a7:
        common_lines, inner_terms, border_terms = _group_common_ac_line_segment_terminals(a)
        _assert_are_equal(common_lines, {a6, a7})
        _assert_are_equal(inner_terms, {list(a6.terminals)[1], *a7.terminals})
        _assert_are_equal(border_terms, {list(a6.terminals)[0]})

    # a8
    common_lines, inner_terms, border_terms = _group_common_ac_line_segment_terminals(a8)
    _assert_are_equal(common_lines, {a8})
    _assert_are_equal(inner_terms, set())
    _assert_are_equal(border_terms, {*a8.terminals})


def test_group_common_ac_line_segment_terminals_end_of_branch_multiple_ec_pec(end_of_branch_multiple_ec_pec):
    assert end_of_branch_multiple_ec_pec is not None

    a1 = end_of_branch_multiple_ec_pec.get("a1")
    assert a1 is not None
    a2 = end_of_branch_multiple_ec_pec.get("a2")
    assert a2 is not None
    ec = end_of_branch_multiple_ec_pec.get("ec")
    assert ec is not None
    pec1 = end_of_branch_multiple_ec_pec.get("pec1")
    assert pec1 is not None
    pec2 = end_of_branch_multiple_ec_pec.get("pec2")
    assert pec2 is not None

    # Validation
    # a1, a2
    for a in a1, a2:
        common_lines, inner_terms, border_terms = _group_common_ac_line_segment_terminals(a)
        _assert_are_equal(common_lines, {a1, a2})
        _assert_are_equal(inner_terms, {list(a1.terminals)[1], list(a2.terminals)[0]})
        _assert_are_equal(border_terms, {list(a1.terminals)[0], list(a2.terminals)[1]})


@pytest.mark.parametrize(
    'single_branch_common_lines_network',
    [False],
    indirect=True
)
def test_group_negligible_impedance_terminals_single_branch_closed_switch(single_branch_common_lines_network):
    assert single_branch_common_lines_network is not None

    acls1 = single_branch_common_lines_network.get("acls1")
    assert acls1 is not None
    acls2 = single_branch_common_lines_network.get("acls2")
    assert acls2 is not None
    acls3 = single_branch_common_lines_network.get("acls3")
    assert acls3 is not None
    acls4 = single_branch_common_lines_network.get("acls4")
    assert acls4 is not None
    acls5 = single_branch_common_lines_network.get("acls5")
    assert acls5 is not None
    sw = single_branch_common_lines_network.get("sw")
    assert sw is not None

    def get_is_open(switch: Switch) -> bool:
        return switch.is_open()

    cn = {"_".join(sorted([t.conducting_equipment.mrid for t in cn.terminals])): cn for cn in single_branch_common_lines_network.objects(ConnectivityNode)}

    # Validation
    # a1_a2
    closed_switches, inner_terms, border_terms = _group_negligible_impedance_terminals(cn["acls1_acls2"], get_is_open)
    _assert_are_equal(closed_switches, set())
    _assert_are_equal(inner_terms, set())
    _assert_are_equal(border_terms, {list(acls2.terminals)[0], *acls1.terminals})

    # a2_a3
    closed_switches, inner_terms, border_terms = _group_negligible_impedance_terminals(cn["acls2_acls3"], get_is_open)
    _assert_are_equal(closed_switches, set())
    _assert_are_equal(inner_terms, set())
    _assert_are_equal(border_terms, {list(acls2.terminals)[1], list(acls3.terminals)[0]})

    # a3_sw
    closed_switches, inner_terms, border_terms = _group_negligible_impedance_terminals(cn["acls3_sw"], get_is_open)
    _assert_are_equal(closed_switches, {sw})
    _assert_are_equal(inner_terms, {*sw.terminals})
    _assert_are_equal(border_terms, {list(acls3.terminals)[1], list(acls4.terminals)[0]})

    # sw_a4
    closed_switches, inner_terms, border_terms = _group_negligible_impedance_terminals(cn["acls4_sw"], get_is_open)
    _assert_are_equal(closed_switches, {sw})
    _assert_are_equal(inner_terms, {*sw.terminals})
    _assert_are_equal(border_terms, {list(acls3.terminals)[1], list(acls4.terminals)[0]})

    # a4_a5
    closed_switches, inner_terms, border_terms = _group_negligible_impedance_terminals(cn["acls4_acls5"], get_is_open)
    _assert_are_equal(closed_switches, set())
    _assert_are_equal(inner_terms, set())
    _assert_are_equal(border_terms, {list(acls4.terminals)[1], *acls5.terminals})


@pytest.mark.parametrize(
    'single_branch_common_lines_network',
    [True],
    indirect=True
)
def test_group_negligible_impedance_terminals_single_branch_open_switch(single_branch_common_lines_network):
    assert single_branch_common_lines_network is not None

    acls1 = single_branch_common_lines_network.get("acls1")
    assert acls1 is not None
    acls2 = single_branch_common_lines_network.get("acls2")
    assert acls2 is not None
    acls3 = single_branch_common_lines_network.get("acls3")
    assert acls3 is not None
    acls4 = single_branch_common_lines_network.get("acls4")
    assert acls4 is not None
    acls5 = single_branch_common_lines_network.get("acls5")
    assert acls5 is not None
    sw = single_branch_common_lines_network.get("sw")
    assert sw is not None

    def get_is_open(switch: Switch) -> bool:
        return switch.is_open()

    cn = {"_".join(sorted([t.conducting_equipment.mrid for t in cn.terminals])): cn for cn in single_branch_common_lines_network.objects(ConnectivityNode)}

    # Validation
    # a1_a2
    closed_switches, inner_terms, border_terms = _group_negligible_impedance_terminals(cn["acls1_acls2"], get_is_open)
    _assert_are_equal(closed_switches, set())
    _assert_are_equal(inner_terms, set())
    _assert_are_equal(border_terms, {list(acls2.terminals)[0], *acls1.terminals})

    # a2_a3
    closed_switches, inner_terms, border_terms = _group_negligible_impedance_terminals(cn["acls2_acls3"], get_is_open)
    _assert_are_equal(closed_switches, set())
    _assert_are_equal(inner_terms, set())
    _assert_are_equal(border_terms, {list(acls2.terminals)[1], list(acls3.terminals)[0]})

    # a3_sw
    closed_switches, inner_terms, border_terms = _group_negligible_impedance_terminals(cn["acls3_sw"], get_is_open)
    _assert_are_equal(closed_switches, set())
    _assert_are_equal(inner_terms, set())
    _assert_are_equal(border_terms, {list(acls3.terminals)[1], list(sw.terminals)[0]})

    # sw_a4
    closed_switches, inner_terms, border_terms = _group_negligible_impedance_terminals(cn["acls4_sw"], get_is_open)
    _assert_are_equal(closed_switches, set())
    _assert_are_equal(inner_terms, set())
    _assert_are_equal(border_terms, {list(sw.terminals)[1], list(acls4.terminals)[0]})

    # a4_a5
    closed_switches, inner_terms, border_terms = _group_negligible_impedance_terminals(cn["acls4_acls5"], get_is_open)
    _assert_are_equal(closed_switches, set())
    _assert_are_equal(inner_terms, set())
    _assert_are_equal(border_terms, {list(acls4.terminals)[1], *acls5.terminals})


def test_group_negligible_impedance_terminals_multi_branch(multi_branch_common_lines_network):
    assert multi_branch_common_lines_network is not None

    a0 = multi_branch_common_lines_network.get("a0")
    assert a0 is not None
    a1 = multi_branch_common_lines_network.get("a1")
    assert a1 is not None
    a2 = multi_branch_common_lines_network.get("a2")
    assert a2 is not None
    a3 = multi_branch_common_lines_network.get("a3")
    assert a3 is not None
    a4 = multi_branch_common_lines_network.get("a4")
    assert a4 is not None
    a5 = multi_branch_common_lines_network.get("a5")
    assert a5 is not None
    a6 = multi_branch_common_lines_network.get("a6")
    assert a6 is not None
    a7 = multi_branch_common_lines_network.get("a7")
    assert a7 is not None
    a8 = multi_branch_common_lines_network.get("a8")
    assert a8 is not None

    def get_is_open(switch: Switch) -> bool:
        return switch.is_open()

    cn = {"_".join(sorted([t.conducting_equipment.mrid for t in cn.terminals])): cn for cn in multi_branch_common_lines_network.objects(ConnectivityNode)}

    # Validation
    # a0_a1
    closed_switches, inner_terms, border_terms = _group_negligible_impedance_terminals(cn["a0_a1"], get_is_open)
    _assert_are_equal(closed_switches, set())
    _assert_are_equal(inner_terms, set())
    _assert_are_equal(border_terms, {list(a1.terminals)[0], *a0.terminals})

    # a1_a2
    closed_switches, inner_terms, border_terms = _group_negligible_impedance_terminals(cn["a1_a2"], get_is_open)
    _assert_are_equal(closed_switches, set())
    _assert_are_equal(inner_terms, set())
    _assert_are_equal(border_terms, {list(a1.terminals)[1], list(a2.terminals)[0]})

    # a2_a3_a6
    closed_switches, inner_terms, border_terms = _group_negligible_impedance_terminals(cn["a2_a3_a6"], get_is_open)
    _assert_are_equal(closed_switches, set())
    _assert_are_equal(inner_terms, set())
    _assert_are_equal(border_terms, {list(a2.terminals)[1], list(a3.terminals)[0], list(a6.terminals)[0]})

    # a3_a4_a8
    closed_switches, inner_terms, border_terms = _group_negligible_impedance_terminals(cn["a3_a4_a8"], get_is_open)
    _assert_are_equal(closed_switches, set())
    _assert_are_equal(inner_terms, set())
    _assert_are_equal(border_terms, {list(a3.terminals)[1], list(a4.terminals)[0], *a8.terminals})

    # a4_a5
    closed_switches, inner_terms, border_terms = _group_negligible_impedance_terminals(cn["a4_a5"], get_is_open)
    _assert_are_equal(closed_switches, set())
    _assert_are_equal(inner_terms, set())
    _assert_are_equal(border_terms, {list(a4.terminals)[1], list(a5.terminals)[0]})

    # a6_a7
    closed_switches, inner_terms, border_terms = _group_negligible_impedance_terminals(cn["a6_a7"], get_is_open)
    _assert_are_equal(closed_switches, set())
    _assert_are_equal(inner_terms, set())
    _assert_are_equal(border_terms, {list(a6.terminals)[1], *a7.terminals})


@pytest.mark.parametrize(
    'negligible_impedance_equipment_basic_network',
    [
        lambda mrid: Junction(mrid=mrid),
        lambda mrid: Disconnector(mrid=mrid),
        lambda mrid: BusbarSection(mrid=mrid)
    ],
    indirect=True
)
def test_group_negligible_impedance_terminals_groups_negligible_impedance_equipment(negligible_impedance_equipment_basic_network):
    assert negligible_impedance_equipment_basic_network is not None

    nie1 = negligible_impedance_equipment_basic_network.get("nie1")
    assert nie1 is not None
    nie2 = negligible_impedance_equipment_basic_network.get("nie2")
    assert nie2 is not None
    a0 = negligible_impedance_equipment_basic_network.get("a0")
    assert a0 is not None
    a1 = negligible_impedance_equipment_basic_network.get("a1")
    assert a1 is not None
    a2 = negligible_impedance_equipment_basic_network.get("a2")
    assert a2 is not None
    a3 = negligible_impedance_equipment_basic_network.get("a3")
    assert a3 is not None
    a4 = negligible_impedance_equipment_basic_network.get("a4")
    assert a4 is not None
    a5 = negligible_impedance_equipment_basic_network.get("a5")

    def get_is_open(switch: Switch) -> bool:
        return switch.is_open()

    cn = {"_".join(sorted([t.conducting_equipment.mrid for t in cn.terminals])): cn for cn in
          negligible_impedance_equipment_basic_network.objects(ConnectivityNode)}

    # Validation
    # a0_nie1
    ni_equipment, inner_terms, border_terms = _group_negligible_impedance_terminals(cn["a0_nie1"], get_is_open)
    _assert_are_equal(ni_equipment, {nie1})
    _assert_are_equal(inner_terms, {*nie1.terminals})
    _assert_are_equal(border_terms, {list(a1.terminals)[0], *a0.terminals})

    # j1_a1
    ni_equipment, inner_terms, border_terms = _group_negligible_impedance_terminals(cn["a1_nie1"], get_is_open)
    _assert_are_equal(ni_equipment, {nie1})
    _assert_are_equal(inner_terms, {*nie1.terminals})
    _assert_are_equal(border_terms, {list(a1.terminals)[0], *a0.terminals})

    # a1_a2
    ni_equipment, inner_terms, border_terms = _group_negligible_impedance_terminals(cn["a1_a2"], get_is_open)
    _assert_are_equal(ni_equipment, set())
    _assert_are_equal(inner_terms, set())
    _assert_are_equal(border_terms, {list(a1.terminals)[1], list(a2.terminals)[0]})

    # a2_nie2
    ni_equipment, inner_terms, border_terms = _group_negligible_impedance_terminals(cn["a2_nie2"], get_is_open)
    _assert_are_equal(ni_equipment, {nie2})
    _assert_are_equal(inner_terms, {*nie2.terminals})
    _assert_are_equal(border_terms, {list(a2.terminals)[1], list(a3.terminals)[0], list(a4.terminals)[0]})

    # a3_nie2
    ni_equipment, inner_terms, border_terms = _group_negligible_impedance_terminals(cn["a3_nie2"], get_is_open)
    _assert_are_equal(ni_equipment, {nie2})
    _assert_are_equal(inner_terms, {*nie2.terminals})
    _assert_are_equal(border_terms, {list(a2.terminals)[1], list(a3.terminals)[0], list(a4.terminals)[0]})

    # a4_nie2
    ni_equipment, inner_terms, border_terms = _group_negligible_impedance_terminals(cn["a4_nie2"], get_is_open)
    _assert_are_equal(ni_equipment, {nie2})
    _assert_are_equal(inner_terms, {*nie2.terminals})
    _assert_are_equal(border_terms, {list(a2.terminals)[1], list(a3.terminals)[0], list(a4.terminals)[0]})

    # a4_a5
    ni_equipment, inner_terms, border_terms = _group_negligible_impedance_terminals(cn["a4_a5"], get_is_open)
    _assert_are_equal(ni_equipment, set())
    _assert_are_equal(inner_terms, set())
    _assert_are_equal(border_terms, {list(a4.terminals)[1], *a5.terminals})


def test_group_negligible_impedance_terminals_end_of_branch_multiple_ec_pec(end_of_branch_multiple_ec_pec):
    assert end_of_branch_multiple_ec_pec is not None

    a1 = end_of_branch_multiple_ec_pec.get("a1")
    assert a1 is not None
    a2 = end_of_branch_multiple_ec_pec.get("a2")
    assert a2 is not None
    ec = end_of_branch_multiple_ec_pec.get("ec")
    assert ec is not None
    pec1 = end_of_branch_multiple_ec_pec.get("pec1")
    assert pec1 is not None
    pec2 = end_of_branch_multiple_ec_pec.get("pec2")
    assert pec2 is not None

    def get_is_open(switch: Switch) -> bool:
        return switch.is_open()

    cn = {"_".join(sorted([t.conducting_equipment.mrid for t in cn.terminals])): cn for cn in end_of_branch_multiple_ec_pec.objects(ConnectivityNode)}

    # Validation
    # a2_ec
    closed_switches, inner_terms, border_terms = _group_negligible_impedance_terminals(cn["a2_ec_pec1_pec2"], get_is_open)
    _assert_are_equal(closed_switches, set())
    _assert_are_equal(inner_terms, set())
    _assert_are_equal(border_terms, {list(a2.terminals)[1], list(ec.terminals)[0], list(pec1.terminals)[0], list(pec2.terminals)[0]})


def _assert_are_equal(a: Union[Set, FrozenSet], b: Union[Set, FrozenSet]):
    diff = a ^ b
    assert not diff, f"Sets {a} and {b} are different"


def _assert_sets_of_sets_are_equal(a: Union[Set, FrozenSet], b: Union[Set, FrozenSet]):
    b_c = b.copy()
    for cl in a:
        matched_group = None
        for ex_g in b_c:
            diff = cl ^ ex_g
            if not diff:
                matched_group = ex_g
                break
        if matched_group is not None:
            b_c.remove(matched_group)
    assert len(b_c) == 0, f"Sets are not equal. Number of non-matching elements: {len(b_c)}"
