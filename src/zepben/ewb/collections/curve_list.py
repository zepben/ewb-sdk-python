#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Optional

from zepben.ewb import CurveData, require
from zepben.ewb.collections.zepben_list import ZepbenList


class CurveList(ZepbenList[CurveData]):

    def get(self, x: float):
        try:
            return next(it for it in self if it.x_value == x)
        except StopIteration:
            raise KeyError(x)

    def add(self, curve_data: CurveData):
        require(all([it.x_value != curve_data.x_value for it in self]),
                lambda: f"Unable to add datapoint to {self}. x_value {curve_data.x_value} " +
                        f"is invalid, as data with same x_value already exist in this Curve.")

        super().add(curve_data)
        self._data.sort(key=lambda it: it.x_value)

        return self

    def add_data(self, x: float, y1: float, y2: Optional[float], y3: Optional[float]):
        self.add(CurveData(x, y1, y2, y3))

    def remove_at(self, x: float):
        data = self.get(x)
        self.remove(data)
        return data