#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Set, Callable, Dict

import pytest
from hypothesis import given
from hypothesis.strategies import booleans, sampled_from

from busbranch.data.open_switch_between_different_voltages import open_switch_between_different_voltages
from busbranch.data.lv_equivalent_branch_network import lv_equivalent_branch_network
from busbranch.data.end_of_branch_multiple_ec_pec import end_of_branch_multiple_ec_pec
from busbranch.data.multi_branch_common_lines_network import multi_branch_common_lines_network
from busbranch.data.negligible_impedance_equipment_basic_network import negligible_impedance_equipment_basic_network
from busbranch.data.simple_node_breaker_network import simple_node_breaker_network
from busbranch.data.single_branch_common_lines_network import single_branch_common_lines_network
from busbranch.data.three_common_lines_network import three_common_lines_network
from busbranch.test_bus_branch_creator import TestBusBranchCreator, create_terminal_based_id
from zepben.evolve import ConnectivityNode, Junction, Disconnector, BusbarSection, Switch, ConductingEquipment, AcLineSegment, Terminal, NetworkService, \
    BusBranchNetworkCreationMappings
# noinspection PyProtectedMember
from zepben.evolve.model.busbranch.bus_branch import _group_negligible_impedance_terminals, _group_common_ac_line_segment_terminals


@pytest.mark.asyncio
async def test_create_bus_branch_model_callbacks():
    nb_network = simple_node_breaker_network()
    plsi, wire_info, pt_info, es, pt, line, ec, pec, eb, ec_eb1, ec_eb2 = _get_validated_conducting_equipment(nb_network)
    exp_bb0, exp_bb1, exp_bb2, exp_bb3, exp_branch, exp_tx, exp_es, exp_ec, exp_pec, exp_eb, exp_ec_eb1, exp_ec_eb2 = _get_expected(
        nb_network,
        line,
        pt,
        es,
        ec,
        pec,
        eb,
        ec_eb1,
        ec_eb2
    )

    creator = TestBusBranchCreator()
    result = await creator.create(nb_network)

    validator, mappings, bb_network = _get_validated_results(result)

    _validate_validator_calls(validator)
    _validate_mappings(mappings, exp_bb0, exp_bb1, exp_bb2, exp_bb3, exp_branch, exp_tx, exp_es, exp_ec, exp_pec, exp_eb, exp_ec_eb1, exp_ec_eb2,
                       line, pt, es, ec, pec, eb, ec_eb1, ec_eb2)
    _validate_network(bb_network, exp_bb0, exp_bb1, exp_bb2, exp_bb3, exp_branch, exp_tx, exp_es, exp_ec, exp_pec, exp_eb, exp_ec_eb1, exp_ec_eb2)


@pytest.mark.asyncio
async def test_topological_nodes_inside_grouped_lines_do_not_get_created():
    nb_network = three_common_lines_network()
    creator = TestBusBranchCreator()
    result = await creator.create(nb_network)

    validator, mappings, bb_network = _get_validated_results(result)

    assert len(bb_network.bus) == 2
    assert len(bb_network.topological_branch) == 1


