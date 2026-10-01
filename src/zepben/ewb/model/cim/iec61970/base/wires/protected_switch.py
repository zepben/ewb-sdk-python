#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["ProtectedSwitch"]

from typing import Optional, List, TYPE_CHECKING
from abc import ABCMeta
from dataclasses import field
from typing_extensions import deprecated

from zepben.ewb.model.cim.iec61970.base.wires.switch import Switch
from zepben.ewb.boilerplate.dataclass_base import zb_dataclass
from zepben.ewb.boilerplate.collections.lazy_mrid_list import LazyMridList
from zepben.ewb.boilerplate.collections.mrid_collection import MridCollection

if TYPE_CHECKING:
    from zepben.ewb.model.cim.extensions.iec61970.base.protection.protection_relay_function import ProtectionRelayFunction


@zb_dataclass
class ProtectedSwitch(Switch, metaclass=ABCMeta):
    """
    A ProtectedSwitch is a switching device that can be operated by :class:`ProtectionRelayFunction`.
    """

    breaking_capacity: Optional[int] = None
    """The maximum fault current in amps a breaking device can break safely under prescribed conditions of use."""

    _relay_functions: Optional[List[ProtectionRelayFunction]] = field(default=None)

    relay_functions: MridCollection[ProtectionRelayFunction] = LazyMridList(
        _relay_functions,
        "A ProtectionRelayFunction",
    )


    # region deprecated list boilerplate
    # region relay_functions boilerplate

    @deprecated("Use len(obj.relay_functions) instead.")
    def num_relay_functions(self) -> int:
        return len(self.relay_functions)

    @deprecated("Use obj.relay_functions.get_by_mrid(mrid) instead.")
    def get_relay_function(self, mrid: str) -> ProtectionRelayFunction:
        return self.relay_functions.get_by_mrid(mrid)

    @deprecated("Use obj.relay_functions.append(relay_function) instead.")
    def add_relay_function(self, relay_function: ProtectionRelayFunction) -> ProtectedSwitch:
        self.relay_functions.append(relay_function)
        return self

    @deprecated("Use obj.relay_functions.remove(relay_function) instead.")
    def remove_relay_function(self, relay_function: Optional[ProtectionRelayFunction]) -> ProtectedSwitch:
        self.relay_functions.remove(relay_function)
        return self

    @deprecated("Use obj.relay_functions.clear() instead.")
    def clear_relay_functions(self) -> ProtectedSwitch:
        self.relay_functions.clear()
        return self

    # endregion relay_functions boilerplate

    # endregion deprecated list boilerplate
