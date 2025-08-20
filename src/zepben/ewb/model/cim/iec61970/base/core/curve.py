#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["Curve"]

from typing import Optional, List, Generator

from zepben.ewb.collections.curve_list import CurveList
from zepben.ewb.collections.zepben_list import ZepbenList
from zepben.ewb.model.cim.iec61970.base.core.curve_data import CurveData
from zepben.ewb.model.cim.iec61970.base.core.identified_object import IdentifiedObject
from zepben.ewb.util import require, ngen, nlen, safe_remove


class Curve(IdentifiedObject):
    """
    The Curve class is a multipurpose functional relationship between an independent variable (X-axis) and dependent (Y-axis) variables.
    """

    data: Optional[List[CurveData]] = None

    def __post_init__(self):
        """
        `data` A list of `CurveData`s to associate with this `Curve`.
        """
        _data = self.data
        self.data : CurveList = CurveList(self.data)

    def num_data(self):
        """Return the number of :class:`CurveData` associated with this :class:`Curve`."""
        return len(self.data)

    def get_data(self, x: float) -> CurveData:
        """
        Get the :class:`CurveData` for this :class:`Curve` identified by its `x_value`.

        :param x: The X value of the required :class:`CurveData`.
        :returns: The :class:`CurveData` with the specified `x` if it exists.
        :raises KeyError: When no `CurveData` was found with `x`.
        """
        return self.data.get(x)

    def __getitem__(self, x: float) -> CurveData:
        """
        Get the :class:`CurveData` for this :class:`Curve` identified by its `x_value`.

        :param x: The X value of the required :class:`CurveData`.
        :returns: The :class:`CurveData` with the specified `x` if it exists.
        :raises IndexError: When no `CurveData` was found with `x`.
        """
        return self.get_data(x)

    def add_data(self, x: float, y1: float, y2: Optional[float], y3: Optional[float]) -> 'Curve':
        """
        Add a data point to this :class:`Curve`.

        :param x: The data value of the X-axis variable, depending on the X-axis units.
        :param y1: The data value of the first Y-axis variable, depending on the Y-axis units.
        :param y2: The data value of the second Y-axis variable (if present), depending on the Y-axis units.
        :param y3: The data value of the third Y-axis variable (if present), depending on the Y-axis units.
        :raises ValueError: if a :class:`CurveData` for the provided `x` value already exists for this :class:`Curve`.
        """
        self.data.add_data(x, y1, y2, y3)
        return self

    def add_curve_data(self, curve_data: CurveData) -> 'Curve':
        """
        Associate a :class:`CurveData` with this :class:`Curve`.

        :param curve_data: The :class:`CurveData` to associate with this :class:`Curve`.
        :returns: A reference to this :class:`Curve` to allow fluent use.
        :raises ValueError: If another :class:`CurveData` with the same `x_value` already exists for this :class:`Curve`.
        """
        return self.data.add(curve_data)

    def remove_data(self, curve_data: CurveData) -> 'Curve':
        """
        Disassociate a :class:`CurveData` from this :class:`Curve`.

        :param curve_data: The :class:`CurveData` to disassociate from this :class:`Curve`.
        :returns: A reference to this :class:`Curve` to allow fluent use.
        :raises ValueError: If `curve_data` was not associated with this :class:`Curve`.
        """
        self.data.remove(curve_data)
        return self

    def remove_data_at(self, x: float) -> CurveData:
        """
        Disassociate a :class:`CurveData` from this :class:`Curve` based on its `x_value`.

        :param x: The :class:`CurveData` to disassociate from this :class:`Curve`.
        :returns: A reference to the removed :class:`CurveData`.
        :raises IndexError: If no :class:`CurveData` with a value of `x` was not associated with this :class:`Curve`.
        """
        return self.data.remove_at(x)

    def clear_data(self) -> 'Curve':
        """
        Clear all :class:`CurveData` associated with this :class:`Curve`.
        :returns: A reference to this :class:`Curve` to allow fluent use.
        """
        self.data.clear()
        return self
