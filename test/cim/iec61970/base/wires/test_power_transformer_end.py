#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import re

import pytest
from pytest import raises
from hypothesis import given
from hypothesis.strategies import builds, integers, floats, sampled_from
from zepben.ewb import PowerTransformerEnd, PowerTransformer, WindingConnection, TransformerCoolingType
from zepben.ewb.model.cim.extensions.iec61970.base.wires.transformer_end_rated_s import TransformerEndRatedS

from cim.cim_creators import MIN_32_BIT_INTEGER, MAX_32_BIT_INTEGER, FLOAT_MIN, FLOAT_MAX
from cim.iec61970.base.wires.test_transformer_end import verify_transformer_end_constructor_default, \
    verify_transformer_end_constructor_kwargs, verify_transformer_end_constructor_args, transformer_end_kwargs, transformer_end_args
from cim.private_collection_validator import validate_unordered_other_1234567890

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
    assert pte.connection_kind == WindingConnection.UNKNOWN
    assert pte.phase_angle_clock is None


@given(**power_transformer_end_kwargs)
def test_power_transformer_end_constructor_kwargs(power_transformer, rated_s, rated_u, r, x, r0, x0, g, g0, b, b0, connection_kind, phase_angle_clock,
                                                  **kwargs):
    pte = PowerTransformerEnd(
        power_transformer=power_transformer,
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
        **kwargs
    )

    verify_transformer_end_constructor_kwargs(pte, **kwargs)
    assert pte.power_transformer == power_transformer
    assert pte.rated_s == rated_s
    # noinspection PyArgumentList
    assert list(pte.s_ratings) == [TransformerEndRatedS(TransformerCoolingType.UNKNOWN, rated_s)]
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


from pytest import mark
@mark.skip(reason="Args are deprecated")
def test_power_transformer_end_constructor_args():
    pte = PowerTransformerEnd(*power_transformer_end_args)

    verify_transformer_end_constructor_args(pte)
    assert power_transformer_end_args[-13:-11] == [
        pte.power_transformer,
        pte.rated_s
    ]
    # We use a different style of matching here as the passed in arg for rated_s is translated to a TransformerEndRatedS.
    assert list(pte.s_ratings) == [TransformerEndRatedS(TransformerCoolingType.UNKNOWN, power_transformer_end_args[-12])]
    assert power_transformer_end_args[-11:] == [
        pte.rated_u,
        pte.r,
        pte.x,
        pte.r0,
        pte.x0,
        pte.g,
        pte.g0,
        pte.b,
        pte.b0,
        pte.connection_kind,
        pte.phase_angle_clock
    ]


def test_power_transformer_end_s_ratings():
    validate_unordered_other_1234567890(
        PowerTransformerEnd,
        lambda i: TransformerEndRatedS(cooling_type=TransformerCoolingType(int(i)), rated_s=int(i)),  # how python?
        PowerTransformerEnd.s_ratings,
        PowerTransformerEnd.num_ratings,
        PowerTransformerEnd.get_rating,
        PowerTransformerEnd.add_transformer_end_rated_s,
        PowerTransformerEnd.remove_rating,
        PowerTransformerEnd.clear_ratings,
        lambda rs: rs.cooling_type,
        lambda ct: ct.name
    )


def test_power_transformer_cant_add_rating_with_same_cooling_type():
    pte = PowerTransformerEnd()
    s_rating = TransformerEndRatedS(TransformerCoolingType.KNAF, 1)
    pte.add_transformer_end_rated_s(s_rating)

    with raises(ValueError, match=re.escape("A rating for coolingType KNAF already exists, please remove it first.")):
        s_rating2 = TransformerEndRatedS(TransformerCoolingType.KNAF, 2)
        pte.add_transformer_end_rated_s(s_rating2)
    with raises(ValueError, match=re.escape("A rating for coolingType KNAF already exists, please remove it first.")):
        pte.add_rating(3, TransformerCoolingType.KNAF)


def test_power_transformer_remove_rating_by_cooling_type():
    pte = PowerTransformerEnd()
    for index, cooling_type in enumerate(TransformerCoolingType):
        pte.add_rating(index * 10, cooling_type)

    for index, cooling_type in enumerate(TransformerCoolingType):
        assert pte.remove_rating_by_cooling_type(cooling_type) == TransformerEndRatedS(cooling_type, index * 10)
        assert pte.num_ratings() == len(TransformerCoolingType) - (index + 1)
        with pytest.raises(KeyError):
            pte.get_rating(cooling_type)


def test_power_transformer_rated_s_backwards_compatibility():
    pte = PowerTransformerEnd()
    pte.rated_s = 1
    assert pte.rated_s == 1
    assert list(pte.s_ratings) == [TransformerEndRatedS(TransformerCoolingType.UNKNOWN, 1)]
    assert pte.num_ratings() == 1
    pte.rated_s = None
    assert pte.rated_s is None
    assert not list(pte.s_ratings)
    assert pte.num_ratings() == 0

    # s_rating's can be added on top of rated_s but adding rated_s clears any existing s_rating's
    pte.rated_s = 2
    pte.add_rating(333, TransformerCoolingType.KNAF)
    assert pte.num_ratings() == 2
    pte.rated_s = 4
    assert list(pte.s_ratings) == [TransformerEndRatedS(TransformerCoolingType.UNKNOWN, 4)]
    assert pte.num_ratings() == 1
    assert pte.rated_s == 4


def test_power_transformer_s_ratings_backing_field_cant_through_the_constructor():
    with raises(ValueError, match="Do not directly set s_ratings through the constructor. You have one more constructor parameter than expected."):
        PowerTransformerEnd(_s_ratings=[TransformerEndRatedS(TransformerCoolingType.UNKNOWN, 4)])
