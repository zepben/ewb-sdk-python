#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from typing import TYPE_CHECKING, Union, Set, Callable, List, Iterable, Optional

from zepben.evolve import connected_terminals
from zepben.evolve.exceptions import PhaseException
from zepben.evolve.exceptions import TracingException
from zepben.evolve.model.cim.iec61970.base.core.phase_code import PhaseCode
from zepben.evolve.model.cim.iec61970.base.wires.energy_source import EnergySource
from zepben.evolve.model.cim.iec61970.base.wires.single_phase_kind import SinglePhaseKind
from zepben.evolve.services.network.tracing.connectivity.connectivity_result import ConnectivityResult
from zepben.evolve.services.network.tracing.connectivity.terminal_connectivity_internal import TerminalConnectivityInternal
from zepben.evolve.services.network.tracing.phases.phase_status import normal_phases, current_phases
from zepben.evolve.services.network.tracing.traversals.branch_recursive_tracing import BranchRecursiveTraversal
from zepben.evolve.services.network.tracing.traversals.queue import PriorityQueue
from zepben.evolve.services.network.tracing.util import normally_open, currently_open
if TYPE_CHECKING:
    from zepben.evolve import Terminal, ConductingEquipment, NetworkService
    from zepben.evolve.types import PhaseSelector

__all__ = ["SetPhases"]


