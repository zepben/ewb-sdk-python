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
from zepben.model.diagram_layout import DiagramObject
from zepben.model.common import Location
from zepben.model.base_voltage import BaseVoltage
from typing import List





class ConductingEquipment(IdentifiedObject):
    def __init__(self, mrid: str, in_service: bool, base_voltage: BaseVoltage, name: str, terminals: List,
                 diag_objs: List[DiagramObject], location: Location):
        self.in_service = in_service
        self.location = location
        self.base_voltage = base_voltage
        if terminals is None:
            self.terminals = list()
        else:
            self.terminals = terminals

        # We set a reference for each terminal back to its equipment to make iteration over a network easier
        for term in self.terminals:
            term.equipment = self
        super().__init__(mrid, name, diag_objs)

    def __str__(self):
        return f"{super().__str__()} in_serv: {self.in_service}, lnglat: {self.location} terms: {self.terminals}"

    def __repr__(self):
        return f"{super().__repr__()} in_serv: {self.in_service}, lnglat: {self.location} terms: {self.terminals}"

    @property
    def nominal_voltage(self):
        return self.base_voltage.nominal_voltage

    def connected(self):
        return self.in_service

    def add_terminal(self, terminal):
        self.terminals.add(terminal)

    def get_diag_objs(self):
        return self.diagram_objects

    def pos_point(self, sequence_number):
        try:
            return self.location.position_points[sequence_number]
        except IndexError:
            return None

    def has_points(self):
        return len(self.location.position_points) > 0

    def terminal_sequence_number(self, terminal):
        """
        Sequence number for terminals is stored as the index of the terminal in `self.terminals`
        :param terminal: The terminal to retrieve the sequence number for
        :return:
        """
        for i, term in enumerate(self.terminals):
            if term is terminal:
                return i
        raise NoEquipmentException("Terminal does not exist in this equipment")

    def get_terminal_for_node(self, node):
        for t in self.terminals:
            if t.connectivity_node.mrid == node.mrid:
                return t
        raise NoEquipmentException(f"Equipment {self.mrid} is not connected to node {node.mrid}")

    def get_terminal(self, seq_num):
        try:
            return self.terminals[seq_num]
        except KeyError | IndexError:
            raise NoEquipmentException(f"Equipment {self.mrid} does not have a terminal {seq_num}")

    def get_nominal_voltage(self, terminal=None):
        """
        Get the nominal voltage for this piece of equipment.
        In cases where this equipment has multiple nominal voltages (i.e, transformers),
        this method should be overridden so providing a terminal will provide the voltage corresponding to that terminal

        :param terminal: Terminal to fetch voltage for
        """
        return self.nominal_voltage

    def get_cons(self):
        return [term.connectivity_node for term in self.terminals]

    def _pb_args(self, exclude=None):
        args = super()._pb_args()
        if self.base_voltage is not None:
            args['baseVoltageMRID'] = self.base_voltage.mrid
            del args['baseVoltage']
        return args
