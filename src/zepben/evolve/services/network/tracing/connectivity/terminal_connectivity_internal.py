#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Set, Optional

from zepben.evolve import Terminal, PowerTransformer, SinglePhaseKind, ConnectivityResult, NominalPhasePath
from zepben.evolve.services.network.tracing.connectivity.transformer_phase_paths import transformer_phase_paths

__all__ = ["TerminalConnectivityInternal"]


class TerminalConnectivityInternal:
    """
    Helper class for finding the paths through equipment.
    """

    def between(
        self,
        terminal: Terminal,
        other_terminal: Terminal,
        include_phases: Optional[Set[SinglePhaseKind]] = None
    ) -> ConnectivityResult:
        """
         * Find the connectivity between the two terminals. The function assumes they are on the same conducting equipment.
         *
         * @param terminal The terminal you are moving from
         * @param other_terminal The terminal you are moving to
         * @param include_phases The nominal phases on the [terminal] you want to use.
         *
         * @return The connectivity between [terminal] and [other_terminal]. If the conducting equipment is a power transformer the nominal phase paths may
         *         contain an entry with the 'from' phase set to NONE and the 'to' phase set to N, indicating a neutral has been added by the transformer1.
        """
        if include_phases is None:
            include_phases = set(terminal.phases.single_phases)

        if isinstance(terminal.conducting_equipment, PowerTransformer):
            return self._transformer_terminal_connectivity(terminal, other_terminal, include_phases)

        return self._straight_terminal_connectivity(terminal, other_terminal, include_phases)

    @staticmethod
    def _transformer_terminal_connectivity(
        terminal: Terminal,
        other_terminal: Terminal,
        include_phases: Set[SinglePhaseKind]
    ) -> ConnectivityResult:
        paths = [it for it in transformer_phase_paths.get(terminal.phases, {}).get(other_terminal.phases, [])
                 if (it.from_phase in include_phases) or (it.from_phase == SinglePhaseKind.NONE)]

        return ConnectivityResult(terminal, other_terminal, paths)

    @staticmethod
    def _straight_terminal_connectivity(
        terminal: Terminal,
        other_terminal: Terminal,
        include_phases: Set[SinglePhaseKind]
    ) -> ConnectivityResult:
        # noinspection PyArgumentList
        paths = [NominalPhasePath(it, it) for it in set(terminal.phases.single_phases).intersection(set(other_terminal.phases.single_phases))
                 if it in include_phases]

        return ConnectivityResult(terminal, other_terminal, paths)
