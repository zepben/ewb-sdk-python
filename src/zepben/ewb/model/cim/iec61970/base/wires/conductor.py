#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["Conductor"]

from typing import Optional, TYPE_CHECKING

from zepben.ewb.dataslot import custom_len, MRIDListRouter, MRIDDictRouter, boilermaker, TypeRestrictedDescriptor, WeakrefDescriptor, dataslot, BackedDescriptor, ListAccessor, ValidatedDescriptor, MRIDListAccessor, custom_get, custom_remove, override_boilerplate, ListActions, MRIDDictAccessor, BackingValue, custom_clear, custom_get_by_mrid, custom_add, NoResetDescriptor, ListRouter, validate
from typing_extensions import deprecated

from zepben.ewb.dataslot.dataslot import Alias
from zepben.ewb.model.cim.iec61970.base.core.conducting_equipment import ConductingEquipment

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61968.assetinfo.cable_info import CableInfo
    from zepben.ewb.model.cim.iec61968.assetinfo.wire_info import WireInfo


@dataslot
class Conductor(ConductingEquipment):
    """
    Combination of conducting material with consistent electrical characteristics, building a single electrical
    system, used to carry current between points in the power system.
    """

    length: float | None = None
    """Segment length for calculating line section capabilities."""

    design_temperature: int | None = None
    """[ZBEX] The temperature in degrees Celsius for the network design of this conductor."""

    design_rating: float | None = None
    """[ZBEX] The current rating in Amperes at the specified design temperature that can be used without the conductor breaching physical network"""

    wire_info: Optional['WireInfo'] = Alias(backed_name='asset_info')


    def is_underground(self):
        """
        :return: True if this `Conductor` is underground.
        """
        return isinstance(self.wire_info, CableInfo)
