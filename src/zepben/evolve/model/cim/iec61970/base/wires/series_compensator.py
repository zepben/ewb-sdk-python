#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Optional

from zepben.evolve.model.cim.iec61970.base.core.conducting_equipment import ConductingEquipment

__all__ = ["SeriesCompensator"]


class SeriesCompensator(ConductingEquipment):
    """
    A Series Compensator is a series capacitor or reactor or an AC transmission line without charging susceptance. It is a two terminal device.
    """
    r: Optional[float] = None
    """Positive sequence resistance in ohms."""

    r0: Optional[float] = None
    """Zero sequence resistance in ohms."""

    x: Optional[float] = None
    """Positive sequence reactance in ohms."""

    x0: Optional[float] = None
    """Zero sequence reactance in ohms."""

    varistor_rated_current: Optional[int] = None
    """
    The maximum current in amps the varistor is designed to handle at specified duration. It is used for short circuit calculations. The attribute shall 
    be a positive value. If null and varistorVoltageThreshold is null, a varistor is not present.
    """

    varistor_voltage_threshold: Optional[int] = None
    """
    The dc voltage in volts at which the varistor starts conducting. It is used for short circuit calculations. If null and varistorRatedCurrent is null, 
    a varistor is not present.
    """

    def varistor_present(self) -> bool:
        return self.varistor_rated_current is not None or self.varistor_voltage_threshold is not None
