#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import List, Generator

from dataclassy import dataclass

from zepben.evolve import DataSource

__all__ = ["MetadataCollection"]


@dataclass(slots=True)
class MetadataCollection(object):
    _data_sources: List[DataSource] = list()

    @property
    def data_sources(self) -> Generator[DataSource, None, None]:
        for source in self._data_sources:
            yield source

    def num_sources(self) -> int:
        return len(self._data_sources)

    def add(self, data_source: DataSource):
        self._data_sources.append(data_source)

