#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import logging
from typing import Dict, Callable, List, Set, Awaitable

from zepben.evolve import Terminal, SinglePhaseKind, ConductingEquipment, NetworkService, normal_phases, normal_direction, \
    FeederDirection, X_PRIORITY, Y_PRIORITY, SetPhases, is_before, is_after, current_phases, current_direction
from zepben.evolve.types import PhaseSelector, DirectionSelector

__all__ = ["PhaseInferrer"]

logger = logging.getLogger(__name__)


class PhaseInferrer:
    """
    A class that can infer missing phases on a network that has been processed by `SetPhases`.
    """

    def __init__(self) -> None:
        super().__init__()

        self._tracking: Dict[ConductingEquipment, bool] = {}

    async def run(self, network: NetworkService):
        """
        Infer the missing phases on the specified `network`.

        :param network: The `NetworkService` to infer phases on.
        """
        self._tracking = {}

        await self._infer_missing_phases(network, normal_phases, normal_direction)
        await self._infer_missing_phases(network, current_phases, current_direction)

        for (conducting_equipment, has_suspect_inferred) in self._tracking.items():
            if has_suspect_inferred:
                logger.warning(
                    "*** Action Required *** Inferred missing phases for '%s' [%s] which may not be correct. The phases were inferred due to a disconnected "
                    "nominal phase because of an upstream error in the source data. Phasing information for the upstream equipment should be fixed in the "
                    "source system.",
                    conducting_equipment.name,
                    conducting_equipment.mrid
                )
            else:
                logger.warning(
                    "*** Action Required *** Inferred missing phase for '%s' [%s] which should be correct. The phase was inferred due to a disconnected "
                    "nominal phase because of an upstream error in the source data. Phasing information for the upstream equipment should be fixed in the "
                    "source system.",
                    conducting_equipment.name,
                    conducting_equipment.mrid
                )

    async def _infer_missing_phases(self, network: NetworkService, phase_selector: PhaseSelector, direction_selector: DirectionSelector):
        while True:
            terms_missing_phases = [it for it in network.objects(Terminal) if self._is_connected_to_others(it) and self._has_none_phase(it, phase_selector)]
            terms_missing_xy_phases = [it for it in terms_missing_phases if self._has_xy_phases(it)]

            async def set_missing_to_nominal(terminal: Terminal) -> bool:
                return await self._set_missing_to_nominal(terminal, phase_selector)

            async def infer_xy_phases_1(terminal: Terminal) -> bool:
                return await self._infer_xy_phases(terminal, phase_selector, 1)

            async def infer_xy_phases_4(terminal: Terminal) -> bool:
                return await self._infer_xy_phases(terminal, phase_selector, 4)

            did_nominal = await self._process(terms_missing_phases, phase_selector, direction_selector, set_missing_to_nominal)
            did_xy_1 = await self._process(terms_missing_xy_phases, phase_selector, direction_selector, infer_xy_phases_1)
            did_xy_4 = await self._process(terms_missing_xy_phases, phase_selector, direction_selector, infer_xy_phases_4)

            if not (did_nominal or did_xy_1 or did_xy_4):
                break

    @staticmethod
    def _is_connected_to_others(terminal: Terminal) -> bool:
        return terminal.connectivity_node and (terminal.connectivity_node.num_terminals() > 1)

    @staticmethod
    def _has_none_phase(terminal: Terminal, phase_selector: PhaseSelector) -> bool:
        phases = phase_selector(terminal)
        return any(phases[it] == SinglePhaseKind.NONE for it in terminal.phases.single_phases)

    @staticmethod
    def _has_xy_phases(terminal: Terminal) -> bool:
        return (SinglePhaseKind.X in terminal.phases) or (SinglePhaseKind.Y in terminal.phases)

    def _find_terminal_at_start_of_missing_phases(
        self,
        terminals: List[Terminal],
        phase_selector: PhaseSelector,
        direction_selector: DirectionSelector
    ) -> List[Terminal]:
        candidates = self._missing_from_down_to_up(terminals, phase_selector, direction_selector)
        if not candidates:
            candidates = self._missing_from_down_to_any(terminals, phase_selector, direction_selector)
        if not candidates:
            candidates = self._missing_from_any(terminals, phase_selector)

        return candidates

    def _missing_from_down_to_up(self, terminals: List[Terminal], phase_selector: PhaseSelector, direction_selector: DirectionSelector) -> List[Terminal]:
        return [
            terminal for terminal in terminals
            if (self._has_none_phase(terminal, phase_selector) and
                (FeederDirection.UPSTREAM in direction_selector(terminal).value()) and
                terminal.connectivity_node and
                any(not self._has_none_phase(t, phase_selector) for t in terminal.connectivity_node.terminals if
                    (t != terminal) and (FeederDirection.DOWNSTREAM in direction_selector(t).value())))
        ]

    def _missing_from_down_to_any(self, terminals: List[Terminal], phase_selector: PhaseSelector, direction_selector: DirectionSelector) -> List[Terminal]:
        return [
            terminal for terminal in terminals
            if (self._has_none_phase(terminal, phase_selector) and
                terminal.connectivity_node and
                any(not self._has_none_phase(t, phase_selector) for t in terminal.connectivity_node.terminals if
                    (t != terminal) and (FeederDirection.DOWNSTREAM in direction_selector(t).value())))
        ]

    def _missing_from_any(self, terminals: List[Terminal], phase_selector: PhaseSelector) -> List[Terminal]:
        return [
            terminal for terminal in terminals
            if (self._has_none_phase(terminal, phase_selector) and
                terminal.connectivity_node and
                any(not self._has_none_phase(t, phase_selector) for t in terminal.connectivity_node.terminals if t != terminal))
        ]

    async def _process(
        self,
        terminals: List[Terminal],
        phase_selector: PhaseSelector,
        direction_selector: DirectionSelector,
        processor: Callable[[Terminal], Awaitable[bool]]
    ) -> bool:
        terminals_to_process = self._find_terminal_at_start_of_missing_phases(terminals, phase_selector, direction_selector)

        has_processed = False
        while True:
            continue_processing = False

            for terminal in terminals_to_process:
                continue_processing = await processor(terminal) or continue_processing

            terminals_to_process = self._find_terminal_at_start_of_missing_phases(terminals, phase_selector, direction_selector)

            has_processed = has_processed or continue_processing
            if not continue_processing:
                break

        return has_processed

    async def _set_missing_to_nominal(self, terminal: Terminal, phase_selector: PhaseSelector) -> bool:
        phases = phase_selector(terminal)

        phases_to_process = [it for it in terminal.phases.single_phases if
                             (it != SinglePhaseKind.X) and (it != SinglePhaseKind.Y) and (phases[it] == SinglePhaseKind.NONE)]

        if not phases_to_process:
            return False

        for it in phases_to_process:
            phases[it] = it
        await self._continue_phases(terminal, phase_selector)

        if terminal.conducting_equipment:
            self._tracking[terminal.conducting_equipment] = False

        return True

    async def _infer_xy_phases(self, terminal: Terminal, phase_selector: PhaseSelector, max_missing_phases: int) -> bool:
        none: List[SinglePhaseKind] = []
        used_phases: Set[SinglePhaseKind] = set()

        if not terminal.conducting_equipment:
            return False

        phases = phase_selector(terminal)
        for nominal_phase in terminal.phases:
            phase = phases[nominal_phase]
            if phase == SinglePhaseKind.NONE:
                none.append(nominal_phase)
            else:
                used_phases.add(phase)

        if not none or (len(none) > max_missing_phases):
            return False

        self._tracking[terminal.conducting_equipment] = True

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

        await self._continue_phases(terminal, phase_selector)
        return had_changes

    @staticmethod
    async def _continue_phases(terminal: Terminal, phase_selector: PhaseSelector):
        if terminal.conducting_equipment:
            for other in terminal.conducting_equipment.terminals:
                if other != terminal:
                    set_phases = SetPhases()
                    set_phases.spread_phases(terminal, other, phase_selector=phase_selector)
                    await set_phases.run_with_terminal_and_phase_selector(other, phase_selector)

    @staticmethod
    def _first_unused(phases: List[SinglePhaseKind], used_phases: Set[SinglePhaseKind], validate: Callable[[SinglePhaseKind], bool]) -> SinglePhaseKind:
        for phase in phases:
            if (phase not in used_phases) and validate(phase):
                return phase

        return SinglePhaseKind.NONE
