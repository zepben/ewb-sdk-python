#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Set, Union, FrozenSet

import pytest

from test.busbranch.test_bus_branch_creator import TestBusBranchCreator, create_terminal_based_id
from zepben.evolve import ConnectivityNode, Junction, Disconnector, BusbarSection, Switch, ConductingEquipment, AcLineSegment, BusBranchNetworkCreationMappings
from zepben.evolve.model.busbranch.bus_branch import _group_negligible_impedance_terminals, _group_common_ac_line_segment_terminals


@pytest.mark.asyncio
async def test_create_bus_branch_model_callbacks(simple_node_breaker_network):
    nb_network = simple_node_breaker_network
    plsi, wire_info, pt_info, es, pt, line, ec, pec = _get_validated_conducting_equipment(nb_network)

    creator = TestBusBranchCreator()
    result = await creator.create(nb_network)

    was_successful, validator, mappings, bb_network = _get_validated_results(result)

    expected_bus_0, \
    expected_bus_1, \
    expected_bus_2, \
    expected_branch, \
    expected_transformer, \
    expected_energy_source, \
    expected_energy_consumer, \
    expected_power_electronics_connection = _get_expected(nb_network, line, pt, es, ec, pec)

    _validate_validator_calls(validator)
    _validate_network(bb_network, expected_bus_0, expected_bus_1, expected_bus_2, expected_branch, expected_transformer, expected_energy_source,
                      expected_energy_consumer, expected_power_electronics_connection)
    _validate_mappings(mappings, expected_bus_0, expected_bus_1, expected_bus_2, expected_branch, expected_transformer, expected_energy_source,
                       expected_energy_consumer, expected_power_electronics_connection, line, pt, es, ec, pec)


def _get_expected(
    nb_network,
    line,
    pt,
    es,
    ec,
    pec
):
    # -- Bus
    expected_bus_0 = (
        create_terminal_based_id({next(es.terminals), list(pt.terminals)[0]}),
        (
            20000,
            frozenset(),
            frozenset({list(es.terminals)[0], list(pt.terminals)[0]}),
            frozenset(),
            nb_network
        )
    )
    expected_bus_1 = (
        create_terminal_based_id({list(pt.terminals)[1], list(line.terminals)[0]}),
        (
            400,
            frozenset(),
            frozenset({list(line.terminals)[0], list(pt.terminals)[1]}),
            frozenset(),
            nb_network
        )
    )
    expected_bus_2 = (
        create_terminal_based_id({list(line.terminals)[1], next(ec.terminals), next(pec.terminals)}),
        (
            400,
            frozenset(),
            frozenset({list(ec.terminals)[0], list(line.terminals)[1], list(pec.terminals)[0]}),
            frozenset(),
            nb_network
        )
    )

    # -- Branch
    expected_branch = (
        f"tb_{line.mrid}",
        (
            (expected_bus_1[1], expected_bus_2[1]),
            100,
            frozenset({line}),
            frozenset({*line.terminals}),
            frozenset(),
            nb_network
        )
    )

    # -- Transformer
    expected_end_to_bus_pairs = ((list(pt.ends)[0], expected_bus_0[1]), (list(pt.ends)[1], expected_bus_1[1]))
    expected_transformer = (
        f"pt_{pt.mrid}",
        (
            pt,
            expected_end_to_bus_pairs,
            nb_network
        )
    )

    # -- Source
    expected_energy_source = (
        f"es_{es.mrid}",
        (
            es,
            expected_bus_0[1],
            nb_network
        )
    )

    # -- Consumer
    expected_energy_consumer = (
        f"ec_{ec.mrid}",
        (
            ec,
            expected_bus_2[1],
            nb_network
        )
    )

    # -- PowerElectronicsConnection
    expected_power_electronics_connection = (
        f"pec_{pec.mrid}",
        (
            pec,
            expected_bus_2[1],
            nb_network
        )
    )

    return expected_bus_0, expected_bus_1, expected_bus_2, expected_branch, expected_transformer, expected_energy_source, expected_energy_consumer, expected_power_electronics_connection


def _get_validated_results(result):
    was_successful = result.was_successful
    validator = result.validator
    mappings = result.mappings
    bb_network = result.network

    assert was_successful is True
    assert validator is not None
    assert mappings is not None
    assert bb_network is not None

    return was_successful, validator, mappings, bb_network


