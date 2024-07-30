#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from cim.iec61968.assets.test_asset import asset_kwargs, verify_asset_constructor_default, \
    verify_asset_constructor_kwargs, verify_asset_constructor_args, asset_args
from zepben.evolve import AssetContainer

asset_container_kwargs = asset_kwargs
asset_container_args = asset_args


def verify_asset_container_constructor_default(ac: AssetContainer):
    verify_asset_constructor_default(ac)


def verify_asset_container_constructor_kwargs(ac: AssetContainer, **kwargs):
    verify_asset_constructor_kwargs(ac, **kwargs)


def verify_asset_container_constructor_args(ac: AssetContainer):
    verify_asset_constructor_args(ac)
