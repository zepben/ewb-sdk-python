#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import pytest
from hypothesis import given
from hypothesis.strategies import lists, builds

from cim.private_collection_validator import validate_unordered_other
from zepben.ewb import SinglePhaseKind, single_phase_kind_by_id, generate_id

from cim.iec61970.base.wires.test_per_length_impedance import verify_per_length_impedance_constructor_default, \
    verify_per_length_impedance_constructor_kwargs, verify_per_length_impedance_constructor_args, per_length_impedance_kwargs, per_length_impedance_args
from zepben.ewb.model.cim.iec61970.base.wires.per_length_phase_impedance import PerLengthPhaseImpedance
from zepben.ewb.model.cim.iec61970.base.wires.phase_impedance_data import PhaseImpedanceData

per_length_phase_impedance_kwargs = {
    **per_length_impedance_kwargs,
    "phase_impedance_data": lists(builds(PhaseImpedanceData), max_size=1),
}

per_length_phase_impedance_args = [*per_length_impedance_args, [PhaseImpedanceData(SinglePhaseKind.A, SinglePhaseKind.A)]]


def test_per_length_phase_impedance_constructor_default():
    plpi = PerLengthPhaseImpedance(mrid=generate_id())

    verify_per_length_impedance_constructor_default(plpi)
    assert not list(plpi.data)


@given(**per_length_phase_impedance_kwargs)
def test_per_length_phase_impedance_constructor_kwargs(phase_impedance_data, **kwargs):
    # noinspection PyArgumentList
    plpi = PerLengthPhaseImpedance(data=phase_impedance_data, **kwargs)

    verify_per_length_impedance_constructor_kwargs(plpi, **kwargs)
    assert list(plpi.data) == phase_impedance_data


def test_per_length_phase_impedance_constructor_args():
    # noinspection PyArgumentList
    plpi = PerLengthPhaseImpedance(*per_length_phase_impedance_args)

    verify_per_length_impedance_constructor_args(plpi)
    assert per_length_phase_impedance_args[-1:] == [
        list(plpi.data),
    ]


@pytest.mark.timeout(10000)
def test_phase_impedance_data():
    validate_unordered_other(
        PerLengthPhaseImpedance,
        lambda it: PhaseImpedanceData(single_phase_kind_by_id(it), single_phase_kind_by_id(it + 1), it, it, it, it),
        PerLengthPhaseImpedance.data,
        PerLengthPhaseImpedance.num_data,
        lambda it, key: it.get_data(key[0], key[1]),
        PerLengthPhaseImpedance.add_data,
        PerLengthPhaseImpedance.remove_data,
        PerLengthPhaseImpedance.clear_data,
        lambda it: (it.from_phase, it.to_phase),
        lambda rs: f"from_phase {rs[0]} and to_phase {rs[1]}"
    )


def test_diagonals_returns_only_diagonals():
    pi1 = PhaseImpedanceData(SinglePhaseKind.A, SinglePhaseKind.B)
    pi2 = PhaseImpedanceData(SinglePhaseKind.A, SinglePhaseKind.C)
    pi3 = PhaseImpedanceData(SinglePhaseKind.B, SinglePhaseKind.C)

    pid1 = PhaseImpedanceData(SinglePhaseKind.A, SinglePhaseKind.A)
    pid2 = PhaseImpedanceData(SinglePhaseKind.B, SinglePhaseKind.B)
    pid3 = PhaseImpedanceData(SinglePhaseKind.C, SinglePhaseKind.C)

    plpi = PerLengthPhaseImpedance(mrid=generate_id())
    plpi.add_data(pi1)
    plpi.add_data(pi2)
    plpi.add_data(pi3)
    plpi.add_data(pid1)
    plpi.add_data(pid2)
    plpi.add_data(pid3)

    diagonals = list(plpi.diagonal)
    assert diagonals == [pid1, pid2, pid3]
    assert pi1 not in diagonals
    assert pi2 not in diagonals
    assert pi3 not in diagonals
