#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from zepben.evolve import ConductingEquipmentStepTracker, ConductingEquipmentStep, Junction


class TestConductingEquipmentStepTracker:

    tracker = ConductingEquipmentStepTracker()

    def test_visited_step_is_reported_as_visited(self):
        # noinspection PyArgumentList
        step = ConductingEquipmentStep(Junction())

        # pylint: disable=protected-access
        print()
        print(step.conducting_equipment)
        print("----------------")
        assert not(self.tracker.has_visited(step)), "has_visited returns false for unvisited equipment"
        print(self.tracker._minimum_steps)
        print("----------------")
        assert self.tracker.visit(step), "Visiting unvisited equipment returns true"
        print(self.tracker._minimum_steps)
        print("----------------")
        assert self.tracker.has_visited(step), "has_visited returns true for visited equipment"
        print(self.tracker._minimum_steps)
        print("----------------")
        assert not(self.tracker.visit(step)), "Revisiting visited equipment returns false"
        print(self.tracker._minimum_steps)
        print("----------------")
        # pylint: enable=protected-access

    def test_smaller_step_for_same_equipment_is_reported_as_unvisited(self):
        ce = Junction()
        # noinspection PyArgumentList
        step1 = ConductingEquipmentStep(ce, 1)
        # noinspection PyArgumentList
        step2 = ConductingEquipmentStep(ce)

        self.tracker.visit(step1)

        assert not(self.tracker.has_visited(step2)), "has_visited returns false for smaller step of visited"
        assert self.tracker.visit(step2), "Visiting smaller step of visited returns true"

    def test_larger_step_for_same_equipment_is_reported_as_visited(self):
        ce = Junction()
        # noinspection PyArgumentList
        step1 = ConductingEquipmentStep(ce)
        # noinspection PyArgumentList
        step2 = ConductingEquipmentStep(ce, 1)

        self.tracker.visit(step1)

        assert self.tracker.has_visited(step2), "has_visited returns true for larger step of visited"
        assert not(self.tracker.visit(step2)), "Visiting larger step of visited returns false"

    def test_steps_of_different_equipment_are_tracked_separately(self):
        # noinspection PyArgumentList
        step1 = ConductingEquipmentStep(Junction())
        # noinspection PyArgumentList
        step2 = ConductingEquipmentStep(Junction())

        self.tracker.visit(step1)

        assert not(self.tracker.has_visited(step2)), "has_visited returns false for same step on different equipment"
        assert self.tracker.visit(step2), "Visiting same step on different equipment returns true"
