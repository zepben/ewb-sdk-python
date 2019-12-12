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
from zepben.model.exceptions import NoEquipmentException, NoConnectivityNodeException
from typing import List
from enum import Enum


class Direction(Enum):
    NONE = 0
    IN = 1
    OUT = 2
    BOTH = 3


class Terminal(IdentifiedObject):
    """
    A terminal is a connection point on a piece of ConductingEquipment. All ConductingEquipment must have terminals and
    all terminals must have an associated piece of ConductingEquipment.

    Note: If you are extending this class you must ensure you always safely access the linked equipment (i.e, check it is
    not None)

    Attributes:
        - equipment : A reference back to the equipment this Terminal belongs to. This reference will typically
                      be added in :class:`zepben.model.ConductingEquipment::__init__()`.
        - phases : A :class:`zepben.cim.iec61970.PhaseCode` representing the normal network phasing condition of this
                   Terminal.
        - connected : The connected status is related to a bus-branch model and the topological node to terminal relation.
                      True implies the terminal is connected to the related topological node and false implies it is not.
                      In a bus-branch model, the connected status is used to tell if equipment is disconnected without having to change
                      the connectivity described by the topological node to terminal relation. A valid case is that conducting
                      equipment can be connected in one end and open in the other. In particular for an AC line segment,
                      where the reactive line charging can be significant, this is a relevant case.
    """

    def __init__(self, mrid: str, phases: PhaseCode, connectivity_node, name: str = "",
                 diag_objs: List[DiagramObject] = None, equipment=None, direction: Direction = Direction.NONE,
                 connected: bool = True):
        """
        Create a Terminal
        :param mrid: Master resource identifier for this Terminal.
        :param phases: A :class:`zepben.cim.iec61970.PhaseCode` representing the normal network phasing condition of this
                       Terminal.
        :param connectivity_node: The :class:`zepben.model.ConnectivityNode` that this terminal is attached to.
        :param name: Any free human readable and possibly non unique text naming the object.
        :param diag_objs: An ordered list of :class:`zepben.model.DiagramObject`'s.
        :param connected: Whether this terminal is connected (potentially energised). See description in class definition.
        :param equipment: A reference to the equipment that owns this terminal. This can be set after instantiation as
                          to resolve chicken-and-egg issues between terminals and equipment (as both have references).
        :param direction: (experimental) True if this terminal is "closest" to its primary EnergySource. I.e, it is the
                        first terminal on a piece of equipment to receive power (specifically from the primary EnergySource).
        """
        self.phases = phases
        self.connected = connected
        self.__connectivity_node = connectivity_node
        self.__equipment = equipment
        self.__direction = direction
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
    def direction(self):
        return self.__direction

    @direction.setter
    def direction(self, direction):
        self.__direction = direction

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

    @staticmethod
    def from_pb(pb_t, network):
        """
        Every terminal requires a connectivityNodeMRID to be specified.
        :param pb_t: A protobuf Terminal to convert to Terminal
        :param network: The EquipmentContainer that the terminal belongs to. Associated ConnectivityNode's will be
                        added to this network.
        :return: A zepben.model.Terminal
        :raises: NoConnectivityNodeException when connectivityNodeMRID is not set.
        """
        if not pb_t.connectivityNodeMRID:
            raise NoConnectivityNodeException(f"Terminal {pb_t.mRID} has no connectivity node declared.")
        conn_node = network.add_connectivitynode(pb_t.connectivityNodeMRID)
        term = Terminal(mrid=pb_t.mRID,
                        phases=pb_t.phases,
                        connectivity_node=conn_node,
                        name=pb_t.name,
                        connected=pb_t.connected,
                        diag_objs=DiagramObject.from_pbs(pb_t.diagramObjects))
        conn_node.add_terminal(term)
        return term

    def __str__(self):
        return f"{super().__repr__()}, phase: {self.phases}, connectivityNode: {self.connectivity_node.mrid} direction: {self.direction}"

