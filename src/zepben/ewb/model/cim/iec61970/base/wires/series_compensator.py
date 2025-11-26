#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["SeriesCompensator"]

from zepben.ewb.dataslot import dataslot
from zepben.ewb.model.cim.iec61970.base.core.conducting_equipment import ConductingEquipment


@dataslot
class SeriesCompensator(ConductingEquipment):
    """
    A Series Compensator is a series capacitor or reactor or an AC transmission line without charging susceptance. It is a two terminal device.
    """
    r: float | None = None
    """Positive sequence resistance in ohms."""

    r0: float | None = None
    """Zero sequence resistance in ohms."""

    x: float | None = None
    """Positive sequence reactance in ohms."""

    x0: float | None = None
    """Zero sequence reactance in ohms."""

    varistor_rated_current: int | None = None
    """
    The maximum current in amps the varistor is designed to handle at specified duration. It is used for short circuit calculations. The attribute shall 
    be a positive value. If null and varistorVoltageThreshold is null, a varistor is not present.
    """

    varistor_voltage_threshold: int | None = None
    """
    The dc voltage in volts at which the varistor starts conducting. It is used for short circuit calculations. If null and varistorRatedCurrent is null, 
    a varistor is not present.
    """

    def varistor_present(self) -> bool:
        return self.varistor_rated_current is not None or self.varistor_voltage_threshold is not None
