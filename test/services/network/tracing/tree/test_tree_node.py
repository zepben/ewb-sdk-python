#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import List

from zepben.evolve import Junction, TreeNode, PhaseCode, Terminal, AcLineSegment


def test_accessors():
    tree_node_0 = TreeNode(Junction(mrid="node0"), None)
    tree_node_1 = TreeNode(Junction(mrid="node1"), tree_node_0)
    tree_node_2 = TreeNode(Junction(mrid="node2"), tree_node_0)
    tree_node_3 = TreeNode(Junction(mrid="node3"), tree_node_0)
    tree_node_4 = TreeNode(Junction(mrid="node4"), tree_node_3)
    tree_node_5 = TreeNode(Junction(mrid="node5"), tree_node_3)
    tree_node_6 = TreeNode(Junction(mrid="node6"), tree_node_5)
    tree_node_7 = TreeNode(Junction(mrid="node7"), tree_node_6)
    tree_node_8 = TreeNode(Junction(mrid="node8"), tree_node_7)
    tree_node_9 = TreeNode(Junction(mrid="node9"), tree_node_8)

    assert tree_node_0.conducting_equipment.mrid == "node0"
    assert tree_node_0.parent is None

    tree_node_0.add_child(tree_node_1)
    tree_node_0.add_child(tree_node_2)
    tree_node_0.add_child(tree_node_3)
    tree_node_3.add_child(tree_node_4)
    tree_node_3.add_child(tree_node_5)
    tree_node_5.add_child(tree_node_6)
    tree_node_6.add_child(tree_node_7)
    tree_node_7.add_child(tree_node_8)
    tree_node_8.add_child(tree_node_9)

    children = list(tree_node_0.children)
    assert tree_node_1 in children
    assert tree_node_2 in children
    assert tree_node_3 in children

    tree_nodes = [tree_node_0, tree_node_1, tree_node_2, tree_node_3, tree_node_4, tree_node_5, tree_node_6, tree_node_7, tree_node_8, tree_node_9]
    _assert_children(tree_nodes, [3, 0, 0, 2, 0, 1, 1, 1, 1, 0])
    _assert_parents(tree_nodes, [-1, 0, 0, 0, 3, 3, 5, 6, 7, 8])


def test_sort_weight():
    tree_node_0 = TreeNode(Junction(mrid="node0"), None)
    tree_node_1 = TreeNode(Junction(mrid="node1", terminals=[Terminal(phases=PhaseCode.AB)]), None)

    assert tree_node_0.sort_weight == 1
    assert tree_node_1.sort_weight == 2

    # Nodes for equipment with more phases on their terminals come first when building equipment trees.
    assert tree_node_1 < tree_node_0


def test_str():
    tree_node_0 = TreeNode(Junction(mrid="junction"), None)
    tree_node_1 = TreeNode(AcLineSegment(mrid="acls"), tree_node_0)
    tree_node_0.add_child(tree_node_1)

    assert str(tree_node_0) == "{conducting_equipment: junction, parent: None, num children: 1}"
    assert str(tree_node_1) == "{conducting_equipment: acls, parent: junction, num children: 0}"


def _assert_children(tree_nodes: List[TreeNode], child_counts: List[int]):
    assert len(tree_nodes) == len(child_counts)
    for node, count in zip(tree_nodes, child_counts):
        assert len(list(node.children)) == count


def _assert_parents(tree_nodes: List[TreeNode], parents: List[int]):
    for i, node in enumerate(tree_nodes):
        if parents[i] < 0:
            assert node.parent is None
        else:
            assert node.parent is tree_nodes[parents[i]]
