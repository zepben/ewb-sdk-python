#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["ProtectionRelaySystem"]

from typing import Optional, List, Generator, TYPE_CHECKING

from zepben.ewb.dataslot import custom_len, MRIDListRouter, MRIDDictRouter, boilermaker, TypeRestrictedDescriptor, WeakrefDescriptor, dataslot, BackedDescriptor, ListAccessor, ValidatedDescriptor, MRIDListAccessor, custom_get, custom_remove, override_boilerplate, ListActions, MRIDDictAccessor, BackingValue, custom_clear, custom_get_by_mrid, custom_add, NoResetDescriptor, ListRouter, validate
from typing_extensions import deprecated
from zepben.ewb.model.cim.extensions.iec61970.base.protection.protection_kind import ProtectionKind
from zepben.ewb.model.cim.extensions.zbex import zbex
from zepben.ewb.model.cim.iec61970.base.core.equipment import Equipment
from zepben.ewb.util import ngen, get_by_mrid, nlen, safe_remove

if TYPE_CHECKING:
    from zepben.ewb.model.cim.extensions.iec61970.base.protection.protection_relay_scheme import ProtectionRelayScheme


@zbex
@dataslot
@boilermaker
class ProtectionRelaySystem(Equipment):
    """
    [ZBEX]
    A relay system for controlling ProtectedSwitches.
    """

    protection_kind: ProtectionKind = ProtectionKind.UNKNOWN
    """[ZBEX] The kind of protection being provided by this protection equipment."""

    schemes: List[ProtectionRelayScheme] | None = MRIDListAccessor()

    def _retype(self):
        self.schemes: MRIDListRouter = ...
    
    @deprecated("BOILERPLATE: Use schemes.get_by_mrid(mrid) instead")
    def get_scheme(self, mrid: str) -> ProtectionRelayScheme:
        return self.schemes.get_by_mrid(mrid)

    @deprecated("Boilerplate: Use schemes.append(scheme) instead")
    def add_scheme(self, scheme: ProtectionRelayScheme) -> ProtectionRelaySystem:
        self.schemes.append(scheme)
        return self

    @deprecated("BOILERPLATE: Use len(schemes) instead")
    def num_schemes(self) -> int:
        return len(self.schemes)

    @deprecated("Boilerplate: Use schemes.remove(scheme) instead")
    def remove_scheme(self, scheme: ProtectionRelayScheme | None) -> ProtectionRelaySystem:
        self.schemes.remove(scheme)
        return self

    @deprecated("BOILERPLATE: Use schemes.clear() instead")
    def clear_scheme(self) -> ProtectionRelaySystem:
        self.schemes.clear()
        return self

