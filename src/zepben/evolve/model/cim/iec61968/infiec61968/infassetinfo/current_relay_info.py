#  Copyright 2023 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations
from typing import Optional, List, Generator

from zepben.evolve.model.cim.iec61968.assets.asset_info import AssetInfo
from zepben.evolve.util import ngen, nlen

__all__ = ["CurrentRelayInfo"]


class CurrentRelayInfo(AssetInfo):
    """Current Relay Datasheet Information."""

    curve_setting: Optional[str] = None
    """The type of curve used for the Current Relay."""

    _reclose_delays: Optional[List[float]] = None

    def __init__(self, reclose_delays: Optional[List[float]] = None, **kwargs):
        super(CurrentRelayInfo, self).__init__(**kwargs)
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
        Get the numder of `Delays` for this `CurrentRelayInfo`
        """
        return nlen(self._reclose_delays)

    def add_delay(self, delay: float, index: int = None) -> CurrentRelayInfo:
        """
        Add a reclose delay
        `delay` The delay in seconds to add.
        `index` The index into the list to add the delay at. Defaults to the end of the list.
        Returns A reference to this `CurrentRelayInfo` to allow fluent use.
        """
        if self._reclose_delays is None:
            self._reclose_delays = list()
        if index is None:
            index = self.num_delays()
        self._reclose_delays.insert(index, delay)
        return self

    def remove_delay(self, index: int) -> Optional[float]:
        """
        Remove a delay from the list.
        `index` The index of the delay to remove.
        Returns The delay that was removed, or `None` if no delay was present at `index`.
        """
        if self._reclose_delays:
            try:
                return self._reclose_delays.pop(index)
            except IndexError:
                return None

    def clear_delays(self) -> CurrentRelayInfo:
        self._reclose_delays = None
        return self
