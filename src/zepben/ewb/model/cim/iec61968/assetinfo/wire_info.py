#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["WireInfo"]

from typing import Optional

from zepben.ewb.model.cim.iec61968.assetinfo.wire_insulation_kind import WireInsulationKind
from zepben.ewb.model.cim.iec61968.assetinfo.wire_material_kind import WireMaterialKind
from zepben.ewb.model.cim.iec61968.assets.asset_info import AssetInfo


class WireInfo(AssetInfo):
    """
    Wire data that can be specified per line segment phase, or for the line segment as a whole in case its phases all
    have the same wire characteristics

    :var rated_current: Current carrying capacity of the wire under stated thermal conditions in amperes.
    :var material: ``zepben.protobuf.cim.iec61968.assetinfo.WireMaterialKind`` - Conductor material.
    :var size_description: Describes the wire gauge or cross section (e.g., 4/0,
    :var strand_count: Number of strands in the conductor.
    :var core_strand_count: (if used) Number of strands in the steel core.
    :var insulated: True if conductor is insulated.
    :var insulation_material: (if insulated conductor) Material used for insulation.
    :var insulation_thickness: (if insulated conductor) Thickness of the insulation.
    """
    rated_current: int | None = None
    material: WireMaterialKind = WireMaterialKind.UNKNOWN
    size_description: str | None = None
    strand_count: str | None = None
    core_strand_count: str | None = None
    insulated: bool | None = None
    insulation_material: WireInsulationKind = WireInsulationKind.UNKNOWN
    insulation_thickness: float | None = None
