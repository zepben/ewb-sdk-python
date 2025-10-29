#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["ShuntCompensatorInfo"]

from typing import Optional

from zepben.ewb.dataslot import custom_len, MRIDListRouter, MRIDDictRouter, boilermaker, TypeRestrictedDescriptor, WeakrefDescriptor, dataslot, BackedDescriptor, ListAccessor, ValidatedDescriptor, MRIDListAccessor, custom_get, custom_remove, override_boilerplate, ListActions, MRIDDictAccessor, BackingValue, custom_clear, custom_get_by_mrid, custom_add, NoResetDescriptor, ListRouter, validate
from typing_extensions import deprecated
from zepben.ewb.model.cim.iec61968.assets.asset_info import AssetInfo


@dataslot
class ShuntCompensatorInfo(AssetInfo):
    """Properties of shunt capacitor, shunt reactor or switchable bank of shunt capacitor or reactor assets."""

    max_power_loss: int | None = None
    """Maximum allowed apparent power loss in watts."""

    rated_current: int | None = None
    """Rated current in amperes."""

    rated_reactive_power: int | None = None
    """Rated reactive power in volt-amperes reactive."""

    rated_voltage: int | None = None
    """Rated voltage in volts."""
