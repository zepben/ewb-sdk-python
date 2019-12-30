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


from zepben.model.identified_object import IdentifiedObject
from zepben.model.diagram_layout import DiagramObject
from typing import List
__all__ = ["GeographicalRegion", "SubGeographicalRegion", "UNKNOWN_SUBGEO", "UNKNOWN_GEO"]
# TODO: implement from_pb/to_pb


class GeographicalRegion(IdentifiedObject):
    def __init__(self, mrid: str, name: str = "", diag_objs: List[DiagramObject] = None):
        super().__init__(mrid=mrid, name=name, diagram_objects=diag_objs)
        self.sub_geographical_regions = dict()

    @staticmethod
    def from_pb(pb_gr):
        raise NotImplementedError()

    def to_pb(self):
        raise NotImplementedError()


class SubGeographicalRegion(IdentifiedObject):
    def __init__(self, mrid: str, geo_region: GeographicalRegion, name: str = "", diag_objs: List[DiagramObject] = None):
        super().__init__(mrid=mrid, name=name, diagram_objects=diag_objs)
        self.geographical_region = geo_region
        self.substations = dict()

    @staticmethod
    def from_pb(pb_sgr):
        raise NotImplementedError()

    def to_pb(self):
        raise NotImplementedError()


UNKNOWN_GEO = GeographicalRegion(mrid="cb593aff-c5a2-4d8c-9548-f7309141cca6", name="unknown_geo")
UNKNOWN_SUBGEO = SubGeographicalRegion(mrid="cb95892f-695f-487e-9251-1dcaf3f36875", geo_region=UNKNOWN_GEO,
                                       name="unknown_subgeo")
