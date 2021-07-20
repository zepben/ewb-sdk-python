#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
# noinspection PyPackageRequirements
from google.protobuf.timestamp_pb2 import Timestamp as PBTimestamp
from zepben.protobuf.cim.iec61968.common.Document_pb2 import Document as PBDocument
from zepben.protobuf.cim.iec61968.common.OrganisationRole_pb2 import OrganisationRole as PBOrganisationRole
from zepben.protobuf.cim.iec61968.common.Organisation_pb2 import Organisation as PBOrganisation
from zepben.protobuf.cim.iec61970.base.core.IdentifiedObject_pb2 import IdentifiedObject as PBIdentifiedObject
from zepben.protobuf.cim.iec61970.base.core.NameType_pb2 import NameType as PBNameType
from zepben.protobuf.cim.iec61970.base.core.Name_pb2 import Name as PBName

from zepben.evolve.model.cim.iec61968.common.document import Document
from zepben.evolve.model.cim.iec61968.common.organisation import Organisation
from zepben.evolve.model.cim.iec61968.common.organisation_role import OrganisationRole
from zepben.evolve.model.cim.iec61970.base.core.identified_object import IdentifiedObject
from zepben.evolve.model.cim.iec61970.base.core.name import Name
from zepben.evolve.model.cim.iec61970.base.core.name_type import NameType
from zepben.evolve.services.common.translator.util import mrid_or_empty

__all__ = ["identified_object_to_pb", "document_to_pb", "organisation_role_to_pb", "organisation_to_pb"]


###################
# IEC61968 COMMON #
###################

def document_to_pb(cim: Document) -> PBDocument:
    timestamp = PBTimestamp()
    if cim.created_date_time:
        timestamp.FromDatetime(cim.created_date_time)

    return PBDocument(
        io=identified_object_to_pb(cim),
        title=cim.title,
        createdDateTime=timestamp,
        authorName=cim.author_name,
        type=cim.type,
        status=cim.status,
        comment=cim.comment
    )


def organisation_to_pb(cim: Organisation) -> PBOrganisation:
    return PBOrganisation(io=identified_object_to_pb(cim))


def organisation_role_to_pb(cim: OrganisationRole) -> PBOrganisationRole:
    return PBOrganisationRole(
        io=identified_object_to_pb(cim),
        organisationMRID=mrid_or_empty(cim.organisation)
    )


Document.to_pb = document_to_pb
Organisation.to_pb = organisation_to_pb
OrganisationRole.to_pb = organisation_role_to_pb


######################
# IEC61970 BASE CORE #
######################

def identified_object_to_pb(cim: IdentifiedObject) -> PBIdentifiedObject:
    return PBIdentifiedObject(
        mRID=str(cim.mrid),
        name=cim.name,
        description=cim.description,
        names=[name_to_pb(name) for name in cim.names]
    )


def name_to_pb(cim: Name) -> PBName:
    return PBName(
        name=cim.name,
        type=cim.type.name if cim.type else None
    )


def name_type_to_pb(cim: NameType) -> PBNameType:
    return PBNameType(
        name=cim.name,
        description=cim.description
    )


IdentifiedObject.to_pb = identified_object_to_pb
Name.to_pb = name_to_pb
NameType.to_pb = name_type_to_pb
