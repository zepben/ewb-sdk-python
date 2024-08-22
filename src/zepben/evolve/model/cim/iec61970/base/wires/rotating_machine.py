#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Optional

from zepben.evolve.model.cim.iec61970.base.wires.energy_connection import RegulatingCondEq


class RotatingMachine(RegulatingCondEq):
    """
    A rotating machine which may be used as a generator or motor.
    """

    rated_power_factor: Optional[float] = None
    """Power factor (nameplate data). It is primarily used for short circuit data exchange according to IEC 60909. The attribute cannot be a negative value."""

    rated_s: Optional[float] = None
    """Nameplate apparent power rating for the unit in volt-amperes (VA). The attribute shall have a positive value."""

    rated_u: Optional[int] = None
    """
    Rated voltage in volts (nameplate data, Ur in IEC 60909-0). It is primarily used for short circuit data exchange according to IEC 60909.
    The attribute shall be a positive value.
    """

    p: Optional[float] = None
    """
    Active power injection in watts. Load sign convention is used, i.e. positive sign means flow out from a node. Starting value for a steady state solution.
    """

    q: Optional[float] = None
    """Reactive power injection. Load sign convention is used, i.e. positive sign means flow out from a node. Starting value for a steady state solution."""
