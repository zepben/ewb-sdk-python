#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations

from typing import Callable, Optional, TypeVar
from zepben.evolve import ConductingEquipment, SinglePhaseKind, Traversal, Terminal, DirectionStatus

T = TypeVar("T")

__all__ = ["OpenTest", "QueueNext", "DirectionSelector"]

OpenTest = Callable[[ConductingEquipment, Optional[SinglePhaseKind]], bool]
QueueNext = Callable[[T, Traversal[T]], None]
DirectionSelector = Callable[[Terminal], DirectionStatus]
