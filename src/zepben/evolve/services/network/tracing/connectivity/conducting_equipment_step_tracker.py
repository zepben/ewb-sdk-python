#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations

from typing import Dict

from zepben.evolve import Tracker, ConductingEquipmentStep, ConductingEquipment


class ConductingEquipmentStepTracker(Tracker[ConductingEquipmentStep]):
    """
    A specialised tracker for traversals that use [ConductingEquipmentStep].

    Will consider something visited only if the number of steps is greater than or equal to minimum number of steps used to get to an item previously. This
    means that the same item can be visited multiple times if a short path is traversed.
    """

    _minimum_steps: Dict[ConductingEquipment, int] = {}

    def has_visited(self, item: ConductingEquipmentStep) -> bool:
        """
        Check if the tracker has already seen an item. The item is only considered seen if it has been seen with the equal, or fewer, steps.

        :param item: The item to check if it has been visited.
        :return: True if the item has been visited with equal, or fewer, steps, otherwise False.
        """
        existing_steps = self._minimum_steps.get(item.conducting_equipment, None)
        return existing_steps <= item.step if existing_steps is not None else False

    def visit(self, item: ConductingEquipmentStep) -> bool:
        """
        Visit an item. Item will not be visited if it has previously been visited.

        :param item: The item to visit.
        :return: True if visit succeeds. False otherwise.
        """
        previous_steps = self._minimum_steps.get(item.conducting_equipment, None)
        new_steps = previous_steps if previous_steps is not None and previous_steps <= item.step else item.step

        if previous_steps is None or (new_steps < previous_steps):
            self._minimum_steps[item.conducting_equipment] = new_steps
            return True
        else:
            return False

    def clear(self):
        """
        Clear the tracker, removing all visited items.
        """
        self._minimum_steps = {}

    def copy(self) -> ConductingEquipmentStepTracker:
        # noinspection PyArgumentList
        return ConductingEquipmentStepTracker(_minimum_steps=self._minimum_steps.copy())
