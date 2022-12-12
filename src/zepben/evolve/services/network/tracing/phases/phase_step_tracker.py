#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING, TypeVar, Dict, Set

from zepben.evolve.services.network.tracing.phases.phase_step import PhaseStep
from zepben.evolve.services.network.tracing.traversals.tracker import Tracker
if TYPE_CHECKING:
    from zepben.evolve import ConductingEquipment, SinglePhaseKind

T = TypeVar("T")

__all__ = ["PhaseStepTracker"]


class PhaseStepTracker(Tracker[PhaseStep]):
    """
    A specialised tracker that tracks the cores that have been visited on a piece of conducting equipment. When attempting to visit
    for the second time, this tracker will return false if the cores being tracked are a subset of those already visited.
    For example, if you visit A1 on cores 0, 1, 2 and later attempt to visit A1 on core 0, 1, visit will return false,
    but an attempt to visit on cores 2, 3 would return true as 3 has not been visited before.

    This tracker does not support null items.
    """

    _visited: Dict[ConductingEquipment, Set[SinglePhaseKind]] = defaultdict(set)

    def has_visited(self, item: PhaseStep) -> bool:
        return item.phases.issubset(self._visited[item.conducting_equipment])

    def visit(self, item: PhaseStep) -> bool:
        visited_phases = self._visited[item.conducting_equipment]

        changed = False
        for phase in item.phases:
            changed = changed or phase not in visited_phases
            visited_phases.add(phase)

        return changed

    def clear(self):
        self._visited.clear()

    def copy(self) -> PhaseStepTracker:
        # noinspection PyArgumentList
        return PhaseStepTracker(_visited=defaultdict(set, {ce: visited_phases.copy() for ce, visited_phases in self._visited.items()}))
