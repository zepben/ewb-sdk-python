#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations
__all__ = ["IdentifiedObject", "TIdentifiedObject"]

import logging
from abc import ABCMeta
from typing import Callable, Any, List, Generator, Optional, overload, TypeVar

from zepben.evolve.dataclassy import dataclass

from zepben.evolve.model.cim.iec61970.base.core.name import Name
from zepben.evolve.model.cim.iec61970.base.core.name_type import NameType
from zepben.evolve.util import require, CopyableUUID, nlen, ngen, safe_remove

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

    def __init__(self, names: Optional[List[Name]] = None, **kwargs):
        super(IdentifiedObject, self).__init__(**kwargs)
        if names:
            for name in names:
                self.add_name(name.type, name.name)

    def __str__(self):
        return f"{self.__class__.__name__}{{{'|'.join(a for a in (str(self.mrid), str(self.name)) if a)}}}"

    @property
    def names(self) -> Generator[Name, None, None]:
        """All names of this identified object. The returned collection is read only."""
        return ngen(self._names)

    def num_names(self) -> int:
        """Get the number of entries in the `Name` collection."""
        return nlen(self._names)

    @overload
    def has_name(self, name_type: NameType, name: str) -> bool:
        ...

    @overload
    def has_name(self, name_type: str, name: str) -> bool:
        ...

    def has_name(self, name_type, name) -> bool:
        """
        Check to see if this object has a `Name` with the matching `name_type` and `name`

        :return: True if a matching `Name` was found, otherwise False.
        """
        if self._names:
            for name_ in self._names:
                if isinstance(name_type, str):
                    if name_.type.name == name_type and name_.name == name:
                        return True
                elif isinstance(name_type, NameType):
                    if name_.type == name_type and name_.name == name:
                        return True
        return False

    @overload
    def get_name(self, name_type: NameType, name: str) -> Name:
        ...

    @overload
    def get_name(self, name_type: str, name: str) -> Name:
        ...

    def get_name(self, name_type, name):
        """
        Find the `Name` with the matching `name_type` and `name`

        :return: The matched Name or None
        :raises KeyError: If `name` in `name_type` wasn't present.
        """
        if self._names:
            for name_ in self._names:
                if isinstance(name_type, str):
                    if name_.type.name == name_type and name_.name == name:
                        return name_
                elif isinstance(name_type, NameType):
                    if name_.type == name_type and name_.name == name:
                        return name_
        raise KeyError(name_type, name)

    @overload
    def get_names(self, name_type: NameType) -> List[Name]:
        ...

    @overload
    def get_names(self, name_type: str) -> List[Name]:
        ...

    def get_names(self, name_type):
        """
        Find all `Name` with the matching `name_type`

        :return: A list of matching Name or None
        :raises KeyError: If `name_type` wasn't present.
        """
        matches = None
        if self._names:
            if isinstance(name_type, str):
                matches = [name for name in self._names if name.type.name == name_type]
            elif isinstance(name_type, NameType):
                matches = [name for name in self._names if name.type == name_type]

        if matches:
            return matches
        else:
            raise KeyError(f"{name_type}")

    def add_name(self, name_type: NameType, name: str) -> IdentifiedObject:
        """
        Associate a `Name` with this `IdentifiedObject`

        :param name_type: A `NameType` this `Name` belongs to.
        :param name: A free string to associate with this `IdentifiedObject`.
        :return: A reference to this `IdentifiedObject` to allow fluent use.
        :raise ValueError: If `name` references another `IdentifiedObject`, or another `Name` already exists with the matching `type` and `name`.
        """

        name_obj = name_type.get_or_add_name(name, self)

        if not name_obj.identified_object:
            name_obj.identified_object = self
        require(name_obj.identified_object is self, lambda: f"Attempting to add a Name to {str(self)} that does not reference this identified object")

        if self.has_name(name_obj.type, name_obj.name):
            existing = self.get_name(name_obj.type, name_obj.name)
            if existing is name_obj:
                return self
            else:
                raise ValueError(f"Failed to add duplicate name {str(name)} to {str(self)}.")

        self._names = list() if not self._names else self._names
        self._names.append(name_obj)
        return self

    def remove_name(self, name: Name) -> IdentifiedObject:
        """
        Disassociate a `Name` from this `IdentifiedObject` and remove the `name` from its `nameType`

        :param name: The `Name` to disassociate from this `IdentifiedObject`.
        :return: A reference to this `IdentifiedObject` to allow fluent use.
        :raises ValueError: If `name` was not associated with this `IdentifiedObject`.
        """
        self._names = safe_remove(self._names, name)

        # Remove the reverse reference from the NameType if it still exists.
        if name.type.has_name(name):
            name.type.remove_name(name)

        return self

    def clear_names(self) -> IdentifiedObject:
        """
        Clear all names.

        :return: A reference to this `IdentifiedObject` to allow fluent use.
        """
        for name in list(self._names):
            self.remove_name(name)
        self._names = None

        return self

    def _validate_reference(self, other: IdentifiedObject, getter: Callable[[str], IdentifiedObject], type_descr: str) -> bool:
        """
        Validate whether a given reference exists to `other` using the provided getter function.

        :param other: The object to look up with the getter using its mRID.
        :param getter: A function that takes an mRID and returns an `IdentifiedObject`, and throws a `KeyError` if it couldn't be found.
        :param type_descr: The type description to use for the lazily generated error message. Should be of the form "A[n] type(other)"
        :return: True if `other` was retrieved with `getter` and was equivalent, False otherwise.
        :raises ValueError: If the object retrieved from `getter` is not `other`.
        """
        try:
            get_result = getter(other.mrid)
            require(get_result is other, lambda: f"{type_descr} with mRID {other.mrid} already exists in {str(self)}")
            return True
        except (KeyError, AttributeError):
            return False

    def _validate_reference_by_field(self, other: IdentifiedObject, field: Any, getter: Callable[[Any], IdentifiedObject],
                                     field_name: str) -> bool:
        """
        Validate whether a given reference exists to `other` using the provided getter function called with `field`.

        :param other: The object to look up with the getter using its mRID.
        :param field: The value of the field from `other` that needs to be validated.
        :param getter: A function that takes `field` and returns an `IdentifiedObject`, and throws an `IndexError` if it couldn't be found.
        :param field_name: The name of the field to use for the lazily generated error message.
        :return: True if `other` was retrieved with `getter` and was equivalent, False otherwise.
        :raises ValueError: If the object retrieved from `getter` is not `other`.
        """
        try:
            get_result = getter(field)
            require(get_result is other, lambda: f"Unable to add {other} to {self}. A {get_result} already exists with {field_name} {field}.")
            return True
        except IndexError:
            return False


TIdentifiedObject = TypeVar("TIdentifiedObject", bound=IdentifiedObject)
"""
Generic type of IdentifiedObject which can be used for type hinting generics.
"""
