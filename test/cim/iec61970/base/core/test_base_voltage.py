#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given

from cim.iec61970.base.core.test_identified_object import identified_object_kwargs, verify_identified_object_constructor_default, \
    verify_identified_object_constructor_kwargs, verify_identified_object_constructor_args, identified_object_args
from hypothesis.strategies import integers

from cim.cim_creators import MIN_32_BIT_INTEGER, MAX_32_BIT_INTEGER
from zepben.evolve import BaseVoltage

base_voltage_kwargs = {
    **identified_object_kwargs,
    "nominal_voltage": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER)
}

base_voltage_args = [*identified_object_args, 1]


def test_base_voltage_constructor_default():
    bv = BaseVoltage()

    verify_identified_object_constructor_default(bv)
    assert bv.nominal_voltage == 0


@given(**base_voltage_kwargs)
def test_base_voltage_constructor_kwargs(nominal_voltage, **kwargs):
    # noinspection PyArgumentList
    bv = BaseVoltage(nominal_voltage=nominal_voltage, **kwargs)

    verify_identified_object_constructor_kwargs(bv, **kwargs)
    assert bv.nominal_voltage == nominal_voltage


def test_base_voltage_constructor_args():
    # noinspection PyArgumentList
    bv = BaseVoltage(*base_voltage_args)

    verify_identified_object_constructor_args(bv)
    assert bv.nominal_voltage == base_voltage_args[-1]
