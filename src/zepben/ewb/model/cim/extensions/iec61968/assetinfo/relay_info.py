#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["RelayInfo"]

from dataclasses import field
from typing import Optional, List, Callable, Any

from typing_extensions import deprecated

from zepben.ewb.boilerplate.dataclass_base import zb_dataclass
from zepben.ewb.boilerplate.collections.lazy_list import LazyList
from zepben.ewb.model.cim.extensions.zbex import zbex
from zepben.ewb.model.cim.iec61968.assets.asset_info import AssetInfo


@zb_dataclass
@zbex
class RelayInfo(AssetInfo):
    """Relay Datasheet Information."""

    curve_setting: Optional[str] = None
    """The type of curve used for the Relay."""

    reclose_fast: Optional[bool] = None
    """True if reclose_delays are associated with a fast Curve, false otherwise."""

    _reclose_delays: Optional[List[float]] = field(default=None)

    reclose_delays: LazyList[float] = LazyList(
        _reclose_delays,
        "float"
    )

    def set_delays(self, delays: List[float]) -> RelayInfo:
        """
        Set the reclose delays for this :class:`RelayInfo`.

        :param delays: The delays to set. The provided list will be copied.
        :return: A reference to this :class:`RelayInfo` to allow fluent use.
        """
        self.reclose_delays.clear()
        self.reclose_delays.extend(delays)
        return self

    # region deprecated methods

    # region reclose_delays boilerplate

    @deprecated("Use len(reclose_delays) instead.")
    def num_delays(self) -> int:
        return len(self.reclose_delays)

    @deprecated("Use reclose_delays[index] instead.")
    def get_delay(self, index: int) -> float:
        return self.reclose_delays[index]

    @deprecated("Use reclose_delays.for_each_indexed(action) instead.")
    def for_each_delay(
        self,
        action: Callable[[int, float], Any],
    ) -> None:
        self.reclose_delays.for_each_indexed(action)

    @deprecated("Use reclose_delays.append(delay)")
    def add_delay(
        self,
        delay: float,
        index: int | None = None,
    ) -> RelayInfo:
        if index is None: index = len(self.reclose_delays)
        self.reclose_delays.insert(index, delay)
        return self

    @deprecated("Use reclose_delays.remove(delay) instead.")
    def remove_delay(self, delay: float) -> RelayInfo:
        self.reclose_delays.remove(delay)
        return self

    @deprecated("Use reclose_delays.pop(index) instead.")
    def remove_delay_at(self, index: int) -> float:
        return self.reclose_delays.pop(index)

    @deprecated("Use reclose_delays.clear() instead.")
    def clear_delays(self) -> RelayInfo:
        self.reclose_delays.clear()
        return self

    # endregion

    # endregion