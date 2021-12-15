#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Optional, Callable, Set, Iterable, TypeVar

from zepben.evolve.model.cim.iec61970.base.core.conducting_equipment import ConductingEquipment
from zepben.evolve.model.cim.iec61970.base.core.terminal import Terminal
from zepben.evolve.model.cim.iec61970.base.wires.single_phase_kind import SinglePhaseKind
from zepben.evolve.model.phasedirection import PhaseDirection
from zepben.evolve.services.network.tracing.feeder.assign_to_feeders import AssignToFeeders
from zepben.evolve.services.network.tracing.phases.phase_step import PhaseStep
from zepben.evolve.services.network.tracing.phases.phase_status import PhaseStatus, current_phases, normal_phases
from zepben.evolve.services.network.tracing.connectivity import get_connectivity
from zepben.evolve.services.network.tracing.queuing_functions import conducting_equipment_queue_next
from zepben.evolve.services.network.tracing.util import currently_open, normally_open
from zepben.evolve.services.network.tracing.traversals.tracing import Traversal
from zepben.evolve.services.network.tracing.traversals.queue import depth_first, Queue, PriorityQueue

__all__ = ["normal_downstream_trace", "create_basic_depth_trace", "connected_equipment_trace", "current_downstream_trace",
           "assign_equipment_containers_to_feeders"]


T = TypeVar("T")


def connected_equipment_trace():
    return create_basic_depth_trace(conducting_equipment_queue_next)


def create_basic_depth_trace(queue_next: Callable[[T, Set[T]], Iterable[T]]):
    return Traversal(queue_next, depth_first())


def current_downstream_trace(queue: Queue = None, **kwargs):
    """
    Create a downstream trace over current phases
    `queue` Queue to use for this trace. Defaults to a `zepben.evolve.traversals.queue.PriorityQueue`
    `kwargs` Args to be passed to `zepben.evolve.Traversal`
    Returns A `zepben.evolve.traversals.Traversal`
    """
    return Traversal(queue_next=_create_downstream_queue_next(currently_open, current_phases), process_queue=queue, **kwargs)


def _create_downstream_queue_next(open_test: Callable[[ConductingEquipment, Optional[SinglePhaseKind]], bool],
                                  active_phases: Callable[[Terminal, SinglePhaseKind], PhaseStatus]):
    """
    Creates a queue_next function from the given open test and phase selector for use with traversals.
    `open_test` Function that takes a ConductingEquipment and a phase and returns whether the phase on the equipment is open (True) or closed (False).
    `active_phases` A `zepben.evolve.phase_status.PhaseStatus`
    Returns A queue_next function for use with `zepben.evolve.BaseTraversal` classes
    """
    def qn(phase_step, visited):
        connected_terms = []
        if not phase_step:
            return connected_terms
        out_phases = set()
        for term in phase_step.conducting_equipment.terminals:
            _get_phases_with_direction(open_test, active_phases, term, phase_step.phases.single_phases, PhaseDirection.OUT, out_phases)

            if out_phases:
                crs = get_connectivity(term, out_phases)
                for cr in crs:
                    if cr.to_equip is not None:
                        if cr.to_equip in visited:
                            continue
                        connected_terms.append(PhaseStep(cr.to_equip, out_phases, cr.from_equip))
        return connected_terms
    return qn


def normal_downstream_trace(queue: Queue = None, **kwargs):
    """
    Create a downstream trace over nominal phases.

    `queue` Queue to use for this trace. Defaults to a `zepben.evolve.traversals.queue.PriorityQueue`
    `kwargs` Args to be passed to `zepben.evolve.Traversal`
    Returns A `zepben.evolve.traversals.Traversal`
    """
    if queue is None:
        queue = PriorityQueue()
    return Traversal(queue_next=_create_downstream_queue_next(normally_open, normal_phases), process_queue=queue, **kwargs)


def _get_phases_with_direction(open_test: Callable[[ConductingEquipment, Optional[SinglePhaseKind]], bool],
                               active_phases: Callable[[Terminal, SinglePhaseKind], PhaseStatus],
                               terminal: Terminal,
                               candidate_phases: Set[SinglePhaseKind],
                               direction: PhaseDirection,
                               matched_phases: Set[SinglePhaseKind]):
    """
    Adds the closed phases from `terminal` in a specified `zepben.evolve.model.phasedirection.PhaseDirection` to `matched_phases`.

    `open_test` Function that takes a ConductingEquipment and a phase and returns whether the phase on the equipment is open (True) or closed (False).
    `active_phases` A `zepben.evolve.phase_status.PhaseStatus`
    `terminal` `zepben.evolve.cim.iec61970.base.core.terminal.Terminal` to retrieve phases for
    `filter_cores` The phases of `terminal` to test.
    `direction` The `zepben.evolve.model.phasedirection.PhaseDirection` to check against.
    `matched_phases` The set of matched phases to add to.
    """
    if terminal.conducting_equipment is None:
        raise TraceException(f"Terminal {terminal} did not have an associated ConductingEquipment, cannot get phases.")
    for phase in candidate_phases:
        if phase in terminal.phases.single_phases and not open_test(terminal.conducting_equipment, phase):
            if active_phases(terminal, phase).direction().has(direction):
                matched_phases.add(phase)


def assign_equipment_containers_to_feeders():
    """Returns an instance of `zepben.evolve.services.network.tracing.feeder.assign_to_feeders.AssignToFeeders convenience class for assigning equipment
    containers to feeders on a network."""
    return AssignToFeeders()


class TraceException(Exception):
    pass


