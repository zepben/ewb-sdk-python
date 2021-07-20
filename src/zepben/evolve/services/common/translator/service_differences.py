#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Callable, Optional, Set, Dict, Generator, Tuple, Any, Iterable

from zepben.evolve import IdentifiedObject
from zepben.evolve.model.cim.iec61970.base.core.name_type import NameType
from zepben.evolve.services.common.difference import ObjectDifference


class ServiceDifferences(object):

    def __init__(
        self,
        source_lookup: Callable[[str], Optional[IdentifiedObject]],
        target_lookup: Callable[[str], Optional[IdentifiedObject]],
        source_name_type_lookup: Callable[[str], Optional[NameType]],
        target_name_type_lookup: Callable[[str], Optional[NameType]]
    ):

        self._source_lookup = source_lookup
        self._target_lookup = target_lookup
        self._source_name_type_lookup = source_name_type_lookup
        self._target_name_type_lookup = target_name_type_lookup

        self._missing_from_target: Set[str] = set()
        self._missing_from_source: Set[str] = set()
        self._modifications: Dict[str, ObjectDifference] = {}

    def missing_from_target(self) -> Generator[str, None, None]:
        for it in self._missing_from_target:
            yield it

    def missing_from_source(self) -> Generator[str, None, None]:
        for it in self._missing_from_source:
            yield it

    def modifications(self) -> Generator[Tuple[str, ObjectDifference], None, None]:
        for k, v in self._modifications.items():
            yield k, v

    def add_to_missing_from_target(self, mrid: str):
        self._missing_from_target.add(mrid)

    def add_to_missing_from_source(self, mrid: str):
        self._missing_from_source.add(mrid)

    def add_modifications(self, mrid: str, difference: ObjectDifference):
        self._modifications[mrid] = difference

    def __str__(self) -> str:
        return "Missing From Target:" + _indent_each(self._missing_from_target, self._source_lookup, self._source_name_type_lookup) + \
               "\nMissing From Source:" + _indent_each(self._missing_from_source, self._target_lookup, self._target_name_type_lookup) + \
               "\nModifications:" + ''.join(_indented_line("{!r}: {!r},".format(k, v)) for k, v in self._modifications.items())


def _indent_each(items: Iterable, obj_lookup, name_lookup) -> str:
    return ''.join([_indented_line(_lookup(it, obj_lookup, name_lookup)) for it in items])


def _indented_line(line: Any) -> str:
    return "\n   " + str(line)


def _lookup(it, obj_lookup, name_lookup):
    try:
        s = obj_lookup(it)
        if s:
            return s
    except KeyError:
        pass

    try:
        s = name_lookup(it)
        if s:
            return s
    except KeyError:
        pass

    return it
