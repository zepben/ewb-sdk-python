#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from zepben.evolve import ConductingEquipmentStepTracker, ConductingEquipmentStep, Junction


def test_visited_step_is_reported_as_visited():
    # noinspection PyArgumentList
    step = ConductingEquipmentStep(Junction())
    tracker = ConductingEquipmentStepTracker()

    # pylint: disable=protected-access
    print()
    print(step.conducting_equipment)
    print("----------------")
    assert not tracker.has_visited(step), "has_visited returns false for unvisited equipment"
    print(tracker._minimum_steps)
    print("----------------")
    assert tracker.visit(step), "Visiting unvisited equipment returns true"
    print(tracker._minimum_steps)
    print("----------------")
    assert tracker.has_visited(step), "has_visited returns true for visited equipment"
    print(tracker._minimum_steps)
    print("----------------")
    assert not tracker.visit(step), "Revisiting visited equipment returns false"
    print(tracker._minimum_steps)
    print("----------------")
    # pylint: enable=protected-access


def test_smaller_step_for_same_equipment_is_reported_as_unvisited():
    ce = Junction()
    # noinspection PyArgumentList
    step1 = ConductingEquipmentStep(ce, 1)
    # noinspection PyArgumentList
    step2 = ConductingEquipmentStep(ce)

    tracker = ConductingEquipmentStepTracker()
    tracker.visit(step1)

    assert not tracker.has_visited(step2), "has_visited returns false for smaller step of visited"
    assert tracker.visit(step2), "Visiting smaller step of visited returns true"


def test_larger_step_for_same_equipment_is_reported_as_visited():
    ce = Junction()
    # noinspection PyArgumentList
    step1 = ConductingEquipmentStep(ce)
    # noinspection PyArgumentList
    step2 = ConductingEquipmentStep(ce, 1)

    tracker = ConductingEquipmentStepTracker()
    tracker.visit(step1)

    assert tracker.has_visited(step2), "has_visited returns true for larger step of visited"
    assert not tracker.visit(step2), "Visiting larger step of visited returns false"


def test_steps_of_different_equipment_are_tracked_separately():
    # noinspection PyArgumentList
    step1 = ConductingEquipmentStep(Junction())
    # noinspection PyArgumentList
    step2 = ConductingEquipmentStep(Junction())

    tracker = ConductingEquipmentStepTracker()
    tracker.visit(step1)

    assert not tracker.has_visited(step2), "has_visited returns false for same step on different equipment"
    assert tracker.visit(step2), "Visiting same step on different equipment returns true"


def test_clear():
    # noinspection PyArgumentList
    step = ConductingEquipmentStep(Junction())

    tracker = ConductingEquipmentStepTracker()
    tracker.visit(step)
    tracker.clear()
    
    assert not tracker.has_visited(step), "clear un-visits all steps"


def test_copy():
    # noinspection PyArgumentList
    step1 = ConductingEquipmentStep(Junction())
    # noinspection PyArgumentList
    step2 = ConductingEquipmentStep(Junction())
    
    tracker = ConductingEquipmentStepTracker()
    # noinspection PyArgumentList
    tracker.visit(step1)
    
    tracker_copy = tracker.copy()
    assert tracker is not tracker_copy, "Tracker copy is not a reference to the original tracker"
    assert tracker_copy.has_visited(step1), "Tracker copy reports has_visited as True for steps original tracker visited"

    tracker_copy.visit(step2)
    assert not tracker.has_visited(step2), "Tracker copy maintains separate tracking records"
