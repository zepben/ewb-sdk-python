#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from collections.abc import Sequence
from typing import Union, Set, Iterable, List

from zepben.evolve.exceptions import TracingException, PhaseException
from zepben.evolve.model.cim.iec61970.base.core.phase_code import PhaseCode
from zepben.evolve.model.cim.iec61970.base.core.terminal import Terminal
from zepben.evolve.model.cim.iec61970.base.wires.energy_source import EnergySource
from zepben.evolve.model.cim.iec61970.base.wires.single_phase_kind import SinglePhaseKind
from zepben.evolve.services.network.network_service import NetworkService
from zepben.evolve.services.network.tracing.connectivity.nominal_phase_path import NominalPhasePath
from zepben.evolve.services.network.tracing.connectivity.terminal_connectivity_connected import TerminalConnectivityConnected
from zepben.evolve.services.network.tracing.connectivity.terminal_connectivity_internal import TerminalConnectivityInternal
from zepben.evolve.services.network.tracing.networktrace.compute_data import ComputeData
from zepben.evolve.services.network.tracing.networktrace.network_trace import NetworkTrace
from zepben.evolve.services.network.tracing.networktrace.network_trace_action_type import NetworkTraceActionType
from zepben.evolve.services.network.tracing.networktrace.operators.network_state_operators import NetworkStateOperators
from zepben.evolve.services.network.tracing.networktrace.tracing import Tracing
from zepben.evolve.services.network.tracing.traversal.traversal import Traversal
from zepben.evolve.services.network.tracing.traversal.weighted_priority_queue import WeightedPriorityQueue

__all__ = ["SetPhases"]


