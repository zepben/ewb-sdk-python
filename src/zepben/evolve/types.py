#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations

from typing import Callable, Optional, TypeVar

from zepben.evolve import BasicTraversal
from zepben.evolve.model.cim.iec61970.base.core.conducting_equipment import ConductingEquipment
from zepben.evolve.model.cim.iec61970.base.core.terminal import Terminal
from zepben.evolve.model.cim.iec61970.base.wires.single_phase_kind import SinglePhaseKind
from zepben.evolve.services.network.tracing.feeder.direction_status import DirectionStatus
from zepben.evolve.services.network.tracing.phases.phase_status import PhaseStatus

T = TypeVar("T")

__all__ = ["OpenTest", "QueueNext", "PhaseSelector", "DirectionSelector"]

OpenTest = Callable[[ConductingEquipment, Optional[SinglePhaseKind]], bool]
QueueNext = Callable[[T, BasicTraversal[T]], None]
PhaseSelector = Callable[[Terminal], PhaseStatus]
DirectionSelector = Callable[[Terminal], DirectionStatus]
