#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["ChangeSetCimReader"]

from typing import Callable

from zepben.ewb.database.sqlite.common.base_cim_reader import BaseCimReader
from zepben.ewb.database.sqlite.extensions.result_set import ResultSet
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
from zepben.ewb.services.common import resolver
from zepben.ewb.services.variant.variant_service import VariantService


class ChangeSetCimReader(BaseCimReader):
    """
    A class for reading the `VariantService` tables from the database.

    :param service: The `VariantService` to populate from the database.
    """

    def __init__(self, service: VariantService):
        super().__init__(service)
        self._service: VariantService
        """The :class:`VariantService` used to store any items read from the database."""

    ##########################################
    # IEC61970 Part303 GenericDataSet       #
    ##########################################

    def load_change_sets(self, table: TableChangeSets, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        """
        Create a `ChangeSet` and populate its fields from `TableChangeSets`.

        :param table: The database table to read the `ChangeSet` fields from.
        :param result_set: The record in the database table containing the fields for this `ChangeSet`.
        :param set_identifier: A callback to register the mRID of this `ChangeSet` for logging purposes.

        :return: True if the `ChangeSet` was successfully read from the database and added to the service.
        """
        change_set = ChangeSet(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))
        self._service.resolve_or_defer_reference(
            resolver.stage(change_set),
            result_set.get_string(table.network_model_project_stage_mrid.query_index, on_none=None),
            change_set.mrid
        )

        return self._load_data_set(change_set, table, result_set) and self._add_or_throw(change_set)

    def _load_data_set(self, data_set: DataSet, table: TableDataSets, result_set: ResultSet) -> bool:
        data_set.name = result_set.get_string(table.name_.query_index, on_none=None)
        data_set.description = result_set.get_string(table.description.query_index, on_none=None)

        return True

    def _load_change_set_member(self, cim: ChangeSetMember, table: TableChangeSetMembers, result_set: ResultSet,
                                set_identifier: Callable[[str], str]) -> bool:
        change_set_mrid = result_set.get_string(table.change_set_mrid.query_index)
        set_identifier(f"{change_set_mrid}-to-UNKNOWN")
        cim.target_object_mrid = result_set.get_string(table.target_object_mrid.query_index)
        ident = set_identifier(f"{change_set_mrid}-to-{cim.target_object_mrid}")

        cim.change_set = self._service.get(change_set_mrid, ChangeSet, generate_error=lambda mrid, typ: ident)
        cim.change_set.add_member(cim)

        return True

    def load_object_creations(self, table: TableObjectCreations, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        """
        Create an `ObjectCreation` and populate its fields from `TableObjectCreations`.

        :param table: The database table to read the `ObjectCreation` fields from.
        :param result_set: The record in the database table containing the fields for this `ObjectCreation`.
        :param set_identifier: A callback to register the identifier of this `ObjectCreation` for logging purposes.

        :return: True if the `ObjectCreation` was successfully read from the database and added to the service.
        """
        object_creation = ObjectCreation()

        return self._load_change_set_member(object_creation, table, result_set, set_identifier) and self._add_or_throw(object_creation)

    def load_object_deletions(self, table: TableObjectDeletions, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        """
        Create an `ObjectDeletion` and populate its fields from `TableObjectDeletions`.

        :param table: The database table to read the `ObjectDeletion` fields from.
        :param result_set: The record in the database table containing the fields for this `ObjectDeletion`.
        :param set_identifier: A callback to register the identifier of this `ObjectDeletion` for logging purposes.

        :return: True if the `ObjectDeletion` was successfully read from the database and added to the service.
        """
        object_deletion = ObjectDeletion()

        return self._load_change_set_member(object_deletion, table, result_set, set_identifier) and self._add_or_throw(object_deletion)

    def load_object_modifications(self, table: TableObjectModifications, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        """
        Create an `ObjectModification` and populate its fields from `TableObjectModifications`.

        :param table: The database table to read the `ObjectModification` fields from.
        :param result_set: The record in the database table containing the fields for this `ObjectModification`.
        :param set_identifier: A callback to register the identifier of this `ObjectModification` for logging purposes.

        :return: True if the `ObjectModification` was successfully read from the database and added to the service.
        """
        object_modification = ObjectModification()

        return self._load_change_set_member(object_modification, table, result_set, set_identifier) and self._add_or_throw(object_modification)
