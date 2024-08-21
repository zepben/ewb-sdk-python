#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations
from typing import Optional, List, Generator

__all__ = ["ProtectionRelaySystem"]

from zepben.evolve.util import ngen, get_by_mrid, nlen, safe_remove
from zepben.evolve.model.cim.iec61970.base.protection.protection_relay_scheme import ProtectionRelayScheme
from zepben.evolve.model.cim.iec61970.base.core.equipment import Equipment
from zepben.evolve.model.cim.iec61970.infiec61970.protection.protection_kind import ProtectionKind


class ProtectionRelaySystem(Equipment):
    """A relay system for controlling ProtectedSwitches."""

    protection_kind: ProtectionKind = ProtectionKind.UNKNOWN
    """The kind of protection being provided by this protection equipment."""

    _schemes: Optional[List[ProtectionRelayScheme]] = None

    def __init__(self, schemes: Optional[List[ProtectionRelayScheme]] = None, **kwargs):
        super(ProtectionRelaySystem, self).__init__(**kwargs)
        if schemes is not None:
            for scheme in schemes:
                self.add_scheme(scheme)

    @property
    def schemes(self) -> Generator[ProtectionRelayScheme, None, None]:
        """
        Yields all the schemes implemented by this :class:`ProtectionRelaySystem`.

        :return: A generator that iterates over all the schemes implemented by this :class:`ProtectionRelaySystem`.
        """
        return ngen(self._schemes)

    def get_scheme(self, mrid: str) -> ProtectionRelayScheme:
        """
        Get a :class:`ProtectionRelayScheme` for this :class:`ProtectionRelaySystem` by its mRID.

        :param mrid: The mRID of the desired :class:`ProtectionRelayScheme`.
        :returns: The :class:`ProtectionRelayScheme` with the specified mrid if it exists, otherwise None.
        :raises KeyError: If `mrid` wasn't present.
        """
        return get_by_mrid(self._schemes, mrid)

    def add_scheme(self, scheme: ProtectionRelayScheme) -> ProtectionRelaySystem:
        """
        Add a :class:`ProtectionRelayScheme` to this :class:`ProtectionRelaySystem`.

        :param scheme: The :class:`ProtectionRelayScheme` to add.
        :return: A reference to this :class:`ProtectionRelaySystem` for fluent use.
        """
        if self._validate_reference(scheme, self.get_scheme, "A ProtectionRelayScheme"):
            return self
        self._schemes = list() if self._schemes is None else self._schemes
        self._schemes.append(scheme)
        return self

    def num_schemes(self) -> int:
        """
        Get the number of :class:`ProtectionRelaySchemes<ProtectionRelayScheme>` for this :class:`ProtectionRelaySystem`.

        :return: The number of :class:`ProtectionRelaySchemes<ProtectionRelayScheme>` for this :class:`ProtectionRelaySystem`.
        """
        return nlen(self._schemes)

    def remove_scheme(self, scheme: Optional[ProtectionRelayScheme]) -> ProtectionRelaySystem:
        """
        Remove a :class:`ProtectionRelayScheme` from this :class:`ProtectionRelaySystem`.

        :param scheme: The :class:`ProtectionRelayScheme` to remove.
        :raises ValueError: If scheme was not associated with this :class:`ProtectionRelaySystem`.
        :return: A reference to this :class:`ProtectionRelaySystem` for fluent use.
        """
        self._schemes = safe_remove(self._schemes, scheme)
        return self

    def clear_scheme(self) -> ProtectionRelaySystem:
        """
        Remove all :class:`ProtectionRelaySchemes<ProtectionRelayScheme>` from this :class:`ProtectionRelaySystem`.

        :return: A reference to this :class:`ProtectionRelaySystem` for fluent use.
        """
        self._schemes = None
        return self
