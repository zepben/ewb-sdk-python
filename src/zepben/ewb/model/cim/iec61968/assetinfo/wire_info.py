#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["WireInfo"]

from typing import Optional

from zepben.ewb.dataslot import custom_len, MRIDListRouter, MRIDDictRouter, boilermaker, TypeRestrictedDescriptor, WeakrefDescriptor, dataslot, BackedDescriptor, ListAccessor, ValidatedDescriptor, MRIDListAccessor, custom_get, custom_remove, override_boilerplate, ListActions, MRIDDictAccessor, BackingValue, custom_clear, custom_get_by_mrid, custom_add, NoResetDescriptor, ListRouter, validate
from typing_extensions import deprecated
from zepben.ewb.model.cim.iec61968.assetinfo.wire_material_kind import WireMaterialKind
from zepben.ewb.model.cim.iec61968.assets.asset_info import AssetInfo


@dataslot
class WireInfo(AssetInfo):
    """
    Wire data that can be specified per line segment phase, or for the line segment as a whole in case its phases all
    have the same wire characteristics

    Attributes -
        rated_current : Current carrying capacity of the wire under stated thermal conditions in amperes.
        material : `zepben.protobuf.cim.iec61968.assetinfo.WireMaterialKind` - Conductor material.
    """
    rated_current: int | None = None
    material: WireMaterialKind = WireMaterialKind.UNKNOWN
