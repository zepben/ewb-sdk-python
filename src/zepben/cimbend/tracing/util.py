#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations
import logging
from zepben.cimbend.tracing.phase_step import PhaseStep
from zepben.cimbend.model.phasedirection import PhaseDirection
from zepben.cimbend.traversals.tracing import Traversal
from zepben.cimbend.traversals.queue import PriorityQueue, LifoQueue
from zepben.cimbend.tracing.phase_status import normal_phases, current_phases
from typing import Callable

__all__ = ["normally_open", "currently_open", "ignore_open", "queue_next_equipment", "queue_next_terminal", "normal_downstream_trace",
           "current_downstream_trace", "phase_log"]
phase_logger = logging.getLogger("phase_logger")
tracing_logger = logging.getLogger("queue_next")


def normally_open(equip: ConductingEquipment, phase: Optional[SinglePhaseKind] = None):
    """
    Test if a given core on an equipment is normally open.
    `equip` The equipment to test
    `phase` The Phase to test. If None tests all cores.
    Returns True if the equipment is open (de-energised), False otherwise
    """
    try:
        return not equip.normally_in_service or equip.is_normally_open(phase)
    except AttributeError:
        return not equip.normally_in_service


def currently_open(equip: ConductingEquipment, phase: Optional[SinglePhaseKind] = None):
    """
    Test if a given core on an equipment is open.
    `equip` The equipment to test
    `phase` The phase to test. If None tests all cores.
    Returns True if the equipment is open (de-energised), False otherwise
    """
    try:
        return not equip.in_service or equip.is_open(phase)
    except AttributeError:
        return not equip.in_service


def ignore_open(ce: ConductingEquipment, phase: Optional[SinglePhaseKind] = None):
    return False


def queue_next_equipment(item, exclude=None):
    connected_equips = item.get_connected_equipment(exclude=exclude)
    tracing_logger.debug(f"Queuing connections [{', '.join(e.mrid for e in connected_equips)}] from {item.mrid}")
    return connected_equips


def queue_next_terminal(item, exclude=None):
    """
    Wrapper tracing queue function for queuing terminals via their connectivity

    `item`
    `exclude`
    Returns
    """
    other_terms = item.get_other_terminals()
    if not other_terms:
        # If there are no other terminals we get connectivity for this one and return that. Note that this will
        # also return connections for EnergyConsumer's, but upstream will be covered by the exclude parameter and thus
        # should yield an empty list.
        to_terms = [cr.to_terminal for cr in item.get_connectivity(exclude=exclude)]
        if len(to_terms) > 0:
            tracing_logger.debug(f"Queuing {to_terms[0].mrid} from single terminal equipment {item.mrid}")
        return to_terms

    crs = []
    for term in other_terms:
        crs.extend(term.get_connectivity(exclude=exclude))

    to_terms = [cr.to_terminal for cr in crs]
    tracing_logger.debug(f"Queuing terminals: [{', '.join(t.mrid for t in to_terms)}] from {item.mrid}")
    return to_terms


def normal_downstream_trace(queue: Queue = None, **kwargs):
    """
    Create a downstream trace over nominal phases.

    `queue` Queue to use for this trace. Defaults to a `zepben.cimbend.traversals.queue.PriorityQueue`
    `kwargs` Args to be passed to `zepben.cimbend.tracing.tracing.Traversal`
    Returns A `zepben.cimbend.traversals.tracing.Traversal`
    """
    if queue is None:
        queue = PriorityQueue()
    return Traversal(queue_next=_create_downstream_queue_next(normally_open, normal_phases), process_queue=queue, **kwargs)


def current_downstream_trace(queue: Queue = None, **kwargs):
    """
    Create a downstream trace over current phases
    `queue` Queue to use for this trace. Defaults to a `zepben.cimbend.traversals.queue.PriorityQueue`
    `kwargs` Args to be passed to `zepben.cimbend.tracing.tracing.Traversal`
    Returns A `zepben.cimbend.traversals.tracing.Traversal`
    """
    return Traversal(queue_next=_create_downstream_queue_next(currently_open, current_phases), process_queue=queue, **kwargs)


