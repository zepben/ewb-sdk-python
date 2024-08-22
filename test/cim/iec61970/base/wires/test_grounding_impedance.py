#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import floats, one_of, none
from zepben.evolve import GroundingImpedance

from cim.cim_creators import FLOAT_MIN, FLOAT_MAX
from cim.iec61970.base.wires.test_earth_fault_compensator import earth_fault_compensator_kwargs, earth_fault_compensator_args, \
    verify_earth_fault_compensator_constructor_default, verify_earth_fault_compensator_constructor_kwargs, verify_earth_fault_compensator_constructor_args

grounding_impedance_kwargs = {
    **earth_fault_compensator_kwargs,
    "x": one_of(none(), floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX))
}

grounding_impedance_args = [*earth_fault_compensator_args, 1.0]


def verify_grounding_impedance_constructor_default():
    gi = GroundingImpedance()

    verify_earth_fault_compensator_constructor_default(gi)
    assert gi.x is None


@given(**grounding_impedance_kwargs)
def verify_grounding_impedance_constructor_kwargs(x, **kwargs):
    gi = GroundingImpedance(x = x, **kwargs)

    verify_earth_fault_compensator_constructor_kwargs(gi, **kwargs)
    assert gi.x == x


def verify_grounding_impedance_constructor_args():
    gi = GroundingImpedance(*grounding_impedance_args)

    verify_earth_fault_compensator_constructor_args(gi)
    assert grounding_impedance_args[-1:] == [
        gi.x
    ]
