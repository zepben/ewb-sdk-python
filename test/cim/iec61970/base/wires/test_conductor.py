#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis.strategies import floats, integers

from cim.iec61970.base.core.test_conducting_equipment import conducting_equipment_kwargs, verify_conducting_equipment_constructor_default, \
    verify_conducting_equipment_constructor_kwargs, verify_conducting_equipment_constructor_args, conducting_equipment_args
from cim.property_validator import validate_property_accessor
from cim.cim_creators import FLOAT_MIN, FLOAT_MAX, MIN_32_BIT_INTEGER, MAX_32_BIT_INTEGER
from zepben.ewb import WireInfo
from zepben.ewb.model.cim.iec61970.base.wires.conductor import Conductor

conductor_kwargs = {
    **conducting_equipment_kwargs,
    "length": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "design_temperature": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    "design_rating": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)
}

conductor_args = [*conducting_equipment_args, 1, 2, 3.3]


def verify_conductor_constructor_default(c: Conductor):
    verify_conducting_equipment_constructor_default(c)
    assert c.length is None
    assert c.design_temperature is None
    assert c.design_rating is None


def verify_conductor_constructor_kwargs(c: Conductor, length, design_temperature, design_rating, **kwargs):
    verify_conducting_equipment_constructor_kwargs(c, **kwargs)
    assert c.length == length
    assert c.design_temperature == design_temperature
    assert c.design_rating == design_rating


def verify_conductor_constructor_args(c: Conductor):
    verify_conducting_equipment_constructor_args(c)
    assert conductor_args[-3:] == [
        c.length,
        c.design_temperature,
        c.design_rating
    ]


def test_wire_info_accessor():
    validate_property_accessor(Conductor, WireInfo, Conductor.wire_info)
