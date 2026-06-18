#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["ConnectivityNodeContainer"]

from abc import ABCMeta

from zepben.ewb.dataclass_descriptors import zb_dataclass
from zepben.ewb.model.cim.iec61970.base.core.power_system_resource import PowerSystemResource


@zb_dataclass
class ConnectivityNodeContainer(PowerSystemResource, metaclass=ABCMeta):
    """
    A base class for all objects that may contain connectivity nodes or topological nodes.
    """
    pass
