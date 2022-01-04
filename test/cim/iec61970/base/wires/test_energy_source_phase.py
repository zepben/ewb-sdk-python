#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import builds, sampled_from, data

from test.cim.common_testing_functions import verify
from test.cim.iec61970.base.core.test_power_system_resource import verify_power_system_resource_constructor_default, \
    verify_power_system_resource_constructor_kwargs, verify_power_system_resource_constructor_args, power_system_resource_kwargs, power_system_resource_args
from zepben.evolve import SinglePhaseKind, EnergySource, EnergySourcePhase
from zepben.evolve.model.cim.iec61970.base.wires.create_wires_components import create_energy_source_phase

energy_source_phase_kwargs = {
    **power_system_resource_kwargs,
    "energy_source": builds(EnergySource),
    "phase": sampled_from(SinglePhaseKind)
}

energy_source_phase_args = [*power_system_resource_args, EnergySource(), SinglePhaseKind.A]


def test_energy_source_phase_constructor_default():
    esp = EnergySourcePhase()
    esp2 = create_energy_source_phase()
    verify_default_energy_source_phase_constructor(esp)
    verify_default_energy_source_phase_constructor(esp2)


def verify_default_energy_source_phase_constructor(esp):
    verify_power_system_resource_constructor_default(esp)
    assert esp.energy_source is None
    assert esp.phase is SinglePhaseKind.NONE


# noinspection PyShadowingNames
@given(data())
def test_energy_source_phase_constructor_kwargs(data):
    verify(
        [EnergySourcePhase, create_energy_source_phase],
        data, energy_source_phase_kwargs, verify_energy_source_phase_values
    )


def verify_energy_source_phase_values(esp, energy_source, phase, **kwargs):
    verify_power_system_resource_constructor_kwargs(esp, **kwargs)
    assert esp.energy_source == energy_source
    assert esp.phase == phase


def test_energy_consumer_phase_constructor_args():
    esp = EnergySourcePhase(*energy_source_phase_args)

    verify_power_system_resource_constructor_args(esp)
    assert esp.energy_source == energy_source_phase_args[-2]
    assert esp.phase == energy_source_phase_args[-1]


def test_auto_two_way_connections_for_energy_source_phase_constructor():
    es = EnergySource()
    esp = create_energy_source_phase(energy_source=es)

    assert es.get_phase(esp.mrid) == esp
