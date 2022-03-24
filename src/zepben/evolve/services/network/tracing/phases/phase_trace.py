#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations

from typing import TYPE_CHECKING, Set, Iterable, Union, Optional

from zepben.evolve.exceptions import TracingException
from zepben.evolve.services.network.network_service import connected_terminals
from zepben.evolve.services.network.tracing.feeder.feeder_direction import FeederDirection
from zepben.evolve.services.network.tracing.phases.phase_step_tracker import PhaseStepTracker
from zepben.evolve.services.network.tracing.traversals.queue import PriorityQueue
from zepben.evolve.services.network.tracing.phases.phase_step import PhaseStep
from zepben.evolve.services.network.tracing.traversals.traversal import Traversal
if TYPE_CHECKING:
    from zepben.evolve import Terminal, SinglePhaseKind, ConnectivityResult, ConductingEquipment, PhaseCode
    from zepben.evolve.types import OpenTest, QueueNext, DirectionSelector

__all__ = ["new_phase_trace", "new_downstream_phase_trace", "new_upstream_phase_trace"]


def new_phase_trace(open_test: OpenTest) -> Traversal[PhaseStep]:
    # noinspection PyArgumentList
    return Traversal(queue_next=_queue_next(open_test), process_queue=PriorityQueue(), tracker=PhaseStepTracker())


def new_downstream_phase_trace(open_test: OpenTest, active_direction: DirectionSelector) -> Traversal[PhaseStep]:
    # noinspection PyArgumentList
    return Traversal(queue_next=_queue_next_downstream(open_test, active_direction), process_queue=PriorityQueue(), tracker=PhaseStepTracker())


def new_upstream_phase_trace(open_test: OpenTest, active_direction: DirectionSelector) -> Traversal[PhaseStep]:
    # noinspection PyArgumentList
    return Traversal(queue_next=_queue_next_upstream(open_test, active_direction), process_queue=PriorityQueue(), tracker=PhaseStepTracker())


def _queue_next(open_test: OpenTest) -> QueueNext[PhaseStep]:
    def queue_next(phase_step: PhaseStep, traversal: Traversal[PhaseStep]):
        down_phases = set()

        for term in phase_step.conducting_equipment.terminals:
            down_phases.clear()
            for phase in phase_step.phases:
                if not open_test(phase_step.conducting_equipment, phase):
                    down_phases.add(phase)

            _queue_connected(traversal, term, down_phases)

    return queue_next


def _queue_next_downstream(open_test: OpenTest, active_direction: DirectionSelector) -> QueueNext[PhaseStep]:
    def queue_next(phase_step: PhaseStep, traversal: Traversal[PhaseStep]):
        for term in phase_step.conducting_equipment.terminals:
            _queue_connected(traversal, term, _get_phases_with_direction(open_test, active_direction, term, phase_step.phases, FeederDirection.DOWNSTREAM))

    return queue_next


def _queue_next_upstream(open_test: OpenTest, active_direction: DirectionSelector) -> QueueNext[PhaseStep]:
    def queue_next(phase_step: PhaseStep, traversal: Traversal[PhaseStep]):
        for term in phase_step.conducting_equipment.terminals:
            up_phases = _get_phases_with_direction(open_test, active_direction, term, phase_step.phases, FeederDirection.UPSTREAM)
            if up_phases:
                for cr in connected_terminals(term, up_phases):
                    # When going upstream, we only want to traverse to connected terminals that have a DOWNSTREAM direction
                    if active_direction(cr.to_terminal).value().has(FeederDirection.DOWNSTREAM):
                        _try_queue(traversal, cr, cr.to_nominal_phases)

    return queue_next


def _queue_connected(traversal: Traversal[PhaseStep], terminal: Terminal, down_phases: Set[SinglePhaseKind]):
    if down_phases:
        for cr in connected_terminals(terminal, down_phases):
            _try_queue(traversal, cr, cr.to_nominal_phases)


def _try_queue(traversal: Traversal[PhaseStep], cr: ConnectivityResult, down_phases: Iterable[SinglePhaseKind]):
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

    if not active_direction(terminal).value().has(direction):
        return matched_phases

    conducting_equipment = terminal.conducting_equipment
    if conducting_equipment is None:
        raise TracingException(f"Missing conducting equipment for terminal {terminal.mrid}.")

    for phase in candidate_phases:
        if phase in terminal.phases.single_phases and not open_test(conducting_equipment, phase):
            matched_phases.add(phase)

    return matched_phases
