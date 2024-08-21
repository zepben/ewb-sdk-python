#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations
from typing import Optional, List, Generator, Callable

from zepben.evolve.model.cim.iec61968.assets.asset_info import AssetInfo
from zepben.evolve.util import ngen, nlen, safe_remove, require

__all__ = ["RelayInfo"]


class RelayInfo(AssetInfo):
    """Relay Datasheet Information."""

    curve_setting: Optional[str] = None
    """The type of curve used for the Relay."""

    reclose_fast: Optional[bool] = None
    """True if reclose_delays are associated with a fast Curve, false otherwise."""

    _reclose_delays: Optional[List[float]] = None

    def __init__(self, reclose_delays: Optional[List[float]] = None, **kwargs):
        super(RelayInfo, self).__init__(**kwargs)
        if reclose_delays:
            for index, delay in enumerate(reclose_delays):
                self.add_delay(delay, index)

    @property
    def reclose_delays(self) -> Generator[float, None, None]:
        """
        The reclose delays for this curve and relay type. The index of the list is the reclose step, and the value is the overall delay time.
        """
        return ngen(self._reclose_delays)

    def num_delays(self) -> int:
        """
        Get the number of reclose delays for this :class:`RelayInfo`
        """
        return nlen(self._reclose_delays)

    def get_delay(self, index: int) -> float:
        """
        Get the reclose delay at the specified index, if it exists. Otherwise, this returns

        :param index: The index of the delay to retrieve.
        :return: The reclose delay at `index` if it exists, otherwise None.
        """
        if self._reclose_delays:
            return self._reclose_delays[index]
        else:
            raise IndexError(index)

    def for_each_delay(self, action: Callable[[int, float], None]):
        """
        Call the `action` on each delay in the `reclose_delays` collection

        :param action: An action to apply to each delay in the `reclose_delays` collection, taking the index of the delay, and the delay itself.
        """
        for index, point in enumerate(self._reclose_delays):
            action(index, point)

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
        self._reclose_delays = list() if self._reclose_delays is None else self._reclose_delays
        self._reclose_delays.insert(index, delay)
        return self

    def set_delays(self, delays: List[float]) -> RelayInfo:
        """
        Set the reclose delays for this :class:`RelayInfo`.

        :param delays: The delays to set. The provided list will be copied.
        :return: A reference to this :class:`RelayInfo` to allow fluent use.
        """
        self._reclose_delays = delays.copy()
        return self

    def remove_delay(self, delay: float) -> RelayInfo:
        """
        Remove a delay from the list.

        :param delay: The delay to remove.
        :return: A reference to this :class:`RelayInfo` to allow fluent use.
        """
        self._reclose_delays = safe_remove(self._reclose_delays, delay)
        return self

    def remove_delay_at(self, index: int) -> float:
        """
        Remove a delay from the list.

        :param index: The index of the delay to remove.
        :return: The delay that was removed, or `None` if no delay was present at `index`.
        :raises IndexError: If `sequence_number` is out of range.
        """
        if self._reclose_delays:
            delay = self._reclose_delays.pop(index)
            self._reclose_delays = self._reclose_delays if self._reclose_delays else None
            return delay
        raise IndexError(index)

    def clear_delays(self) -> RelayInfo:
        """
        Clear all reclose delays.

        :return: A reference to this :class:`RelayInfo` to allow fluent use.
        """
        self._reclose_delays = None
        return self
