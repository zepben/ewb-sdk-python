#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from typing import Optional

from zepben.evolve.model.cim.iec61970.base.core.equipment import Equipment
from zepben.evolve.model.cim.iec61970.base.core.terminal import Terminal

__all__ = ["AuxiliaryEquipment", "FaultIndicator"]


class AuxiliaryEquipment(Equipment):
    """
    `AuxiliaryEquipment` describe equipment that is not performing any primary functions but support for the
    equipment performing the primary function.

    `AuxiliaryEquipment` is attached to primary equipment via an association with `Terminal`.
    """
    terminal: Optional[Terminal] = None
    """The `zepben.evolve.iec61970.base.core.terminal.Terminal`` at the `Equipment` where the `AuxiliaryEquipment` is attached."""


class FaultIndicator(AuxiliaryEquipment):
    """
    A FaultIndicator is typically only an indicator (which may or may not be remotely monitored), and not a piece of
    equipment that actually initiates a protection event. It is used for FLISR (Fault Location, Isolation and
    Restoration) purposes, assisting with the dispatch of crews to "most likely" part of the network (i.e. assists
    with determining circuit section where the fault most likely happened).
    """
    pass
