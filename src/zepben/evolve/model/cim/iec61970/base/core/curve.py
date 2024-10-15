#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import Optional, List, Generator

from zepben.evolve.util import require, ngen, nlen, safe_remove
from zepben.evolve.model.cim.iec61970.base.core.curve_data import CurveData
from zepben.evolve.model.cim.iec61970.base.core.identified_object import IdentifiedObject


class Curve(IdentifiedObject):
    """
    The Curve class is a multipurpose functional relationship between an independent variable (X-axis) and dependent (Y-axis) variables.
    """

    _data: Optional[List[CurveData]] = None

    def __init__(self, data: List[CurveData] = None, **kwargs):
        """
        `data` A list of `CurveData`s to associate with this `Curve`.
        """
        super(Curve, self).__init__(**kwargs)
        if data:
            for curve_data in data:
                self.add_curve_data(curve_data)

    @property
    def data(self) -> Generator[CurveData, None, None]:
        """
        The point data values that define this curve, sorted by `x_value` in ascending order.
        """
        return ngen(self._data)

    def num_data(self):
        """Return the number of :class:`CurveData` associated with this :class:`Curve`."""
        return nlen(self._data)

    def get_data(self, x: float) -> CurveData:
        """
        Get the :class:`CurveData` for this :class:`Curve` identified by its `x_value`.

        :param x: The X value of the required :class:`CurveData`.
        :returns: The :class:`CurveData` with the specified `x` if it exists.
        :raises KeyError: When no `CurveData` was found with `x`.
        """
        if self._data:
            curve_data = next((it for it in self._data if it.x_value == x), None)
            if curve_data:
                return curve_data
        raise KeyError(x)

    def __getitem__(self, x: float) -> CurveData:
        """
        Get the :class:`CurveData` for this :class:`Curve` identified by its `x_value`.

        :param x: The X value of the required :class:`CurveData`.
        :returns: The :class:`CurveData` with the specified `x` if it exists.
        :raises IndexError: When no `CurveData` was found with `x`.
        """
        return self.get_data(x)

    def add_data(self, x: float, y1: float, y2: Optional[float], y3: Optional[float]) -> "Curve":
        """
        Add a data point to this :class:`Curve`.

        :param x: The data value of the X-axis variable, depending on the X-axis units.
        :param y1: The data value of the first Y-axis variable, depending on the Y-axis units.
        :param y2: The data value of the second Y-axis variable (if present), depending on the Y-axis units.
        :param y3: The data value of the third Y-axis variable (if present), depending on the Y-axis units.
        :raises ValueError: if a :class:`CurveData` for the provided `x` value already exists for this :class:`Curve`.
        """
        require(all([it.x_value != x for it in self.data]),
                lambda: f"Unable to add datapoint to {self}. x_value {x} is invalid, as data with same x_value already exist in this Curve.")

        self._data = self._data or []
        self._data.append(CurveData(x, y1, y2, y3))
        self._data.sort(key=lambda it: it.x_value)

        return self

    def add_curve_data(self, curve_data: CurveData) -> "Curve":
        """
        Associate a :class:`CurveData` with this :class:`Curve`.

        :param curve_data: The :class:`CurveData` to associate with this :class:`Curve`.
        :returns: A reference to this :class:`Curve` to allow fluent use.
        :raises ValueError: If another :class:`CurveData` with the same `x_value` already exists for this :class:`Curve`.
        """
        return self.add_data(curve_data.x_value, curve_data.y1_value, curve_data.y2_value, curve_data.y3_value)

    def remove_data(self, curve_data: CurveData) -> "Curve":
        """
        Disassociate a :class:`CurveData` from this :class:`Curve`.

        :param curve_data: The :class:`CurveData` to disassociate from this :class:`Curve`.
        :returns: A reference to this :class:`Curve` to allow fluent use.
        :raises ValueError: If `curve_data` was not associated with this :class:`Curve`.
        """
        self._data = safe_remove(self._data, curve_data)
        return self

    def remove_data_at(self, x: float) -> CurveData:
        """
        Disassociate a :class:`CurveData` from this :class:`Curve` based on its `x_value`.

        :param x: The :class:`CurveData` to disassociate from this :class:`Curve`.
        :returns: A reference to the removed :class:`CurveData`.
        :raises IndexError: If no :class:`CurveData` with a value of `x` was not associated with this :class:`Curve`.
        """
        data = self.get_data(x)
        self._data = safe_remove(self._data, data)
        return data

    def clear_data(self) -> "Curve":
        """
        Clear all :class:`CurveData` associated with this :class:`Curve`.
        :returns: A reference to this :class:`Curve` to allow fluent use.
        """
        self._data = None
        return self