def _create_downstream_queue_next(open_test: Callable[[ConductingEquipment, Optional[SinglePhaseKind]], bool],
                                  active_phases: Callable[[Terminal, SinglePhaseKind], PhaseStatus]):
    """
    Creates a queue_next function from the given open test and phase selector for use with traversals.
    `open_test` Function that takes a ConductingEquipment and a phase and returns whether the phase on the equipment is open (True) or closed (False).
    `active_phases` A `zepben.cimbend.tracing.phase_status.PhaseStatus`
    Returns A queue_next function for use with `zepben.cimbend.tracing.tracing.BaseTraversal` classes
    """

    def qn(phase_step, visited):
        connected_terms = []
        if not phase_step:
            return connected_terms
        out_phases = set()
        for term in phase_step.conducting_equipment.terminals:
            _get_phases_with_direction(open_test, active_phases, term, phase_step.phases, PhaseDirection.OUT, out_phases)

            if out_phases:
                crs = get_connectivity(term, out_phases)
                for cr in crs:
                    if cr.to_equip is not None:
                        if cr.to_equip in visited:
                            continue
                        connected_terms.append(PhaseStep(cr.to_equip, out_phases, cr.from_equip))
        return connected_terms
    return qn


def _get_phases_with_direction(open_test: Callable[[ConductingEquipment, Optional[SinglePhaseKind]], bool],
                               active_phases: Callable[[Terminal, SinglePhaseKind], PhaseStatus],
                               terminal: Terminal,
                               candidate_phases: Set[SinglePhaseKind],
                               direction: PhaseDirection,
                               matched_phases: Set[SinglePhaseKind]):
    """
    Adds the closed phases from `terminal` in a specified `zepben.cimbend.model.phasedirection.PhaseDirection` to `matched_phases`.

    `open_test` Function that takes a ConductingEquipment and a phase and returns whether the phase on the equipment is open (True) or closed (False).
    `active_phases` A `zepben.cimbend.tracing.phase_status.PhaseStatus`
    `terminal` `zepben.cimbend.cim.iec61970.base.core.terminal.Terminal` to retrieve phases for
    `filter_cores` The phases of `terminal` to test.
    `direction` The `zepben.cimbend.model.phasedirection.PhaseDirection` to check against.
    `matched_phases` The set of matched phases to add to.
    """
    if terminal.conducting_equipment is None:
        raise TraceException(f"Terminal {terminal} did not have an associated ConductingEquipment, cannot get phases.")
    for phase in candidate_phases:
        if phase in terminal.phases.single_phases and not open_test(terminal.conducting_equipment, phase):
            if active_phases(terminal, phase).direction().has(direction):
                matched_phases.add(phase)


async def phase_log(cond_equip):
    msg = ""
    try:
        for e in cond_equip:
            msg = await _phase_log_trace(e)
    except:
        msg = await _phase_log_trace(cond_equip)
    phase_logger.debug(msg)


async def _phase_log_trace(cond_equip):
    log_msg = []

    async def log(e, exc):
        equip_msgs = []
        for term in e.terminals:
            e_msg = f"{e.mrid}-T{term.sequence_number}:"
            for n in term.phases.single_phases:
                ps_n = normal_phases(term, n)
                phase_n_msg = f"n: {ps_n.phase().short_name}:{ps_n.direction().short_name}"
                ps_c = current_phases(term, n)
                phase_c_msg = f"c: {ps_c.phase().short_name}:{ps_c.direction().short_name}"
                e_msg = f"{e_msg} {{core {n}: {phase_n_msg} {phase_c_msg}}}"
            equip_msgs.append(e_msg)
        log_msg.append(equip_msgs)

    trace = Traversal(queue_next=queue_next_equipment, start_item=cond_equip, process_queue=LifoQueue(), step_actions=[log])
    await trace.trace()
    return "\n".join([", ".join(x) for x in log_msg])
