#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from abc import ABCMeta

from dataclassy import dataclass
from zepben.cimbend.common.base_service import BaseService
from zepben.protobuf.cim.iec61970.base.core.IdentifiedObject_pb2 import IdentifiedObject as PBIdentifiedObject
from zepben.protobuf.cim.iec61968.common.Document_pb2 import Document as PBDocument

from zepben.cimbend.cim.iec61968.common.document import Document
from zepben.cimbend.cim.iec61968.common import Organisation
from zepben.cimbend.cim.iec61968.common.organisation_role import OrganisationRole
from zepben.protobuf.cim.iec61968.common.Organisation_pb2 import Organisation as PBOrganisation
from zepben.protobuf.cim.iec61968.common.OrganisationRole_pb2 import OrganisationRole as PBOrganisationRole
from zepben.cimbend.cim.iec61970.base.core.identified_object import IdentifiedObject
from zepben.cimbend.common import resolver

__all__ = ["identifiedobject_to_cim", "document_to_cim", "organisation_to_cim", "organisationrole_to_cim", "BaseProtoToCim"]


# IEC61970 CORE #
def identifiedobject_to_cim(pb: PBIdentifiedObject, cim: IdentifiedObject, service: BaseService):
    cim.mrid = pb.mRID
    cim.name = pb.name
    cim.description = pb.description


# IEC61968 COMMON #
def document_to_cim(pb: PBDocument, cim: Document, service: BaseService):
    cim.title = pb.title
    cim.created_date_time = pb.createdDateTime.ToDatetime()
    cim.author_name = pb.authorName
    cim.type = pb.type
    cim.status = pb.status
    cim.comment = pb.comment
    identifiedobject_to_cim(pb.io, cim, service)


def organisation_to_cim(pb: PBOrganisation, service: BaseService):
    cim = Organisation()
    identifiedobject_to_cim(pb.io, cim, service)
    service.add(cim)


def organisationrole_to_cim(pb: PBOrganisationRole, cim: OrganisationRole, service: BaseService):
    cim.organisation = service.resolve_or_defer_reference(resolver.organisation(cim), pb.organisationMRID)
    identifiedobject_to_cim(pb.io, cim, service)


PBDocument.to_cim = document_to_cim
PBOrganisation.to_cim = organisation_to_cim
PBOrganisationRole.to_cim = organisationrole_to_cim
PBIdentifiedObject.to_cim = identifiedobject_to_cim


@dataclass(slots=True)
class BaseProtoToCim(object, metaclass=ABCMeta):
    service: BaseService

