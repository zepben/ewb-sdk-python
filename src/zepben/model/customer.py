from zepben.model.identified_object import IdentifiedObject
from zepben.model import DiagramObject
from zepben.cim.iec61968.customers.Customer_pb2 import Customer as PBCustomer


class Customer(IdentifiedObject):
    def __init__(self, mrid, name, diagram_objects):
        super().__init__(mrid, name, diagram_objects=diagram_objects)

    def to_pb(self):
        return PBCustomer(**self._pb_args())

    @staticmethod
    def from_pb(pb_c):
        return Customer(pb_c.mRID, pb_c.name, DiagramObject.from_pbs(pb_c.diagramObjects))
