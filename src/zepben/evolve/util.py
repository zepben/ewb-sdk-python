#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = [
    "get_by_mrid",
    "contains_mrid",
    "safe_remove",
    "safe_remove_by_id",
    "nlen",
    "ngen",
    "is_none_or_empty",
    "require",
    "pb_or_none",
    "CopyableUUID",
    "datetime_to_timestamp",
    "none",
    "classproperty",
]

import os
import re
from collections.abc import Sized
from datetime import datetime
from typing import List, Optional, Iterable, Callable, Any, TypeVar, Generator, Dict, Collection
from typing import TYPE_CHECKING
from uuid import UUID

from google.protobuf.timestamp_pb2 import Timestamp as PBTimestamp

if TYPE_CHECKING:
    from zepben.evolve import IdentifiedObject, TIdentifiedObject

T = TypeVar('T')


def snake2camelback(name: str):
    return ''.join(word.title() for word in name.split('_'))


_camel_pattern = re.compile(r'(?<!^)(?=[A-Z])')


def camel2snake(name: str):
    return _camel_pattern.sub('_', name).lower()


def iter_but_not_str(obj: Any):
    return isinstance(obj, Iterable) and not isinstance(obj, (str, bytes, bytearray, dict))


def get_by_mrid(collection: Optional[Iterable[TIdentifiedObject]], mrid: str) -> TIdentifiedObject:
    """
    Get an `IdentifiedObject` from `collection` based on
    its mRID.
    `collection` The collection to operate on
    `mrid` The mRID of the `IdentifiedObject` to lookup in the collection
    Returns The `IdentifiedObject`
    Raises `KeyError` if `mrid` was not found in the collection.
    """
    if not collection:
        raise KeyError(mrid)
    for io in collection:
        if io.mrid == mrid:
            return io
    raise KeyError(mrid)


def contains_mrid(collection: Optional[Iterable[IdentifiedObject]], mrid: str) -> bool:
    """
    Check if a collection of `IdentifiedObject` contains an
    object with a specified mRID.
    `collection` The collection to operate on
    `mrid` The mRID to look up.
    Returns True if an `IdentifiedObject` is found in the collection with the specified mRID, False otherwise.
    """
    if not collection:
        return False
    try:
        if get_by_mrid(collection, mrid):
            return True
    except KeyError:
        return False


def safe_remove(collection: Optional[List[T]], obj: T) -> Optional[List[T]]:
    """
    Remove an IdentifiedObject from a collection safely.
    Raises `ValueError` if `obj` is not in the collection.
    Returns The collection if successfully removed or None if after removal the collection was empty.
    """
    if not collection:
        raise ValueError(obj)

    collection.remove(obj)

    return collection if collection else None


def safe_remove_by_id(collection: Optional[Dict[str, IdentifiedObject]], obj: IdentifiedObject) -> {Optional[Dict[str, IdentifiedObject]]}:
    """
    Remove an IdentifiedObject from a collection safely.
    Raises `KeyError` if `obj` is not in the collection.
    Returns The collection if successfully removed or None if after removal the collection was empty.
    """
    if not collection:
        raise KeyError(obj)

    del collection[obj.mrid]

    return collection if collection else None


def nlen(sized: Optional[Sized]) -> int:
    """
    Get the len of a nullable sized type.
    `sized` The object to get length of
    Returns 0 if `sized` is None, otherwise len(`sized`)
    """
    return 0 if sized is None else len(sized)


def ngen(collection: Optional[Iterable[T]]) -> Generator[T, None, None]:
    yield from collection or {}


def is_none_or_empty(sized: Optional[Sized]) -> bool:
    """
    Check if a given object is empty and return None if it is.
    `sized` Any type implementing `__len__`
    Returns `sized` if len(sized) > 0, or None if sized is None or len(sized) == 0.
    """
    return sized is None or not len(sized)


def require(condition: bool, lazy_message: Callable[[], Any]):
    """
    Raise a `ValueError` if condition is not met, with the result of calling `lazy_message` as the message,
    if the result is false.
    """
    if not condition:
        raise ValueError(str(lazy_message()))


def pb_or_none(cim: Optional[Any]):
    """Convert to a protobuf type or return None if cim was None"""
    return cim.to_pb() if cim is not None else None


def none(collection: Collection):
    """
    True if no elements in the collection resolve to True
    :param collection: The collection to check
    :raises: ValueError if provided collection is not of type Collection
    """
    if isinstance(collection, Collection):
        if len(collection) == 0:
            return True

        for item in collection:
            if item:
                return False
        return True

    raise ValueError("none() only supports collection types")


class CopyableUUID(UUID):

    def __init__(self):
        super().__init__(bytes=os.urandom(16), version=4)

    @staticmethod
    def copy():
        return str(UUID(bytes=os.urandom(16), version=4))


class classproperty(property):
    def __get__(self, cls, owner: T) -> T:
        return classmethod(self.fget).__get__(None, owner)()


def datetime_to_timestamp(date_time: datetime) -> PBTimestamp:
    timestamp = PBTimestamp()
    timestamp.FromDatetime(date_time)
    return timestamp
