from enum import Enum

from zepben.cim.iec61970.base.wires.WindingConnection_pb2 import WindingConnection as PBWindingConnection

class WindingConnection(Enum):

    # Default
    UNKNOWN_WINDING = 0

    # Delta
    D = 1

    # Wye
    Y = 2

    # ZigZag
    Z = 3

    # Wye, with neutral brought out for grounding
    Yn = 4

    # ZigZag, with neutral brought out for grounding
    Zn = 5

    # Autotransformer common winding
    A = 6

    # Independent winding, for single-phase connections
    I = 7

    def to_pb(self):
        return PBWindingConnection.Value(self.name)

    @staticmethod
    def from_pb(pb_wc, **kwargs):
        return WindingConnection[PBWindingConnection.Name(pb_wc)]
