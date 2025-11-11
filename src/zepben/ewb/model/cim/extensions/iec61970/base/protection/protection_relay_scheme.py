#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["ProtectionRelayScheme"]

from typing import Optional, List, Generator, TYPE_CHECKING

from zepben.ewb.dataslot import custom_len, MRIDListRouter, MRIDDictRouter, boilermaker, TypeRestrictedDescriptor, WeakrefDescriptor, dataslot, BackedDescriptor, ListAccessor, ValidatedDescriptor, MRIDListAccessor, custom_get, custom_remove, override_boilerplate, ListActions, MRIDDictAccessor, BackingValue, custom_clear, custom_get_by_mrid, custom_add, NoResetDescriptor, ListRouter, validate
from typing_extensions import deprecated
from zepben.ewb.model.cim.extensions.zbex import zbex
from zepben.ewb.model.cim.iec61970.base.core.identified_object import IdentifiedObject
from zepben.ewb.util import ngen, get_by_mrid, nlen, safe_remove

if TYPE_CHECKING:
    from zepben.ewb.model.cim.extensions.iec61970.base.protection.protection_relay_system import ProtectionRelaySystem
    from zepben.ewb.model.cim.extensions.iec61970.base.protection.protection_relay_function import ProtectionRelayFunction


@zbex
@dataslot
@boilermaker
class ProtectionRelayScheme(IdentifiedObject):
    """
    [ZBEX]
    A scheme that a group of relay functions implement. For example, typically schemes are primary and secondary, or main and failsafe.
    """

    system: ProtectionRelaySystem | None = None
    """[ZBEX] The system this scheme belongs to."""

    functions: List[ProtectionRelayFunction] | None = MRIDListAccessor()

    def _retype(self):
        self.functions: MRIDListRouter = ...
    
    @deprecated("BOILERPLATE: Use functions.get_by_mrid(mrid) instead")
    def get_function(self, mrid: str) -> ProtectionRelayFunction:
        return self.functions.get_by_mrid(mrid)

    @deprecated("BOILERPLATE: Use functions.append(function) instead")
    def add_function(self, function: ProtectionRelayFunction) -> ProtectionRelayScheme:
        return self.functions.append(function)

    @deprecated("BOILERPLATE: Use len(functions) instead")
    def num_functions(self) -> int:
        return len(self.functions)

    @deprecated("BOILERPLATE: Use functions.remove(function) instead")
    def remove_function(self, function: ProtectionRelayFunction | None) -> ProtectionRelayScheme:
        return self.functions.remove(function)

    @deprecated("BOILERPLATE: Use functions.clear() instead")
    def clear_function(self) -> ProtectionRelayScheme:
        self.functions.clear()
        return self

