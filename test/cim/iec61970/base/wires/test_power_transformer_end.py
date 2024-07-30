#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import re

import pytest
from _pytest.python_api import raises
from hypothesis import given
from hypothesis.strategies import builds, integers, floats, sampled_from

from cim.collection_validator import validate_collection
from cim.iec61970.base.wires.test_transformer_end import verify_transformer_end_constructor_default, \
    verify_transformer_end_constructor_kwargs, verify_transformer_end_constructor_args, transformer_end_kwargs, transformer_end_args
from cim.cim_creators import MIN_32_BIT_INTEGER, MAX_32_BIT_INTEGER, FLOAT_MIN, FLOAT_MAX
from zepben.evolve import PowerTransformerEnd, PowerTransformer, WindingConnection, TransformerEndRatedS, TransformerCoolingType

power_transformer_end_kwargs = {
    **transformer_end_kwargs,
    "power_transformer": builds(PowerTransformer),
    "rated_s": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    "rated_u": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    "r": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "x": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "r0": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "x0": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "g": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "g0": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "b": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "b0": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "connection_kind": sampled_from(WindingConnection),
    "phase_angle_clock": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER)
}

power_transformer_end_args = [*transformer_end_args, PowerTransformer(), 1, 2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9, 10.01, WindingConnection.A, 11]


def test_power_transformer_end_constructor_default():
    pte = PowerTransformerEnd()

    verify_transformer_end_constructor_default(pte)
    assert not pte.power_transformer
    assert pte.rated_s is None
    assert not list(pte.s_ratings)
    assert pte.rated_u is None
    assert pte.r is None
    assert pte.x is None
    assert pte.r0 is None
    assert pte.x0 is None
    assert pte.g is None
    assert pte.g0 is None
    assert pte.b is None
    assert pte.b0 is None
    assert pte.connection_kind == WindingConnection.UNKNOWN_WINDING
    assert pte.phase_angle_clock is None


@given(**power_transformer_end_kwargs)
def test_power_transformer_end_constructor_kwargs(power_transformer, rated_s, rated_u, r, x, r0, x0, g, g0, b, b0, connection_kind, phase_angle_clock,
                                                  **kwargs):
    pte = PowerTransformerEnd(power_transformer=power_transformer,
                              rated_s=rated_s,
                              rated_u=rated_u,
                              r=r,
                              x=x,
                              r0=r0,
                              x0=x0,
                              g=g,
                              g0=g0,
                              b=b,
                              b0=b0,
                              connection_kind=connection_kind,
                              phase_angle_clock=phase_angle_clock,
                              **kwargs)

    verify_transformer_end_constructor_kwargs(pte, **kwargs)
    assert pte.power_transformer == power_transformer
    assert pte.rated_s == rated_s
    assert list(pte.s_ratings) == [TransformerEndRatedS(TransformerCoolingType.UNKNOWN_COOLING_TYPE, rated_s)]
    assert pte.rated_u == rated_u
    assert pte.r == r
    assert pte.x == x
    assert pte.r0 == r0
    assert pte.x0 == x0
    assert pte.g == g
    assert pte.g0 == g0
    assert pte.b == b
    assert pte.b0 == b0
    assert pte.connection_kind == connection_kind
    assert pte.phase_angle_clock == phase_angle_clock


def test_power_transformer_end_constructor_args():
    pte = PowerTransformerEnd(*power_transformer_end_args)

    verify_transformer_end_constructor_args(pte)
    assert pte.power_transformer == power_transformer_end_args[-13]
    assert pte.rated_s == power_transformer_end_args[-12]
    assert list(pte.s_ratings) == [TransformerEndRatedS(TransformerCoolingType.UNKNOWN_COOLING_TYPE, power_transformer_end_args[-12])]
    assert pte.rated_u == power_transformer_end_args[-11]
    assert pte.r == power_transformer_end_args[-10]
    assert pte.x == power_transformer_end_args[-9]
    assert pte.r0 == power_transformer_end_args[-8]
    assert pte.x0 == power_transformer_end_args[-7]
    assert pte.g == power_transformer_end_args[-6]
    assert pte.g0 == power_transformer_end_args[-5]
    assert pte.b == power_transformer_end_args[-4]
    assert pte.b0 == power_transformer_end_args[-3]
    assert pte.connection_kind == power_transformer_end_args[-2]
    assert pte.phase_angle_clock == power_transformer_end_args[-1]


