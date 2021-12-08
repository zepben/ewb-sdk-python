#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from hypothesis import given
from hypothesis.strategies import floats

from test.cim import extract_testing_args
from test.cim.iec61970.base.wires.test_shunt_compensator import verify_shunt_compensator_constructor_default, \
    verify_shunt_compensator_constructor_kwargs, verify_shunt_compensator_constructor_args, shunt_compensator_kwargs, shunt_compensator_args
from test.cim.cim_creators import FLOAT_MIN, FLOAT_MAX
from zepben.evolve import LinearShuntCompensator
from zepben.evolve.model.cim.iec61970.base.wires.create_wires_components import create_linear_shunt_compensator

linear_shunt_compensator_kwargs = {
    **shunt_compensator_kwargs,
    "b0_per_section": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "b_per_section": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "g0_per_section": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "g_per_section": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)
}

linear_shunt_compensator_args = [*shunt_compensator_args, 1.1, 2.2, 3.3, 4.4]


def test_linear_shunt_compensator_constructor_default():
    lsc = LinearShuntCompensator()
    lsc2 = create_linear_shunt_compensator()
    validate_default_linear_shunt_compensator_constructor(lsc)
    validate_default_linear_shunt_compensator_constructor(lsc2)


def validate_default_linear_shunt_compensator_constructor(lsc):
    verify_shunt_compensator_constructor_default(lsc)
    assert lsc.b0_per_section is None
    assert lsc.b_per_section is None
    assert lsc.g0_per_section is None
    assert lsc.g_per_section is None


@given(**linear_shunt_compensator_kwargs)
def test_linear_shunt_compensator_constructor_kwargs(b0_per_section, b_per_section, g0_per_section, g_per_section, **kwargs):
    args = extract_testing_args(locals())
    lsc = LinearShuntCompensator(**args, **kwargs)
    validate_linear_shunt_compensator_values(lsc, **args, **kwargs)


@given(**linear_shunt_compensator_kwargs)
def test_linear_shunt_compensator_creator(b0_per_section, b_per_section, g0_per_section, g_per_section, **kwargs):
    args = extract_testing_args(locals())
    lsc = create_linear_shunt_compensator(**args, **kwargs)
    validate_linear_shunt_compensator_values(lsc, **args, **kwargs)


def validate_linear_shunt_compensator_values(lsc, b0_per_section, b_per_section, g0_per_section, g_per_section, **kwargs):
    verify_shunt_compensator_constructor_kwargs(lsc, **kwargs)
    assert lsc.b0_per_section == b0_per_section
    assert lsc.b_per_section == b_per_section
    assert lsc.g0_per_section == g0_per_section
    assert lsc.g_per_section == g_per_section


def test_linear_shunt_compensator_constructor_args():
    lsc = LinearShuntCompensator(*linear_shunt_compensator_args)

    verify_shunt_compensator_constructor_args(lsc)
    assert lsc.b0_per_section == linear_shunt_compensator_args[-4]
    assert lsc.b_per_section == linear_shunt_compensator_args[-3]
    assert lsc.g0_per_section == linear_shunt_compensator_args[-2]
    assert lsc.g_per_section == linear_shunt_compensator_args[-1]
