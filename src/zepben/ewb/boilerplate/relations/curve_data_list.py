#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import TYPE_CHECKING

from zepben.ewb.boilerplate.collections.lazy_list import LazyList

if TYPE_CHECKING:
    from zepben.ewb import CurveData


class CurveDataList(LazyList):

    def get(self, x: float) -> 'CurveData':
        """
        Get the :class:`CurveData` identified by its `x_value`.

        :param x: The X value of the required :class:`CurveData`.
        :returns: The :class:`CurveData` with the specified `x` if it exists.
        :raises KeyError: When no `CurveData` was found with `x`.
        """
        curve_data = next((it for it in self if it.x_value == x), None)
        if curve_data:
            return curve_data
        raise KeyError(x)

    def remove_data_at(self, x: float) -> 'CurveData':
        """
        Disassociate a :class:`CurveData` from this collection based on its `x_value`.

        :param x: The :class:`CurveData` to disassociate from this :class:`Curve`.
        :returns: A reference to the removed :class:`CurveData`.
        :raises IndexError: If no :class:`CurveData` with a value of `x` was not associated with this :class:`Curve`.
        """
        data = self.get(x)
        self.remove(data)
        return data
