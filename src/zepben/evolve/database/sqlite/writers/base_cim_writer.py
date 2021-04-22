#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

import sqlite3
import logging
from contextlib import contextmanager
from sqlite3 import DatabaseError
from typing import Set, Generator

from dataclassy import dataclass

from zepben.evolve.model.cim.iec61970.base.core.identified_object import IdentifiedObject
from zepben.evolve.model.cim.iec61968.common.organisation import Organisation
from zepben.evolve.model.cim.iec61968.common.organisation_role import OrganisationRole
from zepben.evolve.model.cim.iec61968.common.document import Document
from zepben.evolve.database.sqlite.tables.database_tables import DatabaseTables, PreparedStatement
from zepben.evolve.database.sqlite.tables.iec61968.common_tables import TableDocuments, TableOrganisations, TableOrganisationRoles
from zepben.evolve.database.sqlite.tables.iec61970.base.core_tables import TableIdentifiedObjects

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class BaseCIMWriter(object):
    """
    Helper methods for building insert statements. Note all fields need to be populated.
    """

    database_tables: DatabaseTables
    connection_string: str
    _failed_ids: Set[str] = set()

    @contextmanager
    def connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.connection_string)
        conn.isolation_level = None  # autocommit off
        yield conn
        conn.commit()
        conn.close()

    @contextmanager
    def cursor(self) -> Generator[sqlite3.Cursor, None, None]:
        with self.connection() as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA journal_mode = OFF")
            cursor.execute("PRAGMA synchronous = OFF")
            yield cursor
            cursor.close()

    def save_document(self, table: TableDocuments, insert: PreparedStatement, document: Document, description: str) -> bool:
        insert.add_value(table.title.query_index, document.title)
        insert.add_value(table.created_date_time.query_index, document.created_date_time)
        insert.add_value(table.author_name.query_index, document.author_name)
        insert.add_value(table.type.query_index, document.type)
        insert.add_value(table.status.query_index, document.status)
        insert.add_value(table.comment.query_index, document.comment)

        return self.save_identified_object(table, insert, document, description)

    def save_organisation(self, organisation: Organisation) -> bool:
        table = self.database_tables.get_table(TableOrganisations)
        insert = self.database_tables.get_insert(TableOrganisations)

        return self.save_identified_object(table, insert, organisation, "Organisation")

    def save_organisation_role(self, table: TableOrganisationRoles, insert: PreparedStatement, organisation_role: OrganisationRole, description: str) -> bool:
        if organisation_role.organisation is not None:
            insert.add_value(table.organisation_mrid.query_index, organisation_role.organisation.mrid)
        return self.save_identified_object(table, insert, organisation_role, description)

    def save_identified_object(self, table: TableIdentifiedObjects, insert: PreparedStatement, identified_object: IdentifiedObject, description: str) -> bool:
        insert.add_value(table.mrid.query_index, identified_object.mrid)
        insert.add_value(table.name_.query_index, identified_object.name)
        insert.add_value(table.description.query_index, identified_object.description)
        insert.add_value(table.num_diagram_objects.query_index, 0)  # Currently unused

        return self.try_execute_single_update(insert, identified_object.mrid, description)

    def try_execute_single_update(self, query: PreparedStatement, id: str, description: str) -> bool:
        """
        Execute an update on the database with the given `query`.
        Failures will be logged as warnings.
        `query` The PreparedStatement to execute.
        `id` The mRID of the relevant object that is being saved
        `description` A description of the type of object (e.g AcLineSegment)
        Returns True if the execute was successful, False otherwise.
        """
        try:
            with self.cursor() as c:
                query.execute(c)
            return True
        except DatabaseError as de:
            self._failed_ids.add(id)
            logger.warning(f"Failed to save {description}. Error was: {de}\n  SQL: {query}\n  Fields: {query.parameters()}")
            return False

