#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["AssetContainer"]

from zepben.ewb.model.cim.iec61968.assets.asset import Asset


class AssetContainer(Asset):
    """
    Asset that is aggregation of other assets such as conductors, transformers, switchgear, land, fences, buildings,
    equipment, vehicles, etc.
    """
    pass
