#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations

from typing import Generator, Optional, List, TYPE_CHECKING, Iterable
from zepben.evolve.util import ngen, nlen, get_by_mrid, safe_remove
if TYPE_CHECKING:
    from zepben.evolve.model.cim.iec61970.base.protection.protection_relay_function import ProtectionRelayFunction
from zepben.evolve.model.cim.iec61970.base.auxiliaryequipment.auxiliary_equipment import AuxiliaryEquipment

__all__ = ["Sensor"]


class Sensor(AuxiliaryEquipment):
    """
    This class describes devices that transform a measured quantity into signals that can be presented at displays,
    used in control or be recorded.
    """

    _relay_functions: Optional[List[ProtectionRelayFunction]] = None
    """The relay functions influenced by this [Sensor]."""

    def __init__(self, relay_functions: Iterable[ProtectionRelayFunction] = None, **kwargs):
        super(Sensor, self).__init__(**kwargs)
        if relay_functions is not None:
            for relay_function in relay_functions:
                self.add_relay_function(relay_function)

    @property
    def relay_functions(self) -> Generator[ProtectionRelayFunction, None, None]:
        """
        Yields all the :class:`ProtectionRelayFunction` that are influenced by this :class:`Sensor`.

        :return: A generator that iterates over all ProtectionRelayFunction influenced by this Sensor.
        """
        return ngen(self._relay_functions)

    def num_relay_functions(self) -> int:
        """
        Get the number of :class:`ProtectionRelayFunction` that are influenced by this :class:`Sensor`.

        :return: The number of ProtectionRelayFunction influenced by this Sensor.
        """
        return nlen(self._relay_functions)

    def get_relay_function(self, mrid: str) -> ProtectionRelayFunction:
        """
        Get a :class:`ProtectionRelayFunction` that are influenced by this :class:`Sensor`.

        :param mrid: The mRID of the desired ProtectionRelayFunction
        :return: The ProtectionRelayFunction with the specified mRID if it exists, otherwise None.
        :raises KeyError: If `mrid` wasn't present.
        """
        return get_by_mrid(self._relay_functions, mrid)

    def add_relay_function(self, protection_relay_function: ProtectionRelayFunction) -> Sensor:
        """
        Associate this :class:`Sensor` with a :class:`ProtectionRelayFunction` it is influencing.

        :param protection_relay_function: The ProtectionRelayFunction to associate with this Sensor.
        :return: A reference to this Sensor for fluent use.
        """
        if self._validate_reference(protection_relay_function, self.get_relay_function, "A ProtectionRelayFunction"):
            return self

        self._relay_functions = list() if self._relay_functions is None else self._relay_functions
        self._relay_functions.append(protection_relay_function)
        return self

    def remove_relay_function(self, protection_relay_function: ProtectionRelayFunction) -> Sensor:
        """
        Disassociate this :class:`Sensor` from a :class:`ProtectionRelayFunction` it is influencing.

        :param protection_relay_function: The ProtectionRelayFunction to disassociate from this Sensor.
        :return: A reference to this Sensor for fluent use.
        """
        self._relay_functions = safe_remove(self._relay_functions, protection_relay_function)
        return self

    def clear_relay_function(self) -> Sensor:
        """
        Disassociate all :class:`ProtectionRelayFunction` from this :class:`Sensor`.

        :return: A reference to this Sensor for fluent use.
        """
        self._relay_functions = None
        return self
