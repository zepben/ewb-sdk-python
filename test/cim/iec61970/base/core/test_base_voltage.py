#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given

from cim.fill_fields import base_voltage_kwargs
from cim.iec61970.base.core.test_identified_object import verify_identified_object_constructor_default, \
    verify_identified_object_constructor_kwargs, verify_identified_object_constructor_args, identified_object_args
from zepben.ewb import BaseVoltage, generate_id

base_voltage_args = [*identified_object_args, 1]


def test_base_voltage_constructor_default():
    bv = BaseVoltage(mrid=generate_id())

    verify_identified_object_constructor_default(bv)
    assert bv.nominal_voltage == 0


@given(**base_voltage_kwargs())
def test_base_voltage_constructor_kwargs(nominal_voltage, **kwargs):
    bv = BaseVoltage(nominal_voltage=nominal_voltage, **kwargs)

    verify_identified_object_constructor_kwargs(bv, **kwargs)
    assert bv.nominal_voltage == nominal_voltage


def test_base_voltage_constructor_args():
    bv = BaseVoltage(*base_voltage_args)

    verify_identified_object_constructor_args(bv)
    assert base_voltage_args[-1:] == [
        bv.nominal_voltage
    ]