def _get_validated_conducting_equipment(nb_network):
    assert nb_network is not None

    plsi = nb_network.get("plsi")
    assert plsi is not None

    wire_info = nb_network.get("wire_info")
    assert wire_info is not None

    pt_info = nb_network.get("pt_info")
    assert pt_info is not None

    es = nb_network.get("grid_connection")
    assert es is not None

    pt = nb_network.get("transformer")
    assert pt is not None

    line = nb_network.get("line")
    assert line is not None

    ec = nb_network.get("load")
    assert ec is not None

    pec = nb_network.get("pec")
    assert pec is not None

    return plsi, wire_info, pt_info, es, pt, line, ec, pec


def _validate_validator_calls(validator):
    assert validator.network_data_count is 1
    assert validator.topological_node_data_count is 3
    assert validator.topological_branch_data_count is 1
    assert validator.power_transformer_data_count is 1
    assert validator.energy_source_data_count is 1
    assert validator.energy_consumer_data_count is 1
    assert validator.power_electronics_connection_data_count is 1


def _validate_network(
    bb_network,
    expected_bus_0,
    expected_bus_1,
    expected_bus_2,
    expected_branch,
    expected_transformer,
    expected_energy_source,
    expected_energy_consumer,
    expected_power_electronics_connection,
):
    _assert_are_equal(bb_network.bus, {expected_bus_0, expected_bus_1, expected_bus_2})

    # Branch Comparison
    branch = list(bb_network.branch)[0]
    assert branch[0] == expected_branch[0]
    _assert_are_equal(set(branch[1][0]), set(expected_branch[1][0]))
    assert branch[1][1] == expected_branch[1][1]
    assert branch[1][2] == expected_branch[1][2]
    assert branch[1][3] == expected_branch[1][3]
    assert branch[1][4] == expected_branch[1][4]
    assert branch[1][5] == expected_branch[1][5]

    _assert_are_equal(bb_network.transformer, {expected_transformer})
    _assert_are_equal(bb_network.energy_source, {expected_energy_source})
    _assert_are_equal(bb_network.energy_consumer, {expected_energy_consumer})
    _assert_are_equal(bb_network.power_electronics_connection, {expected_power_electronics_connection})


def _validate_mappings(
    mappings: BusBranchNetworkCreationMappings,
    expected_bus_0,
    expected_bus_1,
    expected_bus_2,
    expected_branch,
    expected_transformer,
    expected_energy_source,
    expected_energy_consumer,
    expected_power_electronics_connection,
    line,
    pt,
    es,
    ec,
    pec
):
    # -- Bus
    _validate_bus_mapping(mappings, expected_bus_0)
    _validate_bus_mapping(mappings, expected_bus_1)
    _validate_bus_mapping(mappings, expected_bus_2)

    # -- Branch
    _validate_branch_mapping(mappings, expected_branch)

    assert list(mappings.to_nbn.power_transformers[expected_transformer[0]])[0] is pt
    assert list(mappings.to_nbn.energy_sources[expected_energy_source[0]])[0] is es
    assert list(mappings.to_nbn.energy_consumers[expected_energy_consumer[0]])[0] is ec
    assert list(mappings.to_nbn.power_electronics_connections[expected_power_electronics_connection[0]])[0] is pec

    # -- Identified Objects
    # --- inner terminals and collapsed conducting equipment maps to bus
    for io in (*expected_bus_0[1][1], *expected_bus_0[1][3]):
        _assert_equal_bus(mappings.to_bbn.objects[io.mrid], expected_bus_0)

    for io in (*expected_bus_1[1][1], *expected_bus_1[1][3]):
        _assert_equal_bus(mappings.to_bbn.objects[io.mrid], expected_bus_1)

    for io in (*expected_bus_2[1][1], *expected_bus_2[1][3]):
        _assert_equal_bus(mappings.to_bbn.objects[io.mrid], expected_bus_2)

    # --- branch
    assert set(list(mappings.to_bbn.objects[line.mrid])[0][0]) == set(expected_branch[1][0])
    assert list(mappings.to_bbn.objects[line.mrid])[0][1] == expected_branch[1][1]
    assert list(mappings.to_bbn.objects[line.mrid])[0][2] == expected_branch[1][2]
    assert list(mappings.to_bbn.objects[line.mrid])[0][3] == expected_branch[1][3]
    assert list(mappings.to_bbn.objects[line.mrid])[0][4] == expected_branch[1][4]
    assert list(mappings.to_bbn.objects[line.mrid])[0][5] == expected_branch[1][5]

    # --- transformer
    assert list(mappings.to_bbn.objects[pt.mrid])[0] == expected_transformer[1]

    # --- energy source
    assert list(mappings.to_bbn.objects[es.mrid])[0] == expected_energy_source[1]

    # --- energy consumer
    assert list(mappings.to_bbn.objects[ec.mrid])[0] == expected_energy_consumer[1]

    # --- power electronics connection
    assert list(mappings.to_bbn.objects[pec.mrid])[0] == expected_power_electronics_connection[1]


