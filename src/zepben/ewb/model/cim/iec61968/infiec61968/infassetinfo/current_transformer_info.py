#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["CurrentTransformerInfo"]

from zepben.ewb.dataslot import dataslot
from zepben.ewb.model.cim.iec61968.assets.asset_info import AssetInfo
from zepben.ewb.model.cim.iec61968.infiec61968.infcommon.ratio import Ratio


@dataslot
class CurrentTransformerInfo(AssetInfo):
    """Properties of current transformer asset."""

    accuracy_class: str | None = None
    """CT accuracy classification."""

    accuracy_limit: float | None = None
    """Accuracy limit."""

    core_count: int | None = None
    """Number of cores."""

    ct_class: str | None = None
    """CT classification; i.e. class 10P."""

    knee_point_voltage: int | None = None
    """Maximum voltage in volts across the secondary terminals where the CT still displays linear characteristics."""

    max_ratio: Ratio | None = None
    """Maximum ratio between the primary and secondary current."""

    nominal_ratio: Ratio | None = None
    """Nominal ratio between the primary and secondary current; i.e. 100:5"""

    primary_ratio: float | None = None
    """Ratio for the primary winding tap changer (numerator)."""

    rated_current: int | None = None
    """Rated current on the primary side in amperes."""

    secondary_fls_rating: int | None = None
    """Full load secondary (FLS) rating for secondary winding in amperes."""

    secondary_ratio: float | None = None
    """Ratio for the secondary winding tap changer (denominator)."""

    usage: str | None = None
    """Intended usage of the CT; i.e. metering, protection."""