@pytest.mark.asyncio
async def test_equivalent_branches_created_only_if_they_have_impedance():
    nb_network = lv_equivalent_branch_network(False)
    creator = TestBusBranchCreator()
    result = await creator.create(nb_network)

    validator, mappings, bb_network = _get_validated_results(result)

    assert len(bb_network.bus) == 1
    assert len(bb_network.topological_branch) == 0
    assert len(bb_network.equivalent_branch) == 0
    assert len(bb_network.transformer) == 1
    assert len(bb_network.energy_consumer) == 2
    assert len(bb_network.power_electronics_connection) == 1

    bus = next(iter(result.mappings.to_bbn.objects.get("ec_t1")))
    ec_bus = next(iter(result.mappings.to_bbn.objects.get("ec")))[1]
    ec_eb_bus = next(iter(result.mappings.to_bbn.objects.get("ec_eb")))[1]
    pec_bus = next(iter(result.mappings.to_bbn.objects.get("pec")))[1]
    pt_bus = next(iter(result.mappings.to_bbn.objects.get("pt")))[1][0][1]

    assert bus == ec_bus
    assert bus == ec_eb_bus
    assert bus == pec_bus
    assert bus == pt_bus

    nb_network = lv_equivalent_branch_network(True)
    creator = TestBusBranchCreator()
    result = await creator.create(nb_network)

    validator, mappings, bb_network = _get_validated_results(result)

    assert len(bb_network.bus) == 2
    assert len(bb_network.topological_branch) == 0
    assert len(bb_network.equivalent_branch) == 1
    assert len(bb_network.transformer) == 1
    assert len(bb_network.energy_consumer) == 2
    assert len(bb_network.power_electronics_connection) == 1

    bus_1 = next(iter(result.mappings.to_bbn.objects.get("ec_t1")))
    bus_2 = next(iter(result.mappings.to_bbn.objects.get("ec_eb_t1")))
    ec_bus = next(iter(result.mappings.to_bbn.objects.get("ec")))[1]
    ec_eb_bus = next(iter(result.mappings.to_bbn.objects.get("ec_eb")))[1]
    pec_bus = next(iter(result.mappings.to_bbn.objects.get("pec")))[1]
    pt_bus = next(iter(result.mappings.to_bbn.objects.get("pt")))[1][0][1]

    assert bus_1 == ec_bus
    assert bus_1 == pec_bus
    assert bus_1 == pt_bus
    assert bus_2 == ec_eb_bus


@pytest.mark.asyncio
@given(sw_is_open=booleans())
async def test_group_common_ac_line_segment_terminals_single_branch(sw_is_open: bool):
    nb_network = single_branch_common_lines_network(sw_is_open)

    acls1 = nb_network.get("acls1")
    acls2 = nb_network.get("acls2")
    acls3 = nb_network.get("acls3")
    acls4 = nb_network.get("acls4")
    acls5 = nb_network.get("acls5")

    await _validate_line_grouping({acls1, acls2, acls3}, {*acls1.terminals, *acls2.terminals, get_term(acls3, 1)}, {get_term(acls3, 2)})
    await _validate_line_grouping({acls4}, set(), {*acls4.terminals})
    await _validate_line_grouping({acls5}, set(), {*acls5.terminals})


@pytest.mark.asyncio
async def test_group_common_ac_line_segment_terminals_multi_branch():
    nb_network = multi_branch_common_lines_network()

    a0 = nb_network.get("a0")
    a1 = nb_network.get("a1")
    a2 = nb_network.get("a2")
    a3 = nb_network.get("a3")
    a4 = nb_network.get("a4")
    a5 = nb_network.get("a5")
    a6 = nb_network.get("a6")
    a7 = nb_network.get("a7")
    a8 = nb_network.get("a8")

    await _validate_line_grouping({a0, a1, a2}, {get_term(a0, 1), *a1.terminals, get_term(a2, 1)}, {get_term(a2, 2)})
    await _validate_line_grouping({a0, a1, a2}, {get_term(a0, 1), *a1.terminals, get_term(a2, 1)}, {get_term(a2, 2)})
    await _validate_line_grouping({a3}, set(), {*a3.terminals})
    await _validate_line_grouping({a4, a5}, {get_term(a4, 2), get_term(a5, 1)}, {get_term(a4, 1), get_term(a5, 2)})
    await _validate_line_grouping({a6, a7}, {get_term(a6, 2), *a7.terminals}, {get_term(a6, 1)})
    await _validate_line_grouping({a8}, set(), {*a8.terminals})


@pytest.mark.asyncio
async def test_group_common_ac_line_segment_terminals_end_of_branch_multiple_ec_pec():
    nb_network = end_of_branch_multiple_ec_pec()

    a1 = nb_network.get("a1")
    a2 = nb_network.get("a2")

    await _validate_line_grouping({a1, a2}, {get_term(a1, 2), get_term(a2, 1)}, {get_term(a1, 1), get_term(a2, 2)})


