#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from collections import deque
from typing import Optional, List

import pytest

from services.network.test_data.looping_network import create_looping_network
from zepben.evolve import set_phases, ConductingEquipment, set_direction, TreeNode
from zepben.evolve.services.network.tracing.tracing import normal_downstream_tree


@pytest.mark.asyncio
async def test_downstream_trace():
    n = create_looping_network()

    await set_phases().run(n)
    feeder_head = n.get("j0", ConductingEquipment)
    await set_direction().run_terminal(feeder_head.get_terminal_by_sn(1))

    start = n.get("j2", ConductingEquipment)
    assert start is not None
    root = await normal_downstream_tree().run(start)

    assert root is not None
    _verify_tree_asset(root, n["j2"], None, [n["c13"], n["c3"]])

    test_node = next(iter(root.children))
    _verify_tree_asset(test_node, n["c13"], n["j2"], [n["j14"]])

    test_node = next(iter(test_node.children))
    _verify_tree_asset(test_node, n["j14"], n["c13"], [n["c15"]])

    test_node = next(iter(test_node.children))
    _verify_tree_asset(test_node, n["c15"], n["j14"], [n["j16"]])

    test_node = next(iter(test_node.children))
    _verify_tree_asset(test_node, n["j16"], n["c15"], [n["c17"]])

    test_node = next(iter(test_node.children))
    _verify_tree_asset(test_node, n["c17"], n["j16"], [n["b18"]])

    test_node = next(iter(test_node.children))
    _verify_tree_asset(test_node, n["b18"], n["c17"], [])

    test_node = list(root.children)[1]
    _verify_tree_asset(test_node, n["c3"], n["j2"], [n["j4"]])

    test_node = next(iter(test_node.children))
    _verify_tree_asset(test_node, n["j4"], n["c3"], [n["c20"], n["c5"]])

    assert len(_find_nodes(root, "j0")) == 0
    assert len(_find_nodes(root, "c1")) == 0
    assert len(_find_nodes(root, "j2")) == 1
    assert len(_find_nodes(root, "c13")) == 1
    assert len(_find_nodes(root, "j14")) == 1
    assert len(_find_nodes(root, "c15")) == 1
    assert len(_find_nodes(root, "j16")) == 1
    assert len(_find_nodes(root, "c17")) == 1
    assert len(_find_nodes(root, "b18")) == 1
    assert len(_find_nodes(root, "c19")) == 1


def _verify_tree_asset(
    tree_node: TreeNode,
    expected_asset: Optional[ConductingEquipment],
    expected_parent: Optional[ConductingEquipment],
    expected_children: List[ConductingEquipment]
):
    assert tree_node.conducting_equipment is expected_asset

    if expected_parent is not None:
        tree_parent = tree_node.parent
        assert tree_parent is not None
        assert tree_parent.conducting_equipment is expected_parent
    else:
        assert tree_node.parent is None

    children_nodes = list(tree_node.children)
    assert len(children_nodes) == len(expected_children)
    for child_node, expected_child in zip(children_nodes, expected_children):
        assert child_node.conducting_equipment is expected_child


def _find_nodes(root: TreeNode, asset_id: str) -> List[TreeNode]:
    matches: List[TreeNode] = []
    process_nodes: deque[TreeNode] = deque()
    process_nodes.append(root)

    while process_nodes:
        node = process_nodes.popleft()
        if node.conducting_equipment.mrid == asset_id:
            matches.append(node)

        for child in node.children:
            process_nodes.append(child)

    return matches


def _find_node_depths(root: TreeNode, asset_id: str) -> List[int]:
    nodes = _find_nodes(root, asset_id)
    depths = []

    for node in nodes:
        depths.append(_depth_in_tree(node))

    return depths


def _depth_in_tree(tree_node: TreeNode):
    depth = -1
    node = tree_node
    while node is not None:
        node = node.parent
        depth += 1

    return depth
