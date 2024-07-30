#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from hypothesis import given
from hypothesis.strategies import sampled_from

from cim.iec61970.base.auxiliaryequipment.test_sensor import sensor_kwargs, verify_sensor_constructor_default, \
    verify_sensor_constructor_kwargs, verify_sensor_constructor_args, sensor_args
from cim.property_validator import validate_property_accessor
from zepben.evolve import PotentialTransformer, PotentialTransformerInfo, PotentialTransformerKind

potential_transformer_kwargs = {
    **sensor_kwargs,
    "type": sampled_from(PotentialTransformerKind)
}
potential_transformer_args = [*sensor_args, PotentialTransformerKind.capacitiveCoupling]


def test_potential_transformer_constructor_default():
    vt = PotentialTransformer()

    verify_sensor_constructor_default(vt)
    assert vt.type == PotentialTransformerKind.UNKNOWN


# noinspection PyShadowingBuiltins
@given(**potential_transformer_kwargs)
def test_potential_transformer_constructor_kwargs(type, **kwargs):
    # noinspection PyArgumentList
    vt = PotentialTransformer(type=type, **kwargs)

    verify_sensor_constructor_kwargs(vt, **kwargs)
    assert vt.type == type


def test_potential_transformer_constructor_args():
    # noinspection PyArgumentList
    vt = PotentialTransformer(*potential_transformer_args)

    verify_sensor_constructor_args(vt)
    assert vt.type == potential_transformer_args[-1]


def test_potential_transformer_info_accessor():
    validate_property_accessor(PotentialTransformer, PotentialTransformerInfo, PotentialTransformer.potential_transformer_info)
