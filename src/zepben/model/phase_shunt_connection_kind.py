from enum import Enum
from zepben.cim.iec61970.base.wires.PhaseShuntConnectionKind_pb2 import PhaseShuntConnectionKind as PBPhaseShuntConnectionKind

class PhaseShuntConnectionKind(Enum):

    # Delta Connection
    D = 0

    # Wye connection
    Y = 1

    # Wye, with neutral brought out for grounding.
    Yn = 2

    # Independent winding, for single-phase connections.
    I = 3

    # Ground connection; use when explicit connection to ground needs to be expressed in combination with the phase
    # code, such as for electrical wire/cable or for meters.
    G = 4

    # Unrecognised
    UNRECOGNIZED = 5

    def to_pb(self):
        return PBPhaseShuntConnectionKind.Value(self.name)

    @staticmethod
    def from_pb(pb_psck, **kwargs):
        return PhaseShuntConnectionKind[PBPhaseShuntConnectionKind.Name(pb_psck)]
