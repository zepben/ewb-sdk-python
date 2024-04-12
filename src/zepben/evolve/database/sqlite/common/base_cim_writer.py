#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
__all__ = ["BaseCimWriter"]

from abc import ABC
from typing import Optional

from zepben.evolve.database.sqlite.common.base_database_tables import BaseDatabaseTables
from zepben.evolve.database.sqlite.common.base_entry_writer import BaseEntryWriter
from zepben.evolve.database.sqlite.extensions.prepared_statement import PreparedStatement
from zepben.evolve.database.sqlite.tables.iec61968.common.table_documents import TableDocuments
from zepben.evolve.database.sqlite.tables.iec61968.common.table_organisation_roles import TableOrganisationRoles
from zepben.evolve.database.sqlite.tables.iec61968.common.table_organisations import TableOrganisations
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_identified_objects import TableIdentifiedObjects
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_name_types import TableNameTypes
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_names import TableNames
from zepben.evolve.model.cim.iec61968.common.document import Document
from zepben.evolve.model.cim.iec61968.common.organisation import Organisation
from zepben.evolve.model.cim.iec61968.common.organisation_role import OrganisationRole
from zepben.evolve.model.cim.iec61970.base.core.identified_object import IdentifiedObject
from zepben.evolve.model.cim.iec61970.base.core.name import Name
from zepben.evolve.model.cim.iec61970.base.core.name_type import NameType


class BaseCimWriter(BaseEntryWriter, ABC):
    """
    A base class for writing CIM objects to a database.
    """

    def __init__(self, database_tables: BaseDatabaseTables):
        super().__init__()
        self._database_tables = database_tables

    ###################
    # IEC61968 Common #
    ###################

    def _save_document(self, table: TableDocuments, insert: PreparedStatement, document: Document, description: str) -> bool:
        """
        Save the `Document` fields to `TableDocuments`.

        :param table: The database table to write the `Document` fields to.
        :param insert: The `PreparedStatement` to bind the field values to.
        :param document: The `Document` instance to write to the database.
        :param description: A readable version of the type of object being written for logging purposes.

        :return: True if the `Document` was successfully written to the database, otherwise false.
        :raises SQLException: For any errors encountered writing to the database.
        """
        insert.add_value(table.title.query_index, document.title)
        # The timestamp in the database uses Z for UTC while python uses +HH:mm format, so convert between them.
        insert.add_value(table.created_date_time.query_index, f"{document.created_date_time.isoformat()}Z" if document.created_date_time else None)
        insert.add_value(table.author_name.query_index, document.author_name)
        insert.add_value(table.type.query_index, document.type)
        insert.add_value(table.status.query_index, document.status)
        insert.add_value(table.comment.query_index, document.comment)

        return self._save_identified_object(table, insert, document, description)

    def save_organisation(self, organisation: Organisation) -> bool:
        """
        Save the `Organisation` fields to `TableOrganisations`.

        :param organisation: The `Organisation` instance to write to the database.

        :return: True if the `Organisation` was successfully written to the database, otherwise false.
        :raises SQLException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableOrganisations)
        insert = self._database_tables.get_insert(TableOrganisations)

        return self._save_identified_object(table, insert, organisation, "organisation")

    def save_name_type(self, name_type: NameType) -> bool:
        """
        Save the `NameType` fields to `TableNameTypes`.

        :param name_type: The `NameType` instance to write to the database.

        :return: True if the `NameType` was successfully written to the database, otherwise false.
        :raises SQLException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableNameTypes)
        insert = self._database_tables.get_insert(TableNameTypes)

        return self._save_name_type(table, insert, name_type)

    def save_name(self, name: Name) -> bool:
        """
        Save the `Name` fields to `TableNames`.

        :param name: The `Name` instance to write to the database.

        :return: True if the `Name` was successfully written to the database, otherwise false.
        :raises SQLException: For any errors encountered writing to the database.
        """
        table = self._database_tables.get_table(TableNames)
        insert = self._database_tables.get_insert(TableNames)

        return self._save_name(table, insert, name)

    def _save_organisation_role(self, table: TableOrganisationRoles, insert: PreparedStatement, organisation_role: OrganisationRole, description: str) -> bool:
        """
        Save the `OrganisationRole` fields to `TableOrganisationRoles`.

        :param table: The database table to write the `OrganisationRole` fields to.
        :param insert: The `PreparedStatement` to bind the field values to.
        :param organisation_role: The `OrganisationRole` instance to write to the database.
        :param description: A readable version of the type of object being written for logging purposes.

        :return: True if the `OrganisationRole` was successfully written to the database, otherwise false.
        :raises SQLException: For any errors encountered writing to the database.
        """
        insert.add_value(table.organisation_mrid.query_index, self._mrid_or_none(organisation_role.organisation))

        return self._save_identified_object(table, insert, organisation_role, description)

    ######################
    # IEC61970 Base Core #
    ######################

    def _save_identified_object(
        self,
        table: TableIdentifiedObjects,
        insert: PreparedStatement,
        identified_object: IdentifiedObject,
        description: str
    ) -> bool:
        """
        Save the `IdentifiedObject` fields to `TableIdentifiedObjects`.

        :param table: The database table to write the `IdentifiedObject` fields to.
        :param insert: The `PreparedStatement` to bind the field values to.
        :param identified_object: The `IdentifiedObject` instance to write to the database.
        :param description: A readable version of the type of object being written for logging purposes.

        :return: True if the `IdentifiedObject` was successfully written to the database, otherwise false.
        :raises SQLException: For any errors encountered writing to the database.
        """
        insert.add_value(table.mrid.query_index, identified_object.mrid)
        insert.add_value(table.name_.query_index, identified_object.name)
        insert.add_value(table.description.query_index, identified_object.description)
        insert.add_value(table.num_diagram_objects.query_index, 0)  # Currently unused

        return self._try_execute_single_update(insert, description)

    def _save_name_type(self, table: TableNameTypes, insert: PreparedStatement, name_type: NameType) -> bool:
        insert.add_value(table.name_.query_index, name_type.name)
        insert.add_value(table.description.query_index, name_type.description)

        return self._try_execute_single_update(insert, "name type")

    def _save_name(self, table: TableNames, insert: PreparedStatement, name: Name) -> bool:
        insert.add_value(table.name_.query_index, name.name)
        insert.add_value(table.name_type_name.query_index, name.type.name)
        insert.add_value(table.identified_object_mrid.query_index, name.identified_object.mrid)

        return self._try_execute_single_update(insert, "name")

    @staticmethod
    def _mrid_or_none(io: Optional[IdentifiedObject]) -> Optional[str]:
        return io.mrid if io is not None else None
