#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

import logging
from abc import ABCMeta
from dataclassy import dataclass
from typing import Union, Callable, Any
from uuid import UUID
from zepben.cimbend.util import require, CopyableUUID

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

    mrid: Union[str, UUID] = CopyableUUID()
    """Master resource identifier issued by a model authority. The mRID is unique within an exchange context. 
    Global uniqueness is easily achieved by using a UUID, as specified in RFC 4122, for the mRID. The use of UUID is strongly recommended."""

    name: str = ""
    """The name is any free human readable and possibly non unique text naming the object."""

    description: str = ""
    """a free human readable text describing or naming the object. It may be non unique and may not correlate to a naming hierarchy."""

    def __str__(self):
        return f"{self.__class__.__name__}{{{'|'.join(a for a in (str(self.mrid), self.name) if a)}}}"

    def _validate_reference(self, other: IdentifiedObject, getter: Callable[[str], IdentifiedObject], type_descr: str) -> bool:
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

    def _validate_reference_by_sn(self, field: Any, other: IdentifiedObject, getter: Callable[[Any], IdentifiedObject], type_descr: str) -> bool:
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
            require(get_result is other, lambda: f"{type_descr} with {field} already exists in {str(self)}")
            return True
        except IndexError:
            return False



