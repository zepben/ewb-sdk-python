#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from zepben.evolve import Breaker, TreeNode, TreeNodeTracker


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


def test_copy():
    tn1 = TreeNode(Breaker(), None)
    tn2 = TreeNode(Breaker(), tn1)

    tracker = TreeNodeTracker()
    tracker.visit(tn1)

    tracker_copy = tracker.copy()
    assert tracker is not tracker_copy, "Tracker copy is not a reference to the original tracker"
    assert tracker_copy.has_visited(tn1), "Tracker copy reports has_visited as True for steps original tracker visited"

    tracker_copy.visit(tn2)
    assert not tracker.has_visited(tn2), "Tracker copy maintains separate tracking records"
