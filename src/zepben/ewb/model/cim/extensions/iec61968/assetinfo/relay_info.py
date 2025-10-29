#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["RelayInfo"]

from typing import Optional, List, Generator, Callable

from zepben.ewb.dataslot import custom_len, MRIDListRouter, MRIDDictRouter, boilermaker, TypeRestrictedDescriptor, WeakrefDescriptor, dataslot, BackedDescriptor, ListAccessor, ValidatedDescriptor, MRIDListAccessor, custom_get, custom_remove, override_boilerplate, ListActions, MRIDDictAccessor, BackingValue, custom_clear, custom_get_by_mrid, custom_add, NoResetDescriptor, ListRouter, validate
from typing_extensions import deprecated
from zepben.ewb.model.cim.extensions.zbex import zbex
from zepben.ewb.model.cim.iec61968.assets.asset_info import AssetInfo
from zepben.ewb.util import ngen, nlen, safe_remove, require


@zbex
@dataslot
@boilermaker
class RelayInfo(AssetInfo):
    """Relay Datasheet Information."""

    curve_setting: str | None = None
    """The type of curve used for the Relay."""

    reclose_fast: bool | None = None
    """True if reclose_delays are associated with a fast Curve, false otherwise."""

    reclose_delays: List[float] | None = ListAccessor()

    def _retype(self):
        self.reclose_delays: ListRouter = ...
    
    @deprecated("BOILERPLATE: Use len(reclose_delays) instead")
    def num_delays(self) -> int:
        return len(self.reclose_delays)

    @custom_get(reclose_delays)
    def get_delay(self, index: int) -> float:
        """
        Get the reclose delay at the specified index, if it exists. Otherwise, this returns

        :param index: The index of the delay to retrieve.
        :return: The reclose delay at `index` if it exists, otherwise None.
        """
        if self.reclose_delays:
            return self.reclose_delays.raw[index]
        else:
            raise IndexError(index)

    def for_each_delay(self, action: Callable[[int, float], None]):
        """
        Call the `action` on each delay in the `reclose_delays` collection

        :param action: An action to apply to each delay in the `reclose_delays` collection, taking the index of the delay, and the delay itself.
        """
        for index, point in enumerate(self.reclose_delays):
            action(index, point)

    @custom_add(reclose_delays)
    def add_delay(self, delay: float, index: int = None) -> RelayInfo:
        """
        Add a reclose delay.

        :param delay: The delay in seconds to add.
        :param index: The index into the list to add the delay at. Defaults to the end of the list.
        :return: A reference to this :class:`RelayInfo` to allow fluent use.
        """
        if index is None:
            index = self.num_delays()
        require(0 <= index <= self.num_delays(),
                lambda: f"Unable to add float to {str(self)}. Index number {index} "
                        f"is invalid. Expected a value between 0 and {self.num_delays()}. Make sure you are "
                        f"adding the items in order and there are no gaps in the numbering.")
        self.reclose_delays.insert_raw(index, delay)
        return self

    def set_delays(self, delays: List[float]) -> RelayInfo:
        """
        Set the reclose delays for this :class:`RelayInfo`.

        :param delays: The delays to set. The provided list will be copied.
        :return: A reference to this :class:`RelayInfo` to allow fluent use.
        """
        self.reclose_delays.set_raw(delays.copy())
        return self

    @deprecated("BOILERPLATE: Use time_limits.remove() instead")
    def remove_delay(self, delay: float) -> RelayInfo:
        """
        Remove a delay from the list.

        :param delay: The delay to remove.
        :return: A reference to this :class:`RelayInfo` to allow fluent use.
        """
        self.reclose_delays.remove(delay)
        return self

    def remove_delay_at(self, index: int) -> float:
        """
        Remove a delay from the list.

        :param index: The index of the delay to remove.
        :return: The delay that was removed, or `None` if no delay was present at `index`.
        :raises IndexError: If `sequence_number` is out of range.
        """
        if self.reclose_delays:
            delay = self.reclose_delays.pop(index)
            return delay
        raise IndexError(index)

    @deprecated("BOILERPLATE: Use reclose_delays.clear() instead")
    def clear_delays(self) -> RelayInfo:
        return self.reclose_delays.clear()
        return self
