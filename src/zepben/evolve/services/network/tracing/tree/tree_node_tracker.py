#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations

from typing import Set

from zepben.evolve import Tracker, ConductingEquipment
from zepben.evolve.services.network.tracing.tree.tree_node import TreeNode

__all__ = ["TreeNodeTracker"]


class TreeNodeTracker(Tracker[TreeNode]):
    """
    Simple tracker for traversals that just tracks the items visited.
    """

    _visited: Set[ConductingEquipment] = set()

    def has_visited(self, item: TreeNode) -> bool:
        return item.conducting_equipment in self._visited

    def visit(self, item: TreeNode) -> bool:
        if item.conducting_equipment in self._visited:
            return False
        else:
            self._visited.add(item.conducting_equipment)
            return True

    def clear(self):
        self._visited.clear()

    def copy(self) -> TreeNodeTracker:
        # noinspection PyArgumentList
        return TreeNodeTracker(_visited=self._visited.copy())
