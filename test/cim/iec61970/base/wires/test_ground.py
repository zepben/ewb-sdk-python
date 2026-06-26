#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from hypothesis import given

from cim.fill_fields import ground_kwargs
from cim.iec61970.base.core.test_conducting_equipment import verify_conducting_equipment_constructor_default, verify_conducting_equipment_constructor_kwargs
from zepben.ewb import Ground, generate_id


def test_ground_constructor_default():
    verify_conducting_equipment_constructor_default(Ground(mrid=generate_id()))


@given(**ground_kwargs())
def test_ground_constructor_kwargs(**kwargs):
    verify_conducting_equipment_constructor_kwargs(Ground(**kwargs), **kwargs)
