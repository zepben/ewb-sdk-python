#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import builds, sampled_from, floats

from test.cim.extract_testing_args import extract_testing_args
from cim.iec61970.base.core.test_power_system_resource import verify_power_system_resource_constructor_default, \
    verify_power_system_resource_constructor_kwargs, verify_power_system_resource_constructor_args, power_system_resource_kwargs, power_system_resource_args
from cim_creators import FLOAT_MIN, FLOAT_MAX
from zepben.evolve import SinglePhaseKind, EnergySource, EnergySourcePhase, PowerElectronicsConnection, PowerElectronicsConnectionPhase
from zepben.evolve.model.cim.iec61970.base.wires.create_wires_components import create_energy_source_phase, create_power_electronics_connection_phase

power_electronics_connection_phase_kwargs = {
    **power_system_resource_kwargs,
    "power_electronics_connection": builds(PowerElectronicsConnection),
    "p": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "phase": sampled_from(SinglePhaseKind),
    "q": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)
}

power_electronics_connection_phase_args = [*power_system_resource_args, PowerElectronicsConnection(), 1.1, SinglePhaseKind.A, 2.2]


def test_power_electronics_connection_phase_constructor_default():
    pecp = PowerElectronicsConnectionPhase()
    pecp2 = create_power_electronics_connection_phase()
    validate_default_power_electronics_connection_phase_constructor(pecp)
    validate_default_power_electronics_connection_phase_constructor(pecp2)


def validate_default_power_electronics_connection_phase_constructor(pecp):
    verify_power_system_resource_constructor_default(pecp)
    assert pecp.power_electronics_connection is None
    assert pecp.p is None
    assert pecp.phase is SinglePhaseKind.X
    assert pecp.q is None


@given(**power_electronics_connection_phase_kwargs)
def test_power_electronics_connection_phase_constructor_kwargs(power_electronics_connection, p, phase, q, **kwargs):
    args = extract_testing_args(locals())
    pecp = PowerElectronicsConnectionPhase(**args, **kwargs)
    validate_power_electronics_connection_phase_values(pecp, **args, **kwargs)


@given(**power_electronics_connection_phase_kwargs)
def test_power_electronics_connection_phase_creator(power_electronics_connection, p, phase, q, **kwargs):
    args = extract_testing_args(locals())
    pecp = create_power_electronics_connection_phase(**args, **kwargs)
    validate_power_electronics_connection_phase_values(pecp, **args, **kwargs)


def validate_power_electronics_connection_phase_values(pecp, power_electronics_connection, p, phase, q, **kwargs):
    verify_power_system_resource_constructor_kwargs(pecp, **kwargs)
    assert pecp.power_electronics_connection == power_electronics_connection
    assert pecp.p == p
    assert pecp.phase == phase
    assert pecp.q == q


def test_power_electronics_connection_phase_constructor_args():
    pecp = PowerElectronicsConnectionPhase(*power_electronics_connection_phase_args)

    verify_power_system_resource_constructor_args(pecp)
    assert pecp.power_electronics_connection == power_electronics_connection_phase_args[-4]
    assert pecp.p == power_electronics_connection_phase_args[-3]
    assert pecp.phase == power_electronics_connection_phase_args[-2]
    assert pecp.q == power_electronics_connection_phase_args[-1]
