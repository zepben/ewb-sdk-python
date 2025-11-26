#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["Sensor"]

from typing import List, TYPE_CHECKING

from typing_extensions import deprecated

from zepben.ewb.dataslot import MRIDListRouter, dataslot, MRIDListAccessor
from zepben.ewb.model.cim.iec61970.base.auxiliaryequipment.auxiliary_equipment import AuxiliaryEquipment

if TYPE_CHECKING:
    from zepben.ewb.model.cim.extensions.iec61970.base.protection.protection_relay_function import ProtectionRelayFunction


@dataslot
class Sensor(AuxiliaryEquipment):
    """
    This class describes devices that transform a measured quantity into signals that can be presented at displays,
    used in control or be recorded.
    """

    relay_functions: List[ProtectionRelayFunction] | None = MRIDListAccessor()
    """The relay functions influenced by this [Sensor]."""

    def _retype(self):
        self.relay_functions: MRIDListRouter[ProtectionRelayFunction] = ...
    
    @deprecated("BOILERPLATE: Use len(relay_functions) instead")
    def num_relay_functions(self) -> int:
        return len(self.relay_functions)

    @deprecated("BOILERPLATE: Use relay_functions.get_by_mrid(mrid) instead")
    def get_relay_function(self, mrid: str) -> ProtectionRelayFunction:
        return self.relay_functions.get_by_mrid(mrid)

    @deprecated("Boilerplate: Use relay_functions.append(protection_relay_function) instead")
    def add_relay_function(self, protection_relay_function: ProtectionRelayFunction) -> Sensor:
        self.relay_functions.append(protection_relay_function)
        return self

    @deprecated("Boilerplate: Use relay_functions.remove(protection_relay_function) instead")
    def remove_relay_function(self, protection_relay_function: ProtectionRelayFunction) -> Sensor:
        self.relay_functions.remove(protection_relay_function)
        return self

    @deprecated("BOILERPLATE: Use relay_functions.clear() instead")
    def clear_relay_function(self) -> Sensor:
        self.relay_functions.clear()
        return self

