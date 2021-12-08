#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given

from test.cim.extract_testing_args import extract_testing_args
from test.cim.iec61970.base.core.test_identified_object import identified_object_kwargs, verify_identified_object_constructor_default, \
    verify_identified_object_constructor_kwargs, verify_identified_object_constructor_args, identified_object_args
from hypothesis.strategies import integers

from test.cim.cim_creators import MIN_32_BIT_INTEGER, MAX_32_BIT_INTEGER
from zepben.evolve import BaseVoltage
from zepben.evolve.model.cim.iec61970.base.core.create_core_components import create_base_voltage

base_voltage_kwargs = {
    **identified_object_kwargs,
    "nominal_voltage": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER)
}

base_voltage_args = [*identified_object_args, 1]


def test_base_voltage_constructor_default():
    bv = BaseVoltage()
    bv2 = create_base_voltage()
    validate_default_base_voltage(bv)
    validate_default_base_voltage(bv2)


def validate_default_base_voltage(bv):
    verify_identified_object_constructor_default(bv)
    assert bv.nominal_voltage == 0


@given(**base_voltage_kwargs)
def test_base_voltage_constructor_kwargs(nominal_voltage, **kwargs):
    args = extract_testing_args(locals())
    bv = BaseVoltage(**args, **kwargs)
    validate_base_voltage_values(bv, **args, **kwargs)


@given(**base_voltage_kwargs)
def test_base_voltage_constructor_kwargs(nominal_voltage, **kwargs):
    args = extract_testing_args(locals())
    bv = create_base_voltage(**args, **kwargs)
    validate_base_voltage_values(bv, **args, **kwargs)


def validate_base_voltage_values(bv, nominal_voltage, **kwargs):
    verify_identified_object_constructor_kwargs(bv, **kwargs)
    assert bv.nominal_voltage == nominal_voltage


def test_base_voltage_constructor_args():
    # noinspection PyArgumentList
    bv = BaseVoltage(*base_voltage_args)

    verify_identified_object_constructor_args(bv)
    assert bv.nominal_voltage == base_voltage_args[-1]
