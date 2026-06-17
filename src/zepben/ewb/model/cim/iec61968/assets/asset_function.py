from abc import ABCMeta

#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from zepben.ewb.dataclass_descriptors import zb_dataclass

__all__ = ["AssetFunction"]

from zepben.ewb.model.cim.iec61970.base.core.identified_object import IdentifiedObject


@zb_dataclass
class AssetFunction(IdentifiedObject, metaclass=ABCMeta):
    """
    Function performed by an asset.
    """
    pass
