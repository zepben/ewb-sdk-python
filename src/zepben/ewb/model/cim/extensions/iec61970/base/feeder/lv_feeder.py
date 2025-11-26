#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["LvFeeder"]

import typing
from typing import Generator, Optional, Dict, List

from zepben.ewb.dataslot import custom_len, MRIDListRouter, MRIDDictRouter, boilermaker, TypeRestrictedDescriptor, WeakrefDescriptor, dataslot, BackedDescriptor, ListAccessor, ValidatedDescriptor, MRIDListAccessor, custom_get, custom_remove, override_boilerplate, ListActions, MRIDDictAccessor, BackingValue, custom_clear, custom_get_by_mrid, custom_add, NoResetDescriptor, ListRouter, validate
from typing_extensions import deprecated
from zepben.ewb.model.cim.extensions.zbex import zbex
from zepben.ewb.model.cim.iec61970.base.core.equipment_container import EquipmentContainer
from zepben.ewb.util import safe_remove_by_id, nlen, ngen

if typing.TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61970.base.core.equipment import Equipment
    from zepben.ewb.model.cim.iec61970.base.core.feeder import Feeder
    from zepben.ewb.model.cim.iec61970.base.core.terminal import Terminal


@zbex
@dataslot
class LvFeeder(EquipmentContainer):
    """
    [ZBEX]
    A branch of LV network starting at a distribution substation and continuing until the end of the LV network.
    """

    normal_head_terminal: Terminal | None = NoResetDescriptor(None)
    """The normal head terminal or terminals of this LvFeeder"""

    normal_energizing_feeders: List[Feeder] | None = MRIDDictAccessor()
    """The feeders that energize this LV feeder in the normal state of the network."""

    current_equipment: List[Equipment] | None = MRIDDictAccessor()
    """The equipment contained in this LvFeeder in the current state of the network."""

    current_energizing_feeders: List[Feeder] | None = MRIDDictAccessor()
    """The feeders that energize this LV feeder in the current state of the network."""

    def _retype(self):
        self.normal_energizing_feeders: MRIDDictRouter[Feeder] = ...
        self.current_equipment: MRIDDictRouter[Equipment] = ...
        self.current_energizing_feeders: MRIDDictRouter[Feeder] = ...

    @deprecated("BOILERPLATE: Use len(normal_energizing_feeders) instead")
    def num_normal_energizing_feeders(self) -> int:
        return len(self.normal_energizing_feeders)

    @deprecated("BOILERPLATE: Use normal_energizing_feeders.get_by_mrid(mrid) instead")
    def get_normal_energizing_feeder(self, mrid: str) -> Feeder:
        """
        Energizing feeder using the normal state of the network.

        @param mrid: The mrid of the `Feeder`.
        @return A matching `Feeder` that energizes this `LvFeeder` in the normal state of the network.
        @raise A `KeyError` if no matching `Feeder` was found.
        """
        return self.normal_energizing_feeders.get_by_mrid(mrid)

    @deprecated("BOILERPLATE: Use normal_energizing_feeders.append(feeder) instead")
    def add_normal_energizing_feeder(self, feeder: Feeder) -> LvFeeder:
        """
        Associate this `LvFeeder` with a `Feeder` in the normal state of the network.

        @param feeder: the HV/MV feeder to associate with this LV feeder in the normal state of the network.
        @return: This `LvFeeder` for fluent use.
        """
        self.normal_energizing_feeders.append(feeder)
        return self

    @deprecated("Boilerplate: Use normal_energizing_feeders.remove(feeder) instead")
    def remove_normal_energizing_feeder(self, feeder: Feeder) -> LvFeeder:
        self.normal_energizing_feeders.remove(feeder)
        return self

    @deprecated("BOILERPLATE: Use normal_energizing_feeders.clear() instead")
    def clear_normal_energizing_feeders(self) -> LvFeeder:
        return self.normal_energizing_feeders.clear()

    @deprecated("BOILERPLATE: Use len(current_energizing_feeders) instead")
    def num_current_energizing_feeders(self) -> int:
        return len(self.current_energizing_feeders)

    @deprecated("BOILERPLATE: Use current_energizing_feeders.get_by_mrid(mrid) instead")
    def get_current_energizing_feeder(self, mrid: str) -> Feeder:
        """
        Energizing feeder using the current state of the network.

        @param mrid: The mrid of the `Feeder`.
        @return A matching `Feeder` that energizes this `LvFeeder` in the current state of the network.
        @raise A `KeyError` if no matching `Feeder` was found.
        """
        return self.current_energizing_feeders.get_by_mrid(mrid)

    @deprecated("BOILERPLATE: Use current_energizing_feeders.append(feeder) instead")
    def add_current_energizing_feeder(self, feeder: Feeder) -> LvFeeder:
        """
        Associate this `LvFeeder` with a `Feeder` in the current state of the network.

        @param feeder: the HV/MV feeder to associate with this LV feeder in the current state of the network.
        @return: This `LvFeeder` for fluent use.
        """
        self.current_energizing_feeders.append(feeder)
        return self

    @deprecated("Boilerplate: Use current_energizing_feeders.remove(feeder) instead")
    def remove_current_energizing_feeder(self, feeder: Feeder) -> LvFeeder:
        self.current_energizing_feeders.remove(feeder)
        return self

    @deprecated("BOILERPLATE: Use current_energizing_feeders.clear() instead")
    def clear_current_energizing_feeders(self) -> LvFeeder:
        return self.current_energizing_feeders.clear()

    @deprecated("BOILERPLATE: Use len(current_equipment) instead")
    def num_current_equipment(self):
        return len(self.current_equipment)

    @deprecated("BOILERPLATE: Use current_equipment.get_by_mrid(mrid) instead")
    def get_current_equipment(self, mrid: str) -> Equipment:
        """
        Get the `Equipment` contained in this `LvFeeder` in the current state of the network, identified by `mrid`

        `mrid` The mRID of the required `Equipment`
        Returns The `Equipment` with the specified `mrid` if it exists
        Raises `KeyError` if `mrid` wasn't present.
        """
        return self.current_equipment.get_by_mrid(mrid)

    @deprecated("BOILERPLATE: Use current_equipment.append(equipment) instead")
    def add_current_equipment(self, equipment: Equipment) -> LvFeeder:
        """
        Associate `equipment` with this `LvFeeder` in the current state of the network.

        `equipment` the `Equipment` to associate with this `LvFeeder` in the current state of the network.
        Returns A reference to this `LvFeeder` to allow fluent use.
        Raises `ValueError` if another `Equipment` with the same `mrid` already exists for this `LvFeeder`.
        """
        self.current_equipment.append(equipment)
        return self

    @deprecated("Boilerplate: Use current_equipment.remove(equipment) instead")
    def remove_current_equipment(self, equipment: Equipment) -> LvFeeder:
        self.current_equipment.remove(equipment)
        return self

    @deprecated("BOILERPLATE: Use current_equipment.clear() instead")
    def clear_current_equipment(self) -> LvFeeder:
        self.current_equipment.clear()
        return self

