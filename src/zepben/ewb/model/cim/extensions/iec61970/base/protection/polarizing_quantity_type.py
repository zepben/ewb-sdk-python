#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["PolarizingQuantityType"]

from enum import Enum

from zepben.ewb.model.cim.extensions.zbex import zbex


@zbex
class PolarizingQuantityType(Enum):
    """
    [ZBEX] Defines the type of polarizing quantity used by the directional relay. This informs how the relay
    determines the reference voltage from the Voltage transformers associated with its parent ProtectionEquipment.
    """

    UNKNOWN = 0
    """[ZBEX] Type is unknown."""

    SELF_PHASE_VOLTAGE = 1
    """[ZBEX] Uses the voltage of the same phase as the current element (e.g., Va for an Ia element)."""

    QUADRATURE_VOLTAGE = 2
    """[ZBEX] Uses a quadrature voltage (e.g., Vbc for an Ia element, specific convention applies."""

    ZERO_SEQUENCE_VOLTAGE = 3
    """[ZBEX] Uses the zero sequence voltage (Vo), derived from three phase voltages."""

    NEGATIVE_SEQUENCE_VOLTAGE = 4
    """[ZBEX] Uses the negative sequence voltage (V2), derived from three phase voltages."""

    POSITIVE_SEQUENCE_VOLTAGE = 5
    """[ZBEX] Uses the positive sequence voltage (V1), derived from three phase voltages."""

    @property
    def short_name(self):
        return str(self)[23:]
