#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis.strategies import integers, sampled_from, one_of, none, text, booleans

from streaming.get.pb_creators import floats
from zepben.ewb import WireInfo, WireMaterialKind

from cim.cim_creators import MIN_32_BIT_INTEGER, MAX_32_BIT_INTEGER, ALPHANUM, FLOAT_MIN, FLOAT_MAX, sampled_wire_insulation_kind
from cim.iec61970.base.core.test_identified_object import identified_object_kwargs, verify_identified_object_constructor_default, \
    verify_identified_object_constructor_kwargs, verify_identified_object_constructor_args, identified_object_args
from zepben.ewb.model.cim.iec61968.assetinfo.wire_insulation_kind import WireInsulationKind

wire_info_kwargs = {
    **identified_object_kwargs,
    "rated_current": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    "material": sampled_from(WireMaterialKind),
    "size_description": one_of(none(), text(alphabet=ALPHANUM)),
    "strand_count": one_of(none(), text(alphabet=ALPHANUM)),
    "core_strand_count": one_of(none(), text(alphabet=ALPHANUM)),
    "insulated": booleans(),
    "insulation_material": sampled_wire_insulation_kind(),
    "insulation_thickness": one_of(none(), floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)),
}

wire_info_args = [*identified_object_args, 1, WireMaterialKind.acsr, "6.7", "8", "4", True, WireInsulationKind.doubleWireArmour, 1.2]


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
    **kwargs
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


def verify_wire_info_constructor_args(wi: WireInfo):
    verify_identified_object_constructor_args(wi)
    assert wire_info_args[-8:] == [
        wi.rated_current,
        wi.material,
        wi.size_description,
        wi.strand_count,
        wi.core_strand_count,
        wi.insulated,
        wi.insulation_material,
        wi.insulation_thickness,
    ]
