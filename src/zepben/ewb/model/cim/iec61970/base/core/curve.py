#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations
__all__ = ["Curve"]

from typing import Optional, List, ClassVar

from typing_extensions import deprecated

from zepben.ewb.collections.autoslot import dataslot, BackingValue
from zepben.ewb.collections.boilerplate import ListAccessor, NamingOptions, ListActions, MRIDListRouter, custom_get, custom_add
from zepben.ewb.model.cim.iec61970.base.core.curve_data import CurveData
from zepben.ewb.model.cim.iec61970.base.core.identified_object import IdentifiedObject


@dataslot
class Curve(IdentifiedObject):
    """
    The Curve class is a multipurpose functional relationship between an independent variable (X-axis) and dependent (Y-axis) variables.
    """

    data: List[CurveData] | None = ListAccessor()

    def _retype(self):
        self.data: MRIDListRouter = ...

    @custom_get(data)
    def get_data(self, x: float) -> CurveData:
        """
        Get the :class:`CurveData` for this :class:`Curve` identified by its `x_value`.

        :param x: The X value of the required :class:`CurveData`.
        :returns: The :class:`CurveData` with the specified `x` if it exists.
        :raises KeyError: When no `CurveData` was found with `x`.
        """
        try:
            return next(it for it in self.data if it.x_value == x)
        except StopIteration:
            raise KeyError(x)

    def __getitem__(self, x: float) -> CurveData:
        """
        Get the :class:`CurveData` for this :class:`Curve` identified by its `x_value`.

        :param x: The X value of the required :class:`CurveData`.
        :returns: The :class:`CurveData` with the specified `x` if it exists.
        :raises IndexError: When no `CurveData` was found with `x`.
        """
        return self.get_data(x)

    @custom_add(data)
    def add_data(self, x: float, y1: float, y2: Optional[float], y3: Optional[float]) -> 'Curve':
        """
        Add a data point to this :class:`Curve`.

        :param x: The data value of the X-axis variable, depending on the X-axis units.
        :param y1: The data value of the first Y-axis variable, depending on the Y-axis units.
        :param y2: The data value of the second Y-axis variable (if present), depending on the Y-axis units.
        :param y3: The data value of the third Y-axis variable (if present), depending on the Y-axis units.
        :raises ValueError: if a :class:`CurveData` for the provided `x` value already exists for this :class:`Curve`.
        """
        self.data.append_unchecked(CurveData(x, y1, y2, y3))
        return self

    def remove_data_at(self, x: float) -> 'CurveData':
        """
        Disassociate a :class:`CurveData` from this :class:`Curve` based on its `x_value`.

        :param x: The :class:`CurveData` to disassociate from this :class:`Curve`.
        :returns: A reference to the removed :class:`CurveData`.
        :raises IndexError: If no :class:`CurveData` with a value of `x` was not associated with this :class:`Curve`.
        """
        cd = self[x]
        self.data.remove(cd)
        return cd

    @deprecated("Use len(data) instead.")
    def num_data(self) -> int: ...

    @deprecated("Use data.append(curve_data) instead.")
    def add_curve_data(self, curve_data: CurveData) -> Curve: ...

    @deprecated("Use len(items) instead.")
    def remove_data(self, curve_data: CurveData) -> 'Curve': ...

    @deprecated("Use data.clear() instead.")
    def clear_data(self) -> 'Curve': ...
