#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Optional

from zepben.evolve.model.cim.iec61970.base.wires.energy_connection import RegulatingCondEq
from zepben.evolve.model.cim.iec61970.base.wires.svc_control_mode import SVCControlMode

__all__ = ["StaticVarCompensator"]


class StaticVarCompensator(RegulatingCondEq):
    """
    A facility for providing variable and controllable shunt reactive power.The SVC typically consists of a step-down transformer, filter, thyristor-controlled reactor,
    and thyristor-switched capacitor arms. The SVC may operate in fixed MVar output mode or in voltage control mode. When in voltage control mode, the output of
    the SVC will be proportional to the deviation of voltage at the controlled bus from the voltage set-point. The SVC characteristic slope defines the proportion.
    If the voltage at the controlled bus is equal to the voltage set-point, the SVC MVar output is zero.
    """
    capacitive_rating: Optional[float] = None
    """Capacitive reactance in Ohms at maximum capacitive reactive power. Shall always be positive."""

    inductive_rating: Optional[float] = None
    """Inductive reactance in Ohms at maximum inductive reactive power. Shall always be negative."""

    q: Optional[float] = None
    """
    Reactive power injection in VAr. Load sign convention is used, i.e. positive sign means flow out from a node. 
    Starting value for a steady state solution.
    """

    svc_control_mode: SVCControlMode = SVCControlMode.UNKNOWN
    """SVC control mode."""

    voltage_set_point: Optional[int] = None
    """
    The reactive power output of the SVC is proportional to the difference between the voltage at the regulated bus and the voltage set-point.
    When the regulated bus voltage is equal to the voltage set-point, the reactive power output is zero. Must be in volts.
    """
