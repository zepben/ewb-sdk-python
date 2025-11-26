#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["Curve"]

from typing import Optional, List, Generator

from zepben.ewb.dataslot import custom_len, MRIDListRouter, MRIDDictRouter, boilermaker, TypeRestrictedDescriptor, WeakrefDescriptor, dataslot, BackedDescriptor, ListAccessor, ValidatedDescriptor, MRIDListAccessor, custom_get, custom_remove, override_boilerplate, ListActions, MRIDDictAccessor, BackingValue, custom_clear, custom_get_by_mrid, custom_add, NoResetDescriptor, ListRouter, validate
from typing_extensions import deprecated
from zepben.ewb.model.cim.iec61970.base.core.curve_data import CurveData
from zepben.ewb.model.cim.iec61970.base.core.identified_object import IdentifiedObject
from zepben.ewb.util import require, ngen, nlen, safe_remove


@dataslot
@boilermaker
class Curve(IdentifiedObject):
    """
    The Curve class is a multipurpose functional relationship between an independent variable (X-axis) and dependent (Y-axis) variables.
    """

    data: List[CurveData] | None = ListAccessor()

    def _retype(self):
        self.data: ListRouter[CurveData] = ...
    
    @deprecated("BOILERPLATE: Use len(data) instead")
    def num_data(self):
        return len(self.data)

    def get_data(self, x: float) -> CurveData:
        """
        Get the :class:`CurveData` for this :class:`Curve` identified by its `x_value`.

        :param x: The X value of the required :class:`CurveData`.
        :returns: The :class:`CurveData` with the specified `x` if it exists.
        :raises KeyError: When no `CurveData` was found with `x`.
        """
        if self.data:
            curve_data = next((it for it in self.data if it.x_value == x), None)
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

    def add_data(self, x: float, y1: float, y2: float | None, y3: float | None) -> 'Curve':
        """
        Add a data point to this :class:`Curve`.

        :param x: The data value of the X-axis variable, depending on the X-axis units.
        :param y1: The data value of the first Y-axis variable, depending on the Y-axis units.
        :param y2: The data value of the second Y-axis variable (if present), depending on the Y-axis units.
        :param y3: The data value of the third Y-axis variable (if present), depending on the Y-axis units.
        :raises ValueError: if a :class:`CurveData` for the provided `x` value already exists for this :class:`Curve`.
        """
        self.add_curve_data(CurveData(x, y1, y2, y3))
        return self

    @custom_add(data)
    def add_curve_data(self, curve_data: CurveData) -> 'Curve':
        """
        Associate a :class:`CurveData` with this :class:`Curve`.

        :param curve_data: The :class:`CurveData` to associate with this :class:`Curve`.
        :returns: A reference to this :class:`Curve` to allow fluent use.
        :raises ValueError: If another :class:`CurveData` with the same `x_value` already exists for this :class:`Curve`.
        """
        x = curve_data.x_value
        require(all([it.x_value != x for it in self.data]),
                lambda: f"Unable to add datapoint to {self}. x_value {x} is invalid, as data with same x_value already exist in this Curve.")
        self.data.append_unchecked(curve_data)
        self.data.sort(key=lambda it: it.x_value)

        return self

    @deprecated("BOILERPLATE: Use data.remove() instead")
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
        data = self.get_data(x)
        self.data.remove(data)
        return data

    @deprecated("BOILERPLATE: Use data.clear() instead")
    def clear_data(self) -> 'Curve':
        self.data.clear()
        return self

