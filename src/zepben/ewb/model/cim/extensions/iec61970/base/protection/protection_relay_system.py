#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["ProtectionRelaySystem"]

from typing import Optional, List, TYPE_CHECKING
from dataclasses import field
from typing_extensions import deprecated

from zepben.ewb.model.cim.extensions.iec61970.base.protection.protection_kind import ProtectionKind
from zepben.ewb.model.cim.extensions.zbex import zbex
from zepben.ewb.model.cim.iec61970.base.core.equipment import Equipment
from zepben.ewb.boilerplate.dataclass_base import zb_dataclass
from zepben.ewb.boilerplate.collections.lazy_mrid_list import LazyMridList
from zepben.ewb.boilerplate.collections.mrid_collection import MridCollection

if TYPE_CHECKING:
    from zepben.ewb.model.cim.extensions.iec61970.base.protection.protection_relay_scheme import ProtectionRelayScheme


@zb_dataclass
@zbex
class ProtectionRelaySystem(Equipment):
    """
    [ZBEX]
    A relay system for controlling ProtectedSwitches.
    """

    protection_kind: ProtectionKind = ProtectionKind.UNKNOWN
    """[ZBEX] The kind of protection being provided by this protection equipment."""

    _schemes: Optional[List[ProtectionRelayScheme]] = field(default=None)

    schemes: MridCollection[ProtectionRelayScheme] = LazyMridList(
        _schemes,
        "A ProtectionRelayScheme",
    )


    # region deprecated list boilerplate
    # region schemes boilerplate

    @deprecated("Use len(obj.schemes) instead.")
    def num_schemes(self) -> int:
        return len(self.schemes)

    @deprecated("Use obj.schemes.get_by_mrid(mrid) instead.")
    def get_scheme(self, mrid: str) -> ProtectionRelayScheme:
        return self.schemes.get_by_mrid(mrid)

    @deprecated("Use obj.schemes.append(scheme) instead.")
    def add_scheme(self, scheme: ProtectionRelayScheme) -> ProtectionRelaySystem:
        self.schemes.append(scheme)
        return self

    @deprecated("Use obj.schemes.remove(scheme) instead.")
    def remove_scheme(self, scheme: Optional[ProtectionRelayScheme]) -> ProtectionRelaySystem:
        self.schemes.remove(scheme)
        return self

    @deprecated("Use obj.schemes.clear() instead.")
    def clear_scheme(self) -> ProtectionRelaySystem:
        self.schemes.clear()
        return self

    # endregion schemes boilerplate

    # endregion deprecated list boilerplate
