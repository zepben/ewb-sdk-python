from zepben.model.identified_object import IdentifiedObject
from zepben.model.diagram_layout import DiagramObject
from zepben.cim.iec61970.base.wires.PerLengthSequenceImpedance_pb2 import PerLengthSequenceImpedance as PBPerLengthSequenceImpedance
from typing import List


class PerLengthSequenceImpedance(IdentifiedObject):
    def __init__(self, mrid: str, r: float, x: float, r0: float, x0: float, bch: float, b0ch: float,
                 name: str = None, diag_objects: List[DiagramObject] = None):
        self.r = r
        self.x = x
        self.r0 = r0
        self.x0 = x0
        self.bch = bch
        self.b0ch = b0ch
        super().__init__(mrid, name, diag_objects)

    @staticmethod
    def from_pb(pb_plsi):
        """
        Convert a Protobuf PerLengthSequenceImpedance
        :param pb_plsi: :class:`zepben.cim.iec61970.base.wires.PerLengthSequenceImpedance`
        :return: PerLengthSequenceImpedance
        """
        diag_objects = []
        for do in pb_plsi.diagramObjects:
            diag_objects.append(DiagramObject.from_pb(do))
        return PerLengthSequenceImpedance(mrid=pb_plsi.mRID, r=pb_plsi.r, x=pb_plsi.x, r0=pb_plsi.r0, x0=pb_plsi.x0,
                                          bch=pb_plsi.bch, b0ch=pb_plsi.b0ch, name=pb_plsi.name, diag_objects=diag_objects)

    def to_pb(self):
        args = self._pb_args()
        return PBPerLengthSequenceImpedance(**args)
