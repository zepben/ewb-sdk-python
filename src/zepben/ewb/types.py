#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["OpenTest"]

from typing import Callable, Optional, TypeVar

from zepben.ewb.model.cim.iec61970.base.core.conducting_equipment import ConductingEquipment
from zepben.ewb.model.cim.iec61970.base.wires.single_phase_kind import SinglePhaseKind

T = TypeVar("T")

OpenTest = Callable[[ConductingEquipment, Optional[SinglePhaseKind]], bool]
