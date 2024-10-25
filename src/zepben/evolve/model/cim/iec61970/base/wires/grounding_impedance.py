#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Optional

from zepben.evolve.model.cim.iec61970.base.wires.earth_fault_compensator import EarthFaultCompensator


class GroundingImpedance(EarthFaultCompensator):
    """
    A fixed impedance device used for grounding.
    """

    x: Optional[float] = None
    """Reactance of device in ohms."""
