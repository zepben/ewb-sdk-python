#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import math
from dataclasses import dataclass
from typing import Optional

from zepben.evolve.util import require
from zepben.evolve.model.cim.iec61970.base.domain.unit_symbol import UnitSymbol

__all__ = ["RelaySetting"]


@dataclass(frozen=True)
class RelaySetting:
    """The threshold settings for a given relay."""

    unit_symbol: UnitSymbol
    """The unit of the value."""

    value: float
    """The value of the setting, e.g voltage, current, etc."""

    name: Optional[str] = None
    """The name of the setting."""

    def __post_init__(self):
        require(self.value is not None and not math.isnan(self.value), lambda: f"RelaySetting.value must be a real number. Provided: {self.value}")
