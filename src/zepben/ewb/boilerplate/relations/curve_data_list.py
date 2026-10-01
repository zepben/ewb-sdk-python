#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import TYPE_CHECKING

from zepben.ewb.boilerplate.collections.lazy_list import LazyList

if TYPE_CHECKING:
    from zepben.ewb import CurveData


class CurveDataList(LazyList):
    """A list of ``CurveData`` objects for a ``Curve``."""

    def get(self, x: float) -> 'CurveData':
        """Return point data by its x-value.

        :param x: The x-value of the requested data.
        :raises KeyError: If no data has the requested x-value.
        """

        curve_data = self.find_by(lambda it: it.x_value == x)
        if curve_data:
            return curve_data
        raise KeyError(x)

    def remove_data_at(self, x: float) -> 'CurveData':
        """Remove and return the data point with x-value ``x``.

        :param x: The x-value of the data point to remove.
        :raises KeyError: If no data has the requested x-value.
        """
        data = self.get(x)
        self.remove(data)
        return data
