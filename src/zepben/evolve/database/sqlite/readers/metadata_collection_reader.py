#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve import BaseServiceReader, MetadataEntryReader, TableMetadataDataSources

__all__ = ["MetadataCollectionReader"]


class MetadataCollectionReader(BaseServiceReader):
    """
    Class for reading the [MetadataCollection] from the database.
    """

    def load(self, reader: MetadataEntryReader) -> bool:
        status = True

        status = status and self._load_each(TableMetadataDataSources, "metadata data sources", reader.load_metadata)

        return status
