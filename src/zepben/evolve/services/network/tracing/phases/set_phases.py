#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

import itertools
from typing import TYPE_CHECKING, Union, Set, Callable, List, Iterable, Optional

from zepben.evolve.model.cim.iec61970.base.core.phase_code import PhaseCode
from zepben.evolve.model.cim.iec61970.base.wires.energy_source import EnergySource
from zepben.evolve.model.cim.iec61970.base.wires.single_phase_kind import SinglePhaseKind
from zepben.evolve.exceptions import PhaseException
from zepben.evolve.services.network.tracing.connectivity.connectivity_result import get_connectivity
from zepben.evolve.exceptions import TracingException
from zepben.evolve.services.network.tracing.phases.phase_status import normal_phases, current_phases
from zepben.evolve.services.network.tracing.traversals.queue import PriorityQueue
from zepben.evolve.services.network.tracing.traversals.branch_recursive_tracing import BranchRecursiveTraversal
from zepben.evolve.services.network.tracing.util import normally_open, currently_open
if TYPE_CHECKING:
    from zepben.evolve import Terminal, ConductingEquipment, NetworkService, PhaseStatus
    PhaseSelector = Callable[[Terminal], PhaseStatus]

__all__ = ["SetPhases", "spread_phases"]


class SetPhases(object):
    """
    Convenience class that provides methods for setting phases on a `NetworkService`.
    This class is backed by a `BranchRecursiveTraversal`.
    """

    def __init__(self):
        # The `BranchRecursiveTraversal` used when tracing the normal state of the network.
        # NOTE: If you add stop conditions to this traversal it may no longer work correctly, use at your own risk.
        # noinspection PyArgumentList
        self.normal_traversal = BranchRecursiveTraversal(queue_next=_set_normal_phases_and_queue_next,
                                                         process_queue=PriorityQueue(),
                                                         branch_queue=PriorityQueue())

        # The `BranchRecursiveTraversal` used when tracing the current state of the network.
        # NOTE: If you add stop conditions to this traversal it may no longer work correctly, use at your own risk.
        # noinspection PyArgumentList
        self.current_traversal = BranchRecursiveTraversal(queue_next=_set_current_phases_and_queue_next,
                                                          process_queue=PriorityQueue(),
                                                          branch_queue=PriorityQueue())

    async def run(self, network: NetworkService):
        """
        Apply phases from all sources in the network.

        @param network: The network in which to apply phases.
        """
        terminals = [term for es in network.objects(EnergySource) for term in es.terminals]

        for term in terminals:
            _apply_phases(term, normal_phases, term.phases.single_phases)
            _apply_phases(term, current_phases, term.phases.single_phases)

        await self._run_with_terminals(terminals)

    async def run_with_terminal(self, terminal: Terminal, phases: Union[None, PhaseCode, List[SinglePhaseKind]] = None):
        """
        Apply phases from the `terminal`.

        @param terminal: The terminal to start applying phases from.
        @param phases: The phases to apply. Must only contain ABCN.
        """
        phases = phases or terminal.phases
        if isinstance(phases, PhaseCode):
            phases = phases.single_phases

        if len(phases) != len(terminal.phases.single_phases):
            raise TracingException(
                f"Attempted to apply phases [{', '.join(phase.name for phase in phases)}] to {terminal} with nominal phases {terminal.phases.name}. "
                f"Number of phases to apply must match the number of nominal phases. Found {len(phases)}, expected {len(terminal.phases.single_phases)}"
            )

        _apply_phases(terminal, normal_phases, phases)
        _apply_phases(terminal, current_phases, phases)

        self.normal_traversal.tracker.clear()
        self.current_traversal.tracker.clear()

        await self._run_with_terminals([terminal])

    async def run_with_terminal_and_phase_selector(self, terminal: Terminal, phase_selector: PhaseSelector):
        """
        Apply phases from the `terminal` on the selected phases. Only spreads existing phases.

        @param terminal: The terminal from which to spread phases.
        @param phase_selector: The selector to use to spread the phases. Must be `normal_phases` or `current_phases`.

        @return: True if any phases were spread, otherwise False.
        """
        if phase_selector is normal_phases:
            await _run_with_traversal_and_phase_selector([terminal], self.normal_traversal, phase_selector)
        elif phase_selector is current_phases:
            await _run_with_traversal_and_phase_selector([terminal], self.current_traversal, phase_selector)
        else:
            raise TracingException("Invalid PhaseSelector specified. Must be normal_phases or current_phases")

    async def _run_with_terminals(self, start_terminals: Iterable[Terminal]):
        await _run_with_traversal_and_phase_selector(start_terminals, self.normal_traversal, normal_phases)
        await _run_with_traversal_and_phase_selector(start_terminals, self.current_traversal, current_phases)


def spread_phases(from_terminal: Terminal,
                  to_terminal: Terminal,
                  phase_selector: PhaseSelector,
                  phases_to_flow: Optional[Set[SinglePhaseKind]] = None) -> bool:
    """
    Apply phases from the `from_terminal` to the `to_terminal`.

    @param from_terminal: The terminal to from which to spread phases.
    @param to_terminal: The terminal to spread phases to.
    @param phase_selector: The selector to use to spread the phases.
    @param phases_to_flow: The nominal phases on which to spread phases.

    @return: True if any phases were spread, otherwise False.
    """
    phase_selector = phase_selector or set(from_terminal.phases.single_phases)

    from_phases = phase_selector(from_terminal)
    to_phases = phase_selector(to_terminal)

    has_changes = False
    for phase in phases_to_flow:
        try:
            has_changes = to_phases.__setitem__(phase, from_phases[phase]) or has_changes
        except PhaseException as ex:
            raise PhaseException(
                f"Attempted to flow conflicting phase {from_phases[phase].name} onto {to_phases[phase].name} on nominal phase {phase.name}. "
                f"This occurred while flowing from {from_terminal} to {to_terminal} through {to_terminal.conducting_equipment}. This is caused by missing "
                f"open points, or incorrect phases in upstream equipment that should be corrected in the source data.", ex)

    return has_changes


