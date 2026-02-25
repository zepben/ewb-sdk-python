#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ['AcLineSegmentPhase']

from typing import TYPE_CHECKING

from zepben.ewb.model.cim.iec61970.base.core.power_system_resource import PowerSystemResource
from zepben.ewb.model.cim.iec61970.base.wires.single_phase_kind import SinglePhaseKind
from zepben.ewb.model.cim.iec61968.assetinfo.wire_info import WireInfo

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61970.base.wires.ac_line_segment import AcLineSegment


class AcLineSegmentPhase(PowerSystemResource):
    """
    Represents a single wire of an alternating current line segment.

    :var phase: The phase connection of the wire at both ends.
    :var sequence_number: Number designation for this line segment phase. Each line segment phase within a line segment should have a unique sequence number. This is useful for unbalanced modelling to bind the mathematical model (PhaseImpedanceData of PerLengthPhaseImpedance) with the connectivity model (this class) and the physical model (WirePosition) without tight coupling.
    :var ac_line_segment: The line segment to which the phase belongs.
    :var asset_info: The wire info for this phase of the AcLineSegment
    """

    phase: SinglePhaseKind = SinglePhaseKind.X
    sequence_number: int | None = None
    _ac_line_segment: AcLineSegment | None = None

    def __init__(self, ac_line_segment: AcLineSegment = None, **kwargs):
        super(AcLineSegmentPhase, self).__init__(**kwargs)
        if ac_line_segment is not None:
            self.ac_line_segment = ac_line_segment

    @property
    def ac_line_segment(self) -> 'AcLineSegment | None':
        return self._ac_line_segment

    @ac_line_segment.setter
    def ac_line_segment(self, ac_line_segment: 'AcLineSegment') -> None:
        if self._ac_line_segment is None:
            self._ac_line_segment = ac_line_segment
            return
        raise ValueError(f"ac_line_segment has already been set to ${self._ac_line_segment}. Cannot set this field again")


    asset_info: WireInfo | None = None
