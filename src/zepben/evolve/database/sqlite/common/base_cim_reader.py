#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
__all__ = ["BaseCimReader"]

import logging
from abc import ABC
from typing import Callable, Optional, Type

from zepben.evolve.database.sqlite.common.reader_exceptions import DuplicateMRIDException
from zepben.evolve.database.sqlite.extensions.result_set import ResultSet
from zepben.evolve.database.sqlite.tables.iec61968.common.table_documents import TableDocuments
from zepben.evolve.database.sqlite.tables.iec61968.common.table_organisation_roles import TableOrganisationRoles
from zepben.evolve.database.sqlite.tables.iec61968.common.table_organisations import TableOrganisations
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_identified_objects import TableIdentifiedObjects
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_name_types import TableNameTypes
from zepben.evolve.database.sqlite.tables.iec61970.base.core.table_names import TableNames
from zepben.evolve.model.cim.iec61968.common.document import Document
from zepben.evolve.model.cim.iec61968.common.organisation import Organisation
from zepben.evolve.model.cim.iec61968.common.organisation_role import OrganisationRole
from zepben.evolve.model.cim.iec61970.base.core.identified_object import IdentifiedObject, TIdentifiedObject
from zepben.evolve.model.cim.iec61970.base.core.name_type import NameType
from zepben.evolve.services.common.base_service import BaseService


