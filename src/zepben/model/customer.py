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
from zepben.cim.iec61968.customers.Customer_pb2 import Customer as PBCustomer
from typing import List


class Customer(IdentifiedObject):
    def __init__(self, mrid, name: str = "", diagram_objects: List[DiagramObject] = None):
        super().__init__(mrid, name, diagram_objects=diagram_objects)

    def to_pb(self):
        return PBCustomer(**self._pb_args())

    @staticmethod
    def from_pb(pb_c, **kwargs):
        """
        Convert a :class:`zepben.cim.iec61968.customers.Customer` to a Customer.
        :param pb_c: :class:`zepben.cim.iec61968.customers.Customer`
        :return: Customer
        """
        return Customer(mrid=pb_c.mRID, name=pb_c.name, diagram_objects=DiagramObject.from_pbs(pb_c.diagramObjects))
