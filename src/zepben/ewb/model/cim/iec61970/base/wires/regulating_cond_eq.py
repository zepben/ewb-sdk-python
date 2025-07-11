#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["RegulatingCondEq"]

from typing import Optional, TYPE_CHECKING

from zepben.ewb.model.cim.iec61970.base.wires.energy_connection import EnergyConnection

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61970.base.wires.regulating_control import RegulatingControl


class RegulatingCondEq(EnergyConnection):
    """
    A short section of conductor with negligible impedance which can be manually removed and replaced if the circuit is
    de-energized. Note that zero-impedance branches can potentially be modeled by other equipment types.
    """

    control_enabled: bool = True
    """Specifies the regulation status of the equipment.  True is regulating, false is not regulating."""

    _regulating_control: Optional[RegulatingControl] = None

    def __init__(self, regulating_control: Optional[RegulatingControl] = None, **kwargs):
        super(RegulatingCondEq, self).__init__(**kwargs)
        self.regulating_control = regulating_control

    @property
    def regulating_control(self):
        """
        The `RegulatingControl` associated with this `RegulatingCondEq`
        """
        return self._regulating_control

    @regulating_control.setter
    def regulating_control(self, rc):
        if self._regulating_control is None or rc is self._regulating_control:
            self._regulating_control = rc
        else:
            raise ValueError(f"regulating_control for {str(self)} has already been set to {self._regulating_control}, cannot set this field again")
