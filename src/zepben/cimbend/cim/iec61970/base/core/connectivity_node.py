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

from dataclasses import dataclass, field, InitVar
from typing import Generator, List

from zepben.cimbend.cim.iec61970.base.core.identified_object import IdentifiedObject
from zepben.cimbend.cim.iec61970.base.core.terminal import Terminal
from zepben.cimbend.util import get_by_mrid, contains_mrid, require

__all__ = ["ConnectivityNode"]


@dataclass
class ConnectivityNode(IdentifiedObject):
    """
    Connectivity nodes are points where terminals of AC conducting equipment are connected together with zero impedance.
    Attributes -
        _terminals : The :class:`terminal.Terminal`s attached to this ``ConnectivityNode``
    """
    terminals_: InitVar[List[Terminal]] = field(default=list())
    _terminals: List[Terminal] = field(init=False, default_factory=list)

    def __post_init__(self, terminals_: List[Terminal]):
        super().__post_init__()
        for term in terminals_:
            self.add_terminal(term)

    def __iter__(self):
        return iter(self._terminals)

    @property
    def num_terminals(self):
        """
        Get the number of :class:`zepben.cimbend.iec61970.base.core.terminal.Terminal`s for this ``ConnectivityNode``.
        """
        return len(self._terminals)

    def get_terminal_by_mrid(self, mrid: str) -> Terminal:
        """
        Get the ``Terminal`` for this ``ConnectivityNode`` identified by ``mrid``

        :param mrid: the mRID of the required :class:`zepben.cimbend.iec61970.base.core.terminal.Terminal`
        :return: The :class:`zepben.cimbend.iec61970.base.core.terminal.Terminal` with the specified
        ``mrid`` if it exists
        :raises: KeyError if mrid wasn't present.
        """
        return get_by_mrid(self._terminals, mrid)

    @property
    def terminals(self) -> Generator[Terminal, None, None]:
        """
        :return: Generator over the terminals of this ``ConnectivityNode``.
        """
        for term in self._terminals:
            yield term

    def add_terminal(self, terminal: Terminal) -> ConnectivityNode:
        """
        Add a :class:`terminal.Terminal` to this ``ConnectivityNode``
        :param terminal: The ``Terminal`` to add
        :return: This ``ConnectivityNode`` for fluent use.
        """
        require(not contains_mrid(self._terminals, terminal.mrid),
                lambda: f"A Terminal with mRID {terminal.mrid} already exists in {str(self)}.")
        self._terminals.append(terminal)
        return self

    def remove_terminal(self, terminal: Terminal) -> ConnectivityNode:
        """
        :param terminal: the :class:`zepben.cimbend.iec61970.base.core.terminal.Terminal` to
        disassociate from this ``ConnectivityNode``.
        :raises: ValueError if ``terminal`` was not associated with this ``ConnectivityNode``.
        :return: A reference to this ``ConnectivityNode`` to allow fluent use.
        """
        self._terminals.remove(terminal)
        return self

    def clear_terminals(self) -> ConnectivityNode:
        """
        Clear all terminals.
        :return: A reference to this ``ConnectivityNode`` to allow fluent use.
        """
        self._terminals.clear()
        return self

    def is_switched(self):
        if self.get_switch() is not None:
            return True

    def get_switch(self):
        for term in self._terminals:
            try:
                # All switches should implement is_open
                _ = term.conducting_equipment.is_open()
                return term.conducting_equipment
            except AttributeError:
                pass
        return None

