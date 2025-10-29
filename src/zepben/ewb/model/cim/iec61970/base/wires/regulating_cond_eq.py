#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["RegulatingCondEq"]

from typing import Optional, TYPE_CHECKING

from zepben.ewb.dataslot import custom_len, MRIDListRouter, MRIDDictRouter, boilermaker, TypeRestrictedDescriptor, WeakrefDescriptor, dataslot, BackedDescriptor, ListAccessor, ValidatedDescriptor, MRIDListAccessor, custom_get, custom_remove, override_boilerplate, ListActions, MRIDDictAccessor, BackingValue, custom_clear, custom_get_by_mrid, custom_add, NoResetDescriptor, ListRouter, validate
from typing_extensions import deprecated
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

    regulating_control: RegulatingControl | None = ValidatedDescriptor(None)

    @validate(regulating_control)
    def _regulating_control_validate(self, rc):
        if self._regulating_control is None or rc is self._regulating_control:
            return rc
        else:
            raise ValueError(f"regulating_control for {str(self)} has already been set to {self._regulating_control}, cannot set this field again")