@pytest.mark.asyncio
async def test_group_negligible_impedance_terminals_single_branch_closed_switch():
    nb_network = single_branch_common_lines_network(False)

    acls1 = nb_network.get("acls1")
    acls2 = nb_network.get("acls2")
    acls3 = nb_network.get("acls3")
    acls4 = nb_network.get("acls4")
    acls5 = nb_network.get("acls5")
    sw = nb_network.get("sw")

    def has_neg_imp(ce) -> bool:
        if isinstance(ce, Switch):
            return not ce.is_open()
        else:
            return False

    await _validate_term_grouping(has_neg_imp, nb_network, "acls1_acls2", set(), set(), {get_term(acls2, 1), *acls1.terminals})
    await _validate_term_grouping(has_neg_imp, nb_network, "acls2_acls3", set(), set(), {get_term(acls2, 2), get_term(acls3, 1)})
    await _validate_term_grouping(has_neg_imp, nb_network, "acls3_sw", {sw}, {*sw.terminals}, {get_term(acls3, 2), get_term(acls4, 1)})
    await _validate_term_grouping(has_neg_imp, nb_network, "acls4_sw", {sw}, {*sw.terminals}, {get_term(acls3, 2), get_term(acls4, 1)})
    await _validate_term_grouping(has_neg_imp, nb_network, "acls4_acls5", set(), set(), {get_term(acls4, 2), *acls5.terminals})


@pytest.mark.asyncio
async def test_group_negligible_impedance_terminals_single_branch_open_switch():
    nb_network = single_branch_common_lines_network(True)

    acls1 = nb_network.get("acls1")
    acls2 = nb_network.get("acls2")
    acls3 = nb_network.get("acls3")
    acls4 = nb_network.get("acls4")
    acls5 = nb_network.get("acls5")
    sw = nb_network.get("sw")

    def has_neg_imp(ce) -> bool:
        if isinstance(ce, Switch):
            return not ce.is_open()
        else:
            return False

    await _validate_term_grouping(has_neg_imp, nb_network, "acls1_acls2", set(), set(), {get_term(acls2, 1), *acls1.terminals})
    await _validate_term_grouping(has_neg_imp, nb_network, "acls2_acls3", set(), set(), {get_term(acls2, 2), get_term(acls3, 1)})
    await _validate_term_grouping(has_neg_imp, nb_network, "acls3_sw", set(), set(), {get_term(acls3, 2), get_term(sw, 1)})
    await _validate_term_grouping(has_neg_imp, nb_network, "acls4_sw", set(), set(), {get_term(sw, 2), get_term(acls4, 1)})
    await _validate_term_grouping(has_neg_imp, nb_network, "acls4_acls5", set(), set(), {get_term(acls4, 2), *acls5.terminals})


@pytest.mark.asyncio
async def test_group_negligible_impedance_terminals_multi_branch():
    nb_network = multi_branch_common_lines_network()

    a0 = nb_network.get("a0")
    a1 = nb_network.get("a1")
    a2 = nb_network.get("a2")
    a3 = nb_network.get("a3")
    a4 = nb_network.get("a4")
    a5 = nb_network.get("a5")
    a6 = nb_network.get("a6")
    a7 = nb_network.get("a7")
    a8 = nb_network.get("a8")

    def has_neg_imp(ce) -> bool:
        if isinstance(ce, Switch):
            return not ce.is_open()
        else:
            return False

    await _validate_term_grouping(has_neg_imp, nb_network, "a0_a1", set(), set(), {get_term(a1, 1), *a0.terminals})
    await _validate_term_grouping(has_neg_imp, nb_network, "a1_a2", set(), set(), {get_term(a1, 2), get_term(a2, 1)})
    await _validate_term_grouping(has_neg_imp, nb_network, "a2_a3_a6", set(), set(), {get_term(a2, 2), get_term(a3, 1), get_term(a6, 1)})
    await _validate_term_grouping(has_neg_imp, nb_network, "a3_a4_a8", set(), set(), {get_term(a3, 2), get_term(a4, 1), *a8.terminals})
    await _validate_term_grouping(has_neg_imp, nb_network, "a4_a5", set(), set(), {get_term(a4, 2), get_term(a5, 1)})
    await _validate_term_grouping(has_neg_imp, nb_network, "a5", set(), set(), {get_term(a4, 2), get_term(a5, 1)})
    await _validate_term_grouping(has_neg_imp, nb_network, "a6_a7", set(), set(), {get_term(a6, 2), *a7.terminals})


