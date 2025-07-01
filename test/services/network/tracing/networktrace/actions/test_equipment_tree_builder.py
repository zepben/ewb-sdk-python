#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import pprint
from collections import deque
from typing import Optional, List

import pytest

from services.network.test_data.looping_network import create_looping_network
from services.network.tracing.feeder.direction_logger import log_directions
from zepben.evolve import ConductingEquipment, Tracing, NetworkStateOperators
from zepben.evolve import downstream, NetworkTraceActionType
from zepben.evolve.services.network.tracing.networktrace.actions.equipment_tree_builder import EquipmentTreeBuilder
from zepben.evolve.services.network.tracing.networktrace.actions.tree_node import TreeNode


@pytest.mark.asyncio
async def test_downstream_tree():
    n = create_looping_network()
    normal = NetworkStateOperators.NORMAL
    current = NetworkStateOperators.CURRENT

    await Tracing.set_phases().run(n)
    feeder_head = n.get("j0", ConductingEquipment)
    await Tracing.set_direction().run_terminal(feeder_head, network_state_operators=normal)
    await Tracing.set_direction().run_terminal(feeder_head, network_state_operators=current)
    await log_directions(n.get('j0', ConductingEquipment))

    visited_ce = []

    start = n.get("j1", ConductingEquipment)
    assert start is not None
    tree_builder = EquipmentTreeBuilder()
    trace = Tracing.network_trace_branching(
        network_state_operators=normal,
        action_step_type=NetworkTraceActionType.FIRST_STEP_ON_EQUIPMENT) \
        .add_condition(downstream()) \
        .add_step_action(tree_builder) \
        .add_step_action(lambda item, context: visited_ce.append(item.path.to_equipment.mrid))

    await trace.run(start)

    visit_counts = {}
    for ce in visited_ce:
        if visit_counts.get(ce):
            visit_counts[ce] += 1
        else:
            visit_counts[ce] = 1

    pprint.pprint(visit_counts)

    root = list(tree_builder.roots)[0]

    assert root is not None
    _verify_tree_asset(root, n["j1"], None, [n["ac1"], n["ac3"]])

    test_node = root.children[0]
    _verify_tree_asset(test_node, n["ac1"], n["j1"], [n["j2"]])

    test_node = test_node.children[0]
    _verify_tree_asset(test_node, n["j2"], n["ac1"], [n["ac2"]])

    test_node = test_node.children[0]
    _verify_tree_asset(test_node, n["ac2"], n["j2"], [n["j3"]])

    test_node = next(iter(test_node.children))
    _verify_tree_asset(test_node, n["j3"], n["ac2"], [n["ac4"]])

    test_node = next(iter(test_node.children))
    _verify_tree_asset(test_node, n["ac4"], n["j3"], [n["j6"]])

    test_node = next(iter(test_node.children))
    _verify_tree_asset(test_node, n["j6"], n["ac4"], [])

    test_node = list(root.children)[1]
    _verify_tree_asset(test_node, n["ac3"], n["j1"], [n["j4"]])

    test_node = next(iter(test_node.children))
    _verify_tree_asset(test_node, n["j4"], n["ac3"], [n["ac5"], n["ac6"]])

    assert len(_find_nodes(root, "j0")) == 0
    assert len(_find_nodes(root, "ac0")) == 0
    assert len(_find_nodes(root, "j1")) == 1
    assert len(_find_nodes(root, "ac1")) == 1
    assert len(_find_nodes(root, "j2")) == 1
    assert len(_find_nodes(root, "ac2")) == 1
    assert len(_find_nodes(root, "j3")) == 1
    assert len(_find_nodes(root, "ac3")) == 1
    assert len(_find_nodes(root, "j4")) == 1
    assert len(_find_nodes(root, "ac4")) == 1
    assert len(_find_nodes(root, "j5")) == 1
    assert len(_find_nodes(root, "ac5")) == 1
    assert len(_find_nodes(root, "j6")) == 2
    assert len(_find_nodes(root, "ac6")) == 1
    assert len(_find_nodes(root, "j7")) == 1
    assert len(_find_nodes(root, "ac7")) == 1
    assert len(_find_nodes(root, "j8")) == 1
    assert len(_find_nodes(root, "ac8")) == 1
    assert len(_find_nodes(root, "j9")) == 1
    assert len(_find_nodes(root, "ac9")) == 1
    assert len(_find_nodes(root, "j10")) == 1
    assert len(_find_nodes(root, "ac10")) == 1
    assert len(_find_nodes(root, "j11")) == 3  # j11 java sdk
    assert len(_find_nodes(root, "ac11")) == 3  # acLineSegment11 java sdk
    assert len(_find_nodes(root, "j12")) == 3
    assert len(_find_nodes(root, "ac12")) == 4
    assert len(_find_nodes(root, "j13")) == 3
    assert len(_find_nodes(root, "ac13")) == 3  # acLineSegment13 java jdk
    assert len(_find_nodes(root, "j14")) == 4
    assert len(_find_nodes(root, "ac14")) == 3
    assert len(_find_nodes(root, "ac15")) == 4
    assert len(_find_nodes(root, "ac16")) == 4

    assert _find_node_depths(root, "j0") == []
    assert _find_node_depths(root, "ac0") == []
    assert _find_node_depths(root, "j1") == [0]
    assert _find_node_depths(root, "ac1") == [1]
    assert _find_node_depths(root, "j2") == [2]
    assert _find_node_depths(root, "ac2") == [3]
    assert _find_node_depths(root, "j3") == [4]
    assert _find_node_depths(root, "ac3") == [1]
    assert _find_node_depths(root, "j4") == [2]
    assert _find_node_depths(root, "ac4") == [5]
    assert _find_node_depths(root, "j5") == [4]
    assert _find_node_depths(root, "ac5") == [3]
    assert _find_node_depths(root, "j6") == [6, 10]
    assert _find_node_depths(root, "ac6") == [3]
    assert _find_node_depths(root, "j7") == [4]
    assert _find_node_depths(root, "ac7") == [9]
    assert _find_node_depths(root, "j8") == [6]
    assert _find_node_depths(root, "ac8") == [5]
    assert _find_node_depths(root, "j9") == [8]
    assert _find_node_depths(root, "ac9") == [7]
    assert _find_node_depths(root, "j10") == [6]
    assert _find_node_depths(root, "ac10") == [5]
    assert _find_node_depths(root, "j11") == [8, 10, 12]
    assert _find_node_depths(root, "ac11") == [7, 11, 13]
    assert _find_node_depths(root, "j12") == [8, 10, 10]
    assert _find_node_depths(root, "ac12") == [7, 10, 11, 14]
    assert _find_node_depths(root, "j13") == [10, 12, 12]
    assert _find_node_depths(root, "ac13") == [9, 9, 11]
    assert _find_node_depths(root, "j14") == [8, 9, 12, 13]
    assert _find_node_depths(root, "ac14") == [9, 11, 11]
    assert _find_node_depths(root, "ac15") == [7, 10, 12, 13]
    assert _find_node_depths(root, "ac16") == [8, 9, 11, 14]