class BaseCimReader(ABC):
    """
    A base class for reading CIM objects from a database.
    """

    def __init__(self, service: BaseService):
        super().__init__()
        self._logger: logging.Logger = logging.getLogger(self.__class__.__name__)
        """The `Logger` to use for this reader."""

        self._service = service
        """The `BaseService` used to store any items read from the database."""

    ###################
    # IEC61968 Common #
    ###################

    def _load_document(self, document: Document, table: TableDocuments, result_set: ResultSet) -> bool:
        """
        Populate the `Document` fields from `TableDocuments`.

        :param document: The `Document` instance to populate.
        :param table: The database table to read the `Document` fields from.
        :param result_set: The record in the database table containing the fields for this `Document`.

        :return: True if the `Document` was successfully read from the database and added to the service.
        :raises SQLException: For any errors encountered reading from the database.
        """
        document.title = result_set.get_string(table.title.query_index, on_none="")
        document.created_date_time = result_set.get_instant(table.created_date_time.query_index, on_none=None)
        document.author_name = result_set.get_string(table.author_name.query_index, on_none="")
        document.type = result_set.get_string(table.type.query_index, on_none="")
        document.status = result_set.get_string(table.status.query_index, on_none="")
        document.comment = result_set.get_string(table.comment.query_index, on_none="")

        return self._load_identified_object(document, table, result_set)

    def load_organisations(self, table: TableOrganisations, result_set: ResultSet, set_identifier: Callable[[str], str]) -> bool:
        """
        Create an `Organisation` and populate its fields from `TableOrganisations`.

        :param table: The database table to read the `Organisation` fields from.
        :param result_set: The record in the database table containing the fields for this `Organisation`.
        :param set_identifier: A callback to register the mRID of this `Organisation` for logging purposes.

        :return: True if the `Organisation` was successfully read from the database and added to the service.
        :raises SQLException: For any errors encountered reading from the database.
        """
        organisation = Organisation(mrid=set_identifier(result_set.get_string(table.mrid.query_index)))

        return self._load_identified_object(organisation, table, result_set) and self._add_or_throw(organisation)

    def load_name_types(self, table: TableNameTypes, result_set: ResultSet, set_last_name_type: Callable[[str], str]) -> bool:
        """
        Create a `NameType` and populate its fields from `TableNameTypes`.

        :param table: The database table to read the `NameType` fields from.
        :param result_set: The record in the database table containing the fields for this `NameType`.
        :param set_last_name_type: A callback to register the name of this `NameType` for logging purposes.

        :return: True if the `NameType` was successfully read from the database and added to the service.
        :raises SQLException: For any errors encountered reading from the database.
        """
        # noinspection PyArgumentList
        name_type = NameType(set_last_name_type(result_set.get_string(table.name_.query_index)))
        name_type.description = result_set.get_string(table.description.query_index)

        return self._add_or_throw_name_type(name_type)

    def load_names(self, table: TableNames, result_set: ResultSet, set_last_name: Callable[[str], str]) -> bool:
        """
        Create a `Name` and populate its fields from `TableNames`.

        :param table: The database table to read the `Name` fields from.
        :param result_set: The record in the database table containing the fields for this `Name`.
        :param set_last_name: A callback to register the name of this `Name` for logging purposes.

        :return: True if the `Name` was successfully read from the database and added to the service.
        :raises SQLException: For any errors encountered reading from the database.
        """
        name_type_name = result_set.get_string(table.name_type_name.query_index)
        name_name = result_set.get_string(table.name_.query_index)
        set_last_name(f"{name_type_name}:{name_name}")

        name_type = self._service.get_name_type(name_type_name)
        self._service.get(
            result_set.get_string(table.identified_object_mrid.query_index),
            IdentifiedObject,
            generate_error=lambda mrid, typ: f"Failed to find {typ} with mRID {mrid} for Name {name_name} [{name_type_name}]"
        ).add_name(name_type, name_name)

        return True

    def _load_organisation_role(self, organisation_role: OrganisationRole, table: TableOrganisationRoles, result_set: ResultSet) -> bool:
        """
        Populate the `OrganisationRole` fields from `TableOrganisationRoles`.

        :param organisation_role: The `OrganisationRole` instance to populate.
        :param table: The database table to read the `OrganisationRole` fields from.
        :param result_set: The record in the database table containing the fields for this `OrganisationRole`.

        :return: True if the `OrganisationRole` was successfully read from the database and added to the service.
        :raises SQLException: For any errors encountered reading from the database.
        """
        organisation_role.organisation = self._ensure_get(
            result_set.get_string(table.organisation_mrid.query_index, on_none=None),
            Organisation
        )

        return self._load_identified_object(organisation_role, table, result_set)

    ######################
    # IEC61970 Base Core #
    ######################

    @staticmethod
    def _load_identified_object(identified_object: IdentifiedObject, table: TableIdentifiedObjects, result_set: ResultSet) -> bool:
        """
        Populate the `IdentifiedObject` fields from `TableIdentifiedObjects`.

        :param identified_object: The `IdentifiedObject` instance to populate.
        :param table: The database table to read the `IdentifiedObject` fields from.
        :param result_set: The record in the database table containing the fields for this `IdentifiedObject`.

        :return: True if the `IdentifiedObject` was successfully read from the database and added to the service.
        :raises SQLException: For any errors encountered reading from the database.
        """
        identified_object.name = result_set.get_string(table.name_.query_index, on_none="")
        identified_object.description = result_set.get_string(table.description.query_index, on_none="")
        # Currently unused
        # identified_object.num_diagram_objects = result_set.get_int(table.num_diagram_objects.query_index)

        return True

    def _add_or_throw(self, identified_object: IdentifiedObject) -> bool:
        """
        Try and add the `identified_object` to the `service`, and throw an `Exception` if unsuccessful.

        :param identified_object: The `IdentifiedObject` to add to the `service`.

        :return: True in all instances, otherwise it throws.
        :raises DuplicateMRIDException: If the `IdentifiedObject.mRID` has already been used.
        :raises UnsupportedIdentifiedObjectException: If the `IdentifiedObject` is not supported by the `service`. This is an indication of an internal coding
          issue, rather than a problem with the data being read, and in a correctly configured system will never occur.
        """
        if self._service.add(identified_object):
            return True
        else:
            duplicate = self._service.get(identified_object.mrid)
            raise DuplicateMRIDException(
                f"Failed to load {identified_object}. " +
                f"Unable to add to service '{self._service.name}': duplicate MRID ({duplicate})"
            )

    def _add_or_throw_name_type(self, name_type: NameType) -> bool:
        """
        Try and add the `name_type` to the `service`, and throw an `Exception` if unsuccessful.

        :param name_type: The `NameType` to add to the `service`.

        :return: True in all instances, otherwise it throws.
        :raises DuplicateMRIDException: If the `NameType.name` has already been used.
        """
        if self._service.add_name_type(name_type):
            return True
        else:
            raise DuplicateMRIDException(
                f"Failed to load NameType {name_type.name}. " +
                f"Unable to add to service '{self._service.name}': duplicate NameType)"
            )

    def _ensure_get(self, mrid: Optional[str], type_: Type[TIdentifiedObject] = IdentifiedObject) -> Optional[TIdentifiedObject]:
        """
        Optionally get an object associated with this service and throw if it is not found.

        :param mrid: The mRID of the object to find.
        :param type_: The type of object to look for. If this is a base class it will search all subclasses.

        :return: The object identified by `mrid` as `type_` if it was found, or null if no `mrid` was supplied.
        :raises MRIDLookupException: if no objects of type `type_` are found with the specified `mrid`
        """
        if (mrid is None) or (len(mrid) == 0):
            return None
        else:
            return self._service.get(mrid, type_)
