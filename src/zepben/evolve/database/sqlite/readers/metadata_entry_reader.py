#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import datetime
from typing import Callable

from zepben.evolve import MetadataCollection, TableMetadataDataSources, ResultSet, DataSource

__all__ = ["MetadataEntryReader"]


class MetadataEntryReader:
    _metadata_collection: MetadataCollection

    def __init__(self, metadata_collection: MetadataCollection):
        self._metadata_collection = metadata_collection

    def load_metadata(self, table: TableMetadataDataSources, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        # noinspection PyArgumentList
        data_source = DataSource(
            set_last_mrid(rs.get_string(table.source.query_index)),
            rs.get_string(table.version.query_index),
            rs.get_instant(table.timestamp.query_index, datetime.datetime(1970, 1, 1))
        )

        return self._metadata_collection.add(data_source)
