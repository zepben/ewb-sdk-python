
#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations
import re
import os
from collections.abc import Sized
from typing import Set, List, Optional, Iterable, Callable, Any, TypeVar, Generator
from uuid import UUID

T = TypeVar('T')

# phs_to_cores = {SinglePhaseKind.A: 0,
#                 SinglePhaseKind.B: 1,
#                 SinglePhaseKind.C: 2,
#                 SinglePhaseKind.N: 3}
#
# cores_to_phs = {0: SinglePhaseKind.A,
#                 1: SinglePhaseKind.B,
#                 2: SinglePhaseKind.C,
#                 3: SinglePhaseKind.N}


def snake2camelback(name):
    return ''.join(word.title() for word in name.split('_'))


_camel_pattern = re.compile(r'(?<!^)(?=[A-Z])')


def camel2snake(name):
    return _camel_pattern.sub('_', name).lower()


def iter_but_not_str(obj):
    return isinstance(obj, Iterable) and not isinstance(obj, (str, bytes, bytearray, dict))


def get_equipment_connections(cond_equip, exclude: Set = None) -> List:
    """ Utility function wrapping :meth:`zepben.cimbend.ConductingEquipment.get_connections` """
    return cond_equip.get_connected_equipment(exclude=exclude)


# def phs_kind_to_idx(phase: SinglePhaseKind):
#     return phs_to_cores[phase]


def get_by_mrid(collection: Optional[Iterable[IdentifiedObject]], mrid: str) -> IdentifiedObject:
    """
    Get an `zepben.cimbend.cim.iec61970.base.core.identified_object.IdentifiedObject` from `collection` based on
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
    Check if a collection of `zepben.cimbend.cim.iec61970.base.core.identified_object.IdentifiedObject` contains an
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


def safe_remove(collection: Optional[List], obj: IdentifiedObject):
    """
    Remove an IdentifiedObject from a collection safely.
    Raises `ValueError` if `obj` is not in the collection.
    Returns The collection if successfully removed or None if after removal the collection was empty.
    """
    if collection is not None:
        collection.remove(obj)
        if not collection:
            return None
        return collection
    else:
        raise ValueError(obj)


def nlen(sized: Optional[Sized]) -> int:
    """
    Get the len of a nullable sized type.
    `sized` The object to get length of
    Returns 0 if `sized` is None, otherwise len(`sized`)
    """
    return 0 if sized is None else len(sized)


def ngen(collection: Optional[Iterable[T]]) -> Generator[T, None, None]:
    if collection:
        for item in collection:
            yield item


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
    """ Convert to a protobuf type or return None if cim was None """
    return cim.to_pb() if cim is not None else None




class CopyableUUID(UUID):
    
    def __init__(self):
        super().__init__(bytes=os.urandom(16), version=4)

    def copy(self):
        return UUID(bytes=os.urandom(16), version=4)
