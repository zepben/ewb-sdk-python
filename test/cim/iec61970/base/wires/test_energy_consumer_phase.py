#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import builds, floats, sampled_from

from test.cim.extract_testing_args import extract_testing_args
from cim.iec61970.base.core.test_power_system_resource import verify_power_system_resource_constructor_default, \
    verify_power_system_resource_constructor_kwargs, verify_power_system_resource_constructor_args, power_system_resource_kwargs, power_system_resource_args
from test.cim_creators import FLOAT_MIN, FLOAT_MAX
from zepben.evolve import SinglePhaseKind, EnergyConsumer, EnergyConsumerPhase
from zepben.evolve.model.cim.iec61970.base.wires.create_wires_components import create_energy_consumer_phase

energy_consumer_phase_kwargs = {
    **power_system_resource_kwargs,
    "energy_consumer": builds(EnergyConsumer),
    "phase": sampled_from(SinglePhaseKind),
    "p": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "q": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "p_fixed": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "q_fixed": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)
}

energy_consumer_phase_args = [*power_system_resource_args, EnergyConsumer(), SinglePhaseKind.A, 1.1, 2.2, 3.3, 4.4]


def test_energy_consumer_phase_constructor_default():
    ecp = EnergyConsumerPhase()
    ecp2 = create_energy_consumer_phase()
    validate_default_energy_consumer_phase_constructor(ecp)
    validate_default_energy_consumer_phase_constructor(ecp2)


def validate_default_energy_consumer_phase_constructor(ecp):
    verify_power_system_resource_constructor_default(ecp)
    assert ecp.energy_consumer is None
    assert ecp.phase is SinglePhaseKind.X
    assert ecp.p is None
    assert ecp.q is None
    assert ecp.p_fixed is None
    assert ecp.q_fixed is None


@given(**energy_consumer_phase_kwargs)
def test_energy_consumer_phase_constructor_kwargs(energy_consumer, phase, p, p_fixed, q, q_fixed, **kwargs):
    args = extract_testing_args(locals())
    ecp = EnergyConsumerPhase(**args, **kwargs)
    validate_energy_consumer_phase_values(ecp, **args, **kwargs)


@given(**energy_consumer_phase_kwargs)
def test_energy_consumer_phase_creator(energy_consumer, phase, p, p_fixed, q, q_fixed, **kwargs):
    args = extract_testing_args(locals())
    ecp = create_energy_consumer_phase(**args, **kwargs)
    validate_energy_consumer_phase_values(ecp, **args, **kwargs)


def validate_energy_consumer_phase_values(ecp, energy_consumer, phase, p, p_fixed, q, q_fixed, **kwargs):
    verify_power_system_resource_constructor_kwargs(ecp, **kwargs)
    assert ecp.energy_consumer == energy_consumer
    assert ecp.phase == phase
    assert ecp.p == p
    assert ecp.q == q
    assert ecp.p_fixed == p_fixed
    assert ecp.q_fixed == q_fixed


def test_energy_consumer_phase_constructor_args():
    ecp = EnergyConsumerPhase(*energy_consumer_phase_args)

    verify_power_system_resource_constructor_args(ecp)
    assert ecp.energy_consumer == energy_consumer_phase_args[-6]
    assert ecp.phase == energy_consumer_phase_args[-5]
    assert ecp.p == energy_consumer_phase_args[-4]
    assert ecp.q == energy_consumer_phase_args[-3]
    assert ecp.p_fixed == energy_consumer_phase_args[-2]
    assert ecp.q_fixed == energy_consumer_phase_args[-1]
