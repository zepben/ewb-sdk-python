#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations
from typing import Optional, List, Generator, TYPE_CHECKING

from zepben.evolve.util import ngen, get_by_mrid, nlen, safe_remove

if TYPE_CHECKING:
    from zepben.evolve.model.cim.iec61970.base.protection.protection_relay_system import ProtectionRelaySystem
    from zepben.evolve.model.cim.iec61970.base.protection.protection_relay_function import ProtectionRelayFunction

from zepben.evolve.model.cim.iec61970.base.core.identified_object import IdentifiedObject

__all__ = ["ProtectionRelayScheme"]


class ProtectionRelayScheme(IdentifiedObject):
    """A scheme that a group of relay functions implement. For example, typically schemes are primary and secondary, or main and failsafe."""

    system: Optional[ProtectionRelaySystem] = None
    """The system this scheme belongs to."""

    _functions: Optional[List[ProtectionRelayFunction]] = None

    def __init__(self, functions: Optional[List[ProtectionRelayFunction]] = None, **kwargs):
        super(ProtectionRelayScheme, self).__init__(**kwargs)
        if functions is not None:
            for function in functions:
                self.add_function(function)

    @property
    def functions(self) -> Generator[ProtectionRelayFunction, None, None]:
        """
        Yields all the functions operated as part of this :class:`ProtectionRelayScheme`.

        :return: A generator that iterates over all functions operated as part of this :class:`ProtectionRelayScheme`.
        """
        return ngen(self._functions)

    def get_function(self, mrid: str) -> ProtectionRelayFunction:
        """
        Get a :class:`ProtectionRelayFunction` operated as part of this :class:`ProtectionRelayScheme`.

        :param mrid: The mrid of the desired :class:`ProtectionRelayFunction`.
        :returns: The :class:`ProtectionRelayFunction` with the specified mrid if it exists, otherwise None.
        :raises KeyError: If `mrid` wasn't present.
        """
        return get_by_mrid(self._functions, mrid)

    def add_function(self, function: ProtectionRelayFunction) -> ProtectionRelayScheme:
        """
        Associate a :class:`ProtectionRelayFunction` with this :class:`ProtectionRelayScheme`.

        :param function: The :class:`ProtectionRelayFunction` to associate with this :class:`ProtectionRelayScheme`.
        :return: A reference to this :class:`ProtectionRelayScheme` for fluent use.
        """
        if self._validate_reference(function, self.get_function, "A ProtectionRelayFunction"):
            return self
        self._functions = list() if self._functions is None else self._functions
        self._functions.append(function)
        return self

    def num_functions(self) -> int:
        """
        Get the number of :class:`ProtectionRelayFunctions<ProtectionRelayFunction>` operated as part of this :class:`ProtectionRelayScheme`.

        :return: The number of :class:`ProtectionRelayFunctions<ProtectionRelayFunction>` operated as part of this :class:`ProtectionRelayScheme`.
        """
        return nlen(self._functions)

    def remove_function(self, function: Optional[ProtectionRelayFunction]) -> ProtectionRelayScheme:
        """
        Disassociate this :class:`ProtectionRelayScheme` from a :class:`ProtectionRelayFunction`.

        :param function: The :class:`ProtectionRelayFunction` to disassociate from this :class:`ProtectionRelayScheme`.
        :raises ValueError: If function was not associated with this :class:`ProtectionRelayScheme`.
        :return: A reference to this :class:`ProtectionRelayScheme` for fluent use.
        """
        self._functions = safe_remove(self._functions, function)
        return self

    def clear_function(self) -> ProtectionRelayScheme:
        """
        Disassociate all :class:`ProtectionRelayFunctions<ProtectionRelayFunction>` from this :class:`ProtectionRelayScheme`.

        :return: A reference to this :class:`ProtectionRelayScheme` for fluent use.
        """
        self._functions = None
        return self
