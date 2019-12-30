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
from zepben.model.terminal import Terminal
from zepben.model.equipment import ConductingEquipment
from zepben.model.diagram_layout import DiagramObject
from zepben.model.common import Location
from zepben.model.base_voltage import BaseVoltage, UNKNOWN as BV_UNKNOWN
from zepben.model.per_length_sequence_impedance import PerLengthSequenceImpedance
from zepben.model.asset_info import WireInfo
from zepben.model.exceptions import NoPerLengthSeqImpException, NoBaseVoltageException, NoAssetInfoException
from zepben.cim.iec61970 import AcLineSegment as PBAcLineSegment
from typing import List


class ACLineSegment(ConductingEquipment):
    """
    Attributes:
        per_length_sequence_impedance : A :class:`zepben.model.PerLengthSequenceImpedance` that describes this ACLineSegment
        length : Segment length for calculating line section capabilities.
        wire_info : An instance of a subclass of :class:`zepben.model.WireInfo` that describes this ACLineSegment.
                    Can be OverheadWireInfo or CableInfo (underground cable)
    """

    def __init__(self, mrid: str, plsi: PerLengthSequenceImpedance = None, length: float = 0.0,
                 wire_info: WireInfo = None, base_voltage: BaseVoltage = BV_UNKNOWN, in_service: bool = True, name: str = "",
                 terminals: List = None, diag_objs: List[DiagramObject] = None, location: Location = None):
        """
        Create an ACLineSegment
        :param mrid: mRID for this object
        :param plsi: A :class:`zepben.model.PerLengthSequenceImpedance` that describes this ACLineSegment.
        :param length: Segment length for calculating line section capabilities.
        :param wire_info: An instance of a subclass of :class:`zepben.model.WireInfo` that describes this ACLineSegment.
                          Can be OverheadWireInfo or CableInfo (underground cable)
        :param base_voltage: A :class:`zepben.model.BaseVoltage`.
        :param in_service: If True, the equipment is in service.
        :param name: Any free human readable and possibly non unique text naming the object.
        :param terminals: An ordered list of :class:`zepben.model.Terminal`'s. The order is important and the index of
                          each Terminal should reflect each Terminal's `sequenceNumber`.
        :param diag_objs: An ordered list of :class:`zepben.model.DiagramObject`'s.
        :param location: :class:`zepben.model.Location` of this resource.
        """
        self.per_length_sequence_impedance = plsi
        self.length = length
        self.wire_info = wire_info
        super().__init__(mrid=mrid, in_service=in_service, base_voltage=base_voltage, name=name, terminals=terminals,
                         diag_objs=diag_objs, location=location)

    def __str__(self):
        return f"{super().__str__()} r: {self.r}, x: {self.x}"

    def __repr__(self):
        return f"{super().__repr__()} r: {self.r}, x: {self.x}"

    @property
    def rated_current(self):
        return self.wire_info.rated_current

    @property
    def r(self):
        return self.per_length_sequence_impedance.r

    @property
    def x(self):
        return self.per_length_sequence_impedance.x

    @property
    def r0(self):
        return self.per_length_sequence_impedance.r0

    @property
    def x0(self):
        return self.per_length_sequence_impedance.x0

    @property
    def bch(self):
        return self.per_length_sequence_impedance.bch

    @property
    def b0ch(self):
        return self.per_length_sequence_impedance.b0ch

    def _pb_args(self, exclude=None):
        args = super()._pb_args()
        args['perLengthSequenceImpedanceMRID'] = self.per_length_sequence_impedance.mrid
        args['assetInfoMRID'] = self.wire_info.mrid
        del args['perLengthSequenceImpedance']
        del args['wireInfo']
        return args

    def to_pb(self):
        args = self._pb_args()
        return PBAcLineSegment(**args)

    @staticmethod
    def from_pb(pb_acls, network, **kwargs):
        """
        Convert a protobuf AcLineSegment to a :class:`zepben.model.ACLineSegment`
        :param pb_acls: :class:`zepben.cim.iec61970.base.wires.AcLineSegment`
        :param network: EquipmentContainer to extract BaseVoltage, PerLengthSequenceImpedance,
                        and WireInfo (assetInfoMRID)
        :raises: NoBaseVoltageException when pb_acls.baseVoltageMRID isn't found in network
        :raises: NoPerLengthSequenceImpedance when pb_acls.perLengthSequenceImpedanceMRID isn't found in the network.
        :raises: NoAssetInfoException when pb_acls.assetInfoMRID isn't found in the network
        :return: A :class:`zepben.model.ACLineSegment`
        """
        terms = Terminal.from_pbs(pb_acls.terminals, network)
        location = Location.from_pb(pb_acls.location)
        diag_objs = DiagramObject.from_pbs(pb_acls.diagramObjects)
        base_voltage = network.get_base_voltage(pb_acls.baseVoltageMRID) if pb_acls.baseVoltageMRID else None
        plsi = network.get_plsi(pb_acls.perLengthSequenceImpedanceMRID) if pb_acls.perLengthSequenceImpedanceMRID else None
        wire_info = network.get_asset_info(pb_acls.assetInfoMRID) if pb_acls.assetInfoMRID else None

        return ACLineSegment(mrid=pb_acls.mRID,
                             name=pb_acls.name,
                             plsi=plsi,
                             length=pb_acls.length,
                             base_voltage=base_voltage,
                             wire_info=wire_info,
                             in_service=pb_acls.inService,
                             terminals=terms,
                             diag_objs=diag_objs,
                             location=location)
