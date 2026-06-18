#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from cim.fill_fields import base_voltage_kwargs
from cim.iec61970.base.core.test_identified_object import verify_identified_object_constructor_default, \
    verify_identified_object_constructor_kwargs, identified_object_args
from hypothesis import given

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
