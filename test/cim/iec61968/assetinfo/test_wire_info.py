#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from cim.iec61970.base.core.test_identified_object import verify_identified_object_constructor_default, \
    verify_identified_object_constructor_kwargs
from zepben.ewb import WireInfo, WireMaterialKind
from zepben.ewb.model.cim.iec61968.assetinfo.wire_insulation_kind import WireInsulationKind


def verify_wire_info_constructor_default(wi: WireInfo):
    verify_identified_object_constructor_default(wi)
    assert wi.rated_current is None
    assert wi.material == WireMaterialKind.UNKNOWN
    assert wi.size_description is None
    assert wi.strand_count is None
    assert wi.core_strand_count is None
    assert wi.insulated is None
    assert wi.insulation_material is WireInsulationKind.UNKNOWN
    assert wi.insulation_thickness is None


def verify_wire_info_constructor_kwargs(
    wi: WireInfo,
    rated_current,
    material,
    size_description,
    strand_count,
    core_strand_count,
    insulated,
    insulation_material,
    insulation_thickness,
    **kwargs,
):
    verify_identified_object_constructor_kwargs(wi, **kwargs)
    assert wi.rated_current == rated_current
    assert wi.material == material
    assert wi.size_description == size_description
    assert wi.strand_count == strand_count
    assert wi.core_strand_count == core_strand_count
    assert wi.insulated == insulated
    assert wi.insulation_material == insulation_material
    assert wi.insulation_thickness == insulation_thickness
