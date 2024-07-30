#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from zepben.evolve import BasicTracker


def test_single_item_and_clear():
    tracker: BasicTracker[int] = BasicTracker()

    assert not tracker.has_visited(123), "has_visited returns false for unvisited item"
    assert tracker.visit(123), "Visiting unvisited equipment returns True"
    assert tracker.has_visited(123), "has_visited returns True for visited item"
    assert not tracker.visit(123), "Revisiting visited equipment returns False"
    tracker.clear()
    assert not tracker.has_visited(123), "Clearing delists all items"


def test_copy():
    tracker: BasicTracker[int] = BasicTracker()
    # noinspection PyArgumentList
    tracker.visit(1)

    tracker_copy = tracker.copy()
    assert tracker is not tracker_copy, "Tracker copy is not a reference to the original tracker"
    assert tracker_copy.has_visited(1), "Tracker copy reports has_visited as True for steps original tracker visited"

    tracker_copy.visit(2)
    assert not tracker.has_visited(2), "Tracker copy maintains separate tracking records"
