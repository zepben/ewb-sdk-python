#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from zepben.evolve.model.cim.iec61970.base.auxiliaryequipment.potential_transformer_kind import PotentialTransformerKind
from zepben.evolve.model.cim.iec61970.base.auxiliaryequipment.sensor import Sensor

if TYPE_CHECKING:
    from zepben.evolve.model.cim.iec61968.infiec61968.infassetinfo.potential_transformer_info import PotentialTransformerInfo

__all__ = ["PotentialTransformer"]


class PotentialTransformer(Sensor):
    """
    Instrument transformer (also known as Voltage Transformer) used to measure electrical qualities of the circuit that
    is being protected and/or monitored. Typically used as voltage transducer for the purpose of metering, protection, or
    sometimes auxiliary substation supply. A typical secondary voltage rating would be 120V.
    """

    type: PotentialTransformerKind = PotentialTransformerKind.UNKNOWN
    """Potential transformer construction type."""

    @property
    def potential_transformer_info(self) -> Optional[PotentialTransformerInfo]:
        """The `PotentialTransformerInfo` for this `PotentialTransformer`"""
        return self.asset_info

    @potential_transformer_info.setter
    def potential_transformer_info(self, vti: Optional[PotentialTransformerInfo]):
        """
        Set the `PotentialTransformerInfo` for this `PotentialTransformer`
        `vti` The `PotentialTransformerInfo` for this `PotentialTransformer`
        """
        self.asset_info = vti
