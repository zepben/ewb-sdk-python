#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["ProtectionRelayScheme"]

from typing import List, TYPE_CHECKING

from typing_extensions import deprecated

from zepben.ewb.dataslot import MRIDListRouter, dataslot, MRIDListAccessor
from zepben.ewb.model.cim.extensions.zbex import zbex
from zepben.ewb.model.cim.iec61970.base.core.identified_object import IdentifiedObject

if TYPE_CHECKING:
    from zepben.ewb.model.cim.extensions.iec61970.base.protection.protection_relay_system import ProtectionRelaySystem
    from zepben.ewb.model.cim.extensions.iec61970.base.protection.protection_relay_function import ProtectionRelayFunction


@zbex
@dataslot
class ProtectionRelayScheme(IdentifiedObject):
    """
    [ZBEX]
    A scheme that a group of relay functions implement. For example, typically schemes are primary and secondary, or main and failsafe.
    """

    system: ProtectionRelaySystem | None = None
    """[ZBEX] The system this scheme belongs to."""

    functions: List[ProtectionRelayFunction] | None = MRIDListAccessor()

    def _retype(self):
        self.functions: MRIDListRouter[ProtectionRelayFunction] = ...
    
    @deprecated("BOILERPLATE: Use functions.get_by_mrid(mrid) instead")
    def get_function(self, mrid: str) -> ProtectionRelayFunction:
        return self.functions.get_by_mrid(mrid)

    @deprecated("Boilerplate: Use functions.append(function) instead")
    def add_function(self, function: ProtectionRelayFunction) -> ProtectionRelayScheme:
        self.functions.append(function)
        return self

    @deprecated("BOILERPLATE: Use len(functions) instead")
    def num_functions(self) -> int:
        return len(self.functions)

    @deprecated("Boilerplate: Use functions.remove(function) instead")
    def remove_function(self, function: ProtectionRelayFunction | None) -> ProtectionRelayScheme:
        self.functions.remove(function)
        return self

    @deprecated("BOILERPLATE: Use functions.clear() instead")
    def clear_function(self) -> ProtectionRelayScheme:
        self.functions.clear()
        return self

