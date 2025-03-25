#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Union, Set, Callable, Iterable

from zepben.evolve.services.network.tracing.connectivity.nominal_phase_path import NominalPhasePath
from zepben.evolve.exceptions import PhaseException, TracingException
from zepben.evolve.model.cim.iec61970.base.core.phase_code import PhaseCode
from zepben.evolve.model.cim.iec61970.base.wires.energy_source import EnergySource
from zepben.evolve.model.cim.iec61970.base.wires.single_phase_kind import SinglePhaseKind
from zepben.evolve.services.network.tracing.connectivity.connectivity_result import ConnectivityResult
from zepben.evolve.services.network.tracing.connectivity.terminal_connectivity_connected import TerminalConnectivityConnected
from zepben.evolve.services.network.tracing.connectivity.terminal_connectivity_internal import TerminalConnectivityInternal
from zepben.evolve.services.network.tracing.networktrace.compute_data import ComputeData
from zepben.evolve.services.network.tracing.networktrace.network_trace import NetworkTrace
from zepben.evolve.services.network.tracing.networktrace.network_trace_action_type import NetworkTraceActionType
from zepben.evolve.services.network.tracing.networktrace.operators.network_state_operators import NetworkStateOperators
from zepben.evolve.services.network.tracing.networktrace.tracing import Tracing
from zepben.evolve.services.network.network_service import connected_terminals, NetworkService
from zepben.evolve.services.network.tracing.traversal.weighted_priority_queue import WeightedPriorityQueue
if TYPE_CHECKING:
    from zepben.evolve import Terminal, ConductingEquipment
    from zepben.evolve.types import PhaseSelector
    from zepben.evolve.services.network.tracing.traversal.traversal import Traversal

__all__ = ["SetPhases"]


