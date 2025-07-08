#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["Fuse"]

from typing import Optional, TYPE_CHECKING

from zepben.ewb.model.cim.iec61970.base.wires.switch import Switch

if TYPE_CHECKING:
    from zepben.ewb.model.cim.extensions.iec61970.base.protection.protection_relay_function import ProtectionRelayFunction


class Fuse(Switch):
    """
    An overcurrent protective device with a circuit opening fusible part that is heated and severed by the passage of
    overcurrent through it. A fuse is considered a switching device because it breaks current.
    """

    function: Optional['ProtectionRelayFunction'] = None
    """The function implemented by this Fuse"""
