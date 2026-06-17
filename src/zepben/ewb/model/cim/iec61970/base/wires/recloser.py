#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from zepben.ewb.dataclass_descriptors import zb_dataclass


__all__ = ["Recloser"]

from zepben.ewb.model.cim.iec61970.base.wires.protected_switch import ProtectedSwitch


@zb_dataclass
class Recloser(ProtectedSwitch):
    """
    Pole-mounted fault interrupter with built-in phase and ground relays, current transformer (CT), and supplemental controls.
    """
    pass
