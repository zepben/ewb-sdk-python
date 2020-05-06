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

from zepben.protobuf.cim.iec61970.base.core.IdentifiedObject_pb2 import IdentifiedObject as PBIdentifiedObject
from zepben.protobuf.cim.iec61968.common.Document_pb2 import Document as PBDocument

from zepben.cimbend.cim.iec61968.common.document import Document
from zepben.cimbend.cim.iec61968.common import Organisation
from zepben.cimbend.cim.iec61968.common.organisation_role import OrganisationRole
from zepben.protobuf.cim.iec61968.common.Organisation_pb2 import Organisation as PBOrganisation
from zepben.protobuf.cim.iec61968.common.OrganisationRole_pb2 import OrganisationRole as PBOrganisationRole
from zepben.cimbend.cim.iec61970.base.core.identified_object import IdentifiedObject

__all__ = ["get_identifiedobject", "get_document", "get_organisationrole", "get_organisation"]


# IEC61970 CORE #
def get_identifiedobject(cim: IdentifiedObject) -> PBIdentifiedObject:
    return PBIdentifiedObject(mRID=str(cim.mrid),
                              name=cim.name,
                              numDiagramObjects=cim.num_diagram_objects)


# IEC61968 COMMON #
def get_document(cim: Document) -> PBDocument:
    return PBDocument(io=get_identifiedobject(cim),
                      title=cim.title,
                      createdDateTime=cim.created_date_time.timestamp(),
                      authorName=cim.author_name,
                      type=cim.type,
                      status=cim.status,
                      comment=cim.comment)


def get_organisation(cim: Organisation) -> PBOrganisation:
    return PBOrganisation(get_identifiedobject(cim))


def get_organisationrole(cim: OrganisationRole) -> PBOrganisationRole:
    """
    Organisation is sent with OrganisationRole
    :param cim:
    :return:
    """
    return PBOrganisationRole(io=get_identifiedobject(cim),
                              organisationMRID=cim.organisation.mrid)
