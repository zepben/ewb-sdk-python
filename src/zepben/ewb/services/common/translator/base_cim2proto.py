#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["identified_object_to_pb", "document_to_pb", "organisation_role_to_pb", "organisation_to_pb"]

import inspect
from typing import ParamSpec, TypeVar, Callable, Generator

# noinspection PyPackageRequirements,PyUnresolvedReferences
from google.protobuf.timestamp_pb2 import Timestamp as PBTimestamp
from google.protobuf.struct_pb2 import NullValue
from zepben.protobuf.cim.iec61968.common.Document_pb2 import Document as PBDocument
from zepben.protobuf.cim.iec61968.common.OrganisationRole_pb2 import OrganisationRole as PBOrganisationRole
from zepben.protobuf.cim.iec61968.common.Organisation_pb2 import Organisation as PBOrganisation
from zepben.protobuf.cim.iec61970.base.core.IdentifiedObject_pb2 import IdentifiedObject as PBIdentifiedObject
from zepben.protobuf.cim.iec61970.base.core.NameType_pb2 import NameType as PBNameType
from zepben.protobuf.cim.iec61970.base.core.Name_pb2 import Name as PBName

from zepben.ewb.model.cim.iec61968.common.document import Document
from zepben.ewb.model.cim.iec61968.common.organisation import Organisation
from zepben.ewb.model.cim.iec61968.common.organisation_role import OrganisationRole
from zepben.ewb.model.cim.iec61970.base.core.identified_object import IdentifiedObject
from zepben.ewb.model.cim.iec61970.base.core.name import Name
from zepben.ewb.model.cim.iec61970.base.core.name_type import NameType
from zepben.ewb.services.common.translator.util import mrid_or_empty


P = ParamSpec("P")
R = TypeVar("R")


def bind_to_pb(func: Callable[P, R]) -> Callable[P, R]:
    """
    Get the object described in the type hint of the first argument of the function we are wrapping
    set that object's `to_pb` function to be the function we are wrapping
    """
    inspect.get_annotations(func, eval_str=True)[func.__code__.co_varnames[0]].to_pb = func
    return func


def set_or_null(**kwargs):
    return {f'{k}{"Null" if v is None else "Set"}': v if v is not None else NullValue.NULL_VALUE for k, v in kwargs.items()}


###################
# IEC61968 Common #
###################

@bind_to_pb
def document_to_pb(cim: Document) -> PBDocument:
    timestamp = None
    if cim.created_date_time:
        timestamp = PBTimestamp()
        timestamp.FromDatetime(cim.created_date_time)

    return PBDocument(
        io=identified_object_to_pb(cim),
        createdDateTime=timestamp,
        **set_or_null(
            title=cim.title,
            authorName=cim.author_name,
            type=cim.type,
            status=cim.status,
            comment=cim.comment
        )
    )


@bind_to_pb
def organisation_to_pb(cim: Organisation) -> PBOrganisation:
    return PBOrganisation(io=identified_object_to_pb(cim))


@bind_to_pb
def organisation_role_to_pb(cim: OrganisationRole) -> PBOrganisationRole:
    return PBOrganisationRole(
        io=identified_object_to_pb(cim),
        organisationMRID=mrid_or_empty(cim.organisation)
    )


######################
# IEC61970 Base Core #
######################

@bind_to_pb
def identified_object_to_pb(cim: IdentifiedObject) -> PBIdentifiedObject:
    return PBIdentifiedObject(
        mRID=str(cim.mrid),
        **set_or_null(
            name=cim.name,
            description=cim.description
        ),
        names=[name_to_pb(name) for name in cim.names]
    )


@bind_to_pb
def name_to_pb(cim: Name) -> PBName:
    return PBName(
        name=cim.name,
        type=cim.type.name if cim.type else None
    )


@bind_to_pb
def name_type_to_pb(cim: NameType) -> PBNameType:
    return PBNameType(
        name=cim.name,
        **set_or_null(
            description=cim.description
        )
    )
