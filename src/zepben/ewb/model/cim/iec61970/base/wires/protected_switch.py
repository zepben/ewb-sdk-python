#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["ProtectedSwitch"]

from typing import Optional, List, Generator, TYPE_CHECKING, Iterable

from zepben.ewb.dataslot import custom_len, MRIDListRouter, MRIDDictRouter, boilermaker, TypeRestrictedDescriptor, WeakrefDescriptor, dataslot, BackedDescriptor, ListAccessor, ValidatedDescriptor, MRIDListAccessor, custom_get, custom_remove, override_boilerplate, ListActions, MRIDDictAccessor, BackingValue, custom_clear, custom_get_by_mrid, custom_add, NoResetDescriptor, ListRouter, validate
from typing_extensions import deprecated
from zepben.ewb.model.cim.iec61970.base.wires.switch import Switch
from zepben.ewb.util import get_by_mrid, ngen, nlen, safe_remove

if TYPE_CHECKING:
    from zepben.ewb.model.cim.extensions.iec61970.base.protection.protection_relay_function import ProtectionRelayFunction


@dataslot
@boilermaker
class ProtectedSwitch(Switch):
    """
    A ProtectedSwitch is a switching device that can be operated by :class:`ProtectionRelayFunction`.
    """

    breaking_capacity: int | None = None
    """The maximum fault current in amps a breaking device can break safely under prescribed conditions of use."""

    relay_functions: List[ProtectionRelayFunction] | None = MRIDListAccessor()

    def _retype(self):
        self.relay_functions: MRIDListRouter = ...
    
    @deprecated("BOILERPLATE: Use len(relay_functions) instead")
    def num_relay_functions(self) -> int:
        return len(self.relay_functions)

    @deprecated("BOILERPLATE: Use relay_functions.get_by_mrid(mrid) instead")
    def get_relay_function(self, mrid: str) -> ProtectionRelayFunction:
        return self.relay_functions.get_by_mrid(mrid)

    @deprecated("Boilerplate: Use relay_functions.append(relay_function) instead")
    def add_relay_function(self, relay_function: ProtectionRelayFunction) -> ProtectedSwitch:
        self.relay_functions.append(relay_function)
        return self

    @deprecated("Boilerplate: Use relay_functions.remove(relay_function) instead")
    def remove_relay_function(self, relay_function: ProtectionRelayFunction | None) -> ProtectedSwitch:
        self.relay_functions.remove(relay_function)
        return self

    @deprecated("BOILERPLATE: Use relay_functions.clear() instead")
    def clear_relay_functions(self) -> ProtectedSwitch:
        self.relay_functions.clear()
        return self