class SetPhases:
    """
    Convenience class that provides methods for setting phases on a `NetworkService`.
    This class is backed by a `NetworkTrace`.
    """

    class PhasesToFlow:
        def __init__(self, nominal_phase_paths: Iterable[NominalPhasePath], step_flowed_phases: bool = False):
            self.nominal_phase_paths = nominal_phase_paths
            self.step_flowed_phases = step_flowed_phases


    async def run(self,
                  apply_to: Union[NetworkService, Terminal],
                  phases: Union[PhaseCode, Iterable[SinglePhaseKind]]=None,
                  network_state_operators: NetworkStateOperators=NetworkStateOperators.NORMAL):

        if isinstance(apply_to, NetworkService):
            return await self._run(apply_to, network_state_operators)

        elif isinstance(apply_to, Terminal):
            if phases is None:
                return await self._run_terminal(apply_to, network_state_operators)

            return await self._run_with_phases(apply_to, phases, network_state_operators)

        else:
            raise Exception('INTERNAL ERROR: incorrect params')

    async def _run(self,
                   network: NetworkService,
                   network_state_operators: NetworkStateOperators=NetworkStateOperators.NORMAL):
        """
        Apply phases from all sources in the network.

        @param network: The network in which to apply phases.
        """
        trace = await self._create_network_trace(network_state_operators)
        for energy_source in network.objects(EnergySource):
            for terminal in energy_source.terminals:
                self._apply_phases(network_state_operators, terminal, terminal.phases.single_phases)
                await self._run_terminal(terminal, network_state_operators, trace)

    async def _run_with_phases(self,
                                 terminal: Terminal,
                                 phases: Union[PhaseCode, Iterable[SinglePhaseKind]],
                                 network_state_operators: NetworkStateOperators=NetworkStateOperators.NORMAL):
        """
        Apply phases from the `terminal`.

        @param terminal: The terminal to start applying phases from.
        @param phases: The phases to apply. Must only contain ABCN.
        """
        def validate_phases(_phases):
            if len(_phases) != len(terminal.phases.single_phases):
                raise TracingException(
                    f"Attempted to apply phases [{', '.join(phase.name for phase in phases)}] to {terminal} with nominal phases {terminal.phases.name}. "
                    f"Number of phases to apply must match the number of nominal phases. Found {len(_phases)}, expected {len(terminal.phases.single_phases)}"
                )
            return _phases

        if isinstance(phases, PhaseCode):
            self._apply_phases(network_state_operators, terminal, validate_phases(phases.single_phases))

        elif isinstance(phases, (list, set)):
            self._apply_phases(network_state_operators, terminal, validate_phases(phases))

        else:
            raise Exception(f'INTERNAL ERROR: Phase of type {phases.__class__} is wrong.')

        await self._run_terminal(terminal, network_state_operators)

    async def _run_spread_phases_and_flow(self,
                                          seed_terminal: Terminal,
                                          start_terminal: Terminal,
                                          phases: List[SinglePhaseKind],
                                          network_state_operators: NetworkStateOperators=NetworkStateOperators.NORMAL):

        nominal_phase_paths = self._get_nominal_phase_paths(network_state_operators, seed_terminal, start_terminal, list(phases))
        if self._flow_phases(network_state_operators, seed_terminal, start_terminal, nominal_phase_paths):
            await self.run(start_terminal, network_state_operators=network_state_operators)


    async def spread_phases(
        self,
        from_terminal: Terminal,
        to_terminal: Terminal,
        phases: List[SinglePhaseKind]=None,
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
            return await self.spread_phases(from_terminal, to_terminal, from_terminal.phases.single_phases, network_state_operators)
        else:
            paths = self._get_nominal_phase_paths(network_state_operators, from_terminal, to_terminal, list(phases))
            if await self._flow_phases(network_state_operators, from_terminal, to_terminal, paths):
                await self.run(from_terminal, network_state_operators=network_state_operators)

    async def _run_terminal(self, terminal: Terminal, network_state_operators: NetworkStateOperators, trace: NetworkTrace[PhasesToFlow]=None):
        if trace is None:
            trace = await self._create_network_trace(network_state_operators)
        nominal_phase_paths = list(map(lambda it: NominalPhasePath(SinglePhaseKind.NONE, it), terminal.phases))
        await trace.run(terminal, self.PhasesToFlow(nominal_phase_paths), can_stop_on_start_item=False)
        trace.reset()

    async def _create_network_trace(self, state_operators: NetworkStateOperators) -> NetworkTrace[PhasesToFlow]:
        async def step_action(nts, ctx):
            path = nts.path
            phases_to_flow = nts.data
            #  We always assume the first step terminal already has the phases applied, so we don't do anything on the first step
            phases_to_flow.step_flowed_phases = True if ctx.is_start_item else (
                await self._flow_phases(state_operators, path.from_terminal, path.to_terminal, phases_to_flow.nominal_phase_paths)
            )

        def condition(next_step, nctx, step, ctx):
            return len(next_step.data.nominal_phase_paths) > 0

        def _get_weight(it) -> int:
            return it.path.to_terminal.phases.num_phases

        return (
            Tracing.network_trace_branching(
                network_state_operators=state_operators,
                action_step_type=NetworkTraceActionType.ALL_STEPS,
                queue_factory=lambda: WeightedPriorityQueue.process_queue(_get_weight),
                compute_data=self._compute_next_phases_to_flow(state_operators)
            )
            .add_queue_condition(condition)
            .add_step_action(step_action)
        )

    def _compute_next_phases_to_flow(self, state_operators: NetworkStateOperators) -> ComputeData[PhasesToFlow]:
        def inner(step, _, next_path):
            if not step.data.step_flowed_phases:
                return self.PhasesToFlow([])

            return self.PhasesToFlow(
                self._get_nominal_phase_paths(state_operators, next_path.from_terminal, next_path.to_terminal, self._nominal_phase_path_to_phases(step.data.nominal_phase_paths))
            )
        return ComputeData(inner)

    @staticmethod
    def _apply_phases(state_operators: NetworkStateOperators,
                      terminal: Terminal,
                      phases: List[SinglePhaseKind]):

        traced_phases = state_operators.phase_status(terminal)
        for i, nominal_phase in enumerate(terminal.phases.single_phases):
            traced_phases[nominal_phase] = phases[i] if phases[i] not in PhaseCode.XY else SinglePhaseKind.NONE

    def _get_nominal_phase_paths(self, state_operators: NetworkStateOperators,
                                       from_terminal: Terminal,
                                       to_terminal: Terminal,
                                       phases: Sequence[SinglePhaseKind]
                                       ) -> tuple[NominalPhasePath]:
        traced_internally = from_terminal.conducting_equipment == to_terminal.conducting_equipment
        phases_to_flow = self._get_phases_to_flow(state_operators, from_terminal, phases, traced_internally)

        if traced_internally:
            return TerminalConnectivityInternal().between(from_terminal, to_terminal, phases_to_flow).nominal_phase_paths
        else:
            return TerminalConnectivityConnected().terminal_connectivity(from_terminal, to_terminal, phases_to_flow).nominal_phase_paths

    @staticmethod
    async def _flow_phases(state_operators: NetworkStateOperators,
                           from_terminal: Terminal,
                           to_terminal: Terminal,
                           nominal_phase_paths: Iterable[NominalPhasePath]
                           ) -> bool:

        from_phases = state_operators.phase_status(from_terminal)
        to_phases = state_operators.phase_status(to_terminal)
        changed_phases = False

        for nominal_phase_path in nominal_phase_paths:
            (from_, to) = (nominal_phase_path.from_phase, nominal_phase_path.to_phase)

            try:
                def _phase_to_apply():
                    # If the path comes from NONE, then we want to apply the `to phase`
                    if from_ != SinglePhaseKind.NONE:
                        return from_phases[from_]
                    elif to not in PhaseCode.XY:
                        return to
                    else:
                        return to_phases[to]

                phase = _phase_to_apply()

                if phase != SinglePhaseKind.NONE:
                    to_phases[to] = phase
                    changed_phases = True

            except PhaseException:
                phase_desc = f'{from_.name}' if from_ == to else f'path {from_.name} to {to.name}'

                def get_ce_details(terminal: Terminal):
                    if terminal.conducting_equipment:
                        return terminal.conducting_equipment
                    return ''

                if from_terminal.conducting_equipment and from_terminal.conducting_equipment == to_terminal.conducting_equipment:
                    terminal_desc = f'from {from_terminal} to {to_terminal} through {from_terminal.conducting_equipment}'
                else:
                    terminal_desc = f'between {from_terminal} on {get_ce_details(from_terminal)} and {to_terminal} on {get_ce_details(to_terminal)}'

                raise PhaseException(
                    f"Attempted to flow conflicting phase {from_phases[from_].name} onto {to_phases[to].name} on nominal phase {phase_desc}. This occurred while " +
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
        return list(map((lambda it: it.to_phase), nominal_phase_paths))
