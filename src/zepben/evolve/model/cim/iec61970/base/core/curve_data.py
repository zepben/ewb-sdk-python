#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class CurveData:
    """
    Multipurpose data points for defining a curve. The use of this generic class is discouraged if a more specific class can be used to specify the X and
    Y axis values along with their specific data types.
    """

    x_value: float
    """The data value of the X-axis variable, depending on the X-axis units."""

    y1_value: float
    """The data value of the first Y-axis variable, depending on the Y-axis units."""

    y2_value: Optional[float] = None
    """The data value of the second Y-axis variable (if present), depending on the Y-axis units."""

    y3_value: Optional[float] = None
    """The data value of the third Y-axis variable (if present), depending on the Y-axis units."""