class SetPhases:
    """
    Convenience class that provides methods for setting phases on a `NetworkService`.
    This class is backed by a `BranchRecursiveTraversal`.
    """

    def __init__(self, terminal_connectivity_internal: TerminalConnectivityInternal = TerminalConnectivityInternal()):
        self._terminal_connectivity_internal = terminal_connectivity_internal

        # The `BranchRecursiveTraversal` used when tracing the normal state of the network.
        # NOTE: If you add stop conditions to this traversal it may no longer work correctly, use at your own risk.
        # noinspection PyArgumentList
        self.normal_traversal = BranchRecursiveTraversal(queue_next=self._set_normal_phases_and_queue_next,
                                                         process_queue=PriorityQueue(),
                                                         branch_queue=PriorityQueue())

        # The `BranchRecursiveTraversal` used when tracing the current state of the network.
        # NOTE: If you add stop conditions to this traversal it may no longer work correctly, use at your own risk.
        # noinspection PyArgumentList
        self.current_traversal = BranchRecursiveTraversal(queue_next=self._set_current_phases_and_queue_next,
                                                          process_queue=PriorityQueue(),
                                                          branch_queue=PriorityQueue())

    async def run(self, network: NetworkService):
        """
        Apply phases from all sources in the network.

        @param network: The network in which to apply phases.
        """
        terminals = [term for es in network.objects(EnergySource) for term in es.terminals]

        for term in terminals:
            self._apply_phases(term, normal_phases, term.phases.single_phases)
            self._apply_phases(term, current_phases, term.phases.single_phases)

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

        self._apply_phases(terminal, normal_phases, phases)
        self._apply_phases(terminal, current_phases, phases)

        self.normal_traversal.tracker.clear()
        self.current_traversal.tracker.clear()

        await self._run_with_terminals([terminal])

    def spread_phases(
        self,
        from_terminal: Terminal,
        to_terminal: Terminal,
        phase_selector: PhaseSelector,
        phases_to_flow: Optional[Set[SinglePhaseKind]] = None
    ) -> Set[SinglePhaseKind]:
        """
        Apply phases from the `from_terminal` to the `to_terminal`.

        @param from_terminal: The terminal to from which to spread phases.
        @param to_terminal: The terminal to spread phases to.
        @param phase_selector: The selector to use to spread the phases.
        @param phases_to_flow: The nominal phases on which to spread phases.

        @return: True if any phases were spread, otherwise False.
        """
        cr = self._terminal_connectivity_internal.between(from_terminal, to_terminal, phases_to_flow)
        return self._flow_via_paths(cr, phase_selector)

    async def run_with_terminal_and_phase_selector(self, terminal: Terminal, phase_selector: PhaseSelector):
        """
        Apply phases from the `terminal` on the selected phases. Only spreads existing phases.

        @param terminal: The terminal from which to spread phases.
        @param phase_selector: The selector to use to spread the phases. Must be `normal_phases` or `current_phases`.

        @return: True if any phases were spread, otherwise False.
        """
        if phase_selector is normal_phases:
            await self._run_with_traversal_and_phase_selector([terminal], self.normal_traversal, phase_selector)
        elif phase_selector is current_phases:
            await self._run_with_traversal_and_phase_selector([terminal], self.current_traversal, phase_selector)
        else:
            raise TracingException("Invalid PhaseSelector specified. Must be normal_phases or current_phases")

    async def _run_with_terminals(self, start_terminals: Iterable[Terminal]):
        await self._run_with_traversal_and_phase_selector(start_terminals, self.normal_traversal, normal_phases)
        await self._run_with_traversal_and_phase_selector(start_terminals, self.current_traversal, current_phases)

    @staticmethod
    def _apply_phases(terminal: Terminal, phase_selector: PhaseSelector, phases: Iterable[SinglePhaseKind]):
        phases_status = phase_selector(terminal)
        for nominal_phase, traced_phase in zip(terminal.phases.single_phases, phases):
            phases_status[nominal_phase] = traced_phase if traced_phase not in PhaseCode.XY else SinglePhaseKind.NONE

    async def _run_with_traversal_and_phase_selector(
        self,
        start_terminals: Iterable[Terminal],
        traversal: BranchRecursiveTraversal[Terminal],
        phase_selector: PhaseSelector
    ):
        for terminal in start_terminals:
            await self._run_terminal(terminal, traversal, phase_selector)

    async def _run_terminal(self, start: Terminal, traversal: BranchRecursiveTraversal[Terminal], phase_selector: PhaseSelector):
        await self._run_from_terminal(traversal, start, phase_selector, set(start.phases.single_phases))

    async def _run_from_terminal(
        self,
        traversal: BranchRecursiveTraversal[Terminal],
        terminal: Terminal,
        phase_selector: PhaseSelector,
        phases_to_flow: Set[SinglePhaseKind]
    ):
        traversal.reset()
        traversal.tracker.visit(terminal)
        self._flow_to_connected_terminals_and_queue(traversal, terminal, phase_selector, phases_to_flow)
        await traversal.run()

    def _set_normal_phases_and_queue_next(self, terminal: Terminal, traversal: BranchRecursiveTraversal[Terminal]):
        self._set_phases_and_queue_next(terminal, traversal, normally_open, normal_phases)

    def _set_current_phases_and_queue_next(self, terminal: Terminal, traversal: BranchRecursiveTraversal[Terminal]):
        self._set_phases_and_queue_next(terminal, traversal, currently_open, current_phases)

    def _set_phases_and_queue_next(
        self,
        current: Terminal,
        traversal: BranchRecursiveTraversal[Terminal],
        open_test: Callable[[ConductingEquipment, SinglePhaseKind], bool],
        phase_selector: PhaseSelector
    ):
        phases_to_flow = self._get_phases_to_flow(current, open_test)

        if current.conducting_equipment:
            for out_terminal in current.conducting_equipment.terminals:
                if out_terminal != current:
                    phases_flowed = self._flow_through_equipment(traversal, current, out_terminal, phase_selector, phases_to_flow)
                    if phases_flowed:
                        self._flow_to_connected_terminals_and_queue(traversal, out_terminal, phase_selector, phases_flowed)

    def _flow_through_equipment(
        self,
        traversal: BranchRecursiveTraversal[Terminal],
        from_terminal: Terminal,
        to_terminal: Terminal,
        phase_selector: PhaseSelector,
        phases_to_flow: Set[SinglePhaseKind]
    ) -> Set[SinglePhaseKind]:
        traversal.tracker.visit(to_terminal)
        return self.spread_phases(from_terminal, to_terminal, phase_selector, phases_to_flow)

    def _flow_to_connected_terminals_and_queue(
        self,
        traversal: BranchRecursiveTraversal[Terminal],
        from_terminal: Terminal,
        phase_selector: PhaseSelector,
        phases_to_flow: Set[SinglePhaseKind]
    ):
        """
        Applies all the `phases_to_flow` from the `from_terminal` to the connected terminals and queues them.
        """
        connectivity_results = connected_terminals(from_terminal, phases_to_flow)

        conducting_equip = from_terminal.conducting_equipment
        use_branch_queue = len(connectivity_results) > 1 or (conducting_equip and conducting_equip.num_terminals() > 2)

        for cr in connectivity_results:
            if self._flow_via_paths(cr, phase_selector):
                if use_branch_queue:
                    branch = traversal.create_branch()
                    branch.start_item = cr.to_terminal
                    traversal.branch_queue.put(branch)
                else:
                    traversal.process_queue.put(cr.to_terminal)

    @staticmethod
    def _flow_via_paths(cr: ConnectivityResult, phase_selector: PhaseSelector) -> Set[SinglePhaseKind]:
        from_phases = phase_selector(cr.from_terminal)
        to_phases = phase_selector(cr.to_terminal)

        changed_phases = set()
        for path in cr.nominal_phase_paths:
            try:
                # If the path comes from NONE, then we want to apply the `to phase`.
                phase = from_phases[path.from_phase] if path.from_phase != SinglePhaseKind.NONE else \
                    path.to_phase if path.to_phase not in PhaseCode.XY else to_phases[path.to_phase]

                if (phase != SinglePhaseKind.NONE) and to_phases.__setitem__(path.to_phase, phase):
                    changed_phases.add(path.to_phase)
            except PhaseException as ex:
                phase_desc = path.from_phase.name if path.from_phase == path.to_phase else f"path {path.from_phase.name} to {path.to_phase.name}"

                terminal_desc = f"from {cr.from_terminal} to {cr.to_terminal} through {cr.from_equip}" if cr.from_equip == cr.to_equip else \
                    f"between {cr.from_terminal} on {cr.from_equip} and {cr.to_terminal} on {cr.to_equip}"

                raise PhaseException(
                    f"Attempted to flow conflicting phase {from_phases[path.from_phase].name} onto {to_phases[path.to_phase].name} on nominal phase " +
                    f"{phase_desc}. This occurred while flowing {terminal_desc}. This is caused by missing open points, or incorrect phases in upstream " +
                    "equipment that should be corrected in the source data."
                ) from ex

        return changed_phases

    @staticmethod
    def _get_phases_to_flow(
        terminal: Terminal,
        open_test: Callable[[ConductingEquipment, Optional[SinglePhaseKind]], bool]
    ) -> Set[SinglePhaseKind]:
        equip = terminal.conducting_equipment
        if not equip:
            return set()

        return {phase for phase in terminal.phases.single_phases if not open_test(equip, phase)}
