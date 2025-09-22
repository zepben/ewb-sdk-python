#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["ConnectivityNode"]

from typing import List, TYPE_CHECKING

from typing_extensions import deprecated

from zepben.ewb import Switch
from zepben.ewb.collections.autoslot import dataslot
from zepben.ewb.collections.boilerplate import MRIDListAccessor, MRIDListRouter
from zepben.ewb.model.cim.iec61970.base.core.identified_object import IdentifiedObject

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61970.base.core.terminal import Terminal


@dataslot
class ConnectivityNode(IdentifiedObject):
    """
    Connectivity nodes are points where terminals of AC conducting equipment are connected together with zero impedance.
    """
    terminals: List[Terminal] | None = MRIDListAccessor()

    def _retype(self):
        self.terminals: MRIDListRouter = ...

    def __iter__(self):
        return iter(self.terminals)

    @deprecated("Use len(terminals) instead.")
    def num_terminals(self) -> int: ...

    @deprecated("Use terminals[mrid] instead.")
    def get_terminal(self, mrid: str) -> Terminal: ...

    @deprecated("Use terminals.append(terminal) instead.")
    def add_terminal(self, terminal: Terminal) -> ConnectivityNode: ...

    @deprecated("Use len(terminals) instead.")
    def remove_terminal(self, terminal: Terminal) -> ConnectivityNode: ...

    @deprecated("Use terminals.clear() instead.")
    def clear_terminals(self) -> ConnectivityNode: ...


    def is_switched(self):
        return self.get_switch() is not None

    def get_switch(self):
        for term in self.terminals:
            if isinstance(ce := term.conducting_equipment, Switch):
                return ce
        return None


if __name__ == '__main__':
    cn = ConnectivityNode()