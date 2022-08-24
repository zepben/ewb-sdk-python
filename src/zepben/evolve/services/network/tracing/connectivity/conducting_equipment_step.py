#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from dataclassy import dataclass

from zepben.evolve import ConductingEquipment

__all__ = ["ConductingEquipmentStep"]


@dataclass(slots=True)
class ConductingEquipmentStep:
    """
     A class that can be used for traversing `ConductingEquipment` while keeping track of the number of steps taken.
    """

    conducting_equipment: ConductingEquipment
    """
    The `ConductingEquipment` being processed by this step.
    """

    step: int = 0
    """
    The number of steps from the initial `ConductingEquipment`.
    """
