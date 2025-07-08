#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["VoltageRelay"]

from zepben.ewb.model.cim.extensions.iec61970.base.protection.protection_relay_function import ProtectionRelayFunction

from zepben.ewb.model.cim.extensions.zbex import zbex


@zbex
class VoltageRelay(ProtectionRelayFunction):
    """
    [ZBEX]
    A device that detects when the voltage in an AC circuit reaches a preset voltage. There are two basic types of voltage relay operation: overvoltage
    relay for overvoltage detection and undervoltage relay for undervoltage detection.
    """
    pass
