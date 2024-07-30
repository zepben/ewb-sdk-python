#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from zepben.evolve import ConnectivityResult, EnergySource, Terminal, AcLineSegment, EnergyConsumer, NetworkService, ConnectivityTracker


class TestConnectivityTracker:
    es_t = Terminal()
    es = EnergySource(terminals=[es_t])

    acls_t1, acls_t2 = Terminal(), Terminal()
    acls = AcLineSegment(terminals=[acls_t1, acls_t2])

    ec_t = Terminal()
    ac = EnergyConsumer(terminals=[ec_t])

    network = NetworkService()
    network.connect_terminals(es_t, acls_t1)
    network.connect_terminals(acls_t2, ec_t)

    def test_single_equipment_and_clear(self):
        tracker = ConnectivityTracker()
        cr = ConnectivityResult(self.es_t, self.acls_t1, [])

        assert not tracker.has_visited(cr), "has_visited returns false for unvisited equipment"
        assert tracker.visit(cr), "Visiting unvisited equipment returns true"
        assert tracker.has_visited(cr), "has_visited returns true for visited equipment"
        assert not tracker.visit(cr), "Revisiting visited equipment returns false"
        tracker.clear()
        assert not tracker.has_visited(cr), "Clearing delists all equipment"

    def test_tracking_connectivities_with_same_destination_equipment(self):
        tracker = ConnectivityTracker()
        cr1 = ConnectivityResult(self.es_t, self.acls_t1, [])
        cr2 = ConnectivityResult(self.ec_t, self.acls_t2, [])

        tracker.visit(cr1)
        assert tracker.has_visited(cr2), "Tracker has_visited connectivities with visited destination equipment"

    def test_copy(self):
        cr1 = ConnectivityResult(self.es_t, self.acls_t1, [])
        cr2 = ConnectivityResult(self.acls_t2, self.ec_t, [])

        tracker = ConnectivityTracker()
        tracker.visit(cr1)

        tracker_copy = tracker.copy()
        assert tracker is not tracker_copy, "Tracker copy is not a reference to the original tracker"
        assert tracker_copy.has_visited(cr1), "Tracker copy reports has_visited as True for steps original tracker visited"

        tracker_copy.visit(cr2)
        assert not tracker.has_visited(cr2), "Tracker copy maintains separate tracking records"