@pytest.mark.asyncio
@given(nie_constructor=sampled_from([Junction, Disconnector, BusbarSection]))
async def test_group_negligible_impedance_terminals_groups_negligible_impedance_equipment(nie_constructor):
    nb_network = negligible_impedance_equipment_basic_network(lambda mrid: nie_constructor(mrid=mrid))

    nie1 = nb_network.get("nie1")
    nie2 = nb_network.get("nie2")
    a0 = nb_network.get("a0")
    a1 = nb_network.get("a1")
    a2 = nb_network.get("a2")
    a3 = nb_network.get("a3")
    a4 = nb_network.get("a4")
    a5 = nb_network.get("a5")

    def has_neg_imp(ce) -> bool:
        if isinstance(ce, Junction) or isinstance(ce, BusbarSection):
            return True
        if isinstance(ce, AcLineSegment):
            return ce.length == 0
        if isinstance(ce, Switch):
            return not ce.is_open()
        else:
            return False

    await _validate_term_grouping(has_neg_imp, nb_network, "a0_nie1", {nie1, a0, a1}, {*nie1.terminals, *a0.terminals, *a1.terminals}, {get_term(a2, 1)})
    await _validate_term_grouping(has_neg_imp, nb_network, "a1_nie1", {nie1, a0, a1}, {*nie1.terminals, *a0.terminals, *a1.terminals}, {get_term(a2, 1)})
    await _validate_term_grouping(has_neg_imp, nb_network, "a1_a2", {nie1, a0, a1}, {*nie1.terminals, *a0.terminals, *a1.terminals}, {get_term(a2, 1)})
    await _validate_term_grouping(has_neg_imp, nb_network, "a2_nie2", {nie2}, {*nie2.terminals}, {get_term(a2, 2), get_term(a3, 1), get_term(a4, 1)})
    await _validate_term_grouping(has_neg_imp, nb_network, "a3_nie2", {nie2}, {*nie2.terminals}, {get_term(a2, 2), get_term(a3, 1), get_term(a4, 1)})
    await _validate_term_grouping(has_neg_imp, nb_network, "a4_nie2", {nie2}, {*nie2.terminals}, {get_term(a2, 2), get_term(a3, 1), get_term(a4, 1)})
    await _validate_term_grouping(has_neg_imp, nb_network, "a4_a5", set(), set(), {get_term(a4, 2), *a5.terminals})


@pytest.mark.asyncio
async def test_group_negligible_impedance_terminals_end_of_branch_multiple_ec_pec():
    nb_network = end_of_branch_multiple_ec_pec()

    a2 = nb_network.get("a2")
    ec = nb_network.get("ec")
    pec1 = nb_network.get("pec1")
    pec2 = nb_network.get("pec2")

    def has_neg_imp(_) -> bool:
        return False

    await _validate_term_grouping(has_neg_imp, nb_network, "a2_ec_pec1_pec2", set(), set(), get_terms({a2: 2, ec: 1, pec1: 1, pec2: 1}))


@pytest.mark.asyncio
async def test_switches_excluded_when_getting_voltage():
    nb_network = open_switch_between_different_voltages()
    creator = TestBusBranchCreator()
    result = await creator.create(nb_network)

    validator, mappings, bb_network = _get_validated_results(result)

    assert len(bb_network.bus) == 4
    assert len(bb_network.topological_branch) == 2

    for branch_name, (branch_nodes, *_) in bb_network.topological_branch:
        (node0_voltage, *_), (node1_voltage, *_) = branch_nodes
        assert node0_voltage == node1_voltage