def test_power_transformer_end_s_ratings():
    validate_collection(
        PowerTransformerEnd,
        lambda i, _: TransformerEndRatedS(cooling_type=TransformerCoolingType(int(i)), rated_s=int(i)),  # how python?
        PowerTransformerEnd.num_ratings,
        lambda pte, rs: pte.get_rating_by_rated_s(rs.rated_s),  # how python?
        PowerTransformerEnd.s_ratings,
        PowerTransformerEnd.add_transformer_end_rated_s,
        PowerTransformerEnd.remove_rating,
        PowerTransformerEnd.clear_ratings,
        lambda _, dup: rf"A rating for coolingType {dup.cooling_type.name} already exists, please remove it first.",
        support_duplicates=False
    )


def test_power_transformer_cant_add_rating_with_same_cooling_type():
    pte = PowerTransformerEnd()
    s_rating = TransformerEndRatedS(TransformerCoolingType.KNAF, 1)
    pte.add_transformer_end_rated_s(s_rating)

    with raises(ValueError, match=re.escape("A rating for coolingType KNAF already exists, please remove it first.")):
        s_rating2 = TransformerEndRatedS(TransformerCoolingType.KNAF, 2)
        pte.add_transformer_end_rated_s(s_rating2)
    with raises(ValueError, match=re.escape("A rating for coolingType KNAF already exists, please remove it first.")):
        pte.add_rating(TransformerCoolingType.KNAF, 3)


def test_power_transformer_remove_rating_by_cooling_type():
    pte = PowerTransformerEnd()
    for index, cooling_type in enumerate(TransformerCoolingType):
        pte.add_rating(cooling_type, index * 10)

    for index, cooling_type in enumerate(TransformerCoolingType):
        assert pte.remove_rating_by_cooling_type(cooling_type) == TransformerEndRatedS(cooling_type, index * 10)
        assert pte.num_ratings() == len(TransformerCoolingType) - (index + 1)
        assert pte.get_rating_by_cooling_type(cooling_type) is None


def test_power_transformer_rated_s_backwards_compatibility():
    pte = PowerTransformerEnd()
    pte.rated_s = 1
    assert pte.rated_s == 1
    assert list(pte.s_ratings) == [TransformerEndRatedS(TransformerCoolingType.UNKNOWN_COOLING_TYPE, 1)]
    assert pte.num_ratings() == 1
    pte.rated_s = None
    assert pte.rated_s == None
    assert not list(pte.s_ratings)
    assert pte.num_ratings() == 0

    # s_rating's can be added on top of rated_s but adding rated_s clears any existing s_rating's
    pte.rated_s = 2
    pte.add_rating(TransformerCoolingType.KNAF, 333)
    assert pte.num_ratings() == 2
    pte.rated_s = 4
    assert list(pte.s_ratings) == [TransformerEndRatedS(TransformerCoolingType.UNKNOWN_COOLING_TYPE, 4)]
    assert pte.num_ratings() == 1
    assert pte.rated_s == 4


def test_power_transformer_s_ratings_backing_field_cant_through_the_constructor():
    with raises(ValueError, match="Do not directly set s_ratings through the constructor. You have one more constructor parameter than expected."):
        PowerTransformerEnd(_s_ratings=[TransformerEndRatedS(TransformerCoolingType.UNKNOWN_COOLING_TYPE, 4)])
