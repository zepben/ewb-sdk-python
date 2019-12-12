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


from zepben.cim.iec61968 import PositionPoint as PBPositionPoint, TownDetail as PBTownDetail, StreetAddress as PBStreetAddress
from zepben.cim.iec61968 import Location as PBLocation
from zepben.model.identified_object import IdentifiedObject
from zepben.model.diagram_layout import DiagramObject
from typing import List


class PositionPoint(IdentifiedObject):
    """
    Set of spatial coordinates that determine a point, defined in WGS84 (latitudes and longitudes).

    Use a single position point instance to desribe a point-oriented location.
    Use a sequence of position points to describe a line-oriented object (physical location of non-point oriented
    objects like cables or lines), or area of an object (like a substation or a geographical zone - in this case,
    have first and last position point with the same values).

    Attributes:
        x_position : X axis position - longitude
        y_position : Y axis position - latitude
    """
    def __init__(self, latitude: float, longitude: float):
        """
        :param latitude: The latitude of the point
        :param longitude: The longitude of the point
        """
        self.x_position = longitude
        self.y_position = latitude
        # mrid, name, diagramObjects are currently unused.
        super().__init__()

    def __str__(self):
        return f"{self.x_position}:{self.y_position}"

    def __repr__(self):
        return f"{self.x_position}:{self.y_position}"

    @property
    def longitude(self):
        return self.x_position

    @longitude.setter
    def longitude(self, lon):
        self.x_position = lon

    @property
    def latitude(self):
        return self.y_position

    @latitude.setter
    def latitude(self, lat):
        self.y_position = lat

    def to_pb(self):
        return PBPositionPoint(xPosition=self.x_position, yPosition=self.y_position)

    @staticmethod
    def from_pb(pos_point):
        return PositionPoint(pos_point.xPosition, pos_point.yPosition)


class TownDetail(object):
    def __init__(self, name: str, state_or_province: str):
        self.name = name
        self.state_or_province = state_or_province

    def to_pb(self):
        return PBTownDetail(name=self.name, stateOrProvince=self.state_or_province)

    @staticmethod
    def from_pb(pb_td):
        return TownDetail(name=pb_td.name, state_or_province=pb_td.stateOrProvince)


class StreetAddress(object):
    def __init__(self, postal_code: str, town_detail: TownDetail):
        super().__init__()
        self.postal_code = postal_code
        self.town_detail = town_detail

    def to_pb(self):
        return PBStreetAddress(postalCode=self.postal_code, townDetail=self.town_detail.to_pb())

    @staticmethod
    def from_pb(pb_sa):
        return StreetAddress(pb_sa.postalCode, TownDetail.from_pb(pb_sa.townDetail))


class Location(IdentifiedObject):
    """
    The place, scene, or point of something where someone or something has been, is, and/or will be at a given moment
    in time. It can be defined with one or more :class:`PositionPoint`'s.

    Attributes:
        main_address : Main address of the location.
        position_points : List of :class:`PositionPoint`. The ordering of the list is important, and refers to the
                          `sequenceNumber` of each PositionPoint.

    """
    def __init__(self, street_address=None, position_points: List[PositionPoint] = None, mrid: str = "",
                 name: str = "", diag_objs: List[DiagramObject] = None):
        """

        :param street_address: Main address of the location.
        :param position_points: List of :class:`PositionPoint`. The ordering of the list is important, and refers to the
                                `sequenceNumber` of each PositionPoint.
        :param mrid: mRID of Location, typically unused.
        :param name: Name of Location
        :param diag_objs: An ordered list of :class:`zepben.model.DiagramObject`'s.
        """
        self.main_address = street_address
        self.position_points = position_points
        super().__init__(mrid=mrid, name=name, diagram_objects=diag_objs)

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
        return Location(street_address=StreetAddress.from_pb(pb_l.mainAddress),
                        position_points=PositionPoint.from_pbs(pb_l.positionPoints),
                        diag_objs=DiagramObject.from_pbs(pb_l.diagramObjects))