class SetPhases:
    """
    Convenience class that provides methods for setting phases on a `NetworkService`.
    This class is backed by a `Traversal`.
    """

    class PhasesToFlow:
        def __init__(self, nominal_phase_paths: list[NominalPhasePath], step_flowed_phases: bool = False):
            self.nominal_phase_paths = nominal_phase_paths
            self.step_flowed_phases = step_flowed_phases


    async def run(self,
                  apply_to: Union[NetworkService, Terminal],
                  phases: Union[PhaseCode, Iterable[SinglePhaseKind]]=None,
                  network_state_operators: NetworkStateOperators=NetworkStateOperators.NORMAL):

        if isinstance(apply_to, NetworkService):
            await self._run(apply_to, network_state_operators)
        elif isinstance(apply_to, Terminal):
            await self._run_with_terminal(apply_to, phases, network_state_operators)

    async def _run(self,
                   network: NetworkService,
                   network_state_operators: NetworkStateOperators=NetworkStateOperators.NORMAL):
        """
        Apply phases from all sources in the network.

        @param network: The network in which to apply phases.
        """
        trace = await self._create_network_trace(network_state_operators)
        async def apply_run_return(term):
            self._apply_phases(network_state_operators, term, term.phases.single_phases)
            await self._run_terminal(term, network_state_operators, trace)


        [await apply_run_return(term) for es in network.objects(EnergySource) for term in es.terminals]

    async def _run_with_terminal(self,
                                 terminal: Terminal,
                                 phases: Union[PhaseCode, Iterable[SinglePhaseKind]],
                                 network_state_operators: NetworkStateOperators=NetworkStateOperators.NORMAL):
        """
        Apply phases from the `terminal`.

        @param terminal: The terminal to start applying phases from.
        @param phases: The phases to apply. Must only contain ABCN.
        """
        if isinstance(phases, PhaseCode):
            phases = phases.single_phases

        if len(phases) != len(terminal.phases.single_phases):
            raise TracingException(
                f"Attempted to apply phases [{', '.join(phase.name for phase in phases)}] to {terminal} with nominal phases {terminal.phases.name}. "
                f"Number of phases to apply must match the number of nominal phases. Found {len(phases)}, expected {len(terminal.phases.single_phases)}"
            )

        self._apply_phases(network_state_operators, terminal, phases)

        await self._run_terminal(terminal, network_state_operators)

    async def _run_spread_phases_and_flow(self,
                                          seed_terminal: Terminal,
                                          start_terminal: Terminal,
                                          phases: Iterable[SinglePhaseKind],
                                          network_state_operators: NetworkStateOperators=NetworkStateOperators.NORMAL):

        nominal_phase_paths = await self._get_nominal_phase_paths(network_state_operators, seed_terminal, start_terminal, list(phases))
        if self._flow_phases(network_state_operators, seed_terminal, start_terminal, nominal_phase_paths):
            await self.run(start_terminal, network_state_operators=network_state_operators)


    def spread_phases(
        self,
        from_terminal: Terminal,
        to_terminal: Terminal,
        phases: Iterable[SinglePhaseKind]=None,
        network_state_operators: NetworkStateOperators=NetworkStateOperators.NORMAL
    ):
        """
        Apply phases from the `from_terminal` to the `to_terminal`.

        :param from_terminal: The terminal to from which to spread phases.
        :param to_terminal: The terminal to spread phases to.
        :param phases: The nominal phases on which to spread phases.
        :param network_state_operators: The `NetworkStateOperators` to be used when setting phases.
        """
        if phases is None:
            self.spread_phases(from_terminal, to_terminal, from_terminal.phases.single_phases, network_state_operators)
        else:
            paths = self._get_nominal_phase_paths(network_state_operators, from_terminal, to_terminal, list(phases))
            self._flow_phases(network_state_operators, from_terminal, to_terminal, paths)

    @staticmethod
    def _apply_phases(state_operators: NetworkStateOperators,
                      terminal: Terminal,
                      phases: Iterable[SinglePhaseKind]):

        traced_phases = state_operators.phase_status(terminal)
        for i, nominal_phase in enumerate(terminal.phases.single_phases):
            traced_phases[nominal_phase] = phases[i] if phases[i] in PhaseCode.XY  else SinglePhaseKind.NONE

    async def _get_nominal_phase_paths(self, state_operators: NetworkStateOperators,
                                       from_terminal: Terminal,
                                       to_terminal: Terminal,
                                       phases: Iterable[SinglePhaseKind]
                                       ) -> tuple[NominalPhasePath]:
        traced_internally = from_terminal.conducting_equipment == to_terminal.conducting_equipment
        phases_to_flow = self._get_phases_to_flow(state_operators, from_terminal, phases, traced_internally)

        return (TerminalConnectivityInternal().between if traced_internally else TerminalConnectivityConnected().terminal_connectivity)(
            from_terminal, to_terminal, phases_to_flow
        ).nominal_phase_paths

    async def _run_terminal(self, terminal: Terminal, network_state_operators: NetworkStateOperators, trace: NetworkTrace[PhasesToFlow]=None):
        if trace is None:
            trace = self._create_network_trace(network_state_operators)
        nominal_phase_paths = map(lambda it: NominalPhasePath(SinglePhaseKind.NONE, it), terminal.phases)
        trace.run(terminal, self.PhasesToFlow(nominal_phase_paths), can_stop_on_start_item=False)
        trace.reset()

    async def _create_network_trace(self, state_operators: NetworkStateOperators) -> NetworkTrace[PhasesToFlow]:
        def step_action(packed_tuple, ctx):
            path, phases_to_flow = packed_tuple
            phases_to_flow.step_flowed_phases = self._flow_phases(state_operators, path.from_terminal, path.to_terminal, phases_to_flow.nominal_phase_paths) \
                                                if not ctx.is_start_item else None

        nwt = Tracing.network_trace_branching(
            network_state_operators=state_operators,
            action_step_type=NetworkTraceActionType.ALL_STEPS(),
            queue_factory=WeightedPriorityQueue.process_queue(lambda it: it.path.to_terminal.phases.num_phases()),  # TODO: lol, explosions expected
            branch_queue_factory=WeightedPriorityQueue.branch_queue(lambda it: it.path.to_terminal.phases.num_phases()),  # TODO: lol, explosions expected
            compute_data=await self._compute_next_phases_to_flow(state_operators)
        )
        def condition(next_step, *args):
            return len(next_step.data.nominal_phase_paths) > 0
        nwt.add_queue_condition(condition)
        #nwt.add_queue_condition(lambda next_step, *args: len(next_step.data.nominal_phase_paths) > 0)

        nwt.add_step_action(step_action)
        return nwt

    async def _compute_next_phases_to_flow(self, state_operators: NetworkStateOperators) -> ComputeData[PhasesToFlow]:
        def inner(step, _, next_path):
            if not step.data.step_flowed_phases:
                return self.PhasesToFlow([])

            return self.PhasesToFlow(
                self._get_nominal_phase_paths(state_operators, next_path.from_terminal, next_path.to_terminal, step.data.nominal_phase_paths.to_phases())
            )
        return inner

    async def _run_from_terminal(
        self,
        traversal: Traversal[Terminal],
        terminal: Terminal,
        phase_selector: PhaseSelector,
        phases_to_flow: Set[SinglePhaseKind]
    ):
        traversal.reset()
        traversal.tracker.visit(terminal)
        self._flow_to_connected_terminals_and_queue(traversal, terminal, phase_selector, phases_to_flow)
        await traversal.run()

    def _set_phases_and_queue_next(
        self,
        current: Terminal,
        traversal: Traversal[Terminal],
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
        traversal: Traversal[Terminal],
        from_terminal: Terminal,
        to_terminal: Terminal,
        phase_selector: PhaseSelector,
        phases_to_flow: Set[SinglePhaseKind]
    ) -> Set[SinglePhaseKind]:
        traversal.tracker.visit(to_terminal)
        return self.spread_phases(from_terminal, to_terminal, phase_selector, phases_to_flow)

    def _flow_to_connected_terminals_and_queue(
        self,
        traversal: Traversal[Terminal],
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

    async def _flow_phases(self,
                           state_operators: NetworkStateOperators,
                           from_terminal: Terminal,
                           to_terminal: Terminal,
                           nominal_phase_paths: Iterable[NominalPhasePath]
    ) -> bool:
        from zepben.evolve import UnsupportedOperationException  # FIXME: This is a hack to avoid a circular import

        from_phases = state_operators.phase_status(from_terminal)
        to_phases = state_operators.phase_status(to_terminal)
        changed_phases = False

        for from_, to in nominal_phase_paths:
            try:
                phase = from_phases[from_] if from_ != SinglePhaseKind.NONE else to if to not in PhaseCode.XY else to_phases[to]
                if phase != SinglePhaseKind.NONE and to_phases.set(to, phase):
                    changed_phases = True
            except UnsupportedOperationException:
                if from_ == to:
                    phase_desc = f'{from_}'
                else:
                    phase_desc = f'path {from_} to {to}'

                def get_ce_details(terminal: Terminal):  # TODO: implement this below
                    if terminal.conducting_equipment:
                        return terminal.conducting_equipment.type_name_and_mrid
                    return ''

                if from_terminal.conducting_equipment == to_terminal.conducting_equipment:  # TODO: the kotlin sdk has ? for conducting_equipment
                                                                                            #       Im sure its needed, but i want to see why
                    terminal_desc = f'from {from_terminal} to {to_terminal} through {from_terminal.conducting_equipment.type_name_and_mrid()}'
                else:
                    terminal_desc = f'between {from_terminal} on {from_terminal.conducting_equipment.type_name_and_mrid()} and {to_terminal} on {to_terminal.conducting_equipment.type_name_and_mrid}'
                    raise Exception(
                        f"Attempted to flow conflicting phase {from_phases[from_]} onto ${to_phases[to]} on nominal phase {phase_desc}. This occurred while " +
                        f"flowing {terminal_desc}. This is caused by missing open points, or incorrect phases in upstream equipment that should be " +
                        "corrected in the source data."
                    )
        return  changed_phases

    @staticmethod
    def _get_phases_to_flow(
        state_operators: NetworkStateOperators,
        terminal: Terminal,
        phases: Sequence[SinglePhaseKind],
        internal_flow: bool
    ) -> Set[SinglePhaseKind]:

            equip = terminal.conducting_equipment
            if equip and internal_flow:
                return {phase for phase in terminal.phases.single_phases if not state_operators.is_open(equip, phase)}
            return set(phases)

    @staticmethod
    def _nominal_phase_path_to_phases(nominal_phase_paths: list[NominalPhasePath]) -> list[SinglePhaseKind]:
        return list(map(nominal_phase_paths, lambda it: it.to))
