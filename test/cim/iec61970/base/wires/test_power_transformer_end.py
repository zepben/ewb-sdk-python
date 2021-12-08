#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import builds, integers, floats, sampled_from

from test.cim.extract_testing_args import extract_testing_args
from test.cim.iec61970.base.wires.test_transformer_end import verify_transformer_end_constructor_default, \
    verify_transformer_end_constructor_kwargs, verify_transformer_end_constructor_args, transformer_end_kwargs, transformer_end_args
from test.cim.cim_creators import MIN_32_BIT_INTEGER, MAX_32_BIT_INTEGER, FLOAT_MIN, FLOAT_MAX
from zepben.evolve import PowerTransformerEnd, PowerTransformer, WindingConnection
from zepben.evolve.model.cim.iec61970.base.wires.create_wires_components import create_power_transformer_end

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
    pte2 = create_power_transformer_end()
    validate_default_power_transformer_end_constructor(pte)
    validate_default_power_transformer_end_constructor(pte2)


def validate_default_power_transformer_end_constructor(pte):
    verify_transformer_end_constructor_default(pte)
    assert not pte.power_transformer
    assert pte.rated_s is None
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
    args = extract_testing_args(locals())
    pte = PowerTransformerEnd(**args, **kwargs)
    validate_power_transformer_end_values(pte, **args, **kwargs)


@given(**power_transformer_end_kwargs)
def test_power_transformer_end_creator(power_transformer, rated_s, rated_u, r, x, r0, x0, g, g0, b, b0, connection_kind, phase_angle_clock, **kwargs):
    args = extract_testing_args(locals())
    pte = create_power_transformer_end(**args, **kwargs)
    validate_power_transformer_end_values(pte, **args, **kwargs)


def validate_power_transformer_end_values(pte, power_transformer, rated_s, rated_u, r, x, r0, x0, g, g0, b, b0, connection_kind, phase_angle_clock, **kwargs):
    verify_transformer_end_constructor_kwargs(pte, **kwargs)
    assert pte.power_transformer == power_transformer
    assert pte.rated_s == rated_s
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