def _get_expected(nb_network, line, pt, es, ec, pec, eb, ec_eb1, ec_eb2):
    # -- Bus
    exp_bb0 = (create_terminal_based_id({next(es.terminals), get_term(pt, 1)}),
               (20000, frozenset(), frozenset({get_term(es, 1), get_term(pt, 1)}), frozenset(), nb_network))
    exp_bb1 = (create_terminal_based_id({get_term(pt, 2), get_term(line, 1)}),
               (400, frozenset(), frozenset({get_term(line, 1), get_term(pt, 2)}), frozenset(), nb_network))
    exp_bb2 = (create_terminal_based_id({get_term(line, 2), next(ec.terminals), next(pec.terminals), get_term(eb, 1)}),
               (400, frozenset(), frozenset({get_term(ec, 1), get_term(line, 2), get_term(pec, 1), get_term(eb, 1)}), frozenset(), nb_network))

    exp_bb3 = (create_terminal_based_id({get_term(eb, 2), next(ec_eb1.terminals), next(ec_eb2.terminals)}),
               (400, frozenset(), frozenset({get_term(eb, 2), next(ec_eb1.terminals), next(ec_eb2.terminals)}), frozenset(), nb_network))

    # -- Branch
    exp_branch = (f"tb_{line.mrid}", ((exp_bb1[1], exp_bb2[1]), 100, frozenset({line}), frozenset({*line.terminals}), frozenset(), nb_network))

    # -- Transformer
    exp_end_to_bus_pairs = ((list(pt.ends)[0], exp_bb0[1]), (list(pt.ends)[1], exp_bb1[1]))
    exp_tx = (f"pt_{pt.mrid}", (pt, exp_end_to_bus_pairs, nb_network))

    # -- Source
    exp_es = (f"es_{es.mrid}", (es, exp_bb0[1], nb_network))

    # -- Consumer
    exp_ec = (f"ec_{ec.mrid}", (ec, exp_bb2[1], nb_network))
    exp_ec_eb1 = (f"ec_{ec_eb1.mrid}", (ec_eb1, exp_bb3[1], nb_network))
    exp_ec_eb2 = (f"ec_{ec_eb2.mrid}", (ec_eb2, exp_bb3[1], nb_network))

    # -- PowerElectronicsConnection
    exp_pec = (f"pec_{pec.mrid}", (pec, exp_bb2[1], nb_network))

    # -- EquivalentBranch + Consumer
    exp_eb = (f"eb_{eb.mrid}", ((exp_bb2[1], exp_bb3[1]), eb, nb_network))

    return exp_bb0, exp_bb1, exp_bb2, exp_bb3, exp_branch, exp_tx, exp_es, exp_ec, exp_pec, exp_eb, exp_ec_eb1, exp_ec_eb2


def _get_validated_results(result):
    assert result.was_successful is True
    assert result.validator is not None
    assert result.mappings is not None
    assert result.network is not None

    return result.validator, result.mappings, result.network


def _get_validated_conducting_equipment(nb_network):
    plsi = nb_network.get("plsi")
    wire_info = nb_network.get("wire_info")
    pt_info = nb_network.get("pt_info")
    es = nb_network.get("grid_connection")
    pt = nb_network.get("transformer")
    line = nb_network.get("line")
    ec = nb_network.get("load")
    pec = nb_network.get("pec")
    eb = nb_network.get("eb")
    ec_eb1 = nb_network.get("load_eb1")
    ec_eb2 = nb_network.get("load_eb2")

    return plsi, wire_info, pt_info, es, pt, line, ec, pec, eb, ec_eb1, ec_eb2


def _validate_validator_calls(validator):
    assert validator.network_data_count == 1
    assert validator.topological_node_data_count == 4
    assert validator.topological_branch_data_count == 1
    assert validator.equivalent_branch_data_count == 1
    assert validator.power_transformer_data_count == 1
    assert validator.energy_source_data_count == 1
    assert validator.energy_consumer_data_count == 3
    assert validator.power_electronics_connection_data_count == 1


