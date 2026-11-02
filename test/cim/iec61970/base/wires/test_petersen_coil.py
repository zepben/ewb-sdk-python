#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given

from cim.fill_fields import petersen_coil_kwargs
from cim.iec61970.base.wires.test_earth_fault_compensator import verify_earth_fault_compensator_constructor_default, \
    verify_earth_fault_compensator_constructor_kwargs
from zepben.ewb import PetersenCoil


def verify_petersen_coil_constructor_default():
    pc = PetersenCoil()

    verify_earth_fault_compensator_constructor_default(pc)
    assert pc.x_ground_nominal is None


@given(**petersen_coil_kwargs())
def verify_petersen_coil_constructor_kwargs(x_ground_nominal, **kwargs):
    pc = PetersenCoil(x_ground_nominal=x_ground_nominal, **kwargs)

    verify_earth_fault_compensator_constructor_kwargs(pc, **kwargs)
    assert pc.x_ground_nominal == x_ground_nominal
