#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given

from cim.iec61970.base.protection.test_protection_relay_function import protection_relay_function_kwargs, protection_relay_function_args, \
    verify_protection_relay_function_constructor_default, verify_protection_relay_function_constructor_kwargs, verify_protection_relay_function_constructor_args
from zepben.evolve import VoltageRelay

voltage_relay_kwargs = {
    **protection_relay_function_kwargs
}

voltage_relay_args = [*protection_relay_function_args]


def test_voltage_relay_constructor_default():
    vr = VoltageRelay()

    verify_protection_relay_function_constructor_default(vr)


@given(**voltage_relay_kwargs)
def test_voltage_relay_constructor_kwargs(**kwargs):
    vr = VoltageRelay(**kwargs)
    verify_protection_relay_function_constructor_kwargs(vr, **kwargs)


def test_voltage_relay_constructor_args():
    vr = VoltageRelay(*voltage_relay_args)

    verify_protection_relay_function_constructor_args(vr)
