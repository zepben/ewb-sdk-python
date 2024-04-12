#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
__all__ = ["BaseServiceReader"]

from abc import ABC, abstractmethod
from sqlite3 import Connection

from zepben.evolve.database.sqlite.common.base_cim_reader import BaseCimReader
from zepben.evolve.database.sqlite.common.base_collection_reader import BaseCollectionReader
from zepben.evolve.database.sqlite.common.base_database_tables import BaseDatabaseTables
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_name_types import TableNameTypes
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_names import TableNames


class BaseServiceReader(BaseCollectionReader, ABC):
    """
    A base class for reading items stored in a `BaseService` from the database.

    :param tables: The tables available in the database.
    :param connection: A connection to the database.
    :param reader: The `BaseCimReader` used to load the objects from the database.
    """

    def __init__(
        self,
        tables: BaseDatabaseTables,
        connection: Connection,
        reader: BaseCimReader
    ):
        super().__init__(tables, connection)
        self._reader: BaseCimReader = reader
        """
        The `BaseCimReader` used to load the objects from the database.
        """

    def load(self) -> bool:
        return (self._do_load()
                and self._load_each(TableNameTypes, self._reader.load_name_types)
                and self._load_each(TableNames, self._reader.load_names))

    @abstractmethod
    def _do_load(self) -> bool:
        """
        Load the service specific objects from the database.

        :return: True if the objects were successfully loaded from the database, otherwise False
        """
