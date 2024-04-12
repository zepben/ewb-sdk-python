#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
__all__ = ["BaseDatabaseReader"]

import logging
from abc import ABC
from contextlib import closing
from sqlite3 import Connection
from typing import Optional

from zepben.evolve.database.sqlite.common.base_service_reader import BaseServiceReader
from zepben.evolve.database.sqlite.common.metadata_collection_reader import MetadataCollectionReader
from zepben.evolve.database.sqlite.tables.table_version import TableVersion
from zepben.evolve.services.common.base_service import BaseService


class BaseDatabaseReader(ABC):
    """
    A base class for reading objects from one of our databases.
    """

    def __init__(
        self,
        connection: Connection,
        metadata_reader: MetadataCollectionReader,
        service_reader: BaseServiceReader,
        service: BaseService,
        database_description: str,
        table_version: TableVersion
    ):
        super().__init__()
        self._logger: logging.Logger = logging.getLogger(self.__class__.__name__)
        """
        The logger to use for this reader.
        """

        self._connection: Connection = connection
        """
        The connection to the database.
        """

        self._metadata_reader: MetadataCollectionReader = metadata_reader
        """
        The reader for the [MetadataCollection] included in the database.
        """

        self._service_reader: BaseServiceReader = service_reader
        """
        The reader for the [BaseService] supported by the database.
        """

        self._service: BaseService = service
        """
        The [BaseService] that will be populated by the [BaseServiceReader]. Used for post-processing.
        """

        self._database_description: str = database_description
        """
        The description of the database for logging (e.g. filename).
        """

        self._table_version: TableVersion = table_version
        """
        The version table object for checking the database version number.
        """

        self._has_been_used: bool = False
        self._supported_version: int = table_version.SUPPORTED_VERSION

    async def _post_load(self) -> bool:
        """
        Customisable function for performing actions after the database has been loaded.
        """
        self._logger.info("Ensuring all references resolved...")
        for it in self._service.unresolved_references():
            raise ValueError(
                f"Unresolved references found in {self._service.name} service after load - this should not occur. Failing reference was from " +
                f"{it.from_ref} resolving {it.resolver.to_class.__name__} {it.to_mrid}"
            )
        self._logger.info("Unresolved references were all resolved during load.")

        return True

    async def load(self) -> bool:
        """
        Load the database.
        """
        try:
            if self._has_been_used:
                raise ValueError("You can only use the database reader once.")
            self._has_been_used = True

            return self._pre_load() and self._load_from_readers() and await self._post_load()
        except Exception as e:
            self._logger.exception(f"Unable to load database: {e}")
            return False

    def _pre_load(self) -> bool:
        try:
            with closing(self._connection.cursor()) as cur:
                version = self._table_version.get_version(cur)
                if version == self._supported_version:
                    self._logger.info(f"Loading from database version v{version}")
                    return True
                else:
                    self._logger.error(self._format_version_error(version))
                    return False
        except Exception as e:
            self._logger.exception(f"Failed to connect to the database for reading: {e}")
            return False

    def _load_from_readers(self):
        return self._metadata_reader.load() and self._service_reader.load()

    def _format_version_error(self, version: Optional[int]) -> str:
        if version is None:
            return "Failed to read the version number form the selected database. Are you sure it is a EWB database?"
        elif version < self._supported_version:
            return self._unexpected_version(version, "Consider using the UpgradeRunner if you wish to support this database.")
        else:
            return self._unexpected_version(version, "You need to use a newer version of the SDK to load this database.")

    def _unexpected_version(self, version: Optional[int], action: str):
        return f"Unable to load from database {self._database_description} [found v{version}, expected v{self._supported_version}]. {action}"
