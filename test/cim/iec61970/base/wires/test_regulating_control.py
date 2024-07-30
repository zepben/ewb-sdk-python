#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis.strategies import booleans, sampled_from, floats, builds, lists

from cim.cim_creators import sampled_phase_code, create_identified_object, FLOAT_MAX, FLOAT_MIN
from cim.collection_validator import validate_collection_unordered
from cim.iec61970.base.core.test_power_system_resource import power_system_resource_args, verify_power_system_resource_constructor_default, \
    verify_power_system_resource_constructor_kwargs, power_system_resource_kwargs, verify_power_system_resource_constructor_args
from zepben.evolve import RegulatingControlModeKind, Terminal, PowerElectronicsConnection, PhaseCode, RegulatingControl, RegulatingCondEq

regulating_control_kwargs = {
    **power_system_resource_kwargs,
    "discrete": booleans(),
    "mode": sampled_from(RegulatingControlModeKind),
    "monitored_phase": sampled_phase_code(),
    "target_deadband": floats(min_value=0.0, max_value=FLOAT_MAX),
    "target_value": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "enabled": booleans(),
    "max_allowed_target_value": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "min_allowed_target_value": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "rated_current": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "terminal": builds(Terminal),
    "regulating_conducting_equipment": lists(builds(PowerElectronicsConnection))
}

regulating_control_args = [*power_system_resource_args, False, RegulatingControlModeKind.voltage, PhaseCode.ABC, 1.1, 2.2, True, 3.3, 4.4, 5.5, Terminal(),
                           [PowerElectronicsConnection()]]


def verify_regulating_control_constructor_default(rc: RegulatingControl):
    verify_power_system_resource_constructor_default(rc)
    assert rc.discrete is None
    assert rc.mode == RegulatingControlModeKind.UNKNOWN_CONTROL_MODE
    assert rc.monitored_phase == PhaseCode.NONE
    assert rc.target_deadband is None
    assert rc.target_value is None
    assert rc.enabled is None
    assert rc.max_allowed_target_value is None
    assert rc.min_allowed_target_value is None
    assert rc.rated_current is None
    assert rc.terminal is None
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
    regulating_conducting_equipment,
    **kwargs
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
    assert list(rc.regulating_conducting_equipment) == regulating_conducting_equipment


def verify_regulating_control_constructor_args(rc):
    verify_power_system_resource_constructor_args(rc)
    assert rc.discrete == regulating_control_args[-11]
    assert rc.mode == regulating_control_args[-10]
    assert rc.monitored_phase == regulating_control_args[-9]
    assert rc.target_deadband == regulating_control_args[-8]
    assert rc.target_value == regulating_control_args[-7]
    assert rc.enabled == regulating_control_args[-6]
    assert rc.max_allowed_target_value == regulating_control_args[-5]
    assert rc.min_allowed_target_value == regulating_control_args[-4]
    assert rc.rated_current == regulating_control_args[-3]
    assert rc.terminal == regulating_control_args[-2]
    assert list(rc.regulating_conducting_equipment) == regulating_control_args[-1]


def test_regulating_control_regulating_conducting_equipment():
    # noinspection PyArgumentList
    validate_collection_unordered(RegulatingControl,
                                  lambda mrid, _: RegulatingCondEq(mrid),
                                  RegulatingControl.num_regulating_cond_eq,
                                  RegulatingControl.get_regulating_cond_eq,
                                  RegulatingControl.regulating_conducting_equipment,
                                  RegulatingControl.add_regulating_cond_eq,
                                  RegulatingControl.remove_regulating_cond_eq,
                                  RegulatingControl.clear_regulating_cond_eq)
