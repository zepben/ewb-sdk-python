#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import floats, sampled_from
from pytest import raises
from zepben.ewb import SinglePhaseKind

from cim.cim_creators import FLOAT_MIN, FLOAT_MAX
from zepben.ewb.model.cim.iec61970.base.wires.phase_impedance_data import PhaseImpedanceData

phase_impedance_data_kwargs = {
    "from_phase": sampled_from(SinglePhaseKind),
    "to_phase": sampled_from(SinglePhaseKind),
    "b": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "g": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "r": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "x": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
}

phase_impedance_data_args = [SinglePhaseKind.B, SinglePhaseKind.C, 1.1, 2.2, 3.3, 4.4]


# noinspection PyArgumentList
def test_data_constructor_default():
    #
    # NOTE: There is no blank constructor, so check we need to pass both required values.
    #
    with raises(TypeError):
        PhaseImpedanceData()
    with raises(TypeError):
        PhaseImpedanceData(1.0)
    with raises(TypeError):
        PhaseImpedanceData(SinglePhaseKind.A)
    with raises(TypeError):
        PhaseImpedanceData(to_phase=SinglePhaseKind.A)

    # Make sure we can call the constructor without the optional args.
    PhaseImpedanceData(from_phase=SinglePhaseKind.A, to_phase=SinglePhaseKind.B)
    PhaseImpedanceData(from_phase=SinglePhaseKind.A, to_phase=SinglePhaseKind.B, b=1.0)
    PhaseImpedanceData(from_phase=SinglePhaseKind.A, to_phase=SinglePhaseKind.B, b=1.0, g=2.0)
    PhaseImpedanceData(from_phase=SinglePhaseKind.A, to_phase=SinglePhaseKind.B, b=1.0, g=2.0, r=3.0)
    PhaseImpedanceData(from_phase=SinglePhaseKind.A, to_phase=SinglePhaseKind.B, b=1.0, g=2.0, r=3.0, x=4.0)


@given(**phase_impedance_data_kwargs)
def test_phase_impedance_data_constructor_kwargs(from_phase, to_phase, b, g, r, x, **kwargs):
    assert not kwargs

    phase_impedance_data = PhaseImpedanceData(from_phase=from_phase, to_phase=to_phase, b=b, g=g, r=r, x=x)

    assert phase_impedance_data.from_phase == from_phase
    assert phase_impedance_data.to_phase == to_phase
    assert phase_impedance_data.b == b
    assert phase_impedance_data.g == g
    assert phase_impedance_data.r == r
    assert phase_impedance_data.x == x


from pytest import mark
@mark.skip(reason="Args are deprecated")
def test_phase_impedance_data_constructor_args():
    phase_impedance_data = PhaseImpedanceData(*phase_impedance_data_args)

    assert phase_impedance_data_args[-6:] == [
        phase_impedance_data.from_phase,
        phase_impedance_data.to_phase,
        phase_impedance_data.b,
        phase_impedance_data.g,
        phase_impedance_data.r,
        phase_impedance_data.x
    ]
