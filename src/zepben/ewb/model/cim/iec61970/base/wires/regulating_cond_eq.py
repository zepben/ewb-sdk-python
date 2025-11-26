#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["RegulatingCondEq"]

from typing import TYPE_CHECKING

from zepben.ewb.dataslot import dataslot, NoResetDescriptor
from zepben.ewb.model.cim.iec61970.base.wires.energy_connection import EnergyConnection

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61970.base.wires.regulating_control import RegulatingControl


@dataslot
class RegulatingCondEq(EnergyConnection):
    """
    A short section of conductor with negligible impedance which can be manually removed and replaced if the circuit is
    de-energized. Note that zero-impedance branches can potentially be modeled by other equipment types.
    """

    control_enabled: bool | None = None
    """Specifies the regulation status of the equipment.  True is regulating, false is not regulating."""

    regulating_control: RegulatingControl | None = NoResetDescriptor(None)
