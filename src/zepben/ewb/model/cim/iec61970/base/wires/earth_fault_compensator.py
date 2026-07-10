#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["EarthFaultCompensator"]

from typing import Optional
from abc import ABCMeta

from zepben.ewb.model.cim.iec61970.base.core.conducting_equipment import ConductingEquipment
from zepben.ewb.dataclass_descriptors.dataclass_base import zb_dataclass


@zb_dataclass
class EarthFaultCompensator(ConductingEquipment, metaclass=ABCMeta):
    """
    A conducting equipment used to represent a connection to ground which is typically used to compensate earth faults. An earth fault compensator device
    modelled with a single terminal implies a second terminal solidly connected to ground. If two terminals are modelled, the ground is not assumed and
    normal connection rules apply.
    """

    r: Optional[float] = None
    """Nominal resistance of device in ohms."""