def _validate_branches_are_equal(a, b):
    assert a[0][0][0] == b[0][0][0]

    assert a[1] == b[1]
    assert a[2] == b[2]
    _assert_are_equal(a[3], b[3])
    _assert_are_equal(a[4], b[4])
    _assert_are_equal(a[5], b[5])
    assert a[6] is b[6]


def _validate_bus_mapping(mappings, expected_bus):
    mapped_tn = mappings.to_nbn.topological_nodes[expected_bus[0]]
    _assert_equal_bus(mapped_tn, expected_bus)
    assert [list(mappings.to_bbn.objects[t.mrid])[0] for t in mapped_tn.terminals()][0] == expected_bus[1]

    if mapped_tn.conducting_equipment_group:
        assert [list(mappings.to_bbn.objects[ce.mrid])[0] for ce in mapped_tn.conducting_equipment_group][0] == expected_bus[1]


def _assert_equal_bus(terminal_grouping, expected_bus):
    assert terminal_grouping.conducting_equipment_group == expected_bus[1][1]
    assert terminal_grouping.border_terminals == expected_bus[1][2]
    assert terminal_grouping.inner_terminals == expected_bus[1][3]


def _validate_branch_mapping(mappings, expected_branch):
    mapped_branch = mappings.to_nbn.topological_branches[expected_branch[0]]
    _assert_equal_branch(mapped_branch, expected_branch)


def _assert_equal_branch(terminal_grouping, expected_branch):
    assert terminal_grouping.conducting_equipment_group == expected_branch[1][2]
    assert terminal_grouping.border_terminals == expected_branch[1][3]
    assert terminal_grouping.inner_terminals == expected_branch[1][4]


@pytest.mark.asyncio
async def test_topological_nodes_inside_grouped_lines_do_not_get_created(three_common_lines_network):
    nb_network = three_common_lines_network
    creator = TestBusBranchCreator()
    result = await creator.create(nb_network)

    was_successful, validator, mappings, bb_network = _get_validated_results(result)

    assert len(bb_network.bus) == 2
    assert len(bb_network.branch) == 1


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'single_branch_common_lines_network',
    [False, True],
    indirect=True
)
async def test_group_common_ac_line_segment_terminals_single_branch(single_branch_common_lines_network):
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
        lines_grouping = await _group_common_ac_line_segment_terminals(a)
        _assert_are_equal(lines_grouping.conducting_equipment_group, {acls1, acls2, acls3})
        _assert_are_equal(lines_grouping.inner_terminals, {*acls1.terminals, *acls2.terminals, list(acls3.terminals)[0]})
        _assert_are_equal(lines_grouping.border_terminals, {list(acls3.terminals)[1]})

    # acls4
    lines_grouping = await _group_common_ac_line_segment_terminals(acls4)
    _assert_are_equal(lines_grouping.conducting_equipment_group, {acls4})
    _assert_are_equal(lines_grouping.inner_terminals, set())
    _assert_are_equal(lines_grouping.border_terminals, {*acls4.terminals})

    # acls5
    lines_grouping = await _group_common_ac_line_segment_terminals(acls5)
    _assert_are_equal(lines_grouping.conducting_equipment_group, {acls5})
    _assert_are_equal(lines_grouping.inner_terminals, set())
    _assert_are_equal(lines_grouping.border_terminals, {*acls5.terminals})


