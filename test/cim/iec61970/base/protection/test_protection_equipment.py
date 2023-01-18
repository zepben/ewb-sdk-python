#  Copyright 2023 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis.strategies import floats, sampled_from, lists, builds

from cim.cim_creators import FLOAT_MIN, FLOAT_MAX
from cim.collection_validator import validate_collection_unordered
from cim.iec61970.base.core.test_equipment import verify_equipment_constructor_default, equipment_kwargs, verify_equipment_constructor_kwargs, \
    verify_equipment_constructor_args, equipment_args
from zepben.evolve import ProtectionEquipment, ProtectionKind, ProtectedSwitch

protection_equipment_kwargs = {
    **equipment_kwargs,
    "relay_delay_time": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "protection_kind": sampled_from(ProtectionKind),
    "protected_switches": lists(builds(ProtectedSwitch), max_size=2)
}

protection_equipment_args = [*equipment_args, 1.1, ProtectionKind.EF, [ProtectedSwitch()]]


def verify_protection_equipment_constructor_default(pe: ProtectionEquipment):
    verify_equipment_constructor_default(pe)
    assert pe.relay_delay_time is None
    assert pe.protection_kind is ProtectionKind.UNKNOWN
    assert not list(pe.protected_switches)


def verify_protection_equipment_constructor_kwargs(pe: ProtectionEquipment, relay_delay_time, protection_kind, protected_switches, **kwargs):
    verify_equipment_constructor_kwargs(pe, **kwargs)
    assert pe.relay_delay_time == relay_delay_time
    assert pe.protection_kind == protection_kind
    assert list(pe.protected_switches) == protected_switches


def verify_protection_equipment_constructor_args(pe: ProtectionEquipment):
    verify_equipment_constructor_args(pe)
    assert pe.relay_delay_time == protection_equipment_args[-3]
    assert pe.protection_kind == protection_equipment_args[-2]
    assert list(pe.protected_switches) == protection_equipment_args[-1]


def test_protected_switches_collection():
    validate_collection_unordered(ProtectionEquipment,
                                  lambda mrid, _: ProtectedSwitch(mrid),
                                  ProtectionEquipment.num_protected_switches,
                                  ProtectionEquipment.get_protected_switch,
                                  ProtectionEquipment.protected_switches,
                                  ProtectionEquipment.add_protected_switch,
                                  ProtectionEquipment.remove_protected_switch,
                                  ProtectionEquipment.clear_protected_switches)
