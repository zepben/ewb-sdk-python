#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations

from typing import Optional, List, Generator

from zepben.evolve import ConductingEquipment
from zepben.evolve.util import ngen

__all__ = ["TreeNode"]


class TreeNode(object):

    def __init__(self, conducting_equipment: ConductingEquipment, parent: Optional[TreeNode]):
        self.conducting_equipment = conducting_equipment
        self._parent = parent
        self._children: List[TreeNode] = []
        self._sort_weight = max((len(term.phases.single_phases) for term in conducting_equipment.terminals), default=1)

    @property
    def parent(self) -> Optional[TreeNode]:
        return self._parent

    @property
    def children(self) -> Generator[TreeNode, None, None]:
        return ngen(self._children)

    @property
    def sort_weight(self) -> int:
        return self._sort_weight

    def __lt__(self, other: TreeNode):
        """
        This definition should only be used for sorting within a `PriorityQueue`

        @param other: Another PhaseStep to compare against
        @return: True if this node's max phase count over its equipment's terminals is greater than the other's, False otherwise.
        """
        return self._sort_weight > other._sort_weight

    def __str__(self):
        return f"{{conducting_equipment: {self.conducting_equipment.mrid}, parent: {self._parent and self._parent.conducting_equipment.mrid}, " \
               f"num children: {len(self._children)}}}"

    def add_child(self, child: TreeNode):
        self._children.append(child)
