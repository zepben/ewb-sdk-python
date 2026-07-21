#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["ConnectivityNode"]

from typing import Generator, List, TYPE_CHECKING
from dataclasses import field

from typing_extensions import deprecated

from zepben.ewb.dataclass_descriptors.mrid_list import MridCollection, LazyMridList
from zepben.ewb.model.cim.iec61970.base.core.identified_object import IdentifiedObject
from zepben.ewb.util import get_by_mrid, ngen
from zepben.ewb.dataclass_descriptors.dataclass_base import zb_dataclass

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61970.base.core.terminal import Terminal


# TODO: Python 3.11+ has @dataclass(weakref_slot=True) that replaces this hack
class WeakrefSlot:
    __slots__ = ("__weakref__",)


@zb_dataclass
class ConnectivityNode(IdentifiedObject, WeakrefSlot):
    """
    Connectivity nodes are points where terminals of AC conducting equipment are connected together with zero impedance.
    """
    _terminals: List[Terminal] = field(default_factory=list)

    terminals: MridCollection[Terminal] = LazyMridList(
        _terminals,
        "A Terminal"
    )
    """The `Terminal`s attached to this `ConnectivityNode`"""

    def __iter__(self):
        return iter(self._terminals)


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

    # region deprecated list boilerplate

    # region terminals boilerplate

    @deprecated("Use len(terminals) instead.")
    def num_terminals(self) -> int:
        return len(self.terminals)

    @deprecated("Use terminals.get_by_mrid(mrid) instead.")
    def get_terminal(self, mrid: str) -> Terminal:
        return self.terminals.get_by_mrid(mrid)

    @deprecated("Use terminals.append(terminal) instead.")
    def add_terminal(self, terminal: Terminal) -> ConnectivityNode:
        self.terminals.append(terminal)
        return self

    @deprecated("Use terminals.remove(terminal) instead.")
    def remove_terminal(self, terminal: Terminal) -> ConnectivityNode:
        self.terminals.remove(terminal)
        return self

    @deprecated("Use terminals.clear() instead.")
    def clear_terminals(self) -> ConnectivityNode:
        self.terminals.clear()
        return self

    # endregion

    # endregion