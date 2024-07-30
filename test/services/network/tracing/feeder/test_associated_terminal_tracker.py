#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from zepben.evolve import AssociatedTerminalTracker, Terminal, Junction


def test_visit():
    """
    Verify that terminal tracking is linked to its conducting equipment
    """
    junction1 = Junction()
    junction2 = Junction()
    terminal11 = Terminal(conducting_equipment=junction1)
    terminal12 = Terminal(conducting_equipment=junction1)
    terminal21 = Terminal(conducting_equipment=junction2)
    terminal22 = Terminal(conducting_equipment=junction2)

    tracker = AssociatedTerminalTracker()

    assert not tracker.has_visited(terminal11), "has not visited terminal11"
    assert not tracker.has_visited(terminal12), "has not visited terminal12"
    assert not tracker.has_visited(terminal11), "has not visited terminal21"
    assert not tracker.has_visited(terminal12), "has not visited terminal22"

    assert tracker.visit(terminal11), "can visit terminal11"

    assert tracker.has_visited(terminal11), "has visited terminal11"
    assert tracker.has_visited(terminal12), "has visited terminal12"
    assert not tracker.has_visited(terminal21), "has not visited terminal21"
    assert not tracker.has_visited(terminal22), "has not visited terminal22"

    assert not tracker.visit(terminal11), "can't visit terminal11 twice"
    assert not tracker.visit(terminal12), "can't visit terminal12 after terminal11"
    assert tracker.visit(terminal22), "can visit terminal22"

    assert tracker.has_visited(terminal21), "has visited terminal21"
    assert tracker.has_visited(terminal22), "has visited terminal22"


def test_terminals_without_conducting_equipment_are_considered_visited():
    """
    Verify that a terminal that has no conducting equipment is considered visited even without being visited.
    """
    terminal = Terminal()

    tracker = AssociatedTerminalTracker()

    assert tracker.has_visited(terminal), "terminal is considered visited"


def test_cant_visit_terminals_without_conducting_equipment():
    """
    Verify that a terminal that has no conducting equipment can't be visited.
    """
    terminal = Terminal()

    tracker = AssociatedTerminalTracker()

    assert not tracker.visit(terminal), "can't visit terminal"
