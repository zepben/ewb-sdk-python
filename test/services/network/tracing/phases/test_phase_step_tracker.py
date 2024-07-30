#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from zepben.evolve import PhaseStepTracker, Junction, PhaseCode
from zepben.evolve.services.network.tracing.phases import phase_step


def test_visited_set_of_phases_is_reported_as_visited():
    tracker = PhaseStepTracker()
    ce = Junction()
    step = phase_step.start_at(ce, PhaseCode.AB)

    assert not tracker.has_visited(step), "has_visited returns False for unvisited equipment"
    assert tracker.visit(step), "Visiting phases on unvisited equipment returns True"
    assert tracker.has_visited(step), "has_visited returns True for visited phase set"
    assert not tracker.visit(step), "Visiting visited phases returns False"


def test_set_of_phases_disjoint_from_visited_phases_is_reported_as_unvisited():
    tracker = PhaseStepTracker()
    ce = Junction()
    step1 = phase_step.start_at(ce, PhaseCode.AB)
    step2 = phase_step.start_at(ce, PhaseCode.CN)

    tracker.visit(step1)

    assert not tracker.has_visited(step2), "has_visited returns False for phase set disjoint from visited phases"
    assert tracker.visit(step2), "Visiting phase set disjoint from visited phases returns True"


def test_set_of_phases_partially_overlapping_with_visited_phases_is_reported_as_unvisited():
    tracker = PhaseStepTracker()
    ce = Junction()
    step1 = phase_step.start_at(ce, PhaseCode.AB)
    step2 = phase_step.start_at(ce, PhaseCode.BC)

    tracker.visit(step1)

    assert not tracker.has_visited(step2), "has_visited returns False for phase set partially overlapping visited phases"
    assert tracker.visit(step2), "Visiting phase set partially overlapping visited phases returns True"


def test_strict_subset_of_visited_phases_is_reported_as_visited():
    tracker = PhaseStepTracker()
    ce = Junction()
    step1 = phase_step.start_at(ce, PhaseCode.ABC)
    step2 = phase_step.start_at(ce, PhaseCode.BC)

    tracker.visit(step1)

    assert tracker.has_visited(step2), "has_visited returns True for strict subset of visited phases"
    assert not tracker.visit(step2), "Visiting strict subset of visited phases returns False"


def test_phases_of_different_equipment_are_tracked_separately():
    tracker = PhaseStepTracker()
    ce1 = Junction()
    ce2 = Junction()
    step1 = phase_step.start_at(ce1, PhaseCode.AB)
    step2 = phase_step.continue_at(ce2, PhaseCode.AB, ce1)

    tracker.visit(step1)

    assert not tracker.has_visited(step2), "has_visited returns False for same phases on different equipment"
    assert tracker.visit(step2), "Visiting same phases on different equipment returns True"


def test_clear():
    # noinspection PyArgumentList
    step = phase_step.start_at(Junction(), PhaseCode.ABCN)

    tracker = PhaseStepTracker()
    tracker.visit(step)
    tracker.clear()

    assert not tracker.has_visited(step), "clear un-visits all steps"


def test_copy():
    # noinspection PyArgumentList
    step1 = phase_step.start_at(Junction(), PhaseCode.ABCN)
    # noinspection PyArgumentList
    step2 = phase_step.start_at(Junction(), PhaseCode.ABCN)

    tracker = PhaseStepTracker()
    # noinspection PyArgumentList
    tracker.visit(step1)

    tracker_copy = tracker.copy()
    assert tracker is not tracker_copy, "Tracker copy is not a reference to the original tracker"
    assert tracker_copy.has_visited(step1), "Tracker copy reports has_visited as True for steps original tracker visited"

    tracker_copy.visit(step2)
    assert not tracker.has_visited(step2), "Tracker copy maintains separate tracking records"
