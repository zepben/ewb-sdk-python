#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from hypothesis.strategies import booleans

from test.cim.iec61968.assets.test_asset_function import asset_function_kwargs, asset_function_args, verify_asset_function_constructor_default, \
    verify_asset_function_constructor_kwargs, verify_asset_function_constructor_args
from zepben.ewb.model.cim.iec61968.metering.end_device_function import EndDeviceFunction

end_device_function_kwargs = {
    **asset_function_kwargs,
    "enabled": booleans(),
}

end_device_function_args = [*asset_function_args, False]


def verify_end_device_function_constructor_default(edf: EndDeviceFunction):
    verify_asset_function_constructor_default(edf)
    assert edf.enabled == True


def verify_end_device_function_constructor_kwargs(edf: EndDeviceFunction, enabled, **kwargs):
    verify_asset_function_constructor_kwargs(edf, **kwargs)
    assert edf.enabled == enabled


def verify_end_device_function_constructor_args(edf: EndDeviceFunction):
    verify_asset_function_constructor_args(edf)
    assert end_device_function_args[-1:] == [
        edf.enabled
    ]
