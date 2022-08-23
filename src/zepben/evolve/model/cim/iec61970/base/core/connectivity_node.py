#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from typing import Generator, List, TYPE_CHECKING

if TYPE_CHECKING:
    from zepben.evolve import Terminal

from dataclassy import dataclass

from zepben.evolve.model.cim.iec61970.base.core.identified_object import IdentifiedObject
from zepben.evolve.util import get_by_mrid, ngen

__all__ = ["ConnectivityNode"]


@dataclass(slots=False)
class ConnectivityNode(IdentifiedObject):
    """
    Connectivity nodes are points where terminals of AC conducting equipment are connected together with zero impedance.
    """
    # noinspection PyDunderSlots
    __slots__ = ["_terminals", "__weakref__"]
    _terminals: List[Terminal] = []

    def __init__(self, terminals: List[Terminal] = None, **kwargs):
        super(ConnectivityNode, self).__init__(**kwargs)
        if terminals:
            for term in terminals:
                self.add_terminal(term)

    def __iter__(self):
        return iter(self._terminals)

    def num_terminals(self):
        """
        Get the number of `Terminal`s for this `ConnectivityNode`.
        """
        return len(self._terminals)

    @property
    def terminals(self) -> Generator[Terminal, None, None]:
        """
        The `Terminal`s attached to this `ConnectivityNode`
        """
        return ngen(self._terminals)

    def get_terminal(self, mrid: str) -> Terminal:
        """
        Get the `Terminal` for this `ConnectivityNode` identified by `mrid`

        `mrid` The mRID of the required `Terminal`
        Returns The `Terminal` with the specified `mrid` if it exists
        Raises `KeyError` if `mrid` wasn't present.
        """
        return get_by_mrid(self._terminals, mrid)

    def add_terminal(self, terminal: Terminal) -> ConnectivityNode:
        """
        Associate a `terminal.Terminal` with this `ConnectivityNode`

        `terminal` The `Terminal` to add. Will only add to this object if it is not already associated.
        Returns A reference to this `ConnectivityNode` to allow fluent use.
        Raises `ValueError` if another `Terminal` with the same `mrid` already exists for this `ConnectivityNode`.
        """
        if self._validate_reference(terminal, self.get_terminal, "A Terminal"):
            return self

        self._terminals.append(terminal)
        return self

    def remove_terminal(self, terminal: Terminal) -> ConnectivityNode:
        """
        Disassociate `terminal` from this `ConnectivityNode`.

        `terminal` The `Terminal` to disassociate from this `ConnectivityNode`.
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
        return self.get_switch() is not None

    def get_switch(self):
        for term in self._terminals:
            try:
                # All switches should implement is_open
                _ = term.conducting_equipment.is_open()
                return term.conducting_equipment
            except AttributeError:
                pass
        return None
