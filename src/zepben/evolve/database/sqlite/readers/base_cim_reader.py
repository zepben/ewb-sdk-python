#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

import logging
from typing import Callable, Optional, Type, TypeVar

from zepben.evolve import BaseService, Document, TableDocuments, Organisation, TableOrganisations, TableNameTypes, NameType, TableNames, IdentifiedObject, \
    OrganisationRole, TableOrganisationRoles, TableIdentifiedObjects, ResultSet

logger = logging.getLogger(__name__)

__all__ = ["DuplicateMRIDException", "BaseCIMReader"]


class DuplicateMRIDException(Exception):
    pass


T = TypeVar("T", bound=IdentifiedObject)


class BaseCIMReader(object):
    _base_service: BaseService

    def __init__(self, base_service: BaseService):
        self._base_service = base_service

    # ************ IEC61968 COMMON ************

    def _load_document(self, document: Document, table: TableDocuments, rs: ResultSet) -> bool:
        document.title = rs.get_string(table.title.query_index, "")
        document.created_date_time = rs.get_instant(table.created_date_time.query_index, None)
        document.author_name = rs.get_string(table.author_name.query_index, "")
        document.type = rs.get_string(table.type.query_index, "")
        document.status = rs.get_string(table.status.query_index, "")
        document.comment = rs.get_string(table.comment.query_index, "")

        return self._load_identified_object(document, table, rs)

    def load_organisation(self, table: TableOrganisations, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        organisation = Organisation(mrid=set_last_mrid(rs.get_string(table.mrid.query_index)))

        return self._load_identified_object(organisation, table, rs) and self._add_or_throw(organisation)

    def load_name_type(self, table: TableNameTypes, rs: ResultSet, set_last_name_type: Callable[[str], str]) -> bool:
        # noinspection PyArgumentList
        name_type = NameType(name=set_last_name_type(rs.get_string(table.name_.query_index)))
        name_type.description = rs.get_string(table.description.query_index, None)

        return self._add_or_throw_name_type(name_type)

    def load_name(self, table: TableNames, rs: ResultSet, set_last_name: Callable[[str], str]) -> bool:
        name_type_name = rs.get_string(table.name_type_name.query_index)
        name_name = rs.get_string(table.name_.query_index)
        set_last_name(f"{name_type_name}:{name_name}")

        name_type = self._base_service.get_name_type(name_type_name)
        # Because each service type loads all the name types, but not all services hold all identified objects, there can
        # be records in the names table that only apply to certain services. We attempt to find the IdentifiedObject on this
        # service and add a name for it if it exists, but ignore if it doesn't. Note that this can potentially lead to there being
        # a name record that never gets used because that identified object doesn't exist in any service and currently we
        # don't check or warn about that.
        io = self._base_service.get(rs.get_string(table.identified_object_mrid.query_index), default=None)
        if io is not None:
            name = name_type.get_or_add_name(name_name, io)
            io.add_name(name)

        return True

    def _load_organisation_role(self, organisation_role: OrganisationRole, table: TableOrganisationRoles, rs: ResultSet) -> bool:
        organisation_role.organisation = self._ensure_get(rs.get_string(table.organisation_mrid.query_index, None), Organisation)

        return self._load_identified_object(organisation_role, table, rs)

    # ************ IEC61970 CORE ************

    @staticmethod
    def _load_identified_object(identified_object: IdentifiedObject, table: TableIdentifiedObjects, rs: ResultSet) -> bool:
        identified_object.name = rs.get_string(table.name_.query_index, "")
        identified_object.description = rs.get_string(table.description.query_index, "")
        # Currently unused identified_object.num_diagram_objects = rs.get_int(table.num_diagram_objects.query_index)

        return True

    def _add_or_throw(self, identified_object: IdentifiedObject) -> bool:
        if self._base_service.add(identified_object):
            return True
        else:
            duplicate = self._base_service.get(identified_object.mrid)
            raise DuplicateMRIDException(
                f"Failed to load {identified_object}. " +
                f"Unable to add to service '{self._base_service.name}': duplicate MRID ({duplicate})"
            )

    def _add_or_throw_name_type(self, name_type: NameType) -> bool:
        if self._base_service.add_name_type(name_type):
            return True
        else:
            raise DuplicateMRIDException(
                f"Failed to load NameType {name_type.name}. " +
                f"Unable to add to service '{self._base_service.name}': duplicate NameType)"
            )

    def _ensure_get(self, mrid: Optional[str], type_: Type[T] = IdentifiedObject) -> Optional[T]:
        if (mrid is None) or (len(mrid) == 0):
            return None
        else:
            return self._base_service.get(mrid, type_)
