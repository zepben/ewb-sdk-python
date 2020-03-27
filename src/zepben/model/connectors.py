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


from __future__ import annotations

from zepben.cim.iec61970.base.wires.Junction_pb2 import Junction as PBJunction
from zepben.model.terminal import Terminal
from zepben.model.base_voltage import UNKNOWN as BV_UNKNOWN
from zepben.model.common import Location
from zepben.model.diagram_layout import DiagramObject
from zepben.model.conducting_equipment import ConductingEquipment
from typing import List
__all__ = ["Connector", "Junction"]


class Connector(ConductingEquipment):
    """
    A conductor, or group of conductors, with negligible impedance, that serve to connect other conducting equipment
    within a single substation and are modelled with a single logical terminal.
    """
    def __init__(self, mrid: str, base_voltage: BaseVoltage = BV_UNKNOWN, terminals: List[Terminal] = None,
                 in_service: bool = True, normally_in_service: bool = True, name: str = "",
                 diag_objs: List[DiagramObject] = None, location: Location = None):
        super().__init__(mrid=mrid, base_voltage=base_voltage, terminals=terminals, in_service=in_service,
                         normally_in_service=normally_in_service, name=name, diag_objs=diag_objs, location=location)


class Junction(Connector):
    """
    A point where one or more conducting equipments are connected with zero resistance.
    """
    def __init__(self, mrid: str, base_voltage: BaseVoltage = BV_UNKNOWN, terminals: List[Terminal] = None,
                 in_service: bool = True, normally_in_service: bool = True, name: str = "",
                 diag_objs: List[DiagramObject] = None, location: Location = None):
        super().__init__(mrid=mrid, base_voltage=base_voltage, terminals=terminals, in_service=in_service,
                         normally_in_service=normally_in_service, name=name, diag_objs=diag_objs, location=location)

    @staticmethod
    def from_pb(pb_j, network, **kwargs):
        """
        Convert a protobuf Junction to a :class:`zepben.model.connectors.Junction`
        :param pb_j: :class:`zepben.cim.iec61970.base.wires.Junction`
        :param network: Network to extract `pb_j.baseVoltageMRID`
        :raises: NoBaseVoltageException when pb_j.baseVoltageMRID isn't found in network
        :return: A :class:`zepben.model.connectors.Junction`
        """
        terms = Terminal.from_pbs(pb_j.terminals, network)
        location = Location.from_pb(pb_j.location)
        diag_objs = DiagramObject.from_pbs(pb_j.diagramObjects)
        base_voltage = network.get_base_voltage(pb_j.baseVoltageMRID) if pb_j.baseVoltageMRID else None
        return Junction(mrid=pb_j.mRID,
                        name=pb_j.name,
                        base_voltage=base_voltage,
                        in_service=pb_j.inService,
                        normally_in_service=pb_j.normallyInService,
                        terminals=terms,
                        diag_objs=diag_objs,
                        location=location)

    def to_pb(self):
        return PBJunction(**self._pb_args())

