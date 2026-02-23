#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ['DirectionalCurrentRelay']

from zepben.ewb.model.cim.extensions.iec61970.base.protection.protection_relay_function import ProtectionRelayFunction
from zepben.ewb.model.cim.iec61970.base.core.phase_code import PhaseCode
from zepben.ewb.model.cim.extensions.iec61970.base.protection.polarizing_quantity_type import PolarizingQuantityType
from zepben.ewb.model.cim.extensions.zbex import zbex


@zbex
class DirectionalCurrentRelay(ProtectionRelayFunction):
    """
    [ZBEX] A Directional Current Relay is a type of protective relay used in electrical power systems to detect the direction of current flow and operate only
    when the current exceeds a certain threshold in a specified direction.
    """
    #zbex
    directional_characteristic_angle: float | None = None
    """[ZBEX] The characteristic angle (in degrees) that defines the boundary between the operate and restrain regions of the directional element, relative 
    to the polarizing quantity. Often referred to as Maximum Torque Angle (MTA) or Relay Characteristic Angle (RCA)"""

    polarizing_quantity_type: PolarizingQuantityType = PolarizingQuantityType.UNKNOWN
    """[ZBEX] Specifies the type of voltage to be used for polarization. This guides the selection/derivation of voltage from the VTs."""

    relay_element_phase: PhaseCode = PhaseCode.NONE
    """[ZBEX] The phase associated with this directional relay element. This helps in selecting the correct 'self-phase' or other phase-derived."""

    minimum_pickup_current: float | None = None
    """[ZBEX] The minimum current magnitude required for the directional element to operate reliably and determine direction. This might be different from 
    the main pickupCurrent for the overcurrent function."""

    current_limit_1: float | None = None
    """[ZBEX]Current limit number 1 for inverse time pickup in amperes."""

    inverse_time_flag: bool | None = None
    """[ZBEX] Set True if the current relay has inverse time characteristics."""

    time_delay_1: float | None = None
    """[ZBEX] Inverse time delay number 1 for current limit number 1 in seconds."""
