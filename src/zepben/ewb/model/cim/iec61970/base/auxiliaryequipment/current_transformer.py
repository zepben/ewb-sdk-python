#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["CurrentTransformer"]

import sys
from typing import Optional, TYPE_CHECKING
if sys.version_info >= (3, 13):
    from warnings import deprecated
else:
    from typing_extensions import deprecated

from zepben.ewb.model.cim.iec61970.base.auxiliaryequipment.sensor import Sensor

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61968.infiec61968.infassetinfo.current_transformer_info import CurrentTransformerInfo


class CurrentTransformer(Sensor):
    """
    Instrument transformer used to measure electrical qualities of the circuit that is being protected and/or monitored.
    Typically used as current transducer for the purpose of metering or protection.
    A typical secondary current rating would be 5A.
    """

    asset_info: 'CurrentTransformerInfo | None' = None

    core_burden: Optional[int] = None
    """Power burden of the CT core in watts."""

    @property
    @deprecated("use asset_info instead.")
    def current_transformer_info(self) -> Optional['CurrentTransformerInfo']:
        """The `CurrentTransformerInfo` for this `CurrentTransformer`"""
        return self.asset_info

    @current_transformer_info.setter
    @deprecated("use asset_info instead.")
    def current_transformer_info(self, cti: Optional['CurrentTransformerInfo']):
        """
        Set the `CurrentTransformerInfo` for this `CurrentTransformer`
        `cti` The `CurrentTransformerInfo` for this `CurrentTransformer`
        """
        self.asset_info = cti
