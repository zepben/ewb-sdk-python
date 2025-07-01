#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from typing import Set, Union, Type, TYPE_CHECKING

from zepben.evolve import NetworkService
from zepben.evolve.model.cim.iec61970.base.core.phase_code import PhaseCode
from zepben.evolve.model.cim.iec61970.base.core.terminal import Terminal
from zepben.evolve.model.cim.iec61970.base.wires.single_phase_kind import SinglePhaseKind
from zepben.evolve.services.network.tracing.networktrace.conditions.conditions import stop_at_open
from zepben.evolve.services.network.tracing.networktrace.network_trace import NetworkTrace
from zepben.evolve.services.network.tracing.networktrace.network_trace_action_type import NetworkTraceActionType
from zepben.evolve.services.network.tracing.networktrace.network_trace_step import NetworkTraceStep
from zepben.evolve.services.network.tracing.networktrace.operators.network_state_operators import NetworkStateOperators
from zepben.evolve.services.network.tracing.networktrace.tracing import Tracing
from zepben.evolve.services.network.tracing.traversal.weighted_priority_queue import WeightedPriorityQueue

if TYPE_CHECKING:
    from logging import Logger
    from zepben.evolve.services.network.tracing.traversal.step_context import StepContext


class EbbPhases:
    def __init__(self, phases_to_ebb: Set[SinglePhaseKind]):
        self.phases_to_ebb = phases_to_ebb
        self.ebbed_phases: Set[SinglePhaseKind] = set()


class RemovePhases(object):
    """
    Convenience class that provides methods for removing phases on a `NetworkService`
    This class is backed by a `BranchRecursiveTraversal`.
    """

    def __init__(self, debug_logger: Logger = None):
        self._debug_logger = debug_logger

    async def run(
        self,
        start: Union[NetworkService, Terminal],
        nominal_phases_to_ebb: Union[PhaseCode, SinglePhaseKind] = None,
        network_state_operators: Type[NetworkStateOperators] = NetworkStateOperators.NORMAL
    ):
        """
        If nominal_phases_to_ebb is `None` this will remove all phases for all equipment connected
        to `start`
        If `start` is a:
         - `NetworkService` - Remove traced phases from the specified network.
         - `Terminal` - Allows the removal of phases from a terminal and the connected equipment chain
         
        :param start: NetworkService or Terminal to start phase removal 
        :param nominal_phases_to_ebb: The nominal phases to remove traced phasing from. Defaults to all phases.
        :param network_state_operators: The `NetworkStateOperators` to be used when removing phases.
        """

        if nominal_phases_to_ebb is None:

            if isinstance(start, NetworkService):
                return await self._run_with_network(start, network_state_operators)

            if isinstance(start, Terminal):
                return await self._run_with_terminal(start, network_state_operators)

        return await self._run_with_phases_to_ebb(start, nominal_phases_to_ebb, network_state_operators)

    @staticmethod
    async def _run_with_network(network_service: NetworkService, network_state_operators: Type[NetworkStateOperators] = NetworkStateOperators.NORMAL) -> None:
        """
        Remove all traced phases from the specified network.

        :param network_service: The network service to remove traced phasing from.
        :param network_state_operators: The `NetworkStateOperators` to be used when removing phases.
        """

        for t in network_service.objects(Terminal):
            t.traced_phases.phase_status = 0

    async def _run_with_terminal(self, terminal: Terminal, network_state_operators: Type[NetworkStateOperators] = NetworkStateOperators.NORMAL):
        """
        Allows the removal of traced phases from a terminal and the connected equipment chain
        
        :param terminal: Removes all nominal phases a terminal traced phases and the connected equipment chain
        :param network_state_operators: The `NetworkStateOperators` to be used when removing phases.
        """

        return await self._run_with_phases_to_ebb(terminal, terminal.phases, network_state_operators)

    async def _run_with_phases_to_ebb(
        self,
        terminal: Terminal,
        nominal_phases_to_ebb: Union[PhaseCode, Set[SinglePhaseKind]],
        network_state_operators: Type[NetworkStateOperators] = NetworkStateOperators.NORMAL):
        """
        Allows the removal of traced phases from a terminal and the connected equipment chain

        :param terminal: Terminal to start phase removal
        :param nominal_phases_to_ebb: The nominal phases to remove traced phasing from. Defaults to all phases.
        :param network_state_operators: The `NetworkStateOperators` to be used when removing phases.
        """

        if isinstance(nominal_phases_to_ebb, PhaseCode):
            return await self._run_with_phases_to_ebb(terminal, set(nominal_phases_to_ebb.single_phases), network_state_operators)

        trace = await self._create_trace(network_state_operators)
        return await trace.run(terminal, EbbPhases(nominal_phases_to_ebb), terminal.phases)

    async def _create_trace(self, state_operators: Type[NetworkStateOperators]) -> NetworkTrace[EbbPhases]:

        def compute_data(step: NetworkTraceStep[EbbPhases], context: StepContext, next_path: NetworkTraceStep.Path):
            data = []
            for to_phase in [phase.to_phase for phase in next_path.nominal_phase_paths]:
                if to_phase in step.data.phases_to_ebb:
                    data.append(to_phase)
            return EbbPhases(set(data))

        async def step_action(nts: NetworkTraceStep, ctx: StepContext):
            nts.data.ebbed_phases = await self._ebb(state_operators, nts.path.to_terminal, nts.data.phases_to_ebb)

        def queue_condition(next_step: NetworkTraceStep, next_ctx: StepContext = None, step: NetworkTraceStep = None, ctx: StepContext = None):
            return len(next_step.data.phases_to_ebb) > 0 and (step is None or len(step.data.ebbed_phases) > 0)

        return Tracing.network_trace(
            network_state_operators=state_operators,
            action_step_type=NetworkTraceActionType.ALL_STEPS,
            debug_logger=self._debug_logger,
            name=f'RemovePhases({state_operators.description})',
            queue=WeightedPriorityQueue.process_queue(lambda it: len(it.data.phases_to_ebb)),
            compute_data=compute_data
        ).add_condition(stop_at_open()) \
            .add_step_action(step_action) \
            .add_queue_condition(queue_condition)

    @staticmethod
    async def _ebb(state_operators: Type[NetworkStateOperators], terminal: Terminal, phases_to_ebb: Set[SinglePhaseKind]) -> Set[SinglePhaseKind]:
        phases = state_operators.phase_status(terminal)
        for phase in phases_to_ebb:
            if phases[phase] != SinglePhaseKind.NONE:
                phases[phase] = SinglePhaseKind.NONE
        return set(phases_to_ebb)
