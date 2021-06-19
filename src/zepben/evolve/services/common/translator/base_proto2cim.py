#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from abc import ABCMeta
from typing import Optional

from dataclassy import dataclass
# noinspection PyPackageRequirements
from google.protobuf.timestamp_pb2 import Timestamp as PBTimestamp
from zepben.protobuf.cim.iec61968.common.Document_pb2 import Document as PBDocument
from zepben.protobuf.cim.iec61968.common.OrganisationRole_pb2 import OrganisationRole as PBOrganisationRole
from zepben.protobuf.cim.iec61968.common.Organisation_pb2 import Organisation as PBOrganisation
from zepben.protobuf.cim.iec61970.base.core.IdentifiedObject_pb2 import IdentifiedObject as PBIdentifiedObject

from zepben.evolve import Document, IdentifiedObject, Organisation, OrganisationRole
from zepben.evolve.services.common import resolver
from zepben.evolve.services.common.base_service import BaseService

__all__ = ["identified_object_to_cim", "document_to_cim", "organisation_to_cim", "organisation_role_to_cim", "BaseProtoToCim"]


# IEC61970 CORE #


def identified_object_to_cim(pb: PBIdentifiedObject, cim: IdentifiedObject, _: BaseService):
    cim.mrid = pb.mRID
    cim.name = pb.name
    cim.description = pb.description


# IEC61968 COMMON #
def document_to_cim(pb: PBDocument, cim: Document, service: BaseService):
    cim.title = pb.title
    cim.created_date_time = pb.createdDateTime.ToDatetime() if pb.createdDateTime != PBTimestamp() else None
    cim.author_name = pb.authorName
    cim.type = pb.type
    cim.status = pb.status
    cim.comment = pb.comment

    identified_object_to_cim(pb.io, cim, service)


def organisation_to_cim(pb: PBOrganisation, service: BaseService) -> Optional[Organisation]:
    cim = Organisation()

    identified_object_to_cim(pb.io, cim, service)
    return cim if service.add(cim) else None


def organisation_role_to_cim(pb: PBOrganisationRole, cim: OrganisationRole, service: BaseService):
    service.resolve_or_defer_reference(resolver.organisation(cim), pb.organisationMRID)

    identified_object_to_cim(pb.io, cim, service)


PBDocument.to_cim = document_to_cim
PBOrganisation.to_cim = organisation_to_cim
PBOrganisationRole.to_cim = organisation_role_to_cim
PBIdentifiedObject.to_cim = identified_object_to_cim


@dataclass(slots=True)
class BaseProtoToCim(object, metaclass=ABCMeta):
    service: BaseService


# Extensions
def _add_from_pb(service: BaseService, pb) -> Optional[IdentifiedObject]:
    """Must only be called by objects for which .to_cim() takes themselves and the network service."""
    try:
        return pb.to_cim(service)
    except AttributeError as e:
        raise TypeError(f"Type {pb.__class__.__name__} is not supported by {service.__class__.__name__}. (Error was: {e})")


BaseService.add_from_pb = _add_from_pb
