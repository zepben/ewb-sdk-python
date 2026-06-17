from abc import ABCMeta

#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from zepben.ewb.dataclass_descriptors import zb_dataclass

__all__ = ["EndDeviceFunction"]

from zepben.ewb.model.cim.iec61968.assets.asset_function import AssetFunction


@zb_dataclass
class EndDeviceFunction(AssetFunction, metaclass=ABCMeta):
    """
    Function performed by an end device such as a meter, communication equipment, controllers, etc.
    """

    enabled: bool = True
    """True if the function is enabled."""