def _apply_phases(terminal: Terminal, phase_selector: PhaseSelector, phases: Iterable[SinglePhaseKind]):
    phases_status = phase_selector(terminal)
    for nominal_phase, traced_phase in zip(terminal.phases.single_phases, phases):
        phases_status[nominal_phase] = traced_phase if traced_phase not in PhaseCode.XY else SinglePhaseKind.NONE


async def _run_with_traversal_and_phase_selector(start_terminals: Iterable[Terminal],
                                                 traversal: BranchRecursiveTraversal[Terminal],
                                                 phase_selector: PhaseSelector):
    for terminal in start_terminals:
        await _run_terminal(terminal, traversal, phase_selector)


async def _run_terminal(start: Terminal, traversal: BranchRecursiveTraversal[Terminal], phase_selector: PhaseSelector):
    await _run_from_terminal(traversal, start, phase_selector, set(start.phases.single_phases))


async def _run_from_terminal(traversal: BranchRecursiveTraversal[Terminal],
                             terminal: Terminal,
                             phase_selector: PhaseSelector,
                             phases_to_flow: Set[SinglePhaseKind]):
    traversal.reset()
    traversal.tracker.visit(terminal)
    _flow_to_connected_terminals_and_queue(traversal, terminal, phase_selector, phases_to_flow)
    await traversal.trace()


def _set_normal_phases_and_queue_next(terminal: Terminal, traversal: BranchRecursiveTraversal[Terminal]):
    _set_phases_and_queue_next(terminal, traversal, normally_open, normal_phases)


def _set_current_phases_and_queue_next(terminal: Terminal, traversal: BranchRecursiveTraversal[Terminal]):
    _set_phases_and_queue_next(terminal, traversal, currently_open, current_phases)


def _set_phases_and_queue_next(current: Terminal,
                               traversal: BranchRecursiveTraversal[Terminal],
                               open_test: Callable[[ConductingEquipment, SinglePhaseKind], bool],
                               phase_selector: PhaseSelector):
    phases_to_flow = _get_phases_to_flow(current, open_test)

    if current.conducting_equipment:
        for out_terminal in current.conducting_equipment.terminals:
            if out_terminal != current and _flow_through_equipment(traversal, current, out_terminal, phase_selector, phases_to_flow):
                _flow_to_connected_terminals_and_queue(traversal, out_terminal, phase_selector, phases_to_flow)


def _flow_through_equipment(traversal: BranchRecursiveTraversal[Terminal],
                            from_terminal: Terminal,
                            to_terminal: Terminal,
                            phase_selector: PhaseSelector,
                            phases_to_flow: Set[SinglePhaseKind]):
    traversal.tracker.visit(to_terminal)
    return spread_phases(from_terminal, to_terminal, phase_selector, phases_to_flow)


def _flow_to_connected_terminals_and_queue(traversal: BranchRecursiveTraversal[Terminal],
                                           from_terminal: Terminal,
                                           phase_selector: PhaseSelector,
                                           phases_to_flow: Set[SinglePhaseKind]):
    """
    Applies all the `phases_to_flow` from the `from_terminal` to the connected terminals and queues them.
    """

    from_phases = phase_selector(from_terminal)
    connectivity_results = get_connectivity(from_terminal, phases_to_flow)

    conducting_equip = from_terminal.conducting_equipment
    use_branch_queue = len(connectivity_results) > 1 or (conducting_equip and conducting_equip.num_terminals() > 2)

    for cr in connectivity_results:
        to_phases = phase_selector(cr.to_terminal)

        has_changes = False
        for path in cr.nominal_phase_paths:
            try:
                has_changes = to_phases.__setitem__(path.to_phase, from_phases[path.from_phase]) or has_changes
            except PhaseException as ex:
                raise PhaseException(
                    f"Attempted to flow conflicting phase {from_phases[path.from_phase].name} onto {to_phases[path.to_phase].name} on nominal phase path "
                    f"{path.from_phase.name} to {path.to_phase.name}. This occurred while flowing between {from_terminal} on {conducting_equip} and "
                    f"{cr.to_terminal} on {cr.to_equip}. This is caused by missing open points, or incorrect phases in upstream equipment that should be "
                    f"corrected in the source data.", ex)

        if has_changes:
            if use_branch_queue:
                branch = traversal.create_branch()
                branch.start_item = cr.to_terminal
                traversal.branch_queue.put(branch)
            else:
                traversal.process_queue.put(cr.to_terminal)


def _get_phases_to_flow(terminal: Terminal,
                        open_test: Callable[[ConductingEquipment, Optional[SinglePhaseKind]], bool]) -> Set[SinglePhaseKind]:
    equip = terminal.conducting_equipment or set()

    closed_phases = filter(lambda phase: not open_test(equip, phase), terminal.phases.single_phases)
    return set(closed_phases)
