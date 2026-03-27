#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["Conductor"]

import sys
from typing import Optional, TYPE_CHECKING
if sys.version_info >= (3, 13):
    from warnings import deprecated
else:
    from typing_extensions import deprecated

from zepben.ewb.model.cim.iec61968.assetinfo.cable_info import CableInfo
from zepben.ewb.model.cim.iec61970.base.core.conducting_equipment import ConductingEquipment

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61968.assetinfo.wire_info import WireInfo


class Conductor(ConductingEquipment):
    """
    Combination of conducting material with consistent electrical characteristics, building a single electrical
    system, used to carry current between points in the power system.
    """

    asset_info: 'WireInfo | None' = None

    length: Optional[float] = None
    """Segment length for calculating line section capabilities."""

    design_temperature: Optional[int] = None
    """[ZBEX] The temperature in degrees Celsius for the network design of this conductor."""

    design_rating: Optional[float] = None
    """[ZBEX] The current rating in Amperes at the specified design temperature that can be used without the conductor breaching physical network"""

    @property
    @deprecated("use asset_info instead.")
    def wire_info(self):
        """The `WireInfo` for this `Conductor`"""
        return self.asset_info

    @wire_info.setter
    @deprecated("use asset_info instead.")
    def wire_info(self, wi: Optional['WireInfo']):
        """
        Set the `WireInfo` for this `Conductor`
        :param wi: The `WireInfo` for this `Conductor`
        """
        self.asset_info = wi

    def is_underground(self):
        """
        :return: True if this `Conductor` is underground.
        """
        return isinstance(self.asset_info, CableInfo)
