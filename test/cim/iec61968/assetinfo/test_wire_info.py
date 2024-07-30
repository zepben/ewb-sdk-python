#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis.strategies import integers, sampled_from

from cim.iec61970.base.core.test_identified_object import identified_object_kwargs, verify_identified_object_constructor_default, \
    verify_identified_object_constructor_kwargs, verify_identified_object_constructor_args, identified_object_args
from cim.cim_creators import MIN_32_BIT_INTEGER, MAX_32_BIT_INTEGER
from zepben.evolve import WireInfo, WireMaterialKind

wire_info_kwargs = {
    **identified_object_kwargs,
    "rated_current": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    "material": sampled_from(WireMaterialKind)
}

wire_info_args = [*identified_object_args, 1, WireMaterialKind.acsr]


def verify_wire_info_constructor_default(wi: WireInfo):
    verify_identified_object_constructor_default(wi)
    assert wi.rated_current is None
    assert wi.material == WireMaterialKind.UNKNOWN


def verify_wire_info_constructor_kwargs(wi: WireInfo, rated_current, material, **kwargs):
    verify_identified_object_constructor_kwargs(wi, **kwargs)
    assert wi.rated_current == rated_current
    assert wi.material == material


def verify_wire_info_constructor_args(wi: WireInfo):
    verify_identified_object_constructor_args(wi)
    assert wi.rated_current == wire_info_args[-2]
    assert wi.material == wire_info_args[-1]
