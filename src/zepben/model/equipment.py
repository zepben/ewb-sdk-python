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
from zepben.model.diagram_layout import DiagramObjectPoints
from zepben.model.common import PositionPoints
from typing import Set, List


class NoEquipmentException(Exception):
    pass


class ConductingEquipment(IdentifiedObject):
    def __init__(self, mrid: str, in_service: bool, nom_volts: float, name: str, description: str, terminals: Set,
                 diag_point: DiagramObjectPoints, pos_points: List[PositionPoints]):
        self.in_service = in_service
        self.pos_points = pos_points if pos_points is not None else []
        self.nominal_voltage = nom_volts
        if terminals is None:
            self.terminals = set()
        else:
            self.terminals = terminals

        # We set a reference for each terminal back to its equipment to make iteration over a network easier
        for term in self.terminals:
            term.equipment = self
        super().__init__(mrid, name, diag_point, description)

    def __str__(self):
        return f"{super().__str__()} in_serv: {self.in_service}, lnglat: {self.pos_points} terms: {self.terminals}"

    def __repr__(self):
        return f"{super().__repr__()} in_serv: {self.in_service}, lnglat: {self.pos_points} terms: {self.terminals}"

    def connected(self):
        return self.in_service

    def add_terminal(self, terminal):
        self.terminals.add(terminal)

    def get_diag_point(self):
        return self.diagram_points

    def pos_point(self, sequence_number):
        for point in self.pos_points:
            if point.sequence_number == sequence_number:
                return point
        return None

    def has_points(self):
        return len(self.pos_points) > 0

    def get_terminal_for_node(self, node):
        for t in self.terminals:
            if t.connectivity_node.mrid == node.mrid:
                return t
        raise NoEquipmentException(f"Equipment {self.mrid} is not connected to node {node.mrid}")

    def get_cons(self):
        return [term.connectivity_node for term in self.terminals]

