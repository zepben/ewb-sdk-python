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


from zepben.model.equipment import ConductingEquipment
from zepben.model.diagram_layout import DiagramObject
from zepben.model.common import Location
from zepben.model.base_voltage import BaseVoltage, UNKNOWN as BV_UNKNOWN
from zepben.model.per_length_sequence_impedance import PerLengthSequenceImpedance
from zepben.model.asset_info import WireInfo
from zepben.cim.iec61970 import AcLineSegment as PBAcLineSegment
from typing import List


class ACLineSegment(ConductingEquipment):
    def __init__(self, mrid: str, plsi: PerLengthSequenceImpedance = None, length: float = 0.0,
                 wire_info: WireInfo = None, base_voltage: BaseVoltage = BV_UNKNOWN, in_service: bool = True, name: str = "",
                 terminals: List = None, diag_objs: List[DiagramObject] = None, location: Location = None):
        self.per_length_sequence_impedance = plsi
        self.length = length
        self.wire_info = wire_info
        super().__init__(mrid, in_service, base_voltage, name, terminals, diag_objs, location)

    def __str__(self):
        return f"{super().__str__()} r: {self.r}, x: {self.x}"

    def __repr__(self):
        return f"{super().__repr__()} r: {self.r}, x: {self.x}"

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
        args['perLengthSequenceImpedanceMRID'] = self.per_length_sequence_impedance.mrid
        args['assetInfoMRID'] = self.wire_info.mrid
        del args['perLengthSequenceImpedance']
        del args['wireInfo']
        return args

    def to_pb(self):
        args = self._pb_args()
        return PBAcLineSegment(**args)
