#  Copyright 2023 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations

from typing import Optional, List, Generator, TYPE_CHECKING, Iterable

from zepben.evolve.model.cim.iec61970.base.core.equipment import Equipment
from zepben.evolve.model.cim.iec61970.infiec61970.protection.power_direction_kind import PowerDirectionKind
from zepben.evolve.model.cim.iec61970.infiec61970.protection.protection_kind import ProtectionKind
from zepben.evolve.util import nlen, ngen, get_by_mrid, safe_remove

if TYPE_CHECKING:
    from zepben.evolve import ProtectedSwitch

__all__ = ["ProtectionEquipment"]


class ProtectionEquipment(Equipment):
    """
    An electrical device designed to respond to input conditions in a prescribed manner and after specified conditions are met to cause contact operation or
    similar abrupt change in associated electric control circuits, or simply to display the detected condition. Protection equipment is associated with
    conducting equipment and usually operate circuit breakers.
    """

    relay_delay_time: Optional[float] = None
    """The time delay from detection of abnormal conditions to relay operation in seconds."""

    protection_kind: ProtectionKind = ProtectionKind.UNKNOWN
    """The kind of protection being provided by this protection equipment."""

    directable: Optional[bool] = None
    """Whether this ProtectionEquipment responds to power flow in a given direction."""

    power_direction: PowerDirectionKind = PowerDirectionKind.UNKNOWN_DIRECTION
    """The flow of power direction used by this ProtectionEquipment."""

    _protected_switches: Optional[List[ProtectedSwitch]] = None

    def __init__(self, protected_switches: Iterable[ProtectedSwitch] = None, **kwargs):
        super(ProtectionEquipment, self).__init__(**kwargs)
        if protected_switches is not None:
            for protected_switch in protected_switches:
                self.add_protected_switch(protected_switch)

    @property
    def protected_switches(self) -> Generator[ProtectedSwitch, None, None]:
        """
        Yields all :class:`ProtectedSwitch`'s operated by this :class:`ProtectionEquipment`.

        :return: A generator that iterates over all ProtectedSwitches operated by this ProtectionEquipment.
        """
        return ngen(self._protected_switches)

    def num_protected_switches(self) -> int:
        """
        Get the number of :class:`ProtectedSwitch`'s operated by this :class:`ProtectionEquipment`.

        :return: The number of ProtectedSwitches operated by this ProtectionEquipment.
        """
        return nlen(self._protected_switches)

    def get_protected_switch(self, mrid: str) -> Optional[ProtectedSwitch]:
        """
        Get a :class:`ProtectedSwitch` operated by this :class:`ProtectionEquipment` with the specified `mrid`.

        :param mrid: The mRID of the desired ProtectedSwitch
        :return: The ProtectedSwitch with the specified mRID if it exists, otherwise None.
        """
        return get_by_mrid(self._protected_switches, mrid)

    def add_protected_switch(self, protected_switch: ProtectedSwitch) -> ProtectionEquipment:
        """
        Associate this :class:`ProtectionEquipment` with a :class:`ProtectedSwitch` that it operates.
        :param protected_switch: The ProtectedSwitch to associate with this ProtectionEquipment.
        :return: A reference to this ProtectionEquipment for fluent use.
        """
        if self._validate_reference(protected_switch, self.get_protected_switch, "A ProtectedSwitch"):
            return self

        self._protected_switches = list() if self._protected_switches is None else self._protected_switches
        self._protected_switches.append(protected_switch)

        return self

    def remove_protected_switch(self, protected_switch: Optional[ProtectedSwitch]) -> ProtectionEquipment:
        """
        Disassociate this :class:`ProtectionEquipment` from a :class:`ProtectedSwitch`.
        :param protected_switch: The ProtectedSwitch to disassociate from this ProtectionEquipment.
        :return: A reference to this ProtectionEquipment for fluent use.
        """
        self._protected_switches = safe_remove(self._protected_switches, protected_switch)
        return self

    def clear_protected_switches(self) -> ProtectionEquipment:
        """
        Disassociate all :class:`ProtectedSwitch`'s from this :class:`ProtectionEquipment`.
        :return: A reference to this ProtectionEquipment for fluent use.
        """
        self._protected_switches = None
        return self
