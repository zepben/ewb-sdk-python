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
from dataclasses import dataclass
from typing import Optional

from zepben.cimbend.cim.iec61968.assetinfo.wire_info import CableInfo
from zepben.cimbend.cim.iec61970.base.core.conducting_equipment import ConductingEquipment
from zepben.cimbend.cim.iec61970.base.wires.per_length import PerLengthSequenceImpedance

__all__ = ["AcLineSegment", "Conductor"]


@dataclass
class Conductor(ConductingEquipment):
    """
    Combination of conducting material with consistent electrical characteristics, building a single electrical
    system, used to carry current between points in the power system.

    Attributes -
        length : Segment length for calculating line section capabilities.
        wire_info : The :class:`zepben.cimbend.iec61968.assetinfo.wire_info.WireInfo` for this ``Conductor``
    """

    length: float = 0.0

    @property
    def wire_info(self):
        return self.asset_info

    @property
    def is_underground(self):
        return isinstance(self.wire_info, CableInfo)


@dataclass
class AcLineSegment(Conductor):
    """
    A wire or combination of wires, with consistent electrical characteristics, building a single electrical system,
    used to carry alternating current between points in the power system.

    For symmetrical, transposed 3ph lines, it is sufficient to use  attributes of the line segment, which describe
    impedances and admittances for the entire length of the segment.  Additionally impedances can be computed by
    using length and associated per length impedances.

    The BaseVoltage at the two ends of ACLineSegments in a Line shall have the same BaseVoltage.nominalVoltage.
    However, boundary lines  may have slightly different BaseVoltage.nominalVoltages and  variation is allowed.
    Larger voltage difference in general requires use of an equivalent branch.

    Attributes:
        per_length_sequence_impedance : A :class:`zepben.cimbend.PerLengthSequenceImpedance` describing this ACLineSegment
    """
    per_length_sequence_impedance: Optional[PerLengthSequenceImpedance] = None

    @property
    def rated_current(self):
        return self.wire_info.rated_current

    @property
    def r(self):
        return self.per_length_sequence_impedance.r

    @property
    def x(self):
        return self.per_length_sequence_impedance.x

    @property
    def r0(self):
        return self.per_length_sequence_impedance.r0

    @property
    def x0(self):
        return self.per_length_sequence_impedance.x0

    @property
    def bch(self):
        return self.per_length_sequence_impedance.bch

    @property
    def b0ch(self):
        return self.per_length_sequence_impedance.b0ch

    def _pb_args(self, exclude=None):
        args = super()._pb_args()
        if self.per_length_sequence_impedance:
            args['perLengthSequenceImpedanceMRID'] = self.per_length_sequence_impedance.mrid
            del args['perLengthSequenceImpedance']
        if self.asset_info:
            args['assetInfoMRID'] = self.wire_info.mrid
        if 'wireInfo' in args:
            del args['wireInfo']
        return args

