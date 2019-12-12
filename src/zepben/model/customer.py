from zepben.model.identified_object import IdentifiedObject
from zepben.model.diagram_layout import DiagramObject
from zepben.cim.iec61968.customers.Customer_pb2 import Customer as PBCustomer


class Customer(IdentifiedObject):
    def __init__(self, mrid, name, diagram_objects):
        super().__init__(mrid, name, diagram_objects=diagram_objects)

    def to_pb(self):
        return PBCustomer(**self._pb_args())

    @staticmethod
    def from_pb(pb_c):
        """
        Convert a :class:`zepben.cim.iec61968.customers.Customer` to a Customer.
        :param pb_c: :class:`zepben.cim.iec61968.customers.Customer`
        :return: Customer
        """
        return Customer(mrid=pb_c.mRID, name=pb_c.name, diagram_objects=DiagramObject.from_pbs(pb_c.diagramObjects))
