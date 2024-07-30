#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Optional

from zepben.evolve.model.cim.iec61970.base.protection.protection_relay_function import ProtectionRelayFunction

__all__ = ["DistanceRelay"]


class DistanceRelay(ProtectionRelayFunction):
    """
    A protective device used in power systems that measures the impedance of a transmission line to determine the distance to a fault, and initiates
    circuit breaker tripping to isolate the faulty section and safeguard the power system.
    """

    backward_blind: Optional[float] = None
    """The reverse blind impedance (in ohms) that defines the area to be blinded in the opposite direction of the power flow."""

    backward_reach: Optional[float] = None
    """The reverse reach impedance (in ohms) that determines the maximum distance along the transmission line in the opposite direction of power flow for 
    which the relay will provide protection."""

    backward_reactance: Optional[float] = None
    """The reverse reactance (in ohms) that determines the maximum distance along the transmission line in the opposite direction of power flow for which the 
    relay will provide protection."""

    forward_blind: Optional[float] = None
    """The forward blind impedance (in ohms) that defines the area to be blinded in the opposite direction of the power flow."""

    forward_reach: Optional[float] = None
    """The forward reach impedance (in ohms) that determines the maximum distance along the transmission line in the opposite direction of power flow for 
    which the relay will provide protection."""

    forward_reactance: Optional[float] = None
    """The forward reactance (in ohms) that determines the maximum distance along the transmission line in the opposite direction of power flow for which the 
    relay will provide protection."""

    operation_phase_angle1: Optional[float] = None
    """The phase angle (in degrees) between voltage and current during normal operating conditions for zone 1 relay."""

    operation_phase_angle2: Optional[float] = None
    """The phase angle (in degrees) between voltage and current during normal operating conditions for zone 2 relay."""

    operation_phase_angle3: Optional[float] = None
    """The phase angle (in degrees) between voltage and current during normal operating conditions for zone 3 relay."""
