#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.protobuf.cim.iec61970.base.core.IdentifiedObject_pb2 import IdentifiedObject as PBIdentifiedObject
from zepben.protobuf.cim.iec61968.common.Document_pb2 import Document as PBDocument

from zepben.cimbend.common.translator.util import mrid_or_empty
from zepben.cimbend.cim.iec61968.common.document import Document
from zepben.cimbend.cim.iec61968.common import Organisation
from zepben.cimbend.cim.iec61968.common.organisation_role import OrganisationRole
from zepben.protobuf.cim.iec61968.common.Organisation_pb2 import Organisation as PBOrganisation
from zepben.protobuf.cim.iec61968.common.OrganisationRole_pb2 import OrganisationRole as PBOrganisationRole
from zepben.cimbend.cim.iec61970.base.core.identified_object import IdentifiedObject

__all__ = ["identifiedobject_to_pb", "document_to_pb", "organisationrole_to_pb", "organisation_to_pb"]


# IEC61968 COMMON #
def document_to_pb(cim: Document) -> PBDocument:
    return PBDocument(io=identifiedobject_to_pb(cim),
                      title=cim.title,
                      createdDateTime=cim.created_date_time.timestamp() if cim.created_date_time else None,
                      authorName=cim.author_name,
                      type=cim.type,
                      status=cim.status,
                      comment=cim.comment)


def organisation_to_pb(cim: Organisation) -> PBOrganisation:
    return PBOrganisation(identifiedobject_to_pb(cim))


def organisationrole_to_pb(cim: OrganisationRole) -> PBOrganisationRole:
    return PBOrganisationRole(io=identifiedobject_to_pb(cim),
                              organisationMRID=mrid_or_empty(cim.organisation.mrid))


# IEC61970 CORE #
def identifiedobject_to_pb(cim: IdentifiedObject) -> PBIdentifiedObject:
    return PBIdentifiedObject(mRID=str(cim.mrid),
                              name=cim.name,
                              description=cim.description)


Document.to_pb = document_to_pb
Organisation.to_pb = organisation_to_pb
OrganisationRole.to_pb = organisationrole_to_pb
IdentifiedObject.to_pb = identifiedobject_to_pb
