#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["Curve"]

from dataclasses import field
from typing import Optional, List, Generator
from abc import ABCMeta

from typing_extensions import deprecated

from zepben.ewb import remove_descriptor_annotations, zb_dataclass
from zepben.ewb.dataclass_descriptors.lazy_list import LazyValidatedList
from zepben.ewb.model.cim.iec61970.base.core.curve_data import CurveData
from zepben.ewb.model.cim.iec61970.base.core.identified_object import IdentifiedObject
from zepben.ewb.util import require, ngen, nlen, safe_remove


class CurveDataList(LazyValidatedList[CurveData]):

    def get(self, x: float) -> CurveData:
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

    def remove_data_at(self, x: float) -> CurveData:
        """
        Disassociate a :class:`CurveData` from this collection based on its `x_value`.

        :param x: The :class:`CurveData` to disassociate from this :class:`Curve`.
        :returns: A reference to the removed :class:`CurveData`.
        :raises IndexError: If no :class:`CurveData` with a value of `x` was not associated with this :class:`Curve`.
        """
        data = self.get(x)
        self.remove(data)
        return data

@zb_dataclass
class Curve(IdentifiedObject, metaclass=ABCMeta):
    """
    The Curve class is a multipurpose functional relationship between an independent variable (X-axis) and dependent (Y-axis) variables.
    """

    _data: list[CurveData] | None = field(default=None)

    data: CurveDataList[CurveData] = CurveDataList(
        _data,
        validate=lambda self, it: self._validate_data(it),
        sort_by=lambda it: it.x_value
    )

    def _validate_data(self, curve_data: CurveData):
        require(all([it.x_value != curve_data.x_value for it in self.data]),
            lambda: f"Unable to add datapoint to {self}. x_value {curve_data.x_value} is invalid, as data with same x_value already exist in this Curve.")


    # region deprecated list boilerplate
    #
    # ("region/endregion" is an IntelliJ feature letting you hide the entire thing)
    # This boilerplate exists solely to enable backwards compatibility.
    # It will be removed eventually.
    # Every single method simply forwards the call to the corresponding list.

    # region data boilerplate

    @deprecated("Use len(data) instead.")
    def num_data(self):
        return len(self.data)

    @deprecated("Use data.get(x) instead.")
    def get_data(self, x: float) -> CurveData:
        return self.data.get(x)

    @deprecated("Use data.get(x) instead.")
    def __getitem__(self, x: float) -> CurveData:
        return self.data.get(x)

    @deprecated("Use data.append(CurveData(x, y1, y2, y3)) instead.")
    def add_data(
        self,
        x: float,
        y1: float,
        y2: Optional[float],
        y3: Optional[float],
    ) -> "Curve":
        self.data.append(CurveData(x, y1, y2, y3))
        return self

    @deprecated("Use data.append(curve_data) instead.")
    def add_curve_data(self, curve_data: CurveData) -> "Curve":
        self.data.append(curve_data)
        return self

    @deprecated("Use data.remove(curve_data) instead.")
    def remove_data(self, curve_data: CurveData) -> "Curve":
        self.data.remove(curve_data)
        return self

    @deprecated("Use data.remove_data_at(x) instead.")
    def remove_data_at(self, x: float) -> CurveData:
        return self.data.remove_data_at(x)

    @deprecated("Use data.clear() instead.")
    def clear_data(self) -> "Curve":
        self.data.clear()
        return self

    # endregion

    # endregion