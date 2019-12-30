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


from zepben.model.exceptions import CoreException
from zepben.model.cores import CorePath


class ConnectivityResult(object):
    """
    The connectivity between two connected terminals
    Attributes:
        from_terminal : Originating :class:`zepben.model.Terminal`
        to_terminal : Destination :class:`zepben.model.Terminal`
    """
    def __init__(self, from_terminal, to_terminal):
        """
        Create a ConnectivityResult.
        :param from_terminal: The originating :class:`zepben.model.Terminal`
        :param to_terminal: The destination :class:`zepben.model.Terminal`
        """
        self.from_terminal = from_terminal
        self.to_terminal = to_terminal
        self.from_cores = []
        self.to_cores = []
        self._core_paths = []
        self._is_sorted = False

    def __eq__(self, other):
        if self is other:
            return True
        return self.from_terminal == other.from_terminal \
               and self.to_terminal == other.to_terminal \
               and self.sorted_core_paths() == other.sorted_core_paths()

    def __ne__(self, other):
        if self is other:
            return False
        return self.from_terminal != other.from_terminal \
               or self.to_terminal != other.to_terminal \
               or self.sorted_core_paths() != other.sorted_core_paths()

    def __str__(self):
        return (f"ConnectivityResult(from_terminal={self.from_equip().mrid}-t{self.from_terminal.sequence_number()}" 
                f", to_terminal={self.to_equip().mrid}-t{self.to_terminal.sequence_number()}, "
                f"core_paths={self.sorted_core_paths()})"
                )

    def from_equip(self):
        return self.from_terminal.equipment

    def to_equip(self):
        return self.to_terminal.equipment

    @property
    def core_paths(self):
        if not self._core_paths:
            self._populate_core_paths()
        return self._core_paths

    def add_core_path(self, from_core: int, to_core: int):
        if self._core_paths:
            raise CoreException("You cannot add cores after the result has been used")

        self.from_cores.append(from_core)
        self.to_cores.append(to_core)
        return self

    def sorted_core_paths(self):
        if not self._is_sorted:
            self.core_paths.sort()
            self._is_sorted = True
        return self.core_paths

    def _populate_core_paths(self):
        for fc, tc in zip(self.from_cores, self.to_cores):
            self._core_paths.append(CorePath(fc, tc))

