#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["Sensor"]

from typing import TYPE_CHECKING, List
from warnings import deprecated

from zepben.ewb.collections.autoslot import dataslot
from zepben.ewb.collections.boilerplate import MRIDListAccessor, boilermaker, MRIDListRouter
from zepben.ewb.model.cim.iec61970.base.auxiliaryequipment.auxiliary_equipment import AuxiliaryEquipment

if TYPE_CHECKING:
    from zepben.ewb.model.cim.extensions.iec61970.base.protection.protection_relay_function import ProtectionRelayFunction


@dataslot
@boilermaker
class Sensor(AuxiliaryEquipment):
    """
    This class describes devices that transform a measured quantity into signals that can be presented at displays,
    used in control or be recorded.
    """

    relay_functions: List[ProtectionRelayFunction] | None = MRIDListAccessor()
    """The relay functions influenced by this [Sensor]."""

    def _retype(self):
        self.relay_functions: MRIDListRouter = ...


    @deprecated("Use len(relay_functions) instead.")
    def num_relay_functions(self) -> int: ...

    @deprecated("Use relay_functions[mrid] instead.")
    def get_item(self, mrid: str) -> ProtectionRelayFunction: ...

    @deprecated("Use relay_functions.append(item) instead.")
    def add_item(self, protection_relay_function: ProtectionRelayFunction) -> Sensor: ...

    @deprecated("Use len(relay_functions) instead.")
    def remove_item(self, protection_relay_function: ProtectionRelayFunction) -> Sensor: ...

    @deprecated("Use relay_functions.clear() instead.")
    def clear_item(self) -> Sensor: ...