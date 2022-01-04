#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import builds, sampled_from, floats, data

from test.cim.common_testing_functions import verify
from test.cim.iec61970.base.core.test_power_system_resource import verify_power_system_resource_constructor_default, \
    verify_power_system_resource_constructor_kwargs, verify_power_system_resource_constructor_args, power_system_resource_kwargs, power_system_resource_args
from test.cim_creators import FLOAT_MIN, FLOAT_MAX
from zepben.evolve import SinglePhaseKind, PowerElectronicsConnection, PowerElectronicsConnectionPhase
from zepben.evolve.model.cim.iec61970.base.wires.create_wires_components import create_power_electronics_connection_phase

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
    verify_default_power_electronics_connection_phase_constructor(pecp)
    verify_default_power_electronics_connection_phase_constructor(pecp2)


def verify_default_power_electronics_connection_phase_constructor(pecp):
    verify_power_system_resource_constructor_default(pecp)
    assert pecp.power_electronics_connection is None
    assert pecp.p is None
    assert pecp.phase is SinglePhaseKind.X
    assert pecp.q is None


# noinspection PyShadowingNames
@given(data())
def test_power_electronics_connection_phase_constructor_kwargs(data):
    verify(
        [PowerElectronicsConnectionPhase, create_power_electronics_connection_phase],
        data, power_electronics_connection_phase_kwargs, verify_power_electronics_connection_phase_values
    )


def verify_power_electronics_connection_phase_values(pecp, power_electronics_connection, p, phase, q, **kwargs):
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


# noinspection SpellCheckingInspection
def test_auto_two_way_connections_for_power_electronics_connection_phase_constructor():
    pec = PowerElectronicsConnection()
    pecp = create_power_electronics_connection_phase(power_electronics_connection=pec)

    assert pec.get_phase(pecp.mrid) == pecp
