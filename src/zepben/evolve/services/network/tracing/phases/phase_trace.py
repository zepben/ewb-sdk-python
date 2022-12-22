#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations

from typing import TYPE_CHECKING, Set, Iterable, Union, Optional

from zepben.evolve import FeederDirection, connected_terminals, PhaseCode, PhaseStep, PriorityQueue, PhaseStepTracker, BasicTraversal
from zepben.evolve.exceptions import TracingException

if TYPE_CHECKING:
    from zepben.evolve import Terminal, SinglePhaseKind, ConnectivityResult, ConductingEquipment
    from zepben.evolve.types import OpenTest, QueueNext, DirectionSelector

__all__ = ["new_phase_trace", "new_downstream_phase_trace", "new_upstream_phase_trace"]


def new_phase_trace(open_test: OpenTest) -> BasicTraversal[PhaseStep]:
    """
    Creates a new phase-based trace using the provided open state test.

    :param open_test: The test to use when checking if an object should be considered open.
    :return: The new traversal instance.
    """
    # noinspection PyArgumentList
    return BasicTraversal(queue_next=_queue_next(open_test), process_queue=PriorityQueue(), tracker=PhaseStepTracker())


def new_downstream_phase_trace(open_test: OpenTest, active_direction: DirectionSelector) -> BasicTraversal[PhaseStep]:
    """
    Creates a new downstream trace based on the specified phases and state of the network. Note that the phases
    need to be set on the network before a concept of downstream is known.

    :param open_test: The test to use when checking if an object should be considered open.
    :param active_direction: The direction selector that will be used to determine which state of the network to use.
    :return: The new traversal instance.
    """
    # noinspection PyArgumentList
    return BasicTraversal(queue_next=_queue_next_downstream(open_test, active_direction), process_queue=PriorityQueue(), tracker=PhaseStepTracker())


def new_upstream_phase_trace(open_test: OpenTest, active_direction: DirectionSelector) -> BasicTraversal[PhaseStep]:
    """
    Creates a new upstream trace based on the specified phases and state of the network. Note that the phases
    need to be set on the network before a concept of downstream is known.

    :param open_test: The test to use when checking if an object should be considered open.
    :param active_direction: The direction selector that will be used to determine which state of the network to use.
    :return: The new traversal instance.
    """
    # noinspection PyArgumentList
    return BasicTraversal(queue_next=_queue_next_upstream(open_test, active_direction), process_queue=PriorityQueue(), tracker=PhaseStepTracker())


def _queue_next(open_test: OpenTest) -> QueueNext[PhaseStep]:
    def queue_next(phase_step: PhaseStep, traversal: BasicTraversal[PhaseStep]):
        down_phases = set()

        for term in phase_step.conducting_equipment.terminals:
            down_phases.clear()
            for phase in phase_step.phases:
                if not open_test(phase_step.conducting_equipment, phase):
                    down_phases.add(phase)

            _queue_connected(traversal, term, down_phases)

    return queue_next


def _queue_next_downstream(open_test: OpenTest, active_direction: DirectionSelector) -> QueueNext[PhaseStep]:
    def queue_next(phase_step: PhaseStep, traversal: BasicTraversal[PhaseStep]):
        for term in phase_step.conducting_equipment.terminals:
            _queue_connected(traversal, term, _get_phases_with_direction(open_test, active_direction, term, phase_step.phases, FeederDirection.DOWNSTREAM))

    return queue_next


def _queue_next_upstream(open_test: OpenTest, active_direction: DirectionSelector) -> QueueNext[PhaseStep]:
    def queue_next(phase_step: PhaseStep, traversal: BasicTraversal[PhaseStep]):
        for term in phase_step.conducting_equipment.terminals:
            up_phases = _get_phases_with_direction(open_test, active_direction, term, phase_step.phases, FeederDirection.UPSTREAM)
            if up_phases:
                for cr in connected_terminals(term, up_phases):
                    # When going upstream, we only want to traverse to connected terminals that have a DOWNSTREAM direction
                    if FeederDirection.DOWNSTREAM in active_direction(cr.to_terminal).value():
                        _try_queue(traversal, cr, cr.to_nominal_phases)

    return queue_next


def _queue_connected(traversal: BasicTraversal[PhaseStep], terminal: Terminal, down_phases: Set[SinglePhaseKind]):
    if down_phases:
        for cr in connected_terminals(terminal, down_phases):
            _try_queue(traversal, cr, cr.to_nominal_phases)


def _try_queue(traversal: BasicTraversal[PhaseStep], cr: ConnectivityResult, down_phases: Iterable[SinglePhaseKind]):
    if cr.to_equip:
        traversal.process_queue.put(_continue_at(cr.to_equip, down_phases, cr.from_equip))


def _continue_at(conducting_equipment: ConductingEquipment,
                 phases: Union[PhaseCode, Iterable[SinglePhaseKind]],
                 previous: Optional[ConductingEquipment]) -> PhaseStep:
    if isinstance(phases, PhaseCode):
        phases = phases.single_phases

    # noinspection PyArgumentList
    return PhaseStep(conducting_equipment, frozenset(phases), previous)


def _get_phases_with_direction(open_test: OpenTest,
                               active_direction: DirectionSelector,
                               terminal: Terminal,
                               candidate_phases: Iterable[SinglePhaseKind],
                               direction: FeederDirection) -> Set[SinglePhaseKind]:
    matched_phases: Set[SinglePhaseKind] = set()

    if direction not in active_direction(terminal).value():
        return matched_phases

    conducting_equipment = terminal.conducting_equipment
    if conducting_equipment is None:
        raise TracingException(f"Missing conducting equipment for terminal {terminal.mrid}.")

    for phase in candidate_phases:
        if phase in terminal.phases.single_phases and not open_test(conducting_equipment, phase):
            matched_phases.add(phase)

    return matched_phases
