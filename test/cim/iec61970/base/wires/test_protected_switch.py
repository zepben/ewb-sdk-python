#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis.strategies import integers, lists, builds

from cim.cim_creators import MIN_32_BIT_INTEGER, MAX_32_BIT_INTEGER
from cim.iec61970.base.wires.test_switch import switch_kwargs, verify_switch_constructor_default, verify_switch_constructor_kwargs, \
    verify_switch_constructor_args, switch_args
from zepben.evolve import ProtectionEquipment, RecloseSequence, ProtectedSwitch

protected_switch_kwargs = {
    **switch_kwargs,
    "breaking_capacity": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    "reclose_sequences": lists(builds(RecloseSequence), max_size=2),
    "operated_by_protection_equipment": lists(builds(ProtectionEquipment), max_size=2)
}
protected_switch_args = [*switch_args, 1, [RecloseSequence()], [ProtectionEquipment()]]


def verify_protected_switch_constructor_default(ps: ProtectedSwitch):
    verify_switch_constructor_default(ps)

    assert ps.breaking_capacity is None
    assert list(ps.reclose_sequences) == []
    assert list(ps.operated_by_protection_equipment) == []


def verify_protected_switch_constructor_kwargs(ps: ProtectedSwitch, breaking_capacity, reclose_sequences, operated_by_protection_equipment, **kwargs):
    verify_switch_constructor_kwargs(ps, **kwargs)

    assert ps.breaking_capacity == breaking_capacity
    assert list(ps.reclose_sequences) == reclose_sequences
    assert list(ps.operated_by_protection_equipment) == operated_by_protection_equipment


def verify_protected_switch_constructor_args(ps: ProtectedSwitch):
    verify_switch_constructor_args(ps)

    assert ps.breaking_capacity == protected_switch_args[-3]
    assert list(ps.reclose_sequences) == protected_switch_args[-2]
    assert list(ps.operated_by_protection_equipment) == protected_switch_args[-1]
