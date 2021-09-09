#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations

from typing import Optional

from zepben.evolve.model.cim.iec61968.assets.asset_info import AssetInfo

__all__ = ["ShuntCompensatorInfo"]


class ShuntCompensatorInfo(AssetInfo):
    """Properties of shunt capacitor, shunt reactor or switchable bank of shunt capacitor or reactor assets."""

    max_power_loss: Optional[int] = None
    """Maximum allowed apparent power loss in watts."""

    rated_current: Optional[int] = None
    """Rated current in amperes."""

    rated_reactive_power: Optional[int] = None
    """Rated reactive power in volt-amperes reactive."""

    rated_voltage: Optional[int] = None
    """Rated voltage in volts."""
