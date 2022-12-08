#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from zepben.evolve import Breaker
from zepben.evolve.services.network.tracing.tree.downstream_tree import TreeNode
from zepben.evolve.services.network.tracing.tree.tree_node_tracker import TreeNodeTracker


def test_single_tree_node_and_clear():
    tracker = TreeNodeTracker()
    tn = TreeNode(Breaker(), None)

    assert not tracker.has_visited(tn), "has_visited returns false for unvisited equipment"
    assert tracker.visit(tn), "Visiting unvisited equipment returns true"
    assert tracker.has_visited(tn), "has_visited returns true for visited equipment"
    assert not tracker.visit(tn), "Revisiting visited equipment returns false"
    tracker.clear()
    assert not tracker.has_visited(tn), "Clearing delists all equipment"


def test_tracking_tree_nodes_with_same_equipment():
    tracker = TreeNodeTracker()
    ce = Breaker()
    tn1 = TreeNode(ce, None)
    tn2 = TreeNode(ce, tn1)

    tracker.visit(tn1)
    assert tracker.has_visited(tn2), "Tracker has_visited tree nodes with visited equipment"