def _validate_network(
    bb_network,
    expected_bus_0,
    expected_bus_1,
    expected_bus_2,
    expected_bus_3,
    expected_branch,
    expected_transformer,
    expected_energy_source,
    expected_energy_consumer,
    expected_power_electronics_connection,
    expected_equivalent_branch,
    expected_consumer_eb1,
    expected_consumer_eb2
):
    assert bb_network.bus == {expected_bus_0, expected_bus_1, expected_bus_2, expected_bus_3}

    # Branch Comparison
    branch = list(bb_network.topological_branch)[0]
    assert branch[0] == expected_branch[0]
    assert set(branch[1][0]) == set(expected_branch[1][0])
    assert branch[1][1] == expected_branch[1][1]
    assert branch[1][2] == expected_branch[1][2]
    assert branch[1][3] == expected_branch[1][3]
    assert branch[1][4] == expected_branch[1][4]
    assert branch[1][5] == expected_branch[1][5]

    assert bb_network.transformer == {expected_transformer}
    assert bb_network.energy_source == {expected_energy_source}
    assert bb_network.energy_consumer == {expected_energy_consumer, expected_consumer_eb1, expected_consumer_eb2}
    assert bb_network.power_electronics_connection == {expected_power_electronics_connection}
    assert bb_network.equivalent_branch == {expected_equivalent_branch}


def _validate_mappings(
    mappings: BusBranchNetworkCreationMappings,
    expected_bus_0,
    expected_bus_1,
    expected_bus_2,
    expected_bus_3,
    expected_branch,
    expected_transformer,
    expected_energy_source,
    expected_energy_consumer,
    expected_power_electronics_connection,
    expected_equivalent_branch,
    expected_consumer_eb1,
    expected_consumer_eb2,
    line,
    pt,
    es,
    ec,
    pec,
    eb,
    ec_eb1,
    ec_eb2
):
    # -- Bus
    _validate_bus_mapping(mappings, expected_bus_0)
    _validate_bus_mapping(mappings, expected_bus_1)
    _validate_bus_mapping(mappings, expected_bus_2)
    _validate_bus_mapping(mappings, expected_bus_3)

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
    assert list(mappings.to_bbn.objects[ec_eb1.mrid])[0] == expected_consumer_eb1[1]
    assert list(mappings.to_bbn.objects[ec_eb2.mrid])[0] == expected_consumer_eb2[1]

    # --- power electronics connection
    assert list(mappings.to_bbn.objects[pec.mrid])[0] == expected_power_electronics_connection[1]

    # --- equivalent branch
    assert list(mappings.to_bbn.objects[eb.mrid])[0] == expected_equivalent_branch[1]


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


async def _validate_line_grouping(
    expected_acls: Set[AcLineSegment],
    expected_inner: Set[Terminal],
    expected_border: Set[Terminal]
):
    for a in expected_acls:
        grouping = await _group_common_ac_line_segment_terminals(a)
        assert grouping.conducting_equipment_group == expected_acls
        assert grouping.inner_terminals == expected_inner
        assert grouping.border_terminals == expected_border


async def _validate_term_grouping(
    has_negligible_impedance: Callable[[ConductingEquipment], bool],
    nb_network: NetworkService,
    mrid: str,
    expected_ce: Set[ConductingEquipment],
    expected_inner: Set[Terminal],
    expected_border: Set[Terminal]
):
    ce = nb_network.get(mrid, ConductingEquipment, None)
    if ce is not None:
        terminal = get_term(ce, 1)
    else:
        cn = {"_".join(sorted([t.conducting_equipment.mrid for t in cn.terminals])): cn for cn in nb_network.objects(ConnectivityNode)}
        terminal = list(cn[mrid].terminals)[0]

    grouping = await _group_negligible_impedance_terminals(terminal, has_negligible_impedance)
    assert grouping.conducting_equipment_group == expected_ce
    assert grouping.inner_terminals == expected_inner
    assert grouping.border_terminals == expected_border


def get_term(ce: ConductingEquipment, term: int) -> Terminal:
    return ce.get_terminal_by_sn(term)


def get_terms(request: Dict[ConductingEquipment, int]) -> Set[Terminal]:
    return {get_term(ce, term) for ce, term in request.items()}
