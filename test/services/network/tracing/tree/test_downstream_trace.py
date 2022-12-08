#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
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
