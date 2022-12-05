#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from zepben.evolve.model.cim.iec61970.base.auxiliaryequipment.sensor import Sensor

if TYPE_CHECKING:
    from zepben.evolve.model.cim.iec61968.infiec61968.infassetinfo.current_transformer_info import CurrentTransformerInfo

__all__ = ["CurrentTransformer"]


class CurrentTransformer(Sensor):
    """
    Instrument transformer used to measure electrical qualities of the circuit that is being protected and/or monitored.
    Typically used as current transducer for the purpose of metering or protection.
    A typical secondary current rating would be 5A.
    """

    core_burden: Optional[int] = None
    """Power burden of the CT core in watts."""

    @property
    def current_transformer_info(self) -> Optional[CurrentTransformerInfo]:
        """The `CurrentTransformerInfo` for this `CurrentTransformer`"""
        return self.asset_info

    @current_transformer_info.setter
    def current_transformer_info(self, cti: Optional[CurrentTransformerInfo]):
        """
        Set the `CurrentTransformerInfo` for this `CurrentTransformer`
        `cti` The `CurrentTransformerInfo` for this `CurrentTransformer`
        """
        self.asset_info = cti
