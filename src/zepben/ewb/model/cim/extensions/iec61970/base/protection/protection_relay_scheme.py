#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["ProtectionRelayScheme"]

from typing import Optional, List, TYPE_CHECKING
from dataclasses import field
from typing_extensions import deprecated

from zepben.ewb.model.cim.extensions.zbex import zbex
from zepben.ewb.model.cim.iec61970.base.core.identified_object import IdentifiedObject
from zepben.ewb.boilerplate.dataclass_base import zb_dataclass
from zepben.ewb.boilerplate.collections.mrid_list import LazyMridList
from zepben.ewb.boilerplate.collections.mrid_collection import MridCollection

if TYPE_CHECKING:
    from zepben.ewb.model.cim.extensions.iec61970.base.protection.protection_relay_system import ProtectionRelaySystem
    from zepben.ewb.model.cim.extensions.iec61970.base.protection.protection_relay_function import ProtectionRelayFunction


@zb_dataclass
@zbex
class ProtectionRelayScheme(IdentifiedObject):
    """
    [ZBEX]
    A scheme that a group of relay functions implement. For example, typically schemes are primary and secondary, or main and failsafe.
    """

    system: Optional[ProtectionRelaySystem] = None
    """[ZBEX] The system this scheme belongs to."""

    _functions: Optional[List[ProtectionRelayFunction]] = field(default=None)

    functions: MridCollection[ProtectionRelayFunction] = LazyMridList(
        _functions,
        "A ProtectionRelayFunction",
    )


    # region deprecated list boilerplate
    # region functions boilerplate

    @deprecated("Use len(obj.functions) instead.")
    def num_functions(self) -> int:
        return len(self.functions)

    @deprecated("Use obj.functions.get_by_mrid(mrid) instead.")
    def get_function(self, mrid: str) -> ProtectionRelayFunction:
        return self.functions.get_by_mrid(mrid)

    @deprecated("Use obj.functions.append(function) instead.")
    def add_function(self, function: ProtectionRelayFunction) -> ProtectionRelayScheme:
        self.functions.append(function)
        return self

    @deprecated("Use obj.functions.remove(function) instead.")
    def remove_function(self, function: Optional[ProtectionRelayFunction]) -> ProtectionRelayScheme:
        self.functions.remove(function)
        return self

    @deprecated("Use obj.functions.clear() instead.")
    def clear_function(self) -> ProtectionRelayScheme:
        self.functions.clear()
        return self

    # endregion functions boilerplate

    # endregion deprecated list boilerplate
