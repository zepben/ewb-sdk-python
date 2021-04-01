#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

import logging
from abc import ABCMeta
from typing import Callable, Any, List, Generator, Optional

from dataclassy import dataclass

from zepben.evolve.model.cim.iec61970.base.core.name import Name
from zepben.evolve.util import require, CopyableUUID, nlen, ngen, safe_remove

__all__ = ["IdentifiedObject"]

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class IdentifiedObject(object, metaclass=ABCMeta):
    """
    Root class to provide common identification for all classes needing identification and naming attributes.
    Everything should extend this class, however it's not mandated that every subclass must use all the fields
    defined here.

    All names of attributes of classes extending this class *must* directly reflect CIM properties if they have a direct
    relation, however must be in snake case to keep the phases PEP compliant.
    """

    mrid: str = CopyableUUID()
    """Master resource identifier issued by a model authority. The mRID is unique within an exchange context. 
    Global uniqueness is easily achieved by using a UUID, as specified in RFC 4122, for the mRID. The use of UUID is strongly recommended."""

    name: str = ""
    """The name is any free human readable and possibly non unique text naming the object."""

    description: str = ""
    """a free human readable text describing or naming the object. It may be non unique and may not correlate to a naming hierarchy."""

    _names: Optional[List[Name]] = None

    def __str__(self):
        return f"{self.__class__.__name__}{{{'|'.join(a for a in (str(self.mrid), str(self.name)) if a)}}}"

    def _validate_reference(self, other: IdentifiedObject, getter: Callable[[str], IdentifiedObject],
                            type_descr: str) -> bool:
        """
        Validate whether a given reference exists to `other` using the provided getter function.

        `other` The object to look up with the getter using its mRID.
        `getter` A function that takes an mRID and returns an object if it exists, and throws a ``KeyError`` if it couldn't be found.
        `type_descr` The type description to use for the lazily generated error message. Should be of the form "A[n] type(other)"
        Returns True if `other` was retrieved with `getter` and was equivalent, False otherwise.
        Raises `ValueError` if the object retrieved from `getter` is not `other`.
        """
        try:
            get_result = getter(other.mrid)
            require(get_result is other, lambda: f"{type_descr} with mRID {other.mrid} already exists in {str(self)}")
            return True
        except (KeyError, AttributeError):
            return False

    def _validate_reference_by_sn(self, field: Any, other: IdentifiedObject, getter: Callable[[Any], IdentifiedObject],
                                  type_descr: str,
                                  field_name: str = "sequence_number") -> bool:
        """
        Validate whether a given reference exists to `other` using the provided getter function called with `field`.

        `other` The object to compare against.
        `getter` A function that takes `field` and returns an `IdentifiedObject` if it exists, and throws an `IndexError` if it couldn't be found.
        `type_descr` The type description to use for the lazily generated error message. Should be of the form "A[n] type(other)"
        Returns True if `other` was retrieved with a call to `getter(field)` and was equivalent, False otherwise.
        Raises `ValueError` if an object is retrieved from `getter` and it is not `other`.
        """
        try:
            get_result = getter(field)
            require(get_result is other,
                    lambda: f"{type_descr} with {field_name} {field} already exists in {str(self)}")
            return True
        except IndexError:
            return False

    @property
    def names(self):
        """The names for this identified object. The returned collection is read only."""
        return ngen(self._names)

    def num_names(self):
        """Get the number of entries in the [Name] collection."""
        return nlen(self._names)

    def get_name(self, type: str, name: str) -> Optional[Name]:
        """Return first element in _names or return None"""
        if self._names is not None:
            for name_ in self._names:
                if name_.type.name == type and name_.name == name:
                    return name_
        return None

    def add_name(self, name: Name) -> IdentifiedObject:
        """
        Associate an `zepben.evolve.cim.iec61970.base.core.name` with this `Name`

        `name` The `zepben.evolve.cim.iec61970.base.core.name` to associate with this `Name`.
        Returns A reference to this `Name` to allow fluent use.
        Raises `ValueError` if another `EquipmentContainer` with the same `mrid` already exists for this `Name`.
        """

        require(name.identified_object is self,
                lambda: f"Attempting to add a Name to {str(self)} that does not reference this identified object")

        if self.get_name(name.type.name, name.name) is not None:
            return self

        self._names = list() if self._names is None else self._names
        self._names.append(name)
        return self

    def remove_name(self, name: Name) -> Bool:
        """
        Disassociate `name` from this `Name`.

        `name` The `zepben.evolve.cim.iec61970.base.core.name` to disassociate from this `Name`.
        Returns A reference to this `Name` to allow fluent use.
        Raises `ValueError` if `name` was not associated with this `Name`.
        """

        if name in self._names:
            safe_remove(self._names, name)
            return True
        else:
            return False

        #safe_remove(self._names, name)
        #return self
        #check with kurt return self is not needed

    def clear_names(self):
        """
        Clear all name.
        Returns A reference to this `Name` to allow fluent use.
        """
        self._names = None
        return self
