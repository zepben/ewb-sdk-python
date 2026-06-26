#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["LoadBreakSwitch"]

from zepben.ewb.model.cim.iec61970.base.wires.protected_switch import ProtectedSwitch
from zepben.ewb.dataclass_descriptors import zb_dataclass


@zb_dataclass
class LoadBreakSwitch(ProtectedSwitch):
    """A mechanical switching device capable of making, carrying, and breaking currents under normal operating
    conditions. """
    pass
