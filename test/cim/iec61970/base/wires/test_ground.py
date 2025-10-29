#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from hypothesis import given

from cim.iec61970.base.core.test_conducting_equipment import verify_conducting_equipment_constructor_default, verify_conducting_equipment_constructor_kwargs, verify_conducting_equipment_constructor_args, \
    conducting_equipment_kwargs, conducting_equipment_args
from zepben.ewb import Ground

ground_kwargs = conducting_equipment_kwargs
ground_args = conducting_equipment_args


def test_ground_constructor_default():
    verify_conducting_equipment_constructor_default(Ground())


@given(**ground_kwargs)
def test_ground_constructor_kwargs(**kwargs):
    verify_conducting_equipment_constructor_kwargs(Ground(**kwargs), **kwargs)


from pytest import mark
@mark.skip(reason="Args are deprecated")
def test_ground_constructor_args():
    verify_conducting_equipment_constructor_args(Ground(*ground_args))
