#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["SwitchInfo"]

from typing import Optional

from zepben.ewb.model.cim.iec61968.assets.asset_info import AssetInfo


class SwitchInfo(AssetInfo):
    """Switch datasheet information."""

    rated_interrupting_time: Optional[float] = None
    """Switch rated interrupting time in seconds."""
