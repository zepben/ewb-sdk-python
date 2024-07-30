#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from cim.iec61970.base.core.test_identified_object import identified_object_kwargs, verify_identified_object_constructor_default, \
    verify_identified_object_constructor_kwargs, verify_identified_object_constructor_args, identified_object_args
from zepben.evolve import AssetInfo

asset_info_kwargs = identified_object_kwargs
asset_info_args = identified_object_args


def verify_asset_info_constructor_default(ai: AssetInfo):
    verify_identified_object_constructor_default(ai)


def verify_asset_info_constructor_kwargs(ai: AssetInfo, **kwargs):
    verify_identified_object_constructor_kwargs(ai, **kwargs)


def verify_asset_info_constructor_args(ai: AssetInfo):
    verify_identified_object_constructor_args(ai)
