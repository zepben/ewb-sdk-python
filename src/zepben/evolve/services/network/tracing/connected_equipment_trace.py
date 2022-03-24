#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Optional, TypeVar

from zepben.evolve.services.network.network_service import connected_equipment
if TYPE_CHECKING:
    from zepben.evolve import ConductingEquipment, Traversal
    from zepben.evolve.types import OpenTest, QueueNext
    T = TypeVar("T")

__all__ = ["queue_next_connected_equipment_with_open_test"]


# TODO: Rename this to something sane
def queue_next_connected_equipment_with_open_test(open_test: OpenTest) -> QueueNext[ConductingEquipment]:
    def queue_next(conducting_equipment: ConductingEquipment, traversal: Traversal[ConductingEquipment]):
        if open_test(conducting_equipment, None):
            return
        for cr in connected_equipment(conducting_equipment):
            if cr.to_equip:
                traversal.process_queue.put(cr.to_equip)

    return queue_next