@pytest.mark.asyncio
async def test_group_common_ac_line_segment_terminals_multi_branch(multi_branch_common_lines_network):
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
        lines_grouping = await _group_common_ac_line_segment_terminals(a)
        _assert_are_equal(lines_grouping.conducting_equipment_group, {a0, a1, a2})
        _assert_are_equal(lines_grouping.inner_terminals, {list(a0.terminals)[0], *a1.terminals, list(a2.terminals)[0]})
        _assert_are_equal(lines_grouping.border_terminals, {list(a2.terminals)[1]})

    # a3
    lines_grouping = await _group_common_ac_line_segment_terminals(a3)
    _assert_are_equal(lines_grouping.conducting_equipment_group, {a3})
    _assert_are_equal(lines_grouping.inner_terminals, set())
    _assert_are_equal(lines_grouping.border_terminals, {*a3.terminals})

    # a4, a5
    for a in a4, a5:
        lines_grouping = await _group_common_ac_line_segment_terminals(a)
        _assert_are_equal(lines_grouping.conducting_equipment_group, {a4, a5})
        _assert_are_equal(lines_grouping.inner_terminals, {list(a4.terminals)[1], list(a5.terminals)[0]})
        _assert_are_equal(lines_grouping.border_terminals, {list(a4.terminals)[0], list(a5.terminals)[1]})

    # a6, a7
    for a in a6, a7:
        lines_grouping = await _group_common_ac_line_segment_terminals(a)
        _assert_are_equal(lines_grouping.conducting_equipment_group, {a6, a7})
        _assert_are_equal(lines_grouping.inner_terminals, {list(a6.terminals)[1], *a7.terminals})
        _assert_are_equal(lines_grouping.border_terminals, {list(a6.terminals)[0]})

    # a8
    lines_grouping = await _group_common_ac_line_segment_terminals(a8)
    _assert_are_equal(lines_grouping.conducting_equipment_group, {a8})
    _assert_are_equal(lines_grouping.inner_terminals, set())
    _assert_are_equal(lines_grouping.border_terminals, {*a8.terminals})


