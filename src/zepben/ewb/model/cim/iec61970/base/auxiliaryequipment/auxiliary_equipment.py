#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["AuxiliaryEquipment"]

from typing import Optional, TYPE_CHECKING

from zepben.ewb.model.cim.iec61970.base.core.equipment import Equipment

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61970.base.core.terminal import Terminal


class AuxiliaryEquipment(Equipment):
    """
    `AuxiliaryEquipment` describe equipment that is not performing any primary functions but support for the
    equipment performing the primary function.

    `AuxiliaryEquipment` is attached to primary equipment via an association with `Terminal`.
    """
    terminal: Optional['Terminal'] = None
    """The `zepben.ewb.model.cim.iec61970.base.core.terminal.Terminal`` at the `Equipment` where the `AuxiliaryEquipment` is attached."""
