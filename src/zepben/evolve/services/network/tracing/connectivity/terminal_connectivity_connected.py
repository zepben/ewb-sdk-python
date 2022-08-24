#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import List, Iterable, Optional, Set, Dict, Callable

from zepben.evolve import Terminal, PhaseCode, SinglePhaseKind, NominalPhasePath, Queue, LifoQueue, Switch
from zepben.evolve.services.network.tracing.connectivity.connectivity_result import ConnectivityResult
from zepben.evolve.services.network.tracing.connectivity.xy_candidate_phase_paths import XyCandidatePhasePaths
from zepben.evolve.services.network.tracing.connectivity.xy_phase_step import XyPhaseStep
from zepben.evolve.services.network.tracing.connectivity.phase_paths import viable_inferred_phase_connectivity, straight_phase_connectivity

__all__ = ["TerminalConnectivityConnected"]


class TerminalConnectivityConnected:
    """
    A class that can be used to find the phase connectivity between terminals.
    """

    _create_candidate_phases: Callable[[], XyCandidatePhasePaths]

    def __init__(self, create_candidate_phases: Callable[[], XyCandidatePhasePaths] = XyCandidatePhasePaths):
        self._create_candidate_phases = create_candidate_phases

    def connected_terminals(
        self,
        terminal: Terminal,
        phases: Optional[Iterable[SinglePhaseKind]] = None
    ) -> List[ConnectivityResult]:
        """
        Find the terminals that are connected to `terminal`, and the phase paths between them.

        :param terminal: The `Terminal` to find connectivity for.
        :param phases: An `Iterable` of `SinglePhaseKind` to limit the included phase paths to check. Defaults to None (all phases).
        :return: A `List` of `ConnectivityResult` defining the connected terminals, or an empty list if there are no connected terminals.
        """
        phases = set(phases or terminal.phases.single_phases)
        include_phases = phases.intersection(terminal.phases.single_phases)
        connectivity_node = terminal.connectivity_node
        if connectivity_node is None:
            return []

        results = []
        for connected_terminal in connectivity_node.terminals:
            if connected_terminal != terminal:
                cr = self._terminal_connectivity(terminal, connected_terminal, include_phases)
                if cr.nominal_phase_paths:
                    results.append(cr)

        return results

    def _terminal_connectivity(
        self,
        terminal: Terminal,
        connected_terminal: Terminal,
        include_phases: Set[SinglePhaseKind]
    ) -> ConnectivityResult:
        return ConnectivityResult(
            from_terminal=terminal,
            to_terminal=connected_terminal,
            nominal_phase_paths=[
                path for path in (
                    self._find_straight_phase_paths(terminal, connected_terminal)
                    or self._find_xy_phase_paths(terminal, connected_terminal)
                ) if (path.from_phase in include_phases) and (path.to_phase in connected_terminal.phases)
            ]
        )

    @staticmethod
    def _find_straight_phase_paths(terminal: Terminal, connected_terminal: Terminal) -> Optional[List[NominalPhasePath]]:
        paths = straight_phase_connectivity.get(terminal.phases, None)

        return paths and paths.get(connected_terminal.phases)

    def _find_xy_phase_paths(self, terminal: Terminal, connected_terminal: Terminal) -> List[NominalPhasePath]:
        xy_phases = _find_xy_phases(terminal)

        nominal_phase_paths = []
        if SinglePhaseKind.N in terminal.phases and SinglePhaseKind.N in connected_terminal.phases:
            # noinspection PyArgumentList
            nominal_phase_paths.append(NominalPhasePath(SinglePhaseKind.N, SinglePhaseKind.N))

        def add_from_to(from_phase, to_phase):
            # noinspection PyArgumentList
            nominal_phase_paths.append(NominalPhasePath(from_phase, to_phase))

        def add_to_from(from_phase, to_phase):
            # noinspection PyArgumentList
            nominal_phase_paths.append(NominalPhasePath(to_phase, from_phase))

        if _is_not_none(xy_phases):
            self._add_xy_phase_paths(terminal, add_from_to)
        else:
            self._add_xy_phase_paths(terminal, add_to_from)

        return nominal_phase_paths

    def _add_xy_phase_paths(self, terminal: Terminal, add_path: Callable[[SinglePhaseKind, SinglePhaseKind], None]):
        """
                val xyPhases = cn.terminals.associateWith { it.findXyPhases() }.filterValues { it.isNotNone() }
                val primaryPhases = cn.terminals.associateWith { it.findPrimaryPhases() }.filterValues { it.isNotNone() }

                findXyCandidatePhases(xyPhases, primaryPhases).apply {
                    calculatePaths()
                        .asSequence()
                        .filter { (_, to) -> to != SPK.NONE }
                        .filter { (from, to) -> (from in terminal.phases.singlePhases) || (to in terminal.phases.singlePhases) }
                        .forEach { (from, to) -> addPath(from, to) }
                }
        """
        cn = terminal.connectivity_node

        xy_phases = {it: _find_xy_phases(it) for it in cn.terminals if _is_not_none(_find_xy_phases(it))}
        primary_phases = {it: _find_primary_phases(it) for it in cn.terminals if _is_not_none(_find_primary_phases(it))}

        candidate_phases = self._find_xy_candidate_phases(xy_phases, primary_phases)
        for from_phase, to_phase in candidate_phases.calculate_paths().items():
            if (to_phase != SinglePhaseKind.NONE) and ((from_phase in terminal.phases.single_phases) or (to_phase in terminal.phases.single_phases)):
                add_path(from_phase, to_phase)

    def _find_xy_candidate_phases(self, xy_phases: Dict[Terminal, PhaseCode], primary_phases: Dict[Terminal, PhaseCode]) -> XyCandidatePhasePaths:
        queue = LifoQueue()
        visited = set()
        candidate_phases = self._create_candidate_phases()

        for terminal, xy_phase_code in xy_phases.items():
            for primary_phase_code in primary_phases.values():
                for phase, candidates in viable_inferred_phase_connectivity.get(xy_phase_code, {}).get(primary_phase_code, {}).items():
                    candidate_phases.add_candidates(phase, candidates)

            # noinspection PyArgumentList
            self._find_more_xy_candidate_phases(XyPhaseStep(terminal, xy_phase_code), visited, queue, candidate_phases)

        while not queue.empty():
            self._find_more_xy_candidate_phases(queue.get(), visited, queue, candidate_phases)

        return candidate_phases

    def _find_more_xy_candidate_phases(
        self,
        step: XyPhaseStep,
        visited: Set[XyPhaseStep],
        queue: Queue[XyPhaseStep],
        candidate_phases: XyCandidatePhasePaths
    ):
        if step in visited:
            return

        visited.add(step)

        without_neutral = step.terminal.phases.without_neutral
        if (SinglePhaseKind.X in without_neutral) or (SinglePhaseKind.Y in without_neutral):
            if not self._check_traced_phases(step, candidate_phases):
                self._queue_next(step.terminal, without_neutral, queue)
        else:
            for (phase, candidates) in viable_inferred_phase_connectivity.get(step.phase_code, {}).get(without_neutral, {}).items():
                candidate_phases.add_candidates(phase, candidates)

    @staticmethod
    def _check_traced_phases(step: XyPhaseStep, candidate_phases: XyCandidatePhasePaths) -> bool:
        found_traced = False
        normal_x = step.terminal.normal_phases[SinglePhaseKind.X]
        if normal_x != SinglePhaseKind.NONE:
            candidate_phases.add_known(SinglePhaseKind.X, normal_x)
            found_traced = True

        normal_y = step.terminal.normal_phases[SinglePhaseKind.Y]
        if normal_y != SinglePhaseKind.NONE:
            candidate_phases.add_known(SinglePhaseKind.Y, normal_y)
            found_traced = True

        return found_traced

    @staticmethod
    def _queue_next(terminal: Terminal, phase_code: PhaseCode, queue: Queue[XyPhaseStep]):
        ce = terminal.conducting_equipment
        if not ce:
            return

        if not isinstance(ce, Switch) or not ce.is_normally_open:
            for other in ce.terminals:
                if (other != terminal) and other.connectivity_node:
                    for connected in other.connectivity_node.terminals:
                        if connected.conducting_equipment != ce:
                            # noinspection PyArgumentList
                            queue.put(XyPhaseStep(connected, phase_code))


