#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["ConnectivityNode"]

from typing import Generator, List, TYPE_CHECKING


from zepben.ewb.dataslot import custom_len, MRIDListRouter, MRIDDictRouter, boilermaker, TypeRestrictedDescriptor, WeakrefDescriptor, dataslot, BackedDescriptor, ListAccessor, ValidatedDescriptor, MRIDListAccessor, custom_get, custom_remove, override_boilerplate, ListActions, MRIDDictAccessor, BackingValue, custom_clear, custom_get_by_mrid, custom_add, NoResetDescriptor, ListRouter, validate
from typing_extensions import deprecated
from zepben.ewb.model.cim.iec61970.base.core.identified_object import IdentifiedObject
from zepben.ewb.util import get_by_mrid, ngen

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61970.base.core.terminal import Terminal


@dataslot(weakref=True)
@boilermaker
class ConnectivityNode(IdentifiedObject):
    """
    Connectivity nodes are points where terminals of AC conducting equipment are connected together with zero impedance.
    """
    # noinspection PyDunderSlots
    terminals: List[Terminal] | None = MRIDListAccessor()

    def _retype(self):
        self.terminals: MRIDListRouter = ...
    
    def __iter__(self):
        return iter(self.terminals)

    @deprecated("BOILERPLATE: Use len(terminals) instead")
    def num_terminals(self):
        return len(self.terminals)

    @deprecated("BOILERPLATE: Use terminals.get_by_mrid(mrid) instead")
    def get_terminal(self, mrid: str) -> Terminal:
        return self.terminals.get_by_mrid(mrid)

    @custom_add(terminals)
    def add_terminal(self, terminal: Terminal) -> ConnectivityNode:
        """
        Associate a `terminal.Terminal` with this `ConnectivityNode`

        `terminal` The `Terminal` to add. Will only add to this object if it is not already associated.
        Returns A reference to this `ConnectivityNode` to allow fluent use.
        Raises `ValueError` if another `Terminal` with the same `mrid` already exists for this `ConnectivityNode`.
        """
        if self._validate_reference(terminal, self.get_terminal, "A Terminal"):
            return self

        self.terminals.append_unchecked(terminal)
        return self

    @custom_remove(terminals)
    def remove_terminal(self, terminal: Terminal) -> ConnectivityNode:
        """
        Disassociate `terminal` from this `ConnectivityNode`.

        `terminal` The `Terminal` to disassociate from this `ConnectivityNode`.
        Returns A reference to this `ConnectivityNode` to allow fluent use.
        Raises `ValueError` if `terminal` was not associated with this `ConnectivityNode`.
        """
        self.terminals.raw.remove(terminal)
        return self

    @custom_clear(terminals)
    def clear_terminals(self) -> ConnectivityNode:
        """
        Clear all terminals.
        Returns A reference to this `ConnectivityNode` to allow fluent use.
        """
        self.terminals.raw.clear()
        return self

    def is_switched(self):
        return self.get_switch() is not None

    @custom_get(terminals)
    def get_switch(self):
        for term in self.terminals:
            try:
                # All switches should implement is_open
                _ = term.conducting_equipment.is_open()
                return term.conducting_equipment
            except AttributeError:
                pass
        return None
