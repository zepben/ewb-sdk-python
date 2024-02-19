#  Copyright 2024 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Optional

from dataclassy import dataclass

from zepben.evolve.model.cim.iec61970.base.domain.unit_symbol import UnitSymbol

__all__ = ["RelaySetting"]


@dataclass(slots=True)
class RelaySetting:
    """The threshold settings for a given relay."""

    unit_symbol: UnitSymbol
    """The unit of the value."""

    value: float
    """The value of the setting, e.g voltage, current, etc."""

    name: Optional[str] = None
    """The name of the setting."""

    # TODO: check what is going to be passed here
