#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["Circuit"]

from typing import Optional, Generator, List, TYPE_CHECKING

from zepben.ewb.dataslot import custom_len, MRIDListRouter, MRIDDictRouter, boilermaker, TypeRestrictedDescriptor, WeakrefDescriptor, dataslot, BackedDescriptor, ListAccessor, ValidatedDescriptor, MRIDListAccessor, custom_get, custom_remove, override_boilerplate, ListActions, MRIDDictAccessor, BackingValue, custom_clear, custom_get_by_mrid, custom_add, NoResetDescriptor, ListRouter, validate
from typing_extensions import deprecated
from zepben.ewb.model.cim.iec61970.base.wires.line import Line
from zepben.ewb.util import ngen, get_by_mrid, safe_remove, nlen

if TYPE_CHECKING:
    from zepben.ewb.model.cim.extensions.iec61970.base.feeder.loop import Loop
    from zepben.ewb.model.cim.iec61970.base.core.substation import Substation
    from zepben.ewb.model.cim.iec61970.base.core.terminal import Terminal


@dataslot
@boilermaker
class Circuit(Line):
    """Missing description"""

    loop: Loop | None = None
    end_terminals: List[Terminal] | None = MRIDListAccessor()
    end_substations: List[Substation] | None = MRIDListAccessor()

    def _retype(self):
        self.end_terminals: MRIDListRouter = ...
        self.end_substations: MRIDListRouter = ...

    @deprecated("BOILERPLATE: Use len(end_terminals) instead")
    def num_end_terminals(self):
        return len(self.end_terminals)

    @deprecated("BOILERPLATE: Use end_terminals.get_by_mrid(mrid) instead")
    def get_end_terminal(self, mrid: str) -> Terminal:
        return self.end_terminals.get_by_mrid(mrid)

    @deprecated("Boilerplate: Use end_terminals.append(terminal) instead")
    def add_end_terminal(self, terminal: Terminal) -> Circuit:
        self.end_terminals.append(terminal)
        return self

    @deprecated("Boilerplate: Use end_terminals.remove(terminal) instead")
    def remove_end_terminal(self, terminal: Terminal) -> Circuit:
        self.end_terminals.remove(terminal)
        return self

    @deprecated("BOILERPLATE: Use end_terminals.clear() instead")
    def clear_end_terminals(self) -> Circuit:
        return self.end_terminals.clear()

    @deprecated("BOILERPLATE: Use len(end_substations) instead")
    def num_end_substations(self):
        return len(self.end_substations)

    @deprecated("BOILERPLATE: Use end_substations.get_by_mrid(mrid) instead")
    def get_end_substation(self, mrid: str) -> Substation:
        return self.end_substations.get_by_mrid(mrid)

    @deprecated("Boilerplate: Use end_substations.append(substation) instead")
    def add_end_substation(self, substation: Substation) -> Circuit:
        self.end_substations.append(substation)
        return self

    @deprecated("Boilerplate: Use end_substations.remove(substation) instead")
    def remove_end_substation(self, substation: Substation) -> Circuit:
        self.end_substations.remove(substation)
        return self

    @deprecated("BOILERPLATE: Use end_substations.clear() instead")
    def clear_end_substations(self) -> Circuit:
        self.end_substations.clear()
        return self

