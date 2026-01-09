#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["identified_object_to_cim", "document_to_cim", "organisation_to_cim", "organisation_role_to_cim",
           "BaseProtoToCim", "add_to_network_or_none", "bind_to_cim"]

import functools
import inspect
from abc import ABCMeta
from typing import Optional, Callable, TypeVar

from google.protobuf.message import Message
from typing_extensions import ParamSpec
# noinspection PyPackageRequirements
from zepben.protobuf.cim.iec61968.common.Document_pb2 import Document as PBDocument
from zepben.protobuf.cim.iec61968.common.OrganisationRole_pb2 import OrganisationRole as PBOrganisationRole
from zepben.protobuf.cim.iec61968.common.Organisation_pb2 import Organisation as PBOrganisation
from zepben.protobuf.cim.iec61970.base.core.IdentifiedObject_pb2 import IdentifiedObject as PBIdentifiedObject
from zepben.protobuf.cim.iec61970.base.core.NameType_pb2 import NameType as PBNameType
from zepben.protobuf.cim.iec61970.base.core.Name_pb2 import Name as PBName

from zepben.ewb import Document, IdentifiedObject, Organisation, OrganisationRole
from zepben.ewb.dataclassy import dataclass
from zepben.ewb.model.cim.iec61970.base.core.name_type import NameType
from zepben.ewb.services.common import resolver
from zepben.ewb.services.common.base_service import BaseService


TProtoToCimFunc = Callable[[Message, BaseService], Optional[IdentifiedObject]]
P = ParamSpec("P")
R = TypeVar("R")


def add_to_network_or_none(func: TProtoToCimFunc) -> TProtoToCimFunc:
    """
    This should wrap any leaf class of the hierarchy, for example, If you're porting over ewb-sdk-jvm
    changes, any of the classes that get used in a `network.add(Class)`
    """
    @functools.wraps(func)
    def wrapper(pb: Message, service: BaseService) -> Optional[IdentifiedObject]:
        return cim if service.add(cim := func(pb, service)) else None
    return wrapper


def bind_to_cim(func: Callable[P, R]) -> Callable[P, R]:
    """
    Get the object described in the type hint of the first argument of the function we are wrapping
    set that object's `to_cim` function to be the function we are wrapping
    """
    inspect.get_annotations(func, eval_str=True)[func.__code__.co_varnames[0]].to_cim = func
    return func

T = TypeVar("T")

def get_nullable(pb: Message, field: str) -> Optional[T]:
    return getattr(pb, f'{field}Set') if pb.HasField(f'{field}Set') else None


###################
# IEC61968 Common #
###################

@bind_to_cim
def document_to_cim(pb: PBDocument, cim: Document, service: BaseService):
    cim.title = get_nullable(pb, 'title')
    cim.created_date_time = pb.createdDateTime.ToDatetime() if pb.HasField("createdDateTime") else None
    cim.author_name = get_nullable(pb, 'authorName')
    cim.type = get_nullable(pb, 'type')
    cim.status = get_nullable(pb, 'status')
    cim.comment = get_nullable(pb, 'comment')

    identified_object_to_cim(pb.io, cim, service)


@bind_to_cim
@add_to_network_or_none
def organisation_to_cim(pb: PBOrganisation, service: BaseService) -> Optional[Organisation]:
    cim = Organisation(mrid=pb.mrid())

    identified_object_to_cim(pb.io, cim, service)
    return cim


@bind_to_cim
def organisation_role_to_cim(pb: PBOrganisationRole, cim: OrganisationRole, service: BaseService):
    service.resolve_or_defer_reference(resolver.organisation(cim), pb.organisationMRID)

    identified_object_to_cim(pb.io, cim, service)


######################
# IEC61970 Base Core #
######################

@bind_to_cim
def identified_object_to_cim(pb: PBIdentifiedObject, cim: IdentifiedObject, service: BaseService):
    cim.mrid = pb.mRID
    cim.name = get_nullable(pb, 'name')
    cim.description = get_nullable(pb, 'description')
    [cim.add_name(name_to_cim(name, cim, service).type, name.name) for name in pb.names]


@bind_to_cim
def name_to_cim(pb: PBName, io: IdentifiedObject, service: BaseService):
    try:
        nt = service.get_name_type(pb.type)
    except KeyError:
        # noinspection PyArgumentList
        nt = NameType(pb.type)
        service.add_name_type(nt)

    return nt.get_or_add_name(pb.name, io)


@bind_to_cim
def name_type_to_cim(pb: PBNameType, service: BaseService):
    try:
        nt = service.get_name_type(pb.name)
    except KeyError:
        # noinspection PyArgumentList
        nt = NameType(pb.name)
        service.add_name_type(nt)

    nt.description = get_nullable(pb, 'description')
    return nt


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
