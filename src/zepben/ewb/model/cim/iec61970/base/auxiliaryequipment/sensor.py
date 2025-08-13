#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["Sensor"]

from typing import Optional, TYPE_CHECKING, Iterable

from zepben.ewb.collections.mrid_list import MRIDList
from zepben.ewb.model.cim.iec61970.base.auxiliaryequipment.auxiliary_equipment import AuxiliaryEquipment

if TYPE_CHECKING:
    from zepben.ewb.model.cim.extensions.iec61970.base.protection.protection_relay_function import ProtectionRelayFunction


class Sensor(AuxiliaryEquipment):
    """
    This class describes devices that transform a measured quantity into signals that can be presented at displays,
    used in control or be recorded.
    """

    relay_functions: Optional[Iterable[ProtectionRelayFunction]] = None
    """The relay functions influenced by this [Sensor]."""


    def __post_init__(self):
        _relay_functions = MRIDList(self.relay_functions)
        self.relay_functions: MRIDList = _relay_functions



    def num_relay_functions(self) -> int:
        """
        Get the number of :class:`ProtectionRelayFunction` that are influenced by this :class:`Sensor`.

        :return: The number of ProtectionRelayFunction influenced by this Sensor.
        """
        return len(self.relay_functions)

    def get_relay_function(self, mrid: str) -> ProtectionRelayFunction:
        """
        Get a :class:`ProtectionRelayFunction` that are influenced by this :class:`Sensor`.

        :param mrid: The mRID of the desired ProtectionRelayFunction
        :return: The ProtectionRelayFunction with the specified mRID if it exists, otherwise None.
        :raises KeyError: If `mrid` wasn't present.
        """
        return self.relay_functions.get_by_mrid(mrid)

    def add_relay_function(self, protection_relay_function: ProtectionRelayFunction) -> Sensor:
        """
        Associate this :class:`Sensor` with a :class:`ProtectionRelayFunction` it is influencing.

        :param protection_relay_function: The ProtectionRelayFunction to associate with this Sensor.
        :return: A reference to this Sensor for fluent use.
        """
        # if self._validate_reference(protection_relay_function, self.get_relay_function, "A ProtectionRelayFunction"):
        #     return self

        self.relay_functions.add(protection_relay_function)
        return self

    def remove_relay_function(self, protection_relay_function: ProtectionRelayFunction) -> Sensor:
        """
        Disassociate this :class:`Sensor` from a :class:`ProtectionRelayFunction` it is influencing.

        :param protection_relay_function: The ProtectionRelayFunction to disassociate from this Sensor.
        :return: A reference to this Sensor for fluent use.
        """
        # self._relay_functions = safe_remove(self._relay_functions, protection_relay_function)
        self.relay_functions.remove(protection_relay_function)
        return self

    def clear_relay_function(self) -> Sensor:
        """
        Disassociate all :class:`ProtectionRelayFunction` from this :class:`Sensor`.

        :return: A reference to this Sensor for fluent use.
        """
        # self._relay_functions = None
        self.relay_functions.clear()
        return self
