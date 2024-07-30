#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from zepben.evolve import NetworkService, Terminal
from zepben.evolve.services.network.tracing.feeder.associated_terminal_tracker import AssociatedTerminalTracker

from network_fixtures import create_acls_for_connecting


def test_associated_terminal_tracker():
    ns = NetworkService()
    tracker = AssociatedTerminalTracker()

    assert tracker.has_visited(None)
    assert tracker.has_visited(Terminal())
    assert not tracker.visit(None)
    assert not tracker.visit(Terminal())

    acls1 = create_acls_for_connecting(ns, "acls1")
    t1 = acls1.get_terminal_by_sn(1)
    assert not tracker.has_visited(t1)
    assert tracker.visit(t1)
    assert tracker.has_visited(t1)
