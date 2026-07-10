#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["EndDeviceFunction"]

from abc import ABCMeta

from zepben.ewb.model.cim.iec61968.assets.asset_function import AssetFunction
from zepben.ewb.dataclass_descriptors.dataclass_base import zb_dataclass


@zb_dataclass
class EndDeviceFunction(AssetFunction, metaclass=ABCMeta):
    """
    Function performed by an end device such as a meter, communication equipment, controllers, etc.
    """

    enabled: bool = True
    """True if the function is enabled."""
