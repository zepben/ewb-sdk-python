#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["Identifiable", "TIdentifiable"]

from abc import ABCMeta, abstractmethod
from typing import TypeVar, overload, Callable, Any

from zepben.ewb import require
from zepben.ewb.dataclassy import dataclass

TIdentifiable = TypeVar('TIdentifiable')

T = TypeVar('T')


@dataclass(slots=True)
class Identifiable(metaclass=ABCMeta):
    """
    An interface that marks an object as identifiable.

    :var mrid: The identifier for this object.
    """
    mrid: str

    def __init__(self, **kwargs):
        if kwargs:
            raise TypeError("unexpected keyword arguments in Identified constructor: {}".format(kwargs))

    @abstractmethod
    def __str__(self) -> str:
        """
        Printable version of the object including its name, mrid, and optionally, type
        """

    @overload
    def _validate_reference(self, other: 'Identifiable', getter: Callable[[str], 'Identifiable | None'], type_description: str) -> bool: ...

    @overload
    def _validate_reference(self, other: T, get_identifier: Callable[[Callable], str], getter: Callable[[str], T | None], type_description: Callable[[], str]) -> bool: ...

    # FIXME: in python 3.11, the Identifiable type hint can be replaced with Self, and this can all be moved into the class def.
    #  @singledispatchmethod
    def _validate_reference(self, other: 'Identifiable | T', getter: Callable[[str], 'Identifiable | T'], type_description: Callable[[], str] | str, get_identifier: Callable[[...], str]=None) -> bool:
        """
        Validate whether a given reference exists to `other` using the provided getter function.

        :param other: The object to look up with the getter using its mRID.
        :param getter: A function that takes an mRID and returns an `Identifiable`, and throws a `KeyError` if it couldn't be found.
        :param type_description: The type description to use for the lazily generated error message. Should be of the form "A[n] type(other)"
        :param get_identifier: The function to retrieve the identifier from `other`.
        :return: True if `other` was retrieved with `getter` and was equivalent, False otherwise.
        :raises ValueError: If the object retrieved from `getter` is not `other`.
        """
        if isinstance(other, Identifiable):
            get_identifier = lambda _other: _other.mrid
            describe_other = lambda: f"{type_description} with mRID {other.mrid}"
        else:
            require(get_identifier is not None, lambda: "foo")
            describe_other = type_description
        try:
            get_result = getter(get_identifier(other))
        except (KeyError, AttributeError):
            return False

        if get_result is other:
            return True

        raise ValueError(f"{describe_other()} already exists in {str(self)}")

    def _validate_reference_by_field(self, other: 'Identifiable', field: Any, getter: Callable[[Any], 'Identifiable'], field_name: str) -> bool:
        """
        Validate whether a given reference exists to `other` using the provided getter function called with `field`.

        :param other: The object to look up with the getter using its mRID.
        :param field: The value of the field from `other` that needs to be validated.
        :param getter: A function that takes `field` and returns an `Identifiable`, and throws an `IndexError` if it couldn't be found.
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
