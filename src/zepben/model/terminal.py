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


from zepben.cim.iec61970 import Terminal as PBTerminal
from zepben.cim.iec61970 import PhaseCode
from zepben.model.identified_object import IdentifiedObject
from zepben.model.diagram_layout import DiagramObject
from zepben.model.exceptions import NoEquipmentException
from typing import List


class Terminal(IdentifiedObject):
    """
    A terminal is a connection point on a piece of ConductingEquipment. All ConductingEquipment must have terminals and
    all terminals must have an associated piece of ConductingEquipment.

    Note: If you are extending this class you must ensure you always safely access the linked equipment (i.e, check it is
    not None)
    """

    def __init__(self, mrid: str, phases: PhaseCode, connectivity_node, name: str = "",
                 diag_objs: List[DiagramObject] = None, equipment=None, upstream: bool = True, connected: bool = True):
        """

        :param mrid:
        :param phases:
        :param connectivity_node: The ConnectivityNode that this terminal is attached to.
        :param name:
        :param description:
        :param diag_objs:
        :param seq_number: The sequence number for this terminal. Used for mapping terminals to components/properties of
            the equipment.
        :param connected: Whether this terminal is connected (potentially energised)
        :param equipment: A reference to the equipment that owns this terminal. This can be set after instantiation as
                          to resolve chicken-and-egg issues between terminals and equipment (as both have references).
        :param upstream: True if this terminal is "closest" to its primary EnergySource. I.e, it is the first terminal
                         on a piece of equipment to receive power (specifically from the primary EnergySource).
        """
        self.phases = phases
        self.connected = connected
        self.__connectivity_node = connectivity_node
        self.__equipment = equipment
        self.__upstream = upstream
        super().__init__(mrid, name, diag_objs)

    @property
    def connectivity_node(self):
        return self.__connectivity_node

    @connectivity_node.setter
    def connectivity_node(self, cn):
        self.__connectivity_node = cn

    @property
    def equipment(self):
        if self.__equipment is None:
            raise NoEquipmentException("Terminal was missing a reference to its connected piece of equipment, this should not happen.")
        return self.__equipment

    @equipment.setter
    def equipment(self, equip):
        self.__equipment = equip

    @property
    def upstream(self):
        return self.__upstream

    @upstream.setter
    def upstream(self, upstream):
        self.__upstream = upstream

    def get_diag_objs(self):
        return self.equipment.get_diag_objs()

    def get_pos_point(self):
        return self.equipment.pos_point(self.get_sequence_number())

    def get_sequence_number(self):
        return self.equipment.terminal_sequence_number(self)

    def get_switch(self):
        """
        Get any associated switch for this Terminal
        :return: Switch if present in this terminals ConnectivityNode, else None
        """
        return self.connectivity_node.get_switch()

    def get_nominal_voltage(self):
        return self.equipment.get_nominal_voltage(self)

    def to_pb(self):
        args = self._pb_args()
        args['connectivityNodeMRID'] = self.connectivity_node.mrid
        return PBTerminal(**args)

    def __str__(self):
        return f"{super().__repr__()}, phase: {self.phases}, connectivityNode: {self.connectivity_node.mrid} upstream: {self.upstream}"
