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
from zepben.cim.IEC61970.wires_pb2 import Breaker as PBBreaker
from typing import Set


class Switch(ConductingEquipment):
    def __init__(self, mrid: str, open_: bool, nom_volts: float = 0.0, in_service: bool = True, name: str = "",
                 desc: str = "", terminals: Set = None, diag_point: DiagramObjectPoints = None, pos_points: PositionPoints = None):
        self.open = open_
        super().__init__(mrid=mrid, in_service=in_service, nom_volts=nom_volts, name=name, description=desc,
                         terminals=terminals, diag_point=diag_point, pos_points=pos_points)

    def connected(self):
        return not self.is_open()

    def is_open(self):
        return not self.in_service or self.open


class Breaker(Switch):
    def __init__(self, mrid: str, open_: bool, nom_volts: float = 0.0, in_service: bool = True, name: str = "",
                 desc: str = "", terminals: Set = None, diag_point: DiagramObjectPoints = None, pos_points: PositionPoints = None):
        super().__init__(mrid=mrid, open_=open_, in_service=in_service, nom_volts=nom_volts, name=name, desc=desc,
                         terminals=terminals, diag_point=diag_point, pos_points=pos_points)

    def to_pb(self):
        args = self._pb_args()
        return PBBreaker(**args)
