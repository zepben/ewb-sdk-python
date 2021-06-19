#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Callable, Optional, Set, Dict, Generator, Tuple, Any

from zepben.evolve import IdentifiedObject
from zepben.evolve.services.common.difference import ObjectDifference


class ServiceDifferences(object):

    def __init__(self, source_lookup: Callable[[str], Optional[IdentifiedObject]], target_lookup: Callable[[str], Optional[IdentifiedObject]]):
        self._source_lookup = source_lookup
        self._target_lookup = target_lookup

        self._missing_from_target: Set[str] = set()
        self._missing_from_source: Set[str] = set()
        self._modifications = Dict[str, ObjectDifference]()

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
        return "Missing From Target:" + ''.join([self._indented_line(self._source_lookup(it)) for it in self._missing_from_target]) + \
               "\nMissing From Source:" + ''.join([self._indented_line(self._target_lookup(it)) for it in self._missing_from_source]) + \
               "\nModifications:" + ''.join(self._indented_line("{!r}: {!r},".format(k, v)) for k, v in self._modifications.items())

    @staticmethod
    def _indented_line(line: Any) -> str:
        return "\n   " + str(line)
