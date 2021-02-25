#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import logging

from zepben.evolve import MetadataCollection, MetadataEntryWriter
from zepben.evolve.database.sqlite.writers.utils import validate_save

logger = logging.getLogger("metadata_entry_writer")

__all__ = ["MetadataCollectionWriter"]


class MetadataCollectionWriter(object):

    @staticmethod
    def save(metadata_collection: MetadataCollection, writer: MetadataEntryWriter) -> bool:
        status = True

        for data_source in metadata_collection.data_sources:
            status = status and validate_save(data_source, writer.save, lambda e: logger.error(f"Failed to save DataSource '{data_source.source}': {e}"))

        return status
