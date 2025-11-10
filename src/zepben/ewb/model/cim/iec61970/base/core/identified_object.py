#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["IdentifiedObject", "TIdentifiedObject"]

import logging
from abc import ABCMeta
from dataclasses import field, KW_ONLY
from typing import Callable, Any, List, Generator, Optional, overload, TypeVar


from zepben.ewb.dataslot import custom_len, MRIDListRouter, MRIDDictRouter, boilermaker, TypeRestrictedDescriptor, WeakrefDescriptor, dataslot, BackedDescriptor, ListAccessor, ValidatedDescriptor, MRIDListAccessor, custom_get, custom_remove, override_boilerplate, ListActions, MRIDDictAccessor, BackingValue, custom_clear, custom_get_by_mrid, custom_add, NoResetDescriptor, ListRouter, validate
from typing_extensions import deprecated
from zepben.ewb.model.cim.iec61970.base.core.name import Name
from zepben.ewb.model.cim.iec61970.base.core.name_type import NameType
from zepben.ewb.util import require, CopyableUUID, nlen, ngen, safe_remove

logger = logging.getLogger(__name__)


@dataslot
@boilermaker
class IdentifiedObject(object, metaclass=ABCMeta):
    """
    Root class to provide common identification for all classes needing identification and naming attributes.
    Everything should extend this class, however it's not mandated that every subclass must use all the fields
    defined here.

    All names of attributes of classes extending this class *must* directly reflect CIM properties if they have a direct
    relation, however must be in snake case to keep the phases PEP compliant.
    """

    mrid: str = field(default_factory=lambda: CopyableUUID().__str__())
    """Master resource identifier issued by a model authority. The mRID is unique within an exchange context. 
    Global uniqueness is easily achieved by using a UUID, as specified in RFC 4122, for the mRID. The use of UUID is strongly recommended."""

    _: KW_ONLY = ... # Everything from this point on will have to be a kwarg

    name: str | None = None
    """The name is any free human readable and possibly non unique text naming the object."""

    description: str | None = None
    """a free human readable text describing or naming the object. It may be non unique and may not correlate to a naming hierarchy."""

    names: List[Name] | None = ListAccessor()

    # TODO: Missing num_diagram_objects: int = None  def has_diagram_objects(self): return (self.num_diagram_objects or 0) > 0

    def _retype(self):
        self.names: ListRouter = ...

    # def __hash__(self):
        # return super().__hash__(self)
        # return self.mrid.__hash__()

    # def __eq__(self, other: IdentifiedObject | str):
        # if isinstance(other, IdentifiedObject):
        #     return self.mrid.__eq__(other.mrid)
        # return self.mrid.__eq__(other)
        #
    def __str__(self):
        class_name = f'{self.__class__.__name__}'
        if self.name:
            return f'{class_name}{{{self.mrid}|{self.name}}}'
        return f'{class_name}{{{self.mrid}}}'

    @deprecated("BOILERPLATE: Use len(names) instead")
    def num_names(self) -> int:
        return len(self.names)

    def has_name(self, name_type: NameType | str, name) -> bool:
        """
        Check to see if this object has a `Name` with the matching `name_type` and `name`

        :return: True if a matching `Name` was found, otherwise False.
        """
        if self.names:
            for name_ in self.names:
                if isinstance(name_type, str):
                    if name_.type.name == name_type and name_.name == name:
                        return True
                elif isinstance(name_type, NameType):
                    if name_.type == name_type:
                        if name_.name == name:
                            return True
        return False

    def get_name(self, name_type: NameType | str, name):
        """
        Find the `Name` with the matching `name_type` and `name`

        :return: The matched Name or None
        :raises KeyError: If `name` in `name_type` wasn't present.
        """
        if self.names:
            for name_ in self.names:
                if isinstance(name_type, str):
                    if name_.type.name == name_type and name_.name == name:
                        return name_
                elif isinstance(name_type, NameType):
                    if name_.type == name_type and name_.name == name:
                        return name_
        raise KeyError(name_type, name)

    @custom_get(names)
    def get_names(self, name_type: NameType | str):
        """
        Find all `Name` with the matching `name_type`

        :return: A list of matching Name or None
        :raises KeyError: If `name_type` wasn't present.
        """
        matches = None
        if self.names:
            if isinstance(name_type, str):
                matches = [name for name in self.names if name.type.name == name_type]
            elif isinstance(name_type, NameType):
                matches = [name for name in self.names if name.type == name_type]

        if matches:
            return matches
        else:
            raise KeyError(f"{name_type}")

    @custom_add(names)
    def add_name_obj(self, name: Name):
        self.add_name(name.type, name.name)

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

        self.names.append_unchecked(name_obj)
        return self

    @custom_remove(names)
    def remove_name(self, name: Name) -> IdentifiedObject:
        """
        Disassociate a `Name` from this `IdentifiedObject` and remove the `name` from its `nameType`

        :param name: The `Name` to disassociate from this `IdentifiedObject`.
        :return: A reference to this `IdentifiedObject` to allow fluent use.
        :raises ValueError: If `name` was not associated with this `IdentifiedObject`.
        """
        self.names.raw.remove(name)

        # Remove the reverse reference from the NameType if it still exists.
        if name.type.has_name(name):
            name.type.remove_name(name)

        return self

    @custom_clear(names)
    def clear_names(self) -> IdentifiedObject:
        """
        Clear all names.

        :return: A reference to this `IdentifiedObject` to allow fluent use.
        """
        for name in list(self.names):
            self.remove_name(name)

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