@pytest.mark.asyncio
async def test_group_common_ac_line_segment_terminals_end_of_branch_multiple_ec_pec(end_of_branch_multiple_ec_pec):
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
        lines_grouping = await _group_common_ac_line_segment_terminals(a)
        _assert_are_equal(lines_grouping.conducting_equipment_group, {a1, a2})
        _assert_are_equal(lines_grouping.inner_terminals, {list(a1.terminals)[1], list(a2.terminals)[0]})
        _assert_are_equal(lines_grouping.border_terminals, {list(a1.terminals)[0], list(a2.terminals)[1]})


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'single_branch_common_lines_network',
    [False],
    indirect=True
)
async def test_group_negligible_impedance_terminals_single_branch_closed_switch(single_branch_common_lines_network):
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

    def has_negligible_impedance(ce: ConductingEquipment) -> bool:
        if isinstance(ce, Switch):
            return not ce.is_open()
        else:
            return False

    cn = {"_".join(sorted([t.conducting_equipment.mrid for t in cn.terminals])): cn for cn in single_branch_common_lines_network.objects(ConnectivityNode)}

    # Validation
    # a1_a2
    terminal_group = await _group_negligible_impedance_terminals(list(cn["acls1_acls2"].terminals)[0], has_negligible_impedance)
    _assert_are_equal(terminal_group.conducting_equipment_group, set())
    _assert_are_equal(terminal_group.inner_terminals, set())
    _assert_are_equal(terminal_group.border_terminals, {list(acls2.terminals)[0], *acls1.terminals})

    # a2_a3
    terminal_group = await _group_negligible_impedance_terminals(list(cn["acls2_acls3"].terminals)[0], has_negligible_impedance)
    _assert_are_equal(terminal_group.conducting_equipment_group, set())
    _assert_are_equal(terminal_group.inner_terminals, set())
    _assert_are_equal(terminal_group.border_terminals, {list(acls2.terminals)[1], list(acls3.terminals)[0]})

    # a3_sw
    terminal_group = await _group_negligible_impedance_terminals(list(cn["acls3_sw"].terminals)[0], has_negligible_impedance)
    _assert_are_equal(terminal_group.conducting_equipment_group, {sw})
    _assert_are_equal(terminal_group.inner_terminals, {*sw.terminals})
    _assert_are_equal(terminal_group.border_terminals, {list(acls3.terminals)[1], list(acls4.terminals)[0]})

    # sw_a4
    terminal_group = await _group_negligible_impedance_terminals(list(cn["acls4_sw"].terminals)[0], has_negligible_impedance)
    _assert_are_equal(terminal_group.conducting_equipment_group, {sw})
    _assert_are_equal(terminal_group.inner_terminals, {*sw.terminals})
    _assert_are_equal(terminal_group.border_terminals, {list(acls3.terminals)[1], list(acls4.terminals)[0]})

    # a4_a5
    terminal_group = await _group_negligible_impedance_terminals(list(cn["acls4_acls5"].terminals)[0], has_negligible_impedance)
    _assert_are_equal(terminal_group.conducting_equipment_group, set())
    _assert_are_equal(terminal_group.inner_terminals, set())
    _assert_are_equal(terminal_group.border_terminals, {list(acls4.terminals)[1], *acls5.terminals})


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'single_branch_common_lines_network',
    [True],
    indirect=True
)
async def test_group_negligible_impedance_terminals_single_branch_open_switch(single_branch_common_lines_network):
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

    def has_negligible_impedance(ce: ConductingEquipment) -> bool:
        if isinstance(ce, Switch):
            return not ce.is_open()
        else:
            return False

    cn = {"_".join(sorted([t.conducting_equipment.mrid for t in cn.terminals])): cn for cn in single_branch_common_lines_network.objects(ConnectivityNode)}

    # Validation
    # a1_a2
    terminal_grouping = await _group_negligible_impedance_terminals(list(cn["acls1_acls2"].terminals)[0], has_negligible_impedance)
    _assert_are_equal(terminal_grouping.conducting_equipment_group, set())
    _assert_are_equal(terminal_grouping.inner_terminals, set())
    _assert_are_equal(terminal_grouping.border_terminals, {list(acls2.terminals)[0], *acls1.terminals})

    # a2_a3
    terminal_grouping = await _group_negligible_impedance_terminals(list(cn["acls2_acls3"].terminals)[0], has_negligible_impedance)
    _assert_are_equal(terminal_grouping.conducting_equipment_group, set())
    _assert_are_equal(terminal_grouping.inner_terminals, set())
    _assert_are_equal(terminal_grouping.border_terminals, {list(acls2.terminals)[1], list(acls3.terminals)[0]})

    # a3_sw
    terminal_grouping = await _group_negligible_impedance_terminals(list(cn["acls3_sw"].terminals)[0], has_negligible_impedance)
    _assert_are_equal(terminal_grouping.conducting_equipment_group, set())
    _assert_are_equal(terminal_grouping.inner_terminals, set())
    _assert_are_equal(terminal_grouping.border_terminals, {list(acls3.terminals)[1], list(sw.terminals)[0]})

    # sw_a4
    terminal_grouping = await _group_negligible_impedance_terminals(list(cn["acls4_sw"].terminals)[0], has_negligible_impedance)
    _assert_are_equal(terminal_grouping.conducting_equipment_group, set())
    _assert_are_equal(terminal_grouping.inner_terminals, set())
    _assert_are_equal(terminal_grouping.border_terminals, {list(sw.terminals)[1], list(acls4.terminals)[0]})

    # a4_a5
    terminal_grouping = await _group_negligible_impedance_terminals(list(cn["acls4_acls5"].terminals)[0], has_negligible_impedance)
    _assert_are_equal(terminal_grouping.conducting_equipment_group, set())
    _assert_are_equal(terminal_grouping.inner_terminals, set())
    _assert_are_equal(terminal_grouping.border_terminals, {list(acls4.terminals)[1], *acls5.terminals})


