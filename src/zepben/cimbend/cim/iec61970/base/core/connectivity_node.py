#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from typing import Generator, List

from dataclassy import dataclass
from zepben.cimbend.cim.iec61970.base.core.identified_object import IdentifiedObject
from zepben.cimbend.util import get_by_mrid

__all__ = ["ConnectivityNode"]


@dataclass(slots=False)
class ConnectivityNode(IdentifiedObject):
    """
    Connectivity nodes are points where terminals of AC conducting equipment are connected together with zero impedance.
    """
    __slots__ = ["_terminals", "__weakref__"]
    _terminals: List[Terminal] = []

    def __init__(self, terminals: List[Terminal] = None):
        super().__init__()
        if terminals:
            for term in terminals:
                self.add_terminal(term)

    def __iter__(self):
        return iter(self._terminals)

    def num_terminals(self):
        """
        Get the number of `zepben.cimbend.cim.iec61970.base.core.terminal.Terminal`s for this `ConnectivityNode`.
        """
        return len(self._terminals)

    @property
    def terminals(self) -> Generator[Terminal, None, None]:
        """
        The `zepben.cimbend.cim.iec61970.base.core.terminal.Terminal`s attached to this `ConnectivityNode`
        """
        for term in self._terminals:
            yield term

    def get_terminal_by_mrid(self, mrid: str) -> Terminal:
        """
        Get the `zepben.cimbend.iec61970.base.core.terminal.Terminal` for this `ConnectivityNode` identified by `mrid`

        `mrid` The mRID of the required `zepben.cimbend.cim.iec61970.base.core.terminal.Terminal`
        Returns The `zepben.cimbend.cim.iec61970.base.core.terminal.Terminal` with the specified `mrid` if it exists
        Raises `KeyError` if `mrid` wasn't present.
        """
        return get_by_mrid(self._terminals, mrid)

    def add_terminal(self, terminal: Terminal) -> ConnectivityNode:
        """
        Associate a `terminal.Terminal` with this `ConnectivityNode`

        `terminal` The `zepben.cimbend.iec61970.base.core.terminal.Terminal` to add. Will only add to this object if it is not already associated.
        Returns A reference to this `ConnectivityNode` to allow fluent use.
        Raises `ValueError` if another `Terminal` with the same `mrid` already exists for this `ConnectivityNode`.
        """
        if self._validate_reference(terminal, self.get_terminal_by_mrid, "A Terminal"):
            return self

        self._terminals.append(terminal)
        return self

    def remove_terminal(self, terminal: Terminal) -> ConnectivityNode:
        """
        Disassociate `terminal` from this `ConnectivityNode`.

        `terminal` The `zepben.cimbend.cim.iec61970.base.core.terminal.Terminal` to disassociate from this `ConnectivityNode`.
        Returns A reference to this `ConnectivityNode` to allow fluent use.
        Raises `ValueError` if `terminal` was not associated with this `ConnectivityNode`.
        """
        self._terminals.remove(terminal)
        return self

    def clear_terminals(self) -> ConnectivityNode:
        """
        Clear all terminals.
        Returns A reference to this `ConnectivityNode` to allow fluent use.
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

