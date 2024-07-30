#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis.strategies import integers

from cim.cim_creators import MAX_32_BIT_INTEGER
from cim.iec61970.base.core.test_conducting_equipment import conducting_equipment_kwargs, verify_conducting_equipment_constructor_default, \
    verify_conducting_equipment_constructor_kwargs, verify_conducting_equipment_constructor_args, conducting_equipment_args
from cim.property_validator import validate_property_accessor
from zepben.evolve import Switch, SinglePhaseKind, SwitchInfo

switch_kwargs = {
    **conducting_equipment_kwargs,
    "rated_current": integers(min_value=0, max_value=MAX_32_BIT_INTEGER),
    "_open": integers(min_value=0, max_value=15),
    "_normally_open": integers(min_value=0, max_value=15),
}

switch_args = [*conducting_equipment_args, 1, 2, 3]


# noinspection PyProtectedMember
def verify_switch_constructor_default(s: Switch):
    verify_conducting_equipment_constructor_default(s)
    assert s.rated_current is None
    assert s._open == 0
    assert s._normally_open == 0


# noinspection PyProtectedMember
def verify_switch_constructor_kwargs(s: Switch, rated_current, _open, _normally_open, **kwargs):
    verify_conducting_equipment_constructor_kwargs(s, **kwargs)
    assert s.rated_current == rated_current
    assert s._open == _open
    assert s._normally_open == _normally_open


# noinspection PyProtectedMember
def verify_switch_constructor_args(s: Switch):
    verify_conducting_equipment_constructor_args(s)
    assert s.rated_current == switch_args[-3]
    assert s._open == switch_args[-2]
    assert s._normally_open == switch_args[-1]


def test_switch_info_accessor():
    validate_property_accessor(Switch, SwitchInfo, Switch.switch_info)


def test_open_states():
    _validate_open_phase(Switch.is_open, Switch.set_open)
    _validate_open_phase(Switch.is_normally_open, Switch.set_normally_open)


def _validate_open_phase(is_open, set_open):
    s = Switch()

    s.set_normally_open(True)
    assert s.is_normally_open()
    s.set_normally_open(False)
    assert not s.is_normally_open()

    valid_phases = list(SinglePhaseKind)[1:6]
    for phase in valid_phases:
        s = Switch()

        set_open(s, True, phase)
        for validate_phase in valid_phases:
            expect_open = (phase.mask_index == validate_phase.mask_index)
            assert is_open(s, validate_phase) == expect_open, f"open check: {phase} should have been {expect_open}"

        set_open(s, True)
        set_open(s, False, phase)

        for validate_phase in valid_phases:
            expect_closed = (phase.mask_index != validate_phase.mask_index)
            assert is_open(s, validate_phase) == expect_closed, f"close check: {phase} should have been {expect_closed}"
