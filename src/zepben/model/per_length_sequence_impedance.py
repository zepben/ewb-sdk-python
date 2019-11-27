from zepben.model.identified_object import IdentifiedObject
from zepben.model.diagram_layout import DiagramObject
from zepben.cim.iec61970.base.wires.PerLengthSequenceImpedance_pb2 import PerLengthSequenceImpedance as PBPerLengthSequenceImpedance
from typing import List


class PerLengthSequenceImpedance(IdentifiedObject):
    """
    Sequence impedance and admittance parameters per unit length, for transposed lines of 1, 2, or 3 phases.
    For 1-phase lines, define x=x0=xself. For 2-phase lines, define x=xs-xm and x0=xs+xm.

    Typically, one PerLengthSequenceImpedance is used for many ACLineSegments.

    Attributes:
        b0ch : Zero sequence shunt (charging) susceptance, per unit of length.
        bch : Positive sequence shunt (charging) susceptance, per unit of length.
        r : Positive sequence series resistance, per unit of length.
        r0 : Zero sequence series resistance, per unit of length.
        x : Positive sequence series reactance, per unit of length.
        x0 : Zero sequence series reactance, per unit of length.
    """
    def __init__(self, mrid: str, r: float, x: float, r0: float, x0: float, bch: float, b0ch: float,
                 name: str = "", diag_objs: List[DiagramObject] = None):
        """
        Create a PerLengthSequenceImpedance
        :param mrid: mRID for this object
        :param r: Positive sequence series resistance, per unit of length.
        :param x: Positive sequence series reactance, per unit of length.
        :param r0: Zero sequence series resistance, per unit of length.
        :param x0: Zero sequence series reactance, per unit of length.
        :param bch: Positive sequence shunt (charging) susceptance, per unit of length.
        :param b0ch: Zero sequence shunt (charging) susceptance, per unit of length.
        :param name: Any free human readable and possibly non unique text naming the object.
        :param diag_objs: An ordered list of :class:`zepben.model.DiagramObject`'s.
        """
        self.r = r
        self.x = x
        self.r0 = r0
        self.x0 = x0
        self.bch = bch
        self.b0ch = b0ch
        super().__init__(mrid, name, diag_objs)

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
                                          bch=pb_plsi.bch, b0ch=pb_plsi.b0ch, name=pb_plsi.name, diag_objs=diag_objects)

    def to_pb(self):
        args = self._pb_args()
        return PBPerLengthSequenceImpedance(**args)
