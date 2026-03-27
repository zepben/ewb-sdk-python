#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from cim.iec61970.base.core.test_conducting_equipment import verify_conducting_equipment_constructor_default, \
    verify_conducting_equipment_constructor_kwargs, verify_conducting_equipment_constructor_args, conducting_equipment_args
from zepben.ewb.model.cim.iec61970.base.wires.conductor import Conductor

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
