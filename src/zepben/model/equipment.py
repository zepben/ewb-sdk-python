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
from __future__ import annotations

from zepben.model.substation import Substation
from zepben.model.power_system_resource import PowerSystemResource
from zepben.model.asset_info import AssetInfo
from zepben.model.exceptions import NoUsagePointException, AlreadyExistsException
from zepben.model.diagram_layout import DiagramObject
from zepben.model.common import Location
from zepben.model.metering import UsagePoint
from enum import Enum
from typing import List, Set, Dict, TypeVar
EquipmentContainer = TypeVar('Network')
__all__ = ['EquipmentContainerType', 'Equipment']


class EquipmentContainerType(Enum):
    NORMAL_FEEDER = 1
    CURRENT_FEEDER = 2
    SUBSTATION = 3
    LINE = 4
    SITE = 5


class Equipment(PowerSystemResource):
    """
    Abstract class, should only be used through subclasses.
    Any part of a power system that is a physical device, electronic or mechanical.
    Attributes:
        - in_service : If True, the equipment is in service.
        - normally_in_service : If True, the equipment is _normally_ in service.
        - usage_points : List of all usage points associated with this equipment
        - equipment_containers : Mapping of equipment container types to equipment container ID's this equipment
                                 is associated with.
    """
    def __init__(self, mrid: str, in_service: bool, normally_in_service: bool, name: str = "",
                 asset_info: AssetInfo = None, diag_objs: List[DiagramObject] = None, location: Location = None,
                 usage_points: List[UsagePoint] = None):
        """
        :param mrid: mRID for this object
        :param in_service: If True, the equipment is in service.
        :param normally_in_service: If True, the equipment is _normally_ in service.
        :param name: Any free human readable and possibly non unique text naming the object.
        :param asset_info: A subclass of :class:`zepben.model.AssetInfo` providing information about the asset associated
                           with this PowerSystemResource.
        :param diag_objs: An ordered list of :class:`zepben.model.DiagramObject`'s.
        :param location: :class:`zepben.model.Location` of this resource.
        :param usage_points List of :class:`zepben.model.UsagePoint`'s associated with this equipment
        """
        super().__init__(mrid=mrid, name=name, asset_info=asset_info, diag_objs=diag_objs, location=location)
        self.in_service = in_service
        self.normally_in_service = normally_in_service
        self.__usage_points = usage_points if usage_points is not None else []
        self.__equipment_containers: Dict[str, EquipmentContainer] = dict()

    @property
    def substations(self):
        return [ec for ec in self.__equipment_containers if isinstance(ec, Substation)]

    @property
    def position_points(self):
        return self.location.position_points

    def pos_point(self, sequence_number):
        try:
            return self.location.position_points[sequence_number]
        except IndexError:
            return None

    def has_points(self):
        return len(self.location.position_points) > 0

    @property
    def usage_points(self):
        return self.__usage_points

    def has_usage_point(self, usage_point_mrid: str):
        for point in self.__usage_points:
            if point.mrid == usage_point_mrid:
                return True
        else:
            return False

    def get_usage_point(self, usage_point_mrid: str):
        for point in self.__usage_points:
            if point.mrid == usage_point_mrid:
                return point
        else:
            raise NoUsagePointException(f"{usage_point_mrid}")

    def add_usage_point(self, usage_point: UsagePoint):
        if self.has_usage_point(usage_point.mrid):
            raise AlreadyExistsException(f"Usage point {usage_point.mrid} is already associated with {type(self).__name__} {self.mrid}")
        else:
            self.__usage_points.append(usage_point)

    def link_equipment_container(self, container: EquipmentContainer):
        self.__equipment_containers[container.mrid] = container



