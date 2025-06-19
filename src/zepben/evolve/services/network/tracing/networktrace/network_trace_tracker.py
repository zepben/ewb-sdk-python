#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Set, Any, FrozenSet

from zepben.evolve.model.cim.iec61970.base.core.terminal import Terminal
from zepben.evolve.model.cim.iec61970.base.wires.single_phase_kind import SinglePhaseKind


class NetworkTraceTracker:
    """
    Internal class that tracks visited state of a Terminal's Phase in a Network Trace
    """
    def __init__(self):
        self._visited = set()

    def has_visited(self, terminal: Terminal, phases: FrozenSet[SinglePhaseKind]=None) -> bool:
        """Returns True if this Terminal's Phase has been visited, False otherwise"""
        return self._get_key(terminal, phases) in self._visited

    def visit(self, terminal: Terminal, phases: FrozenSet[SinglePhaseKind]=None) -> bool:
        """Marks this Terminal's Phase as visited"""
        key = self._get_key(terminal, phases)
        if key not in self._visited:
            self._visited.add(self._get_key(terminal, phases))
            return True
        return False

    def clear(self):
        """Unmarks this Terminal's Phase as visited"""
        self._visited.clear()

    @staticmethod
    def _get_key(terminal: Terminal, phases: FrozenSet[SinglePhaseKind]) -> Any:
        if phases:
            return terminal.mrid, phases
        else:
            return terminal.mrid
