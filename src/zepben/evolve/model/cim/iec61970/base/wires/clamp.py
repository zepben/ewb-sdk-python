#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations
__all__ = ["Clamp"]

from typing import Optional, TYPE_CHECKING

from zepben.evolve.model.cim.iec61970.base.core.conducting_equipment import ConductingEquipment

if TYPE_CHECKING:
    from zepben.evolve.model.cim.iec61970.base.wires.aclinesegment import AcLineSegment


class Clamp(ConductingEquipment):
    """
    A Clamp is a galvanic connection at a line segment where other equipment is connected. A Clamp does not cut the line segment. A Clamp is ConductingEquipment
    and has one Terminal with an associated ConnectivityNode. Any other ConductingEquipment can be connected to the Clamp ConnectivityNode.
    """

    length_from_terminal_1: Optional[float] = None
    """The length to the place where the clamp is located starting from side one of the line segment, i.e. the line segment terminal with sequence number equal to 1."""

    ac_line_segment: Optional[AcLineSegment] = None
    """The line segment to which the clamp is connected."""

    max_terminals = 1

    @property
    def length_from_T1_or_0(self) -> float:
        return self.length_from_terminal_1 or 0.0
