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
from zepben.cim.iec61970 import Breaker as PBBreaker
from typing import List


class Switch(ConductingEquipment):
    def __init__(self, mrid: str, open_: List[bool], base_voltage: BaseVoltage = BV_UNKNOWN, in_service: bool = True, name: str = "",
                 terminals: List = None, diag_objs: List[DiagramObject] = None, location: Location = None):
        """Unganged switches are supported as a list of booleans, each bool corresponding to a single phase"""
        self.open = open_
        super().__init__(mrid=mrid, in_service=in_service, base_voltage=base_voltage, name=name,
                         terminals=terminals, diag_objs=diag_objs, location=location)

    def __len__(self):
        return len(self.open)

    def connected(self):
        return not self.is_open()

    def is_open(self):
        """Switch is open only if it's not in service OR at least one phase is open"""
        if not self.in_service:
            return not self.in_service
        for o in self.open:
            if o:
                return o
        return False


class Breaker(Switch):
    def __init__(self, mrid: str, open_: bool, base_voltage: BaseVoltage = BV_UNKNOWN, in_service: bool = True, name: str = "",
                 terminals: List = None, diag_objs: List[DiagramObject] = None, location: Location = None):
        super().__init__(mrid=mrid, open_=open_, in_service=in_service, base_voltage=base_voltage, name=name,
                         terminals=terminals, diag_objs=diag_objs, location=location)

    def to_pb(self):
        args = self._pb_args()
        return PBBreaker(**args)
