#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from typing import Optional, List, Generator, TYPE_CHECKING, Iterable

from zepben.evolve.model.cim.iec61970.base.wires.switch import Switch
from zepben.evolve.util import get_by_mrid, ngen, nlen, safe_remove

if TYPE_CHECKING:
    from zepben.evolve import ProtectionRelayFunction

__all__ = ["ProtectedSwitch"]


class ProtectedSwitch(Switch):
    """
    A ProtectedSwitch is a switching device that can be operated by :class:`ProtectionRelayFunction`.
    """

    breaking_capacity: Optional[int] = None
    """The maximum fault current in amps a breaking device can break safely under prescribed conditions of use."""

    _relay_functions: Optional[List[ProtectionRelayFunction]] = None

    def __init__(
        self,
        relay_functions: Iterable[ProtectionRelayFunction] = None,
        **kwargs
    ):
        super(ProtectedSwitch, self).__init__(**kwargs)

        # breaking_capacity is handled via dataclassy.
        if relay_functions is not None:
            for relay_function in relay_functions:
                self.add_relay_function(relay_function)

    @property
    def relay_functions(self) -> Generator[ProtectionRelayFunction, None, None]:
        """
        Yields all :class:`ProtectionRelayFunctions<ProtectionRelayFunction>` operating this :class:`ProtectedSwitch`.

        :return: A generator that iterates over all :class:`ProtectionRelayFunctions<ProtectionRelayFunction>` operating this :class:`ProtectedSwitch`.
        """
        return ngen(self._relay_functions)

    def num_relay_functions(self) -> int:
        """
        Get the number of :class:`ProtectionRelayFunctions<ProtectionRelayFunction>` operating this :class:`ProtectedSwitch`.

        :return: The number of :class:`ProtectionRelayFunctions<ProtectionRelayFunction>` operating this :class:`ProtectedSwitch`.
        """
        return nlen(self._relay_functions)

    def get_relay_function(self, mrid: str) -> ProtectionRelayFunction:
        """
        Get a :class:`ProtectionRelayFunction` operating this :class:`ProtectedSwitch` with the specified `mrid`.

        :param mrid: The mRID of the desired :class:`ProtectionRelayFunction`
        :return: The :class:`ProtectionRelayFunction` with the specified mRID if it exists, otherwise None.
        :raises KeyError: If `mrid` wasn't present.
        """
        return get_by_mrid(self._relay_functions, mrid)

    def add_relay_function(self, relay_function: ProtectionRelayFunction) -> ProtectedSwitch:
        """
        Associate this :class:`ProtectedSwitch` with a :class:`ProtectionRelayFunction` operating it.
        :param relay_function: The :class:`ProtectionRelayFunction` to associate with this :class:`ProtectedSwitch`.
        :return: A reference to this :class:`ProtectedSwitch` for fluent use.
        """
        if self._validate_reference(relay_function, self.get_relay_function, "A ProtectionRelayFunction"):
            return self

        self._relay_functions = list() if self._relay_functions is None else self._relay_functions
        self._relay_functions.append(relay_function)
        return self

    def remove_relay_function(self, relay_function: Optional[ProtectionRelayFunction]) -> ProtectedSwitch:
        """
        Disassociate this :class:`ProtectedSwitch` from a :class:`ProtectionRelayFunction`.
        :param relay_function: The :class:`ProtectionRelayFunction` to disassociate from this :class:`ProtectedSwitch`.
        :return: A reference to this :class:`ProtectedSwitch` for fluent use.
        """
        self._relay_functions = safe_remove(self._relay_functions, relay_function)
        return self

    def clear_relay_functions(self) -> ProtectedSwitch:
        """
        Disassociate all :class:`ProtectionRelayFunction` from this :class:`ProtectedSwitch`.
        :return: A reference to this :class:`ProtectedSwitch` for fluent use.
        """
        self._relay_functions = None
        return self
