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
    def from_pb(bv_pb: PBBaseVoltage, **kwargs):
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
