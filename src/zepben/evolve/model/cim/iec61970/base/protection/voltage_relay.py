#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve.model.cim.iec61970.base.protection.protection_relay_function import ProtectionRelayFunction

__all__ = ["VoltageRelay"]


class VoltageRelay(ProtectionRelayFunction):
    """
    A device that detects when the voltage in an AC circuit reaches a preset voltage. There are two basic types of voltage relay operation: overvoltage
    relay for overvoltage detection and undervoltage relay for undervoltage detection.
    """
    pass
