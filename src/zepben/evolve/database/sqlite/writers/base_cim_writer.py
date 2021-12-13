#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

import logging
from sqlite3 import Cursor
from typing import Set, Optional

from dataclassy import dataclass

from zepben.evolve import NameType, Name
from zepben.evolve.database.sqlite.tables.database_tables import DatabaseTables, PreparedStatement
from zepben.evolve.database.sqlite.tables.iec61968.common_tables import TableDocuments, TableOrganisations, TableOrganisationRoles
from zepben.evolve.database.sqlite.tables.iec61970.base.core_tables import TableIdentifiedObjects, TableNameTypes, TableNames
from zepben.evolve.database.sqlite.writers.utils import try_execute_single_update
from zepben.evolve.model.cim.iec61968.common.document import Document
from zepben.evolve.model.cim.iec61968.common.organisation import Organisation
from zepben.evolve.model.cim.iec61968.common.organisation_role import OrganisationRole
from zepben.evolve.model.cim.iec61970.base.core.identified_object import IdentifiedObject

logger = logging.getLogger(__name__)

__all__ = ["BaseCIMWriter"]


@dataclass(slots=True)
class BaseCIMWriter(object):
    """
    Helper methods for building insert statements. Note all fields need to be populated.
    """

    database_tables: DatabaseTables
    cursor: Cursor
    _failed_ids: Set[str] = set()

    def _save_document(self, table: TableDocuments, insert: PreparedStatement, document: Document, description: str) -> bool:
        insert.add_value(table.title.query_index, document.title)
        # TODO: JVM seems to use Z as TZ offset (for UTC+0?) while python uses +HH:mm format. Need to investigate here
        insert.add_value(table.created_date_time.query_index, f"{document.created_date_time.isoformat()}Z" if document.created_date_time else None)
        insert.add_value(table.author_name.query_index, document.author_name)
        insert.add_value(table.type.query_index, document.type)
        insert.add_value(table.status.query_index, document.status)
        insert.add_value(table.comment.query_index, document.comment)

        return self.save_identified_object(table, insert, document, description)

    def save_organisation(self, organisation: Organisation) -> bool:
        table = self.database_tables.get_table(TableOrganisations)
        insert = self.database_tables.get_insert(TableOrganisations)

        return self.save_identified_object(table, insert, organisation, "Organisation")

    def save_name_type(self, name_type: NameType) -> bool:
        table = self.database_tables.get_table(TableNameTypes)
        insert = self.database_tables.get_insert(TableNameTypes)

        insert.add_value(table.name_.query_index, name_type.name)
        insert.add_value(table.description.query_index, name_type.description)

        return self.try_execute_single_update(insert, name_type.name, "name type")

    def save_name(self, name: Name) -> bool:
        table = self.database_tables.get_table(TableNames)
        insert = self.database_tables.get_insert(TableNames)

        insert.add_value(table.name_.query_index, name.name)
        insert.add_value(table.name_type_name.query_index, name.type.name)
        insert.add_value(table.identified_object_mrid.query_index, name.identified_object.mrid)

        return self.try_execute_single_update(insert, name.name, "name")

    def save_organisation_role(self, table: TableOrganisationRoles, insert: PreparedStatement, organisation_role: OrganisationRole, description: str) -> bool:
        insert.add_value(table.organisation_mrid.query_index, self._mrid_or_none(organisation_role.organisation))
        return self.save_identified_object(table, insert, organisation_role, description)

    def save_identified_object(self, table: TableIdentifiedObjects, insert: PreparedStatement, identified_object: IdentifiedObject, description: str) -> bool:
        insert.add_value(table.mrid.query_index, identified_object.mrid)
        insert.add_value(table.name_.query_index, identified_object.name)
        insert.add_value(table.description.query_index, identified_object.description)
        insert.add_value(table.num_diagram_objects.query_index, 0)  # Currently unused

        return self.try_execute_single_update(insert, identified_object.mrid, description)

    def try_execute_single_update(self, query: PreparedStatement, mrid: str, description: str) -> bool:
        """
        Execute an update on the database with the given `query`.
        Failures will be logged as warnings.
        `query` The PreparedStatement to execute.
        `mrid` The mRID of the relevant object that is being saved
        `description` A description of the type of object (e.g AcLineSegment)
        Returns True if the execute was successful, False otherwise.
        """
        return try_execute_single_update(query, self.cursor, description, lambda: self._failed_ids.add(mrid))

    @staticmethod
    def _mrid_or_none(io: Optional[IdentifiedObject]) -> Optional[str]:
        if io is not None:
            return io.mrid
        else:
            return None
