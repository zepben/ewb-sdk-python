#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from hypothesis.strategies import builds, booleans

from test.cim.iec61968.assets.test_asset_function import asset_function_kwargs, asset_function_args, verify_asset_function_constructor_default, \
    verify_asset_function_constructor_kwargs, verify_asset_function_constructor_args
from zepben.evolve import EndDevice, EndDeviceFunction

end_device_function_kwargs = {
    **asset_function_kwargs,
    "end_device": builds(EndDevice),
    "enabled": booleans(),
}

end_device_function_args = [*asset_function_args, EndDeviceFunction(), False]


def verify_end_device_function_constructor_default(edf: EndDeviceFunction):
    verify_asset_function_constructor_default(edf)
    assert edf.end_device is None
    assert edf.enabled == True


def verify_end_device_function_constructor_kwargs(edf: EndDeviceFunction, end_device, enabled, **kwargs):
    verify_asset_function_constructor_kwargs(edf, **kwargs)
    assert edf.end_device == end_device
    assert edf.enabled == enabled


def verify_end_device_function_constructor_args(edf: EndDeviceFunction):
    verify_asset_function_constructor_args(edf)
    assert end_device_function_args[-2:] == [
        edf.end_device,
        edf.enabled
    ]
