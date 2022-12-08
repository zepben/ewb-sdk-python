#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations

from typing import Set, TYPE_CHECKING
from zepben.evolve import Tracker, ConnectivityResult

if TYPE_CHECKING:
    from zepben.evolve import ConductingEquipment

__all__ = ["ConnectivityTracker"]


class ConnectivityTracker(Tracker[ConnectivityResult]):
    """
    Tracks destination equipment of connectivity results.
    """

    _visited: Set[ConductingEquipment] = set()

    def has_visited(self, item: ConnectivityResult) -> bool:
        return item.to_equip in self._visited

    def visit(self, item: ConnectivityResult) -> bool:
        equip = item.to_equip
        if equip is not None and equip not in self._visited:
            self._visited.add(equip)
            return True
        else:
            return False

    def clear(self):
        self._visited.clear()

    def copy(self) -> ConnectivityTracker:
        # noinspection PyArgumentList
        return ConnectivityTracker(_visited=self._visited.copy())
