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


from zepben.model.network import EquipmentContainer
from zepben.model.containers import UNKNOWN_SUBGEO, SubGeographicalRegion
__all__ = ["Substation", "UNKNOWN_SUBSTATION"]


class Substation(EquipmentContainer):
    def __init__(self, mrid, subgeo: SubGeographicalRegion = None, name: str = ""):
        super().__init__(mrid=mrid, name=name)
        self.sub_geographical_region = subgeo
        self.normal_energized_feeders = dict()

    @staticmethod
    def from_pb(pb_gr):
        raise NotImplementedError()

    def to_pb(self):
        raise NotImplementedError()


UNKNOWN_SUBSTATION = Substation("dc20ec4d-cbf0-474d-886b-42c21ec92ff4", subgeo=UNKNOWN_SUBGEO, name="unknown")
