#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from test.cim.iec61970.base.core.test_identified_object import verify_identified_object_constructor_default, verify_identified_object_constructor_kwargs, \
    verify_identified_object_constructor_args, identified_object_kwargs, identified_object_args
from zepben.evolve.model.cim.iec61968.assets.asset_function import AssetFunction

asset_function_kwargs = identified_object_kwargs
asset_function_args = identified_object_args


def verify_asset_function_constructor_default(af: AssetFunction):
    verify_identified_object_constructor_default(af)


def verify_asset_function_constructor_kwargs(af: AssetFunction, **kwargs):
    verify_identified_object_constructor_kwargs(af, **kwargs)


def verify_asset_function_constructor_args(af: AssetFunction):
    verify_identified_object_constructor_args(af)
