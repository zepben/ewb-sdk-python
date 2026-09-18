#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["ChangeSetCimWriter"]

from zepben.ewb.database.sqlite.changeset.change_set_database_tables import ChangeSetDatabaseTables
from zepben.ewb.database.sqlite.common import using_table
from zepben.ewb.database.sqlite.common.base_cim_writer import BaseCimWriter
from zepben.ewb.database.sqlite.extensions.prepared_statement import PreparedStatement
from zepben.ewb.database.sqlite.tables.iec61970.infiec61970.part303.genericdataset.table_change_set_members import \
    TableChangeSetMembers
from zepben.ewb.database.sqlite.tables.iec61970.infiec61970.part303.genericdataset.table_change_sets import TableChangeSets
from zepben.ewb.database.sqlite.tables.iec61970.infiec61970.part303.genericdataset.table_data_sets import TableDataSets
from zepben.ewb.database.sqlite.tables.iec61970.infiec61970.part303.genericdataset.table_object_creations import \
    TableObjectCreations
from zepben.ewb.database.sqlite.tables.iec61970.infiec61970.part303.genericdataset.table_object_deletions import \
    TableObjectDeletions
from zepben.ewb.database.sqlite.tables.iec61970.infiec61970.part303.genericdataset.table_object_modifications import \
    TableObjectModifications
from zepben.ewb.model.cim.iec61970.infiec61970.part303.genericdataset.change_set import ChangeSet
from zepben.ewb.model.cim.iec61970.infiec61970.part303.genericdataset.change_set_member import ChangeSetMember
from zepben.ewb.model.cim.iec61970.infiec61970.part303.genericdataset.data_set import DataSet
from zepben.ewb.model.cim.iec61970.infiec61970.part303.genericdataset.object_creation import ObjectCreation
from zepben.ewb.model.cim.iec61970.infiec61970.part303.genericdataset.object_deletion import ObjectDeletion
from zepben.ewb.model.cim.iec61970.infiec61970.part303.genericdataset.object_modification import ObjectModification


class ChangeSetCimWriter(BaseCimWriter):
    """
    A class for writing the `VariantService` tables to the database.

    :param database_tables: The tables available in the database.
    """

    def __init__(self, database_tables: ChangeSetDatabaseTables):
        super().__init__(database_tables)
        self._database_tables: ChangeSetDatabaseTables

    ##########################################
    # IEC61970 Part303 GenericDataSet       #
    ##########################################

    @using_table(TableChangeSets)
    def save_change_set(self, change_set: ChangeSet, table, insert) -> bool:
        """
        Save the `ChangeSet` fields to `TableChangeSets`.

        :param change_set: The `ChangeSet` instance to write to the database.

        :return: True if the `ChangeSet` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        insert.add_value(table.network_model_project_stage_mrid.query_index,
                         self._mrid_or_none(change_set.network_model_project_stage))

        return self._save_data_set(table, insert, change_set, "change set")

    def _save_change_set_member(self, table: TableChangeSetMembers, insert: PreparedStatement,
                                change_set_member: ChangeSetMember, description: str) -> bool:
        insert.add_value(table.change_set_mrid.query_index, change_set_member.change_set.mrid)
        insert.add_value(table.target_object_mrid.query_index, change_set_member.target_object_mrid)

        return self._try_execute_single_update(insert, description)

    def _save_data_set(self, table: TableDataSets, insert: PreparedStatement, data_set: DataSet, description: str) -> bool:
        insert.add_value(table.mrid.query_index, data_set.mrid)
        insert.add_value(table.name_.query_index, data_set.name)
        insert.add_value(table.description.query_index, data_set.description)

        return self._try_execute_single_update(insert, description)

    @using_table(TableObjectCreations)
    def save_object_creation(self, object_creation: ObjectCreation, table, insert) -> bool:
        """
        Save the `ObjectCreation` fields to `TableObjectCreations`.

        :param object_creation: The `ObjectCreation` instance to write to the database.

        :return: True if the `ObjectCreation` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        return self._save_change_set_member(table, insert, object_creation, "object creation")

    @using_table(TableObjectDeletions)
    def save_object_deletion(self, object_deletion: ObjectDeletion, table, insert) -> bool:
        """
        Save the `ObjectDeletion` fields to `TableObjectDeletions`.

        :param object_deletion: The `ObjectDeletion` instance to write to the database.

        :return: True if the `ObjectDeletion` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        return self._save_change_set_member(table, insert, object_deletion, "object deletion")

    @using_table(TableObjectModifications)
    def save_object_modification(self, object_modification: ObjectModification, table, insert) -> bool:
        """
        Save the `ObjectModification` fields to `TableObjectModifications`.

        :param object_modification: The `ObjectModification` instance to write to the database.

        :return: True if the `ObjectModification` was successfully written to the database, otherwise False.
        :raises SqlException: For any errors encountered writing to the database.
        """
        return self._save_change_set_member(table, insert, object_modification, "object modification")
