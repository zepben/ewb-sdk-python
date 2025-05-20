#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations
__all__ = ["Cut"]

from typing import Optional, TYPE_CHECKING

from zepben.evolve.model.cim.iec61970.base.wires.switch import Switch

if TYPE_CHECKING:
    from zepben.evolve.model.cim.iec61970.base.wires.aclinesegment import AcLineSegment


class Cut(Switch):
    """
    A cut separates a line segment into two parts. The cut appears as a switch inserted between these two parts and connects them together. As the cut is
    normally open there is no galvanic connection between the two line segment parts. But it is possible to close the cut to get galvanic connection. The cut
    terminals are oriented towards the line segment terminals with the same sequence number. Hence the cut terminal with sequence number equal to 1 is oriented
    to the line segment's terminal with sequence number equal to 1. The cut terminals also act as connection points for jumpers and other equipment, e.g. a
    mobile generator. To enable this, connectivity nodes are placed at the cut terminals. Once the connectivity nodes are in place any conducting equipment can
    be connected at them.
    """

    max_terminals = 2

    length_from_terminal_1: Optional[float] = None
    """The length to the place where the cut is located starting from side one of the cut line segment, i.e. the line segment Terminal with sequenceNumber equal to 1."""

    ac_line_segment: Optional[AcLineSegment] = None
    """The line segment to which the cut is applied."""

    @property
    def length_from_T1_or_0(self) -> float:
        return self.length_from_terminal_1 or 0.0