def _verify_tree_asset(
    tree_node: TreeNode,
    expected_asset: Optional[ConductingEquipment],
    expected_parent: Optional[ConductingEquipment],
    expected_children: List[ConductingEquipment]
):
    assert tree_node.identified_object is expected_asset

    if expected_parent is not None:
        tree_parent = tree_node.parent
        assert tree_parent is not None
        assert tree_parent.identified_object is expected_parent
    else:
        assert tree_node.parent is None

    children_nodes = list(c.identified_object for c in tree_node.children)
    assert children_nodes == expected_children


def _find_nodes(root: TreeNode[ConductingEquipment], asset_id: str) -> List[TreeNode[ConductingEquipment]]:
    matches: List[TreeNode[ConductingEquipment]] = []
    process_nodes: deque[TreeNode[ConductingEquipment]] = deque()
    process_nodes.append(root)

    while process_nodes:
        node = process_nodes.popleft()
        if node.identified_object.mrid == asset_id:
            matches.append(node)

        for child in node.children:
            process_nodes.append(child)

    return matches


def _find_node_depths(root: TreeNode[ConductingEquipment], asset_id: str) -> List[int]:
    nodes = _find_nodes(root, asset_id)
    depths = []

    for node in nodes:
        depths.append(_depth_in_tree(node))

    return depths


def _depth_in_tree(tree_node: TreeNode[ConductingEquipment]):
    depth = -1
    node = tree_node
    while node is not None:
        node = node.parent
        depth += 1

    return depth
