#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from cim.iec61970.base.core.test_power_system_resource import verify_power_system_resource_constructor_default, \
    verify_power_system_resource_constructor_kwargs
from cim.private_collection_validator import validate_unordered
from zepben.ewb import RegulatingControlModeKind, PhaseCode, RegulatingControl, RegulatingCondEq


def verify_regulating_control_constructor_default(rc: RegulatingControl):
    verify_power_system_resource_constructor_default(rc)
    assert rc.discrete is None
    assert rc.mode == RegulatingControlModeKind.UNKNOWN
    assert rc.monitored_phase == PhaseCode.NONE
    assert rc.target_deadband is None
    assert rc.target_value is None
    assert rc.enabled is None
    assert rc.max_allowed_target_value is None
    assert rc.min_allowed_target_value is None
    assert rc.rated_current is None
    assert rc.terminal is None
    assert rc.ct_primary is None
    assert rc.min_target_deadband is None
    assert not list(rc.regulating_conducting_equipment)


def verify_regulating_control_constructor_kwargs(
    rc: RegulatingControl,
    discrete,
    mode,
    monitored_phase,
    target_deadband,
    target_value,
    enabled,
    max_allowed_target_value,
    min_allowed_target_value,
    rated_current,
    terminal,
    ct_primary,
    min_target_deadband,
    regulating_conducting_equipment,
    **kwargs,
):
    verify_power_system_resource_constructor_kwargs(rc, **kwargs)
    assert rc.discrete == discrete
    assert rc.mode == mode
    assert rc.monitored_phase == monitored_phase
    assert rc.target_deadband == target_deadband
    assert rc.target_value == target_value
    assert rc.enabled == enabled
    assert rc.max_allowed_target_value == max_allowed_target_value
    assert rc.min_allowed_target_value == min_allowed_target_value
    assert rc.rated_current == rated_current
    assert rc.terminal == terminal
    assert rc.ct_primary == ct_primary
    assert rc.min_target_deadband == min_target_deadband
    assert list(rc.regulating_conducting_equipment) == regulating_conducting_equipment


def test_regulating_control_regulating_conducting_equipment():
    # noinspection PyArgumentList
    validate_unordered(
        RegulatingControl,
        RegulatingCondEq,
        RegulatingControl.regulating_conducting_equipment,
        RegulatingControl.num_regulating_cond_eq,
        RegulatingControl.get_regulating_cond_eq,
        RegulatingControl.add_regulating_cond_eq,
        RegulatingControl.remove_regulating_cond_eq,
        RegulatingControl.clear_regulating_cond_eq,
    )
