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
from zepben.model.terminal import Terminal
from typing import Set


class ConnectivityNode(IdentifiedObject):
    def __init__(self, mrid: str, terminals: Set[Terminal] = None, name: str = None, description: str = None,
                 diag_point: DiagramObjectPoints = None):
        if terminals is None:
            self.terminals = set()
        else:
            self.terminals = terminals
        super().__init__(mrid, name, diagram_points=diag_point, description=description)

    def __iter__(self):
        return iter(self.terminals)

    #def __next__(self):
    #    for term in self.terminals:
    #        yield term
    #    raise StopIteration()

    def is_switched(self):
        if self.get_switch() is not None:
            return True

    def get_switch(self):
        for term in self.terminals:
            try:
                # All switches should implement is_open
                _ = term.equipment.is_open()
                return term.equipment
            except AttributeError:
                pass
        return None

    def add_terminal(self, terminal):
        # Don't add multiple terminals to the same node
        if terminal not in self.terminals:
            self.terminals.add(terminal)

    def __str__(self):
        return f"{super().__str__()} terminals: {self.terminals}"

    def __repr__(self):
        return f"{super().__repr__()} terminals: {self.terminals}"


