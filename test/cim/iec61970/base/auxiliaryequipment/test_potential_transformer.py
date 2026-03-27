#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from hypothesis import given

from cim.fill_fields import potential_transformer_kwargs
from cim.iec61970.base.auxiliaryequipment.test_sensor import verify_sensor_constructor_default, \
    verify_sensor_constructor_kwargs, verify_sensor_constructor_args, sensor_args
from zepben.ewb import PotentialTransformer, PotentialTransformerKind, generate_id

potential_transformer_args = [*sensor_args, PotentialTransformerKind.capacitiveCoupling]


def test_potential_transformer_constructor_default():
    vt = PotentialTransformer(mrid=generate_id())

    verify_sensor_constructor_default(vt)
    assert vt.type == PotentialTransformerKind.UNKNOWN


# noinspection PyShadowingBuiltins
@given(**potential_transformer_kwargs())
def test_potential_transformer_constructor_kwargs(type, **kwargs):
    vt = PotentialTransformer(type=type, **kwargs)

    verify_sensor_constructor_kwargs(vt, **kwargs)
    assert vt.type == type


def test_potential_transformer_constructor_args():
    vt = PotentialTransformer(*potential_transformer_args)

    verify_sensor_constructor_args(vt)
    assert potential_transformer_args[-1:] == [
        vt.type
    ]
