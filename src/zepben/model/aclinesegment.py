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
from zepben.model.diagram_layout import DiagramObjectPoints
from zepben.model.common import PositionPoints
from zepben.cim.IEC61970.wires_pb2 import ACLineSegment as PBACLineSegment
from typing import Set


class ACLineSegment(ConductingEquipment):
    def __init__(self, mrid: str, r: float = 0.0, x: float = 0.0, r0: float = 0.0, x0: float = 0.0, length: float = 0.0,
                 rated_current: float = 0.0, nom_volts: float = 0.0, in_service: bool = True, name: str = "", description: str = "",
                 terminals: Set = None, diag_point: DiagramObjectPoints = None, pos_points: PositionPoints = None):

        self.r = r
        self.x = x
        self.r0 = r0
        self.x0 = x0
        self.length = length
        self.rated_current = rated_current
        super().__init__(mrid, in_service, nom_volts, name, description, terminals, diag_point, pos_points)

    def __str__(self):
        return f"{super().__str__()} r: {self.r}, x: {self.x}"

    def __repr__(self):
        return f"{super().__repr__()} r: {self.r}, x: {self.x}"

    def to_pb(self):
        args = self._pb_args()
        return PBACLineSegment(**args)
