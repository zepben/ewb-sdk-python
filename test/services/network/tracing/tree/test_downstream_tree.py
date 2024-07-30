#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from collections import deque
from typing import Optional, List

import pytest

from services.network.test_data.looping_network import create_looping_network
from zepben.evolve import set_phases, ConductingEquipment, set_direction, TreeNode, normal_downstream_tree


@pytest.mark.asyncio
async def test_downstream_tree():
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
    assert len(_find_nodes(root, "c3")) == 1
    assert len(_find_nodes(root, "j4")) == 1
    assert len(_find_nodes(root, "c17")) == 1
    assert len(_find_nodes(root, "j21")) == 1
    assert len(_find_nodes(root, "c20")) == 1
    assert len(_find_nodes(root, "b18")) == 2
    assert len(_find_nodes(root, "c5")) == 1
    assert len(_find_nodes(root, "j6")) == 1
    assert len(_find_nodes(root, "c19")) == 1
    assert len(_find_nodes(root, "j23")) == 1
    assert len(_find_nodes(root, "c22")) == 1
    assert len(_find_nodes(root, "j25")) == 1
    assert len(_find_nodes(root, "c24")) == 1
    assert len(_find_nodes(root, "j8")) == 1
    assert len(_find_nodes(root, "c7")) == 1
    assert len(_find_nodes(root, "j30")) == 1  # Would have been 3 if the intermediate loop was reprocessed.
    assert len(_find_nodes(root, "c29")) == 1  # Would have been 3 if the intermediate loop was reprocessed.
    assert len(_find_nodes(root, "j10")) == 3
    assert len(_find_nodes(root, "c9")) == 4
    assert len(_find_nodes(root, "j12")) == 3
    assert len(_find_nodes(root, "c31")) == 1  # Would have been 3 if the intermediate loop was reprocessed.
    assert len(_find_nodes(root, "j27")) == 4
    assert len(_find_nodes(root, "c11")) == 3
    assert len(_find_nodes(root, "c26")) == 4
    assert len(_find_nodes(root, "c28")) == 4

    assert _find_node_depths(root, "j0") == []
    assert _find_node_depths(root, "c1") == []
    assert _find_node_depths(root, "j2") == [0]
    assert _find_node_depths(root, "c13") == [1]
    assert _find_node_depths(root, "j14") == [2]
    assert _find_node_depths(root, "c15") == [3]
    assert _find_node_depths(root, "j16") == [4]
    assert _find_node_depths(root, "c3") == [1]
    assert _find_node_depths(root, "j4") == [2]
    assert _find_node_depths(root, "c17") == [5]
    assert _find_node_depths(root, "j21") == [4]
    assert _find_node_depths(root, "c20") == [3]
    assert _find_node_depths(root, "b18") == [6, 10]
    assert _find_node_depths(root, "c5") == [3]
    assert _find_node_depths(root, "j6") == [4]
    assert _find_node_depths(root, "c19") == [9]
    assert _find_node_depths(root, "j23") == [6]
    assert _find_node_depths(root, "c22") == [5]
    assert _find_node_depths(root, "j25") == [8]
    assert _find_node_depths(root, "c24") == [7]
    assert _find_node_depths(root, "j8") == [6]
    assert _find_node_depths(root, "c7") == [5]
    assert _find_node_depths(root, "j30") == [8]  # Would have been 8, 10, 12 if the intermediate loop was reprocessed.
    assert _find_node_depths(root, "c29") == [7]  # Would have been 7, 11, 13 if the intermediate loop was reprocessed.
    assert _find_node_depths(root, "j10") == [8, 10, 10]
    assert _find_node_depths(root, "c9") == [7, 10, 11, 14]
    assert _find_node_depths(root, "j12") == [10, 12, 12]
    assert _find_node_depths(root, "c31") == [9]  # Would have been 9, 9, 11 if the intermediate loop was reprocessed.
    assert _find_node_depths(root, "j27") == [8, 9, 12, 13]
    assert _find_node_depths(root, "c11") == [9, 11, 11]
    assert _find_node_depths(root, "c26") == [7, 10, 12, 13]
    assert _find_node_depths(root, "c28") == [8, 9, 11, 14]


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
