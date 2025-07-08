#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["RelaySetting"]

import math
from dataclasses import dataclass
from typing import Optional

from zepben.ewb.model.cim.extensions.zbex import zbex
from zepben.ewb.model.cim.iec61970.base.domain.unit_symbol import UnitSymbol
from zepben.ewb.util import require


@zbex
@dataclass(frozen=True)
class RelaySetting:
    """
    [ZBEX]
    The threshold settings for a given relay.
    """

    unit_symbol: UnitSymbol
    """[ZBEX] The unit of the value."""

    value: float
    """[ZBEX] The value of the setting, e.g voltage, current, etc."""

    name: Optional[str] = None
    """[ZBEX] The name of the setting."""

    def __post_init__(self):
        require(self.value is not None and not math.isnan(self.value), lambda: f"RelaySetting.value must be a real number. Provided: {self.value}")
