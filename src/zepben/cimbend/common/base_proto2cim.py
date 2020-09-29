"""
Copyright 2019 Zeppelin Bend Pty Ltd
This file is part of cimbend.

cimbend is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

cimbend is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with cimbend.  If not, see <https://www.gnu.org/licenses/>.
"""


from abc import ABCMeta
from dataclasses import dataclass

from zepben.cimbend.common.base_service import BaseService
from zepben.protobuf.cim.iec61970.base.core.IdentifiedObject_pb2 import IdentifiedObject as PBIdentifiedObject
from zepben.protobuf.cim.iec61968.common.Document_pb2 import Document as PBDocument

from zepben.cimbend.cim.iec61968.common.document import Document
from zepben.cimbend.cim.iec61968.common import Organisation
from zepben.cimbend.cim.iec61968.common.organisation_role import OrganisationRole
from zepben.protobuf.cim.iec61968.common.Organisation_pb2 import Organisation as PBOrganisation
from zepben.protobuf.cim.iec61968.common.OrganisationRole_pb2 import OrganisationRole as PBOrganisationRole
from zepben.cimbend.cim.iec61970.base.core.identified_object import IdentifiedObject
from typing import Any
from zepben.cimbend.common import resolver

__all__ = ["set_identifiedobject", "BaseProtoToCim", "set_document", "organisation_to_cim", "organisationrole_to_cim"]


#def set_field(cim, pb, field):
#    snaked = _cached_fields.setdefault(field, camel2snake(field))
#    if hasattr(cim, snaked):
#        setattr(cim, snaked, getattr(pb, field))
#    elif hasattr(cim, f"_{snaked}"):
#        setattr(cim, f"_{snaked}", getattr(pb, field))
#    else:
#        raise AttributeError(
#            f"{type(cim)} has no field for {snaked}. All CIM objects must have corresponding proto fields")


# IEC61970 CORE #
def set_identifiedobject(pb: PBIdentifiedObject, cim: IdentifiedObject, service: BaseService):
    cim.mrid = pb.mRID
    cim.name = pb.name
    cim.num_diagram_objects = pb.numDiagramObjects
    service.add(cim)


# IEC61968 COMMON #
def set_document(pb: PBDocument, cim: Document, service: BaseService):
    cim.title = pb.title
    cim.created_date_time = pb.createdDateTime.ToDatetime()
    cim.author_name = pb.authorName
    cim.type = pb.type
    cim.status = pb.status
    cim.comment = pb.comment
    set_identifiedobject(pb.io, cim, service)


@dataclass
class BaseProtoToCim(object, metaclass=ABCMeta):
    service: BaseService

    # def set(self, pb: Message, cim: IdentifiedObject):
    #     for field in pb.DESCRIPTOR.fields:
    #         pb_field = getattr(pb, field.name)
    #         if field.name.endswith('MRID'):
    #             if pb_field:
    #                 # Not empty
    #                 self._service.get(pb_field, _type=)
    #
    #         try:
    #             if pb.HasField(field.name):
    #                 # Handle set sub-message
    #                 self.set(pb_field, cim)
    #         except ValueError:
    #             try:
    #                 if len(pb_field) > 0:
    #                     if field.type == FieldDescriptor.TYPE_MESSAGE:
    #                         # repeated sub-message
    #                         for m in pb_field:
    #                             getattr(cim, _type_to_adder_map[field.message_type.name])(m)
    #                     else:
    #                         # repeated scalar
    #                         set_field(cim, pb, field)
    #             except TypeError:
    #                 # non-repeated scalar
    #                 set_field(cim, pb, field)

    def _gen_error(self, mrid: str, _type: str, referent: Any) -> str:
        """

        :param mrid: The mrid that was looked up.
        :param _type: The type of the object referred to by ``mrid``.
        :param referent: Any object which is attempting to refer to this ``mrid``. Ideally should implement __str__ for
        readability.
        :return: An error message.
        """
        return f"{_type}[{mrid}] doesn't exist in the ${self.service.name}. It must be added before {str(referent)} references it."

    def _get(self, mrid: str, type_: type, referent):
        return self.service.get(mrid, type_, generate_error=lambda rid, t: self._gen_error(rid, t, referent))

    def _ensure_get(self, mrid: str, type_: type, referent):
        return self.service.ensure_get(mrid, type_, generate_error=lambda rid, t: self._gen_error(rid, t, referent))

# Extensions


def organisation_to_cim(pb: PBOrganisation, service: BaseService):
    cim = Organisation()
    set_identifiedobject(pb.io, cim, service)


def organisationrole_to_cim(pb: PBOrganisationRole, cim: OrganisationRole, service: BaseService):
    cim.organisation = service.resolve_or_defer_reference(resolver.organisation(cim), pb.organisationMRID)
    set_identifiedobject(pb.io, cim, service)


PBOrganisation.to_cim = organisation_to_cim
PBOrganisationRole.to_cim = organisationrole_to_cim
