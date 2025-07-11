#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["PetersenCoil"]

from typing import Optional

from zepben.ewb.model.cim.iec61970.base.wires.earth_fault_compensator import EarthFaultCompensator


class PetersenCoil(EarthFaultCompensator):
    """
    A variable impedance device normally used to offset line charging during single line faults in an ungrounded section of network.
    """

    x_ground_nominal: Optional[float] = None
    """
    The nominal reactance. This is the operating point (normally over compensation) that is defined based on the resonance point in the
    healthy network condition. The impedance is calculated based on nominal voltage divided by position current.
    """