@pytest.mark.asyncio
async def test_group_negligible_impedance_terminals_multi_branch(multi_branch_common_lines_network):
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

    def has_negligible_impedance(ce: ConductingEquipment) -> bool:
        if isinstance(ce, Switch):
            return not ce.is_open()
        else:
            return False

    cn = {"_".join(sorted([t.conducting_equipment.mrid for t in cn.terminals])): cn for cn in multi_branch_common_lines_network.objects(ConnectivityNode)}

    # Validation
    # a0_a1
    terminal_grouping = await _group_negligible_impedance_terminals(list(cn["a0_a1"].terminals)[0], has_negligible_impedance)
    _assert_are_equal(terminal_grouping.conducting_equipment_group, set())
    _assert_are_equal(terminal_grouping.inner_terminals, set())
    _assert_are_equal(terminal_grouping.border_terminals, {list(a1.terminals)[0], *a0.terminals})

    # a1_a2
    terminal_grouping = await _group_negligible_impedance_terminals(list(cn["a1_a2"].terminals)[0], has_negligible_impedance)
    _assert_are_equal(terminal_grouping.conducting_equipment_group, set())
    _assert_are_equal(terminal_grouping.inner_terminals, set())
    _assert_are_equal(terminal_grouping.border_terminals, {list(a1.terminals)[1], list(a2.terminals)[0]})

    # a2_a3_a6
    terminal_grouping = await _group_negligible_impedance_terminals(list(cn["a2_a3_a6"].terminals)[0], has_negligible_impedance)
    _assert_are_equal(terminal_grouping.conducting_equipment_group, set())
    _assert_are_equal(terminal_grouping.inner_terminals, set())
    _assert_are_equal(terminal_grouping.border_terminals, {list(a2.terminals)[1], list(a3.terminals)[0], list(a6.terminals)[0]})

    # a3_a4_a8
    terminal_grouping = await _group_negligible_impedance_terminals(list(cn["a3_a4_a8"].terminals)[0], has_negligible_impedance)
    _assert_are_equal(terminal_grouping.conducting_equipment_group, set())
    _assert_are_equal(terminal_grouping.inner_terminals, set())
    _assert_are_equal(terminal_grouping.border_terminals, {list(a3.terminals)[1], list(a4.terminals)[0], *a8.terminals})

    # a4_a5
    terminal_grouping = await _group_negligible_impedance_terminals(list(cn["a4_a5"].terminals)[0], has_negligible_impedance)
    _assert_are_equal(terminal_grouping.conducting_equipment_group, set())
    _assert_are_equal(terminal_grouping.inner_terminals, set())
    _assert_are_equal(terminal_grouping.border_terminals, {list(a4.terminals)[1], list(a5.terminals)[0]})

    terminal_grouping = await _group_negligible_impedance_terminals(list(a5.terminals)[0], has_negligible_impedance)
    _assert_are_equal(terminal_grouping.conducting_equipment_group, set())
    _assert_are_equal(terminal_grouping.inner_terminals, set())
    _assert_are_equal(terminal_grouping.border_terminals, {list(a4.terminals)[1], list(a5.terminals)[0]})

    # a6_a7
    terminal_grouping = await _group_negligible_impedance_terminals(list(cn["a6_a7"].terminals)[0], has_negligible_impedance)
    _assert_are_equal(terminal_grouping.conducting_equipment_group, set())
    _assert_are_equal(terminal_grouping.inner_terminals, set())
    _assert_are_equal(terminal_grouping.border_terminals, {list(a6.terminals)[1], *a7.terminals})


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'negligible_impedance_equipment_basic_network',
    [
        lambda mrid: Junction(mrid=mrid),
        lambda mrid: Disconnector(mrid=mrid),
        lambda mrid: BusbarSection(mrid=mrid)
    ],
    indirect=True
)
async def test_group_negligible_impedance_terminals_groups_negligible_impedance_equipment(negligible_impedance_equipment_basic_network):
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

    def has_negligible_impedance(ce: ConductingEquipment) -> bool:
        if isinstance(ce, Junction) or isinstance(ce, BusbarSection):
            return True
        if isinstance(ce, AcLineSegment):
            return ce.length == 0
        if isinstance(ce, Switch):
            return not ce.is_open()
        else:
            return False

    cn = {"_".join(sorted([t.conducting_equipment.mrid for t in cn.terminals])): cn for cn in
          negligible_impedance_equipment_basic_network.objects(ConnectivityNode)}

    # Validation
    # a0_nie1
    terminal_grouping = await _group_negligible_impedance_terminals(list(cn["a0_nie1"].terminals)[0], has_negligible_impedance)
    _assert_are_equal(terminal_grouping.conducting_equipment_group, {nie1, a0, a1})
    _assert_are_equal(terminal_grouping.inner_terminals, {*nie1.terminals, *a0.terminals, *a1.terminals})
    _assert_are_equal(terminal_grouping.border_terminals, {list(a2.terminals)[0]})

    # nie1_a1
    terminal_grouping = await _group_negligible_impedance_terminals(list(cn["a1_nie1"].terminals)[0], has_negligible_impedance)
    _assert_are_equal(terminal_grouping.conducting_equipment_group, {nie1, a0, a1})
    _assert_are_equal(terminal_grouping.inner_terminals, {*nie1.terminals, *a0.terminals, *a1.terminals})
    _assert_are_equal(terminal_grouping.border_terminals, {list(a2.terminals)[0]})

    # a1_a2
    terminal_grouping = await _group_negligible_impedance_terminals(list(cn["a1_a2"].terminals)[0], has_negligible_impedance)
    _assert_are_equal(terminal_grouping.conducting_equipment_group, {nie1, a0, a1})
    _assert_are_equal(terminal_grouping.inner_terminals, {*nie1.terminals, *a0.terminals, *a1.terminals})
    _assert_are_equal(terminal_grouping.border_terminals, {list(a2.terminals)[0]})

    # a2_nie2
    terminal_grouping = await _group_negligible_impedance_terminals(list(cn["a2_nie2"].terminals)[0], has_negligible_impedance)
    _assert_are_equal(terminal_grouping.conducting_equipment_group, {nie2})
    _assert_are_equal(terminal_grouping.inner_terminals, {*nie2.terminals})
    _assert_are_equal(terminal_grouping.border_terminals, {list(a2.terminals)[1], list(a3.terminals)[0], list(a4.terminals)[0]})

    # a3_nie2
    terminal_grouping = await _group_negligible_impedance_terminals(list(cn["a3_nie2"].terminals)[0], has_negligible_impedance)
    _assert_are_equal(terminal_grouping.conducting_equipment_group, {nie2})
    _assert_are_equal(terminal_grouping.inner_terminals, {*nie2.terminals})
    _assert_are_equal(terminal_grouping.border_terminals, {list(a2.terminals)[1], list(a3.terminals)[0], list(a4.terminals)[0]})

    # a4_nie2
    terminal_grouping = await _group_negligible_impedance_terminals(list(cn["a4_nie2"].terminals)[0], has_negligible_impedance)
    _assert_are_equal(terminal_grouping.conducting_equipment_group, {nie2})
    _assert_are_equal(terminal_grouping.inner_terminals, {*nie2.terminals})
    _assert_are_equal(terminal_grouping.border_terminals, {list(a2.terminals)[1], list(a3.terminals)[0], list(a4.terminals)[0]})

    # a4_a5
    terminal_grouping = await _group_negligible_impedance_terminals(list(cn["a4_a5"].terminals)[0], has_negligible_impedance)
    _assert_are_equal(terminal_grouping.conducting_equipment_group, set())
    _assert_are_equal(terminal_grouping.inner_terminals, set())
    _assert_are_equal(terminal_grouping.border_terminals, {list(a4.terminals)[1], *a5.terminals})


@pytest.mark.asyncio
async def test_group_negligible_impedance_terminals_end_of_branch_multiple_ec_pec(end_of_branch_multiple_ec_pec):
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

    def has_negligible_impedance(ce: ConductingEquipment) -> bool:
        return False

    cn = {"_".join(sorted([t.conducting_equipment.mrid for t in cn.terminals])): cn for cn in end_of_branch_multiple_ec_pec.objects(ConnectivityNode)}

    # Validation
    # a2_ec
    terminal_grouping = await _group_negligible_impedance_terminals(list(cn["a2_ec_pec1_pec2"].terminals)[0], has_negligible_impedance)
    _assert_are_equal(terminal_grouping.conducting_equipment_group, set())
    _assert_are_equal(terminal_grouping.inner_terminals, set())
    _assert_are_equal(terminal_grouping.border_terminals, {list(a2.terminals)[1], list(ec.terminals)[0], list(pec1.terminals)[0], list(pec2.terminals)[0]})


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
