#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["Circuit"]

from typing import Optional, List, TYPE_CHECKING
from dataclasses import field
from typing_extensions import deprecated

from zepben.ewb.model.cim.iec61970.base.wires.line import Line
from zepben.ewb.boilerplate.dataclass_base import zb_dataclass
from zepben.ewb.boilerplate.collections.mrid_list import LazyMridList
from zepben.ewb.boilerplate.collections.mrid_collection import MridCollection

if TYPE_CHECKING:
    from zepben.ewb.model.cim.extensions.iec61970.base.feeder.loop import Loop
    from zepben.ewb.model.cim.iec61970.base.core.substation import Substation
    from zepben.ewb.model.cim.iec61970.base.core.terminal import Terminal


@zb_dataclass
class Circuit(Line):
    """Missing description"""

    loop: Optional[Loop] = None
    _end_terminals: Optional[List[Terminal]] = field(default=None)
    _end_substations: Optional[List[Substation]] = field(default=None)

    end_terminals: MridCollection[Terminal] = LazyMridList(
        _end_terminals,
        "An Terminal",
    )

    end_substations: MridCollection[Substation] = LazyMridList(
        _end_substations,
        "An Substation",
    )


    # region deprecated list boilerplate
    # region end_terminals boilerplate

    @deprecated("Use len(obj.end_terminals) instead.")
    def num_end_terminals(self):
        return len(self.end_terminals)

    @deprecated("Use obj.end_terminals.get_by_mrid(mrid) instead.")
    def get_end_terminal(self, mrid: str) -> Terminal:
        return self.end_terminals.get_by_mrid(mrid)

    @deprecated("Use obj.end_terminals.append(terminal) instead.")
    def add_end_terminal(self, terminal: Terminal) -> Circuit:
        self.end_terminals.append(terminal)
        return self

    @deprecated("Use obj.end_terminals.remove(terminal) instead.")
    def remove_end_terminal(self, terminal: Terminal) -> Circuit:
        self.end_terminals.remove(terminal)
        return self

    @deprecated("Use obj.end_terminals.clear() instead.")
    def clear_end_terminals(self) -> Circuit:
        self.end_terminals.clear()
        return self

    # endregion end_terminals boilerplate

    # region end_substations boilerplate

    @deprecated("Use len(obj.end_substations) instead.")
    def num_end_substations(self):
        return len(self.end_substations)

    @deprecated("Use obj.end_substations.get_by_mrid(mrid) instead.")
    def get_end_substation(self, mrid: str) -> Substation:
        return self.end_substations.get_by_mrid(mrid)

    @deprecated("Use obj.end_substations.append(substation) instead.")
    def add_end_substation(self, substation: Substation) -> Circuit:
        self.end_substations.append(substation)
        return self

    @deprecated("Use obj.end_substations.remove(substation) instead.")
    def remove_end_substation(self, substation: Substation) -> Circuit:
        self.end_substations.remove(substation)
        return self

    @deprecated("Use obj.end_substations.clear() instead.")
    def clear_end_substations(self) -> Circuit:
        self.end_substations.clear()
        return self

    # endregion end_substations boilerplate

    # endregion deprecated list boilerplate
