#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given

from cim.fill_fields import grounding_impedance_kwargs
from cim.iec61970.base.wires.test_earth_fault_compensator import verify_earth_fault_compensator_constructor_default, \
    verify_earth_fault_compensator_constructor_kwargs
from zepben.ewb import GroundingImpedance


def verify_grounding_impedance_constructor_default():
    gi = GroundingImpedance()

    verify_earth_fault_compensator_constructor_default(gi)
    assert gi.x is None


@given(**grounding_impedance_kwargs())
def verify_grounding_impedance_constructor_kwargs(x, **kwargs):
    gi = GroundingImpedance(x=x, **kwargs)

    verify_earth_fault_compensator_constructor_kwargs(gi, **kwargs)
    assert gi.x == x
