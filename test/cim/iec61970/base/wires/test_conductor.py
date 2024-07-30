#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis.strategies import floats

from cim.iec61970.base.core.test_conducting_equipment import conducting_equipment_kwargs, verify_conducting_equipment_constructor_default, \
    verify_conducting_equipment_constructor_kwargs, verify_conducting_equipment_constructor_args, conducting_equipment_args
from cim.property_validator import validate_property_accessor
from cim.cim_creators import FLOAT_MIN, FLOAT_MAX
from zepben.evolve import Conductor, WireInfo

conductor_kwargs = {
    **conducting_equipment_kwargs,
    "length": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)
}

conductor_args = [*conducting_equipment_args, 1]


def verify_conductor_constructor_default(c: Conductor):
    verify_conducting_equipment_constructor_default(c)
    assert c.length is None


def verify_conductor_constructor_kwargs(c: Conductor, length, **kwargs):
    verify_conducting_equipment_constructor_kwargs(c, **kwargs)
    assert c.length == length


def verify_conductor_constructor_args(c: Conductor):
    verify_conducting_equipment_constructor_args(c)
    assert c.length == conductor_args[-1]


def test_wire_info_accessor():
    validate_property_accessor(Conductor, WireInfo, Conductor.wire_info)
