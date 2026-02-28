#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["Feeder"]

from typing import Optional, Dict, List, Generator, TYPE_CHECKING

from zepben.ewb import get_by_mrid
from zepben.ewb.model.cim.extensions.zbex import zbex
from zepben.ewb.model.cim.iec61970.base.core.equipment_container import EquipmentContainer
from zepben.ewb.util import ngen, nlen, safe_remove_by_id

if TYPE_CHECKING:
    from zepben.ewb.model.cim.extensions.iec61970.base.feeder.lv_substation import LvSubstation
    from zepben.ewb.model.cim.extensions.iec61970.base.feeder.lv_feeder import LvFeeder
    from zepben.ewb.model.cim.iec61970.base.core.equipment import Equipment
    from zepben.ewb.model.cim.iec61970.base.core.substation import Substation
    from zepben.ewb.model.cim.iec61970.base.core.terminal import Terminal


class Feeder(EquipmentContainer):
    """
    A collection of equipment for organizational purposes, used for grouping distribution resources.
    The organization of a feeder does not necessarily reflect connectivity or current operation state.
    """

    _normal_head_terminal: Terminal | None = None
    """The normal head terminal or terminals of the feeder."""

    normal_energizing_substation: Substation | None = None
    """The substation that normally energizes the feeder. Also used for naming purposes."""

    _current_equipment: Dict[str, Equipment] | None = None
    """The equipment contained in this feeder in the current state of the network."""

    _normal_energized_lv_feeders: Dict[str, LvFeeder] | None = None
    """The LV feeders that are energized by this feeder in the normal state of the network."""

    _current_energized_lv_feeders: Dict[str, LvFeeder] | None = None
    """The LV feeders that are energized by this feeder in the current state of the network."""

    _normal_energized_lv_substations: Dict[str, 'LvSubstation'] | None = None
    _current_energized_lv_substations: Dict[str, 'LvSubstation'] | None = None

    def __init__(
        self,
        normal_head_terminal: Terminal = None,
        normal_energizing_substation: Substation = None,
        current_equipment: List[Equipment] = None,
        normal_energized_lv_feeders: List[LvFeeder] = None,
        current_energized_lv_feeders: List[LvFeeder] = None,
        normal_energized_lv_substations: List[LvSubstation] = None,
        current_energized_lv_substations: List[LvSubstation] = None,
        **kwargs
    ):
        super(Feeder, self).__init__(**kwargs)
        if normal_head_terminal:
            self.normal_head_terminal = normal_head_terminal
        if normal_energizing_substation:
            self.normal_energizing_substation = normal_energizing_substation
        if normal_energized_lv_feeders:
            for lv_feeder in normal_energized_lv_feeders:
                self.add_normal_energized_lv_feeder(lv_feeder)
        if current_equipment:
            for eq in current_equipment:
                self.add_current_equipment(eq)
        if current_energized_lv_feeders:
            for lv_feeder in current_energized_lv_feeders:
                self.add_current_energized_lv_feeder(lv_feeder)
        if normal_energized_lv_substations:
            for lv_substation in normal_energized_lv_substations:
                self.add_normal_energized_lv_substation(lv_substation)
        if current_energized_lv_substations:
            for lv_substation in current_energized_lv_substations:
                self.add_current_energized_lv_substation(lv_substation)

    @property
    def normal_head_terminal(self) -> Optional[Terminal]:
        """The normal head terminal or terminals of the feeder."""
        return self._normal_head_terminal

    @normal_head_terminal.setter
    def normal_head_terminal(self, term: Optional[Terminal]):
        if self._normal_head_terminal is None or self._normal_head_terminal is term or (self.num_equipment() == 0 and self.num_current_equipment() == 0):
            self._normal_head_terminal = term
        else:
            raise ValueError(f"Feeder {self.mrid} has equipment assigned to it. Cannot update normalHeadTerminal on a feeder with equipment assigned.")

    @property
    def current_equipment(self) -> Generator[Equipment, None, None]:
        """
        Contained `Equipment` using the current state of the network.
        """
        return ngen(self._current_equipment)

    def num_current_equipment(self):
        """
        :returns: The number of `Equipment` associated with this `Feeder`
        """
        return nlen(self._current_equipment)

    def get_current_equipment(self, mrid: str) -> Equipment:
        """
        Get the `Equipment` for this `Feeder` identified by `mrid`

        `mrid` The mRID of the required `Equipment`
        :returns: The `Equipment` with the specified `mrid` if it exists
        :raises: `KeyError` if `mrid` wasn't present.
        """
        return get_by_mrid(self._current_equipment, mrid)

    def add_current_equipment(self, equipment: Equipment) -> Feeder:
        """
        Associate `equipment` with this `Feeder`.

        `equipment` the `Equipment` to associate with this `Feeder`.
        :returns: A reference to this `Feeder` to allow fluent use.
        :raises: `ValueError` if another `Equipment` with the same `mrid` already exists for this `Feeder`.
        """
        if self._validate_reference(equipment, self.get_current_equipment, "An Equipment"):
            return self
        self._current_equipment = dict() if self._current_equipment is None else self._current_equipment
        self._current_equipment[equipment.mrid] = equipment
        return self

    def remove_current_equipment(self, equipment: Equipment) -> Feeder:
        """
        Disassociate `equipment` from this `Feeder`

        `equipment` The `Equipment` to disassociate from this `Feeder`.
        :returns: A reference to this `Feeder` to allow fluent use.
        :raises: `KeyError` if `equipment` was not associated with this `Feeder`.
        """
        self._current_equipment = safe_remove_by_id(self._current_equipment, equipment)
        return self

    def clear_current_equipment(self) -> Feeder:
        """
        Clear all equipment.
        :returns: A reference to this `Feeder` to allow fluent use.
        """
        self._current_equipment = None
        return self

    @property
    def normal_energized_lv_feeders(self) -> Generator[LvFeeder, None, None]:
        """
        The LV feeders that are normally energized by this feeder.
        """
        return ngen(self._normal_energized_lv_feeders)

    def num_normal_energized_lv_feeders(self) -> int:
        """
        Get the number of LV feeders that are normally energized by this feeder.
        """
        return nlen(self._normal_energized_lv_feeders)

    def get_normal_energized_lv_feeder(self, mrid: str) -> LvFeeder:
        """
        Energized LvFeeder in the normal state of the network.

        :param mrid: The mrid of the `LvFeeder`.
        :returns: A matching `LvFeeder` that is energized by this `Feeder` in the normal state of the network.
        :raise sA `KeyError` if no matching `LvFeeder` was found.
        """
        return get_by_mrid(self._normal_energized_lv_feeders, mrid)

    def add_normal_energized_lv_feeder(self, lv_feeder: LvFeeder) -> Feeder:
        """
        Associate this `Feeder` with an `LvFeeder` in the normal state of the network.

        :param lv_feeder: the LV feeder to associate with this feeder in the normal state of the network.
        :return: This `Feeder` for fluent use.
        """
        if self._validate_reference(lv_feeder, self.get_normal_energized_lv_feeder, "An LvFeeder"):
            return self
        self._normal_energized_lv_feeders = dict() if self._normal_energized_lv_feeders is None else self._normal_energized_lv_feeders
        self._normal_energized_lv_feeders[lv_feeder.mrid] = lv_feeder
        return self

    def remove_normal_energized_lv_feeder(self, lv_feeder: LvFeeder) -> Feeder:
        """
        Disassociate this `Feeder` from an `LvFeeder` in the normal state of the network.

        :param lv_feeder: the LV feeder to disassociate from this feeder in the normal state of the network.
        :return: This `Feeder` for fluent use.
        :raises: A `ValueError` if `lv_feeder` is not found in the normal energized lv feeders collection.
        """
        self._normal_energized_lv_feeders = safe_remove_by_id(self._normal_energized_lv_feeders, lv_feeder)
        return self

    def clear_normal_energized_lv_feeders(self) -> Feeder:
        """
        Clear all `LvFeeder`s associated with `Feeder` in the normal state of the network.

        :return: This `Feeder` for fluent use.
        """
        self._normal_energized_lv_feeders = None
        return self

    @zbex
    @property
    def current_energized_lv_feeders(self) -> Generator[LvFeeder, None, None]:
        """
        The LV feeders that are currently energized by this feeder.
        """
        return ngen(self._current_energized_lv_feeders)

    def num_current_energized_lv_feeders(self) -> int:
        """
        Get the number of LV feeders that are currently energized by this feeder.
        """
        return nlen(self._current_energized_lv_feeders)

    def get_current_energized_lv_feeder(self, mrid: str) -> LvFeeder:
        """
        Energized LvFeeder in the current state of the network.

        :param mrid: The mrid of the `LvFeeder`.
        :return: A matching `LvFeeder` that is energized by this `Feeder` in the current state of the network.
        :raises: A `KeyError` if no matching `LvFeeder` was found.
        """
        return get_by_mrid(self._current_energized_lv_feeders, mrid)

    def add_current_energized_lv_feeder(self, lv_feeder: LvFeeder) -> Feeder:
        """
        Associate this `Feeder` with an `LvFeeder` in the current state of the network.

        :param lv_feeder: the LV feeder to associate with this feeder in the current state of the network.
        :return: This `Feeder` for fluent use.
        """
        if self._validate_reference(lv_feeder, self.get_current_energized_lv_feeder, "An LvFeeder"):
            return self
        self._current_energized_lv_feeders = dict() if self._current_energized_lv_feeders is None else self._current_energized_lv_feeders
        self._current_energized_lv_feeders[lv_feeder.mrid] = lv_feeder
        return self

    def remove_current_energized_lv_feeder(self, lv_feeder: LvFeeder) -> Feeder:
        """
        Disassociate this `Feeder` from an `LvFeeder` in the current state of the network.

        :param lv_feeder: the LV feeder to disassociate from this feeder in the current state of the network.
        :return: This `Feeder` for fluent use.
        :raises: A `ValueError` if `lv_feeder` is not found in the current energized lv feeders collection.
        """
        self._current_energized_lv_feeders = safe_remove_by_id(self._current_energized_lv_feeders, lv_feeder)
        return self

    def clear_current_energized_lv_feeders(self) -> Feeder:
        """
        Clear all `LvFeeder`s associated with `Feeder` in the current state of the network.

        :return: This `Feeder` for fluent use.
        """
        self._current_energized_lv_feeders = None
        return self

    @zbex
    @property
    def normal_energized_lv_substations(self) -> Generator['LvSubstation', None, None]:
        return ngen(self._normal_energized_lv_substations)

    def num_normal_energized_lv_substations(self) -> int:
        """
        Get the number of entries in the normal [LvSubstation] collection.
        """
        return nlen(self._normal_energized_lv_substations)

    def get_normal_energized_lv_substation(self, mrid: str) -> 'LvSubstation | None':
        """
        Retrieve an energized LvSubstation using the normal state of the network.

        :param mrid: the mRID of the required normal [LvSubstation]
        :returns: The [LvSubstation] with the specified [mRID] if it exists, otherwise null
        """
        return get_by_mrid(self._normal_energized_lv_substations, mrid)

    def add_normal_energized_lv_substation(self, lv_substation: 'LvSubstation') -> "Feeder":
        """
        Associate this [Feeder] with a [LvSubstation] in the normal state of the network.

        :param lv_substation: the [LvSubstation] to associate with this LV feeder in the normal state of the network.
        :returns: This [Feeder] for fluent use.
        """
        if self._validate_reference(lv_substation, self.get_normal_energized_lv_substation, "An LvSubstation"):
            return self
        if self._normal_energized_lv_substations is None:
            self._normal_energized_lv_substations = dict()
        self._normal_energized_lv_substations[lv_substation.mrid] = lv_substation
        return self

    def remove_normal_energized_lv_substation(self, lv_substation: 'LvSubstation') -> "Feeder":
        """
        Disassociate this [Feeder] from a [LvSubstation] in the normal state of the network.

        :param lv_substation: the [LvSubstation] to disassociate from this LV feeder in the normal state of the network.
        :returns: true if a matching [LvSubstation] is removed from the collection.
        """
        self._normal_energized_lv_substations = safe_remove_by_id(self._normal_energized_lv_substations, lv_substation)
        return self

    def clear_normal_energized_lv_substations(self) -> "Feeder":
        """
        Clear all [LvSubstation]'s associated with this [Feeder] in the normal state of the network.

        :returns: This [Feeder] for fluent use.
        """
        self._normal_energized_lv_substations = None
        return self

    @zbex
    @property
    def current_energized_lv_substations(self) -> Generator['LvSubstation', None, None]:
        return ngen(self._current_energized_lv_substations)

    def num_current_energized_lv_substations(self) -> int:
        """
        Get the number of entries in the current [LvSubstation] collection.
        """
        return nlen(self._current_energized_lv_substations)

    def get_current_energized_lv_substation(self, mrid: str) -> 'LvSubstation | None':
        """
        Retrieve an energized LvSubstation using the current state of the network.

        :param mrid: the mRID of the required current [LvSubstation]
        :returns: The [LvSubstation] with the specified [mRID] if it exists, otherwise null
        """
        return get_by_mrid(self._current_energized_lv_substations, mrid)

    def add_current_energized_lv_substation(self, lv_substation: 'LvSubstation') -> "Feeder":
        """
        Associate this [Feeder] with a [LvSubstation] in the current state of the network.

        :param lv_substation: the [LvSubstation] to associate with this LV feeder in the current state of the network.
        :returns: This [Feeder] for fluent use.
        """
        if self._validate_reference(lv_substation, self.get_current_energized_lv_substation, "An LvSubstation"):
            return self
        if self._current_energized_lv_substations is None:
            self._current_energized_lv_substations = dict()
        self._current_energized_lv_substations[lv_substation.mrid] = lv_substation
        return self

    def remove_current_energized_lv_substation(self, lv_substation: 'LvSubstation') -> "Feeder":
        """
        Disassociate this [Feeder] from a [LvSubstation] in the current state of the network.

        :param lv_substation: the [LvSubstation] to disassociate from this LV feeder in the current state of the network.
        :returns: true if a matching [LvSubstation] is removed from the collection.
        """
        self._current_energized_lv_substations = safe_remove_by_id(self._current_energized_lv_substations, lv_substation)
        return self

    def clear_current_energized_lv_substations(self) -> "Feeder":
        """
        Clear all [LvSubstation]'s associated with this [Feeder] in the current state of the network.

        :returns: This [Feeder] for fluent use.
        """
        self._current_energized_lv_substations = None
        return self
