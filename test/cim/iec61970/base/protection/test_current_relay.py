#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import pytest
from hypothesis import given
from hypothesis.strategies import floats, booleans

from cim.cim_creators import FLOAT_MIN, FLOAT_MAX
from cim.iec61970.base.protection.test_protection_relay_function import protection_relay_function_kwargs, protection_relay_function_args, \
    verify_protection_relay_function_constructor_default, verify_protection_relay_function_constructor_kwargs, verify_protection_relay_function_constructor_args
from cim.property_validator import validate_property_accessor
from zepben.evolve import CurrentRelay, ProtectionKind, RelayInfo

current_relay_kwargs = {
    **protection_relay_function_kwargs,
    "current_limit_1": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    "inverse_time_flag": booleans(),
    "time_delay_1": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)
}

current_relay_args = [*protection_relay_function_args, 1.1, True, 2.2]


def test_current_relay_constructor_default():
    cr = CurrentRelay()

    verify_protection_relay_function_constructor_default(cr)
    assert cr.current_limit_1 is None
    assert cr.protection_kind is ProtectionKind.UNKNOWN
    assert cr.time_delay_1 is None


@given(**current_relay_kwargs)
def test_current_relay_constructor_kwargs(current_limit_1, inverse_time_flag, time_delay_1, **kwargs):
    cr = CurrentRelay(
        current_limit_1=current_limit_1,
        inverse_time_flag=inverse_time_flag,
        time_delay_1=time_delay_1,
        **kwargs
    )

    verify_protection_relay_function_constructor_kwargs(cr, **kwargs)
    assert cr.current_limit_1 == current_limit_1
    assert cr.inverse_time_flag == inverse_time_flag
    assert cr.time_delay_1 == time_delay_1


def test_current_relay_constructor_args():
    cr = CurrentRelay(*current_relay_args)

    verify_protection_relay_function_constructor_args(cr)
    assert cr.current_limit_1 == current_relay_args[-3]
    assert cr.inverse_time_flag == current_relay_args[-2]
    assert cr.time_delay_1 == current_relay_args[-1]
