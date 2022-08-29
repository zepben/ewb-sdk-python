#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

import typing
from typing import Generator, Optional, Dict, List

if typing.TYPE_CHECKING:
    from zepben.evolve import Equipment, Terminal, Feeder

from zepben.evolve.model.cim.iec61970.base.core.equipment_container import EquipmentContainer
from zepben.evolve.util import safe_remove_by_id, nlen, ngen

__all__ = ["LvFeeder"]


class LvFeeder(EquipmentContainer):
    """
    A branch of LV network starting at a distribution substation and continuing until the end of the LV network.
    """

    _normal_head_terminal: Optional[Terminal] = None
    """The normal head terminal or terminals of this LvFeeder"""

    _normal_energizing_feeders: Optional[Dict[str, Feeder]] = None

    _current_equipment: Optional[Dict[str, Equipment]] = None
    """The equipment contained in this LvFeeder in the current state of the network."""

    def __init__(
        self,
        normal_head_terminal: Terminal = None,
        normal_energizing_feeders: List[Feeder] = None,
        current_equipment: List[Equipment] = None,
        **kwargs
    ):
        super(LvFeeder, self).__init__(**kwargs)
        if normal_head_terminal:
            self.normal_head_terminal = normal_head_terminal
        if normal_energizing_feeders:
            for feeder in normal_energizing_feeders:
                self.add_normal_energizing_feeder(feeder)
        if current_equipment:
            for eq in current_equipment:
                self.add_current_equipment(eq)

    @property
    def normal_head_terminal(self) -> Optional[Terminal]:
        """
        The normal head terminal or terminals of the feeder.
        """
        return self._normal_head_terminal

    @normal_head_terminal.setter
    def normal_head_terminal(self, term: Optional[Terminal]):
        if self._normal_head_terminal is None or self._normal_head_terminal is term:
            self._normal_head_terminal = term
        else:
            raise ValueError(f"normal_head_terminal for {str(self)} has already been set to {self._normal_head_terminal}, cannot reset this field to {term}")

    @property
    def normal_energizing_feeders(self) -> Generator[Feeder, None, None]:
        """
        The HV/MV feeders that energize this LV feeder.
        """
        return ngen(self._normal_energizing_feeders.values() if self._normal_energizing_feeders is not None else None)

    def num_normal_energizing_feeders(self) -> int:
        """
        Get the number of HV/MV feeders that energize this LV feeder.
        """
        return nlen(self._normal_energizing_feeders)

    def get_normal_energizing_feeder(self, mrid: str) -> Feeder:
        """
        Energizing feeder using the normal state of the network.

        @param mrid: The mrid of the `Feeder`.
        @return A matching `Feeder` that energizes this `LvFeeder` in the normal state of the network.
        @raise A `KeyError` if no matching `Feeder` was found.
        """
        if not self._normal_energizing_feeders:
            raise KeyError(mrid)
        try:
            return self._normal_energizing_feeders[mrid]
        except AttributeError:
            raise KeyError(mrid)

    def add_normal_energizing_feeder(self, feeder: Feeder) -> LvFeeder:
        """
        Associate this `LvFeeder` with a `Feeder` in the normal state of the network.

        @param feeder: the HV/MV feeder to associate with this LV feeder in the normal state of the network.
        @return: This `LvFeeder` for fluent use.
        """
        if self._validate_reference(feeder, self.get_normal_energizing_feeder, "A Feeder"):
            return self
        self._normal_energizing_feeders = dict() if self._normal_energizing_feeders is None else self._normal_energizing_feeders
        self._normal_energizing_feeders[feeder.mrid] = feeder
        return self

    def remove_normal_energizing_feeder(self, feeder: Feeder) -> LvFeeder:
        """
        Disassociate this `LvFeeder` from a `Feeder` in the normal state of the network.

        @param feeder: the HV/MV feeder to disassociate from this LV feeder in the normal state of the network.
        @return: This `LvFeeder` for fluent use.
        @raise: A `ValueError` if `feeder` is not found in the normal energizing feeders collection.
        """
        self._normal_energizing_feeders = safe_remove_by_id(self._normal_energizing_feeders, feeder)
        return self

    def clear_normal_energizing_feeders(self) -> LvFeeder:
        """
        Clear all `Feeder`s associated with `LvFeeder` in the normal state of the network.

        @return: This `LvFeeder` for fluent use.
        """
        self._normal_energizing_feeders = None
        return self

    @property
    def current_equipment(self) -> Generator[Equipment, None, None]:
        """
        Contained `Equipment` using the current state of the network.
        """
        return ngen(self._current_equipment.values() if self._current_equipment is not None else None)

    def num_current_equipment(self):
        """
        Returns The number of `Equipment` associated with this `LvFeeder` in the current state of the network.
        """
        return nlen(self._current_equipment)

    def get_current_equipment(self, mrid: str) -> Equipment:
        """
        Get the `Equipment` contained in this `LvFeeder` in the current state of the network, identified by `mrid`

        `mrid` The mRID of the required `Equipment`
        Returns The `Equipment` with the specified `mrid` if it exists
        Raises `KeyError` if `mrid` wasn't present.
        """
        if not self._current_equipment:
            raise KeyError(mrid)
        try:
            return self._current_equipment[mrid]
        except AttributeError:
            raise KeyError(mrid)

    def add_current_equipment(self, equipment: Equipment) -> LvFeeder:
        """
        Associate `equipment` with this `LvFeeder` in the current state of the network.

        `equipment` the `Equipment` to associate with this `LvFeeder` in the current state of the network.
        Returns A reference to this `LvFeeder` to allow fluent use.
        Raises `ValueError` if another `Equipment` with the same `mrid` already exists for this `LvFeeder`.
        """
        if self._validate_reference(equipment, self.get_current_equipment, "An Equipment"):
            return self
        self._current_equipment = dict() if self._current_equipment is None else self._current_equipment
        self._current_equipment[equipment.mrid] = equipment
        return self

    def remove_current_equipment(self, equipment: Equipment) -> LvFeeder:
        """
        Disassociate `equipment` from this `LvFeeder` in the current state of the network.

        `equipment` The `Equipment` to disassociate from this `LvFeeder` in the current state of the network.
        Returns A reference to this `LvFeeder` to allow fluent use.
        Raises `KeyError` if `equipment` was not associated with this `LvFeeder`.
        """
        self._current_equipment = safe_remove_by_id(self._current_equipment, equipment)
        return self

    def clear_current_equipment(self) -> LvFeeder:
        """
        Clear all `Equipment` from this `LvFeeder` in the current state of the network.
        Returns A reference to this `LvFeeder` to allow fluent use.
        """
        self._current_equipment = None
        return self