def _find_xy_phases(terminal: Terminal):
    if terminal.phases in (PhaseCode.XY, PhaseCode.XYN):
        return PhaseCode.XY
    elif terminal.phases in (PhaseCode.X, PhaseCode.XN):
        return PhaseCode.X
    elif terminal.phases in (PhaseCode.Y, PhaseCode.YN):
        return PhaseCode.Y
    else:
        return PhaseCode.NONE


def _find_primary_phases(terminal: Terminal):
    if terminal.phases in (PhaseCode.ABC, PhaseCode.ABCN):
        primary_phases = PhaseCode.ABC
    elif terminal.phases in (PhaseCode.AB, PhaseCode.ABN):
        primary_phases = PhaseCode.AB
    elif terminal.phases in (PhaseCode.AC, PhaseCode.ACN):
        primary_phases = PhaseCode.AC
    elif terminal.phases in (PhaseCode.BC, PhaseCode.BCN):
        primary_phases = PhaseCode.BC
    elif terminal.phases in (PhaseCode.A, PhaseCode.AN):
        primary_phases = PhaseCode.A
    elif terminal.phases in (PhaseCode.B, PhaseCode.BN):
        primary_phases = PhaseCode.B
    elif terminal.phases in (PhaseCode.C, PhaseCode.CN):
        primary_phases = PhaseCode.C
    else:
        primary_phases = PhaseCode.NONE

    return primary_phases


def _is_not_none(phase_code: PhaseCode) -> bool:
    return phase_code != PhaseCode.NONE
