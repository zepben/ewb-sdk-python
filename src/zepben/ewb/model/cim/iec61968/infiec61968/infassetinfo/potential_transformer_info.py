#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["PotentialTransformerInfo"]

from typing import Optional

from zepben.ewb.model.cim.iec61968.assets.asset_info import AssetInfo
from zepben.ewb.model.cim.iec61968.infiec61968.infcommon.ratio import Ratio


class PotentialTransformerInfo(AssetInfo):
    """Properties of potential transformer asset."""

    accuracy_class: Optional[str] = None
    """PT accuracy classification."""

    nominal_ratio: Optional[Ratio] = None
    """Nominal ratio between the primary and secondary voltage."""

    primary_ratio: Optional[float] = None
    """Ratio for the primary winding tap changer (numerator)."""

    pt_class: Optional[str] = None
    """Potential transformer (PT) classification covering burden."""

    rated_voltage: Optional[int] = None
    """Rated voltage on the primary side in Volts."""

    secondary_ratio: Optional[float] = None
    """Ratio for the secondary winding tap changer (denominator)."""
