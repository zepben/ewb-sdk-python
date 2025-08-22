#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["ConnectivityNode"]

from dataclasses import dataclass
from typing import List, TYPE_CHECKING, Optional

from zepben.ewb.collections.terminal_list import TerminalList
from zepben.ewb.model.cim.iec61970.base.core.identified_object import IdentifiedObject

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61970.base.core.terminal import Terminal


@dataclass(slots=False)
class ConnectivityNode(IdentifiedObject):
    """
    Connectivity nodes are points where terminals of AC conducting equipment are connected together with zero impedance.
    """
    # noinspection PyDunderSlots
    # __slots__ = ["terminals", "__weakref__"]
    # __weakref__
    terminals: Optional[List[Terminal]] = None

    def __post_init__(self):
        self.terminals : TerminalList = TerminalList(self.terminals)

    def __iter__(self):
        return iter(self.terminals)

    def num_terminals(self):
        """
        Get the number of `Terminal`s for this `ConnectivityNode`.
        """
        return len(self.terminals)

    def get_terminal(self, mrid: str) -> Terminal:
        """
        Get the `Terminal` for this `ConnectivityNode` identified by `mrid`

        `mrid` The mRID of the required `Terminal`
        Returns The `Terminal` with the specified `mrid` if it exists
        Raises `KeyError` if `mrid` wasn't present.
        """
        return self.terminals.get_by_mrid(mrid)

    def add_terminal(self, terminal: Terminal) -> ConnectivityNode:
        """
        Associate a `terminal.Terminal` with this `ConnectivityNode`

        `terminal` The `Terminal` to add. Will only add to this object if it is not already associated.
        Returns A reference to this `ConnectivityNode` to allow fluent use.
        Raises `ValueError` if another `Terminal` with the same `mrid` already exists for this `ConnectivityNode`.
        """
        if self._validate_reference(terminal, self.get_terminal, "A Terminal"):
            return self

        self.terminals.add(terminal)
        return self

    def remove_terminal(self, terminal: Terminal) -> ConnectivityNode:
        """
        Disassociate `terminal` from this `ConnectivityNode`.

        `terminal` The `Terminal` to disassociate from this `ConnectivityNode`.
        Returns A reference to this `ConnectivityNode` to allow fluent use.
        Raises `ValueError` if `terminal` was not associated with this `ConnectivityNode`.
        """
        self.terminals.remove(terminal)
        return self

    def clear_terminals(self) -> ConnectivityNode:
        """
        Clear all terminals.
        Returns A reference to this `ConnectivityNode` to allow fluent use.
        """
        self.terminals.clear()
        return self

    def is_switched(self):
        return self.get_switch() is not None

    def get_switch(self):
        for term in self.terminals:
            try:
                # All switches should implement is_open
                _ = term.conducting_equipment.is_open()
                return term.conducting_equipment
            except AttributeError:
                pass
        return None
