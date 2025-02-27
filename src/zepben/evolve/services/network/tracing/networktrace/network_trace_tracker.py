#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Set

from zepben.evolve import Terminal, SinglePhaseKind, NominalPhasePath


class NetworkTraceTracker:
    _visited = set()
    def __init__(self, initial_capacity: int):
        self.initial_capacity = initial_capacity

    def has_visited(self, terminal: Terminal, phases: Set[SinglePhaseKind]) -> bool:
        return self._get_key(terminal, phases) in self._visited

    def visit(self, terminal: Terminal, phases: Set[SinglePhaseKind]) -> None:
        return self._visited.add(self._get_key(terminal, phases))

    def clear(self):
        self._visited.clear()

    def _get_key(self, terminal: Terminal, phases: Set[SinglePhaseKind]) -> ... :
        if len(phases) < 1:
            return terminal
        else:
            return terminal, phases  # TODO: unsure if this is right.


# TODO: internal fun List<NominalPhasePath>.toPhasesSet(): Set<SinglePhaseKind> = if (this.isEmpty()) emptySet() else this.mapTo(mutableSetOf()) { it.to }
