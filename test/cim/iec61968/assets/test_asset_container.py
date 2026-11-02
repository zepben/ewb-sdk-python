#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from cim.iec61968.assets.test_asset import verify_asset_constructor_default, \
    verify_asset_constructor_kwargs
from zepben.ewb.model.cim.iec61968.assets.asset_container import AssetContainer


def verify_asset_container_constructor_default(ac: AssetContainer):
    verify_asset_constructor_default(ac)


def verify_asset_container_constructor_kwargs(ac: AssetContainer, **kwargs):
    verify_asset_constructor_kwargs(ac, **kwargs)
