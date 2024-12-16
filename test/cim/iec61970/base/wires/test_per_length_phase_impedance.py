#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from hypothesis import given
from hypothesis.strategies import lists, builds
from zepben.evolve import SinglePhaseKind

from cim.iec61970.base.wires.test_per_length_impedance import verify_per_length_impedance_constructor_default, \
    verify_per_length_impedance_constructor_kwargs, verify_per_length_impedance_constructor_args, per_length_impedance_kwargs, per_length_impedance_args
from zepben.evolve.model.cim.iec61970.base.wires.per_length_phase_impedance import PerLengthPhaseImpedance
from zepben.evolve.model.cim.iec61970.base.wires.phase_impedance_data import PhaseImpedanceData

per_length_phase_impedance_kwargs = {
    **per_length_impedance_kwargs,
    "phase_impedance_data": lists(builds(PhaseImpedanceData), max_size=2),
}

per_length_phase_impedance_args = [*per_length_impedance_args, PhaseImpedanceData(SinglePhaseKind.A, SinglePhaseKind.A)]


def test_per_length_phase_impedance_constructor_default():
    plpi = PerLengthPhaseImpedance()

    verify_per_length_impedance_constructor_default(plpi)
    assert not list(plpi.data)


@given(**per_length_phase_impedance_kwargs)
def test_per_length_phase_impedance_constructor_kwargs(data, **kwargs):
    # noinspection PyArgumentList
    plpi = PerLengthPhaseImpedance(data=data, **kwargs)

    verify_per_length_impedance_constructor_kwargs(plpi, **kwargs)
    assert list(plpi.data) == data


def test_per_length_phase_impedance_constructor_args():
    # noinspection PyArgumentList
    plpi = PerLengthPhaseImpedance(*per_length_phase_impedance_args)

    verify_per_length_impedance_constructor_args(plpi)
    assert per_length_phase_impedance_args[-1:] == [
        list(plpi.data),
    ]
