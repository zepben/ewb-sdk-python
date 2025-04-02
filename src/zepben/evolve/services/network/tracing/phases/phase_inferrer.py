#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import logging
from dataclasses import dataclass
from typing import Dict, Callable, List, Set, Awaitable

from zepben.evolve import Terminal, SinglePhaseKind, ConductingEquipment, NetworkService, \
    FeederDirection, X_PRIORITY, Y_PRIORITY, is_before, is_after
from zepben.evolve.services.network.tracing.networktrace.tracing import Tracing
from zepben.evolve.services.network.tracing.networktrace.operators.network_state_operators import NetworkStateOperators

__all__ = ["PhaseInferrer"]

logger = logging.getLogger(__name__)


class PhaseInferrer:
    """
    A class that can infer missing phases on a network that has been processed by `SetPhases`.
    """

    @dataclass
    class InferredPhase:
        conducting_equipment: ConductingEquipment
        suspect: bool

        def description(self):
            if self.suspect:
                return (f"Inferred missing phases for '{self.conducting_equipment.name}' [{self.conducting_equipment.mrid}] which may not be correct. The "
                        "phases were inferred due to a disconnected nominal phase because of an upstream error in the source data. Phasing information for the "
                        "upstream equipment should be fixed in the source system.")
            else:
                return (f"Inferred missing phase for '{self.conducting_equipment.name}' [{self.conducting_equipment.mrid}] which should be correct. The phase "
                        f"was inferred due to a disconnected nominal phase because of an upstream error in the source data. Phasing information for the "
                        f"upstream equipment should be fixed in the source system.")

    async def run(self, network: NetworkService, network_state_operators: NetworkStateOperators = NetworkStateOperators.NORMAL):
        """
        Infer the missing phases on the specified `network`.

        :param network: The `NetworkService` to infer phases on.
        """
        tracking: Dict[ConductingEquipment, bool] = {}

        await self.PhaseInferrerInternal(network_state_operators).infer_missing_phases(network, tracking)

        return map(lambda it: {it.key, it.value}, tracking)


    class PhaseInferrerInternal:
        def __init__(self, state_operators: NetworkStateOperators):
            self.state_operators = state_operators

        async def infer_missing_phases(self, network: NetworkService, tracking: Dict[ConductingEquipment, bool]):
            while True:
                terms_missing_phases = [it for it in network.objects(Terminal) if self._is_connected_to_others(it) and self._has_none_phase(it)]
                terms_missing_xy_phases = [it for it in terms_missing_phases if self._has_xy_phases(it)]

                async def set_missing_to_nominal(terminal: Terminal) -> bool:
                    return await self._set_missing_to_nominal(terminal, tracking)

                async def infer_xy_phases_1(terminal: Terminal) -> bool:
                    return await self._infer_xy_phases(terminal, tracking, 1)

                async def infer_xy_phases_4(terminal: Terminal) -> bool:
                    return await self._infer_xy_phases(terminal, tracking, 4)

                did_nominal = await self._process(terms_missing_phases, set_missing_to_nominal)
                did_xy_1 = await self._process(terms_missing_xy_phases, infer_xy_phases_1)
                did_xy_4 = await self._process(terms_missing_xy_phases, infer_xy_phases_4)

                if not (did_nominal or did_xy_1 or did_xy_4):
                    break

        @staticmethod
        def _is_connected_to_others(terminal: Terminal) -> bool:
            return terminal.connectivity_node and (terminal.connectivity_node.num_terminals() > 1)

        def _has_none_phase(self, terminal: Terminal) -> bool:
            phases = self.state_operators.phase_status(terminal)
            return any(phases[it] == SinglePhaseKind.NONE for it in terminal.phases.single_phases)

        @staticmethod
        def _has_xy_phases(terminal: Terminal) -> bool:
            return (SinglePhaseKind.X in terminal.phases) or (SinglePhaseKind.Y in terminal.phases)

        def _find_terminal_at_start_of_missing_phases(
            self,
            terminals: List[Terminal],
        ) -> List[Terminal]:
            candidates = self._missing_from_down_to_up(terminals)
            if not candidates:
                candidates = self._missing_from_down_to_any(terminals)
            if not candidates:
                candidates = self._missing_from_any(terminals)

            return candidates

        def _missing_from_down_to_up(self, terminals: List[Terminal]) -> List[Terminal]:
            return [
                terminal for terminal in terminals
                if (self._has_none_phase(terminal) and
                    (FeederDirection.UPSTREAM in self.state_operators.get_direction(terminal).value()) and
                    terminal.connectivity_node and
                    any(not self._has_none_phase(t) for t in terminal.connectivity_node.terminals if
                        (t != terminal) and (FeederDirection.DOWNSTREAM in self.state_operators.get_direction(t).value())))
            ]

        def _missing_from_down_to_any(self, terminals: List[Terminal]) -> List[Terminal]:
            return [
                terminal for terminal in terminals
                if (self._has_none_phase(terminal) and
                    terminal.connectivity_node and
                    any(not self._has_none_phase(t) for t in terminal.connectivity_node.terminals if
                        (t != terminal) and (FeederDirection.DOWNSTREAM in self.state_operators.get_direction(t).value())))
            ]

        def _missing_from_any(self, terminals: List[Terminal]) -> List[Terminal]:
            return [
                terminal for terminal in terminals
                if (self._has_none_phase(terminal) and
                    terminal.connectivity_node and
                    any(not self._has_none_phase(t) for t in terminal.connectivity_node.terminals if t != terminal))
            ]

        async def _process(
            self,
            terminals: List[Terminal],
            processor: Callable[[Terminal], Awaitable[bool]]
        ) -> bool:
            terminals_to_process = self._find_terminal_at_start_of_missing_phases(terminals)

            has_processed = False
            while True:
                continue_processing = False

                for terminal in terminals_to_process:
                    continue_processing = await processor(terminal) or continue_processing

                terminals_to_process = self._find_terminal_at_start_of_missing_phases(terminals)

                has_processed = has_processed or continue_processing
                if not continue_processing:
                    break

            return has_processed

        async def _set_missing_to_nominal(self, terminal: Terminal, tracking: Dict[ConductingEquipment, bool]) -> bool:
            phases = self.state_operators.phase_status(terminal)

            phases_to_process = [it for it in terminal.phases.single_phases if
                                 (it != SinglePhaseKind.X) and (it != SinglePhaseKind.Y) and (phases[it] == SinglePhaseKind.NONE)]

            if not phases_to_process:
                return False

            for it in phases_to_process:
                phases[it] = it
            await self._continue_phases(terminal)

            if terminal.conducting_equipment:
                tracking[terminal.conducting_equipment] = False

            return True

        async def _infer_xy_phases(self, terminal: Terminal, max_missing_phases: int, tracking: Dict[ConductingEquipment, bool]) -> bool:
            none: List[SinglePhaseKind] = []
            used_phases: Set[SinglePhaseKind] = set()

            if not terminal.conducting_equipment:
                return False

            phases = self.state_operators.phase_status(terminal)
            for nominal_phase in terminal.phases:
                phase = phases[nominal_phase]
                if phase == SinglePhaseKind.NONE:
                    none.append(nominal_phase)
                else:
                    used_phases.add(phase)

            if not none or (len(none) > max_missing_phases):
                return False

            tracking[terminal.conducting_equipment] = True

            had_changes = False
            for nominal_phase in none:
                if nominal_phase == SinglePhaseKind.X:
                    new_phase = self._first_unused(X_PRIORITY, used_phases, lambda it: is_before(it, phases[SinglePhaseKind.Y]))
                else:
                    new_phase = self._first_unused(Y_PRIORITY, used_phases, lambda it: is_after(it, phases[SinglePhaseKind.X]))

                if new_phase != SinglePhaseKind.NONE:
                    phases[nominal_phase] = new_phase
                    used_phases.add(phases[nominal_phase])
                    had_changes = True

            await self._continue_phases(terminal)
            return had_changes


        async def _continue_phases(self, terminal: Terminal):
            set_phases_trace = Tracing.set_phases()
            [set_phases_trace.run(terminal, other, terminal.phases.single_phases, network_state_operators=self.state_operators)  for other in terminal.other_terminals()]

        @staticmethod
        def _first_unused(phases: List[SinglePhaseKind], used_phases: Set[SinglePhaseKind], validate: Callable[[SinglePhaseKind], bool]) -> SinglePhaseKind:
            for phase in phases:
                if (phase not in used_phases) and validate(phase):
                    return phase

            return SinglePhaseKind.NONE

