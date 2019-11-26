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


from zepben.cim.iec61968 import PositionPoint as PBPositionPoint
from zepben.cim.iec61968 import Location as PBLocation
from zepben.model.identified_object import IdentifiedObject
from zepben.model.diagram_layout import DiagramObject
from typing import List


class PositionPoint(IdentifiedObject):
    def __init__(self, latitude, longitude):
        self.x_position = longitude
        self.y_position = latitude
        super().__init__()

    def __str__(self):
        return f"{self.x_position}:{self.y_position}"

    def __repr__(self):
        return f"{self.x_position}:{self.y_position}"

    def to_pb(self):
        return PBPositionPoint(xPosition=self.x_position, yPosition=self.y_position)

    @staticmethod
    def from_pb(pos_point):
        return PositionPoint(pos_point.xPosition, pos_point.yPosition)


class Location(IdentifiedObject):
    # TODO: TOMORROW - ADD DIAGRAM OBJECT + points with some kind of sensible default
    def __init__(self, street_address=None, position_points: List[PositionPoint] = None, diag_obj = None):
        self.main_address = street_address
        self.position_points = position_points
        # We currently have no use for the fields in IdentifiedObject for a Location
        super().__init__("")

    def to_pb(self):
        args = self._pb_args()
        return PBLocation(**args)

    @staticmethod
    def from_pb(pb_l):
        """
        Transform a Protobuf Location to a cimbend Location
        TODO: Test this doesn't error on empty positionPoints
        TODO: Create StreetAddress type
        :param pb_l: Protobuf Location
        :return: A location
        """
        return Location(street_address=pb_l.mainAddress,
                        position_points=PositionPoint.from_pbs(pb_l.positionPoints),
                        diag_obj=DiagramObject.from_pbs(pb_l.diagramObjects))
