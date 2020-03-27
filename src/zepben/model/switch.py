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


from zepben.model.conducting_equipment import ConductingEquipment
from zepben.model.diagram_layout import DiagramObject
from zepben.model.exceptions import PhaseException
from zepben.model.common import Location
from zepben.model.terminal import Terminal
from zepben.model.base_voltage import BaseVoltage, UNKNOWN as BV_UNKNOWN
from zepben.cim.iec61970 import Breaker as PBBreaker
from typing import List
import copy
from abc import ABCMeta


class Switch(ConductingEquipment, metaclass=ABCMeta):
    """
    A generic device designed to close, or open, or both, one or more electric circuits.
    All switches are two terminal devices including grounding switches.

    Unganged switches are supported as a list of booleans, each bool corresponding to a single phase
    Attributes:
         open : True if the switch is considered open and not allowing current to flow.
                Can be a list of booleans to represent an unganged switch.
    """
    def __init__(self, mrid: str, open_: List[bool] = None, normal_open: List[bool] = None,
                 base_voltage: BaseVoltage = BV_UNKNOWN, in_service: bool = True, name: str = "",
                 terminals: List = None, diag_objs: List[DiagramObject] = None, location: Location = None):
        """
        Create a Switch. This is an abstract class and typically should not be used directly.
        :param mrid: mRID for this object
        :param open_: True for each core on the switch if it is open, False otherwise. Defaults to [False] * self.num_cores
        :param normal_open: True for each core on the the switch if it is normally open (nominal state of switch).
                            Will default to the same as open_ if not set - i.e, we assume all switches are in their
                            normal state.
        :param base_voltage: A :class:`zepben.model.BaseVoltage`.
        :param in_service: If True, the equipment is in service.
        :param name: Any free human readable and possibly non unique text naming the object.
        :param terminals: An ordered list of :class:`zepben.model.Terminal`'s. The order is important and the index of
                          each Terminal should reflect each Terminal's `sequenceNumber`.
        :param diag_objs: An ordered list of :class:`zepben.model.DiagramObject`'s.
        :param location: :class:`zepben.model.Location` of this resource.
        """
        super().__init__(mrid=mrid, in_service=in_service, base_voltage=base_voltage, name=name,
                         terminals=terminals, diag_objs=diag_objs, location=location)
        # TODO: verify that switch is correctly associated with terminal phases, and open/normal_open reflects
        #       each phase.
        self.open = open_ if open_ is not None else [False] * self.num_cores
        self.normal_open = normal_open if normal_open is not None else copy.deepcopy(self.open)

    def __len__(self):
        return len(self.open)

    def normally_open(self, core: int = None):
        """Switch is normally open only if it isn't normally in service OR at least one phase is open"""
        if not self.normally_in_service:
            return False

        if core is None:
            for core in self.normal_open:
                if not core:
                    return False
        try:
            return self.normal_open[core]
        except (IndexError, KeyError):
            raise PhaseException(f"Switch {self.mrid} is not connected to phase {core}")

    def is_open(self, core: int = None):
        """Switch is open only if it's not in service OR at least one phase is open"""
        if not self.in_service:
            return False

        if core is None:
            for core in self.open:
                if not core:
                    return False
        else:
            try:
                return self.open[core]
            except (IndexError, KeyError):
                raise PhaseException(f"Switch {self.mrid} is not connected to phase {core}")


class Breaker(Switch):
    """
    A mechanical switching device capable of making, carrying, and breaking currents under normal circuit conditions
    and also making, carrying for a specified time, and breaking currents under specified abnormal circuit conditions
    e.g. those of short circuit.

    Attributes:
        Same as :class:`Switch`
    """
    def __init__(self, mrid: str, open_: List[bool] = None, normal_open: List[bool] = None,
                 base_voltage: BaseVoltage = BV_UNKNOWN, in_service: bool = True, name: str = "", terminals: List = None,
                 diag_objs: List[DiagramObject] = None, location: Location = None):
        """
        Create a Breaker
        :param mrid: mRID for this object
        :param open_: True for each core on the switch if it is open
        :param normal_open: True for each core on the the switch if it is normally open (nominal state of switch).
                            Will default to the same as open_ if not set - i.e, we assume all switches are in their
                            normal state.
        :param base_voltage: A :class:`zepben.model.BaseVoltage`.
        :param in_service: If True, the equipment is in service.
        :param name: Any free human readable and possibly non unique text naming the object.
        :param terminals: An ordered list of :class:`zepben.model.Terminal`'s. The order is important and the index of
                          each Terminal should reflect each Terminal's `sequenceNumber`.
        :param diag_objs: An ordered list of :class:`zepben.model.DiagramObject`'s.
        :param location: :class:`zepben.model.Location` of this resource.
        """
        super().__init__(mrid=mrid, open_=open_, normal_open=normal_open, in_service=in_service,
                         base_voltage=base_voltage, name=name, terminals=terminals, diag_objs=diag_objs, location=location)

    def is_substation_breaker(self):
        return len(self.substations) > 0

    def to_pb(self):
        args = self._pb_args()
        return PBBreaker(**args)

    @staticmethod
    def from_pb(pb_br, network, **kwargs):
        """
        Convert a protobuf Breaker to a :class:`zepben.model.Breaker`
        :param pb_br: :class:`zepben.cim.iec61970.base.wires.Breaker`
        :param network: Network to extract BaseVoltage
        :raises: NoBaseVoltageException when pb_br.baseVoltageMRID isn't found in network
        :return: A :class:`zepben.model.Breaker`
        """
        terms = Terminal.from_pbs(pb_br.terminals, network)
        location = Location.from_pb(pb_br.location)
        diag_objs = DiagramObject.from_pbs(pb_br.diagramObjects)
        base_voltage = network.get_base_voltage(pb_br.baseVoltageMRID) if pb_br.baseVoltageMRID else None
        return Breaker(pb_br.mRID,
                       open_=pb_br.open,
                       base_voltage=base_voltage,
                       in_service=pb_br.inService,
                       name=pb_br.name,
                       terminals=terms,
                       diag_objs=diag_objs,
                       location=location)
