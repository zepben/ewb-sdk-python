#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["RemotePoint"]

from abc import ABCMeta

from zepben.ewb.model.cim.iec61970.base.core.identified_object import IdentifiedObject
from zepben.ewb.dataclass_descriptors import zb_dataclass


@zb_dataclass
class RemotePoint(IdentifiedObject, metaclass=ABCMeta):
    """
    For a RTU remote points correspond to telemetered values or control outputs. Other units (e.g. control centers)
    usually also contain calculated values.
    """
    pass
