#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from hypothesis import given

from cim.fill_fields import current_transformer_kwargs
from cim.iec61970.base.auxiliaryequipment.test_sensor import verify_sensor_constructor_default, \
    verify_sensor_constructor_kwargs, verify_sensor_constructor_args, sensor_args
from zepben.ewb import CurrentTransformer, generate_id

current_transformer_args = [*sensor_args, 1]


def test_current_transformer_constructor_default():
    ct = CurrentTransformer(mrid=generate_id())

    verify_sensor_constructor_default(ct)
    assert ct.core_burden is None


@given(**current_transformer_kwargs())
def test_current_transformer_constructor_kwargs(core_burden, **kwargs):
    ct = CurrentTransformer(core_burden=core_burden, **kwargs)

    verify_sensor_constructor_kwargs(ct, **kwargs)
    assert ct.core_burden == core_burden


def test_current_transformer_constructor_args():
    ct = CurrentTransformer(*current_transformer_args)

    verify_sensor_constructor_args(ct)
    assert current_transformer_args[-1:] == [
        ct.core_burden
    ]
