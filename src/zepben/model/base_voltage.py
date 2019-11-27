from zepben.model.identified_object import IdentifiedObject
from zepben.cim.iec61970.base.core.BaseVoltage_pb2 import BaseVoltage as PBBaseVoltage
from zepben.cim.iec61970.base.domain.Voltage_pb2 import Voltage as PBVoltage


class BaseVoltage(IdentifiedObject):
    """
    Defines a system base voltage which is referenced.

    Attributes:
        nominal_voltage: The power system resource's base voltage.
    """
    def __init__(self, mrid: str, nom_volt: int, name: str = ""):
        """
        TODO: nom_volt must always be int32 - need to put in bounds test
        :param mrid: mRID of this BaseVoltage
        :param nom_volt: The nominal voltage in Volts.
        :param name: Name of this BaseVoltage
        """
        self.nominal_voltage = nom_volt
        super().__init__(mrid, name)

    @staticmethod
    def from_pb(bv_pb: PBBaseVoltage):
        """
        :param bv_pb: A :class:`zepben.cim.iec61970.core.BaseVoltage`
        :return: A BaseVoltage
        """
        bv = BaseVoltage(bv_pb.mRID, bv_pb.nominalVoltage.value, bv_pb.name)
        return bv

    def _pb_args(self, exclude=None):
        args = super()._pb_args()
        args['nominalVoltage'] = PBVoltage(value=self.nominal_voltage)
        return args

    def to_pb(self):
        args = self._pb_args()
        return PBBaseVoltage(**args)


# Default BaseVoltage used when unknown.
UNKNOWN = BaseVoltage("", 0)
