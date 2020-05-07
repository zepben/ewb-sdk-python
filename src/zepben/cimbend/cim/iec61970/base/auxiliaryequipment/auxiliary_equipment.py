"""
Copyright 2019 Zeppelin Bend Pty Ltd
This file is part of cimbend.

cimbend is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

cimbend is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with cimbend.  If not, see <https://www.gnu.org/licenses/>.
"""


from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from zepben.cimbend.cim.iec61970.base.core.equipment import Equipment

__all__ = ["AuxiliaryEquipment", "FaultIndicator"]


@dataclass
class AuxiliaryEquipment(Equipment):
    """

    ``AuxiliaryEquipment`` describe equipment that is not performing any primary functions but support for the
    equipment performing the primary function.

    ``AuxiliaryEquipment`` is attached to primary equipment via an association with :class:`zepben.cimbend.iec61970.base.core.Terminal`.
    Attributes -
        terminal : The ``Terminal`` at the equipment where the ``AuxiliaryEquipment`` is attached.
    """
    terminal: Optional[Terminal] = None


@dataclass
class FaultIndicator(AuxiliaryEquipment):
    """
    A FaultIndicator is typically only an indicator (which may or may not be remotely monitored), and not a piece of
    equipment that actually initiates a protection event. It is used for FLISR (Fault Location, Isolation and
    Restoration) purposes, assisting with the dispatch of crews to "most likely" part of the network (i.e. assists
    with determining circuit section where the fault most likely happened).
    """
    pass
