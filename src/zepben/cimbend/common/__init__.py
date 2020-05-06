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

from zepben.protobuf.cim.iec61968.common.Document_pb2 import Document as PBDocument
from zepben.protobuf.cim.iec61968.common.OrganisationRole_pb2 import OrganisationRole as PBOrganisationRole
from zepben.protobuf.cim.iec61968.common.Organisation_pb2 import Organisation as PBOrganisation
from zepben.protobuf.cim.iec61970.base.core.IdentifiedObject_pb2 import IdentifiedObject as PBIdentifiedObject
from zepben.cimbend.common.base_service import *
from zepben.cimbend.common.base_proto2cim import *
from zepben.cimbend.common.base_cim2proto import *

__all__ = ["base_proto2cim", "base_service", "base_cim2proto", "mrid_or_empty"]

PBOrganisationRole.mrid = lambda self: self.io.mRID
PBDocument.mrid = lambda self: self.io.mRID
PBOrganisation.mrid = lambda self: self.io.mRID
PBIdentifiedObject.name_and_mrid = lambda self: f"{self.mRID}{f' [{self.name}]' if self.name else ''}"
PBDocument.name_and_mrid = lambda self: self.io.name_and_mrid()


def mrid_or_empty(io: PBIdentifiedObject) -> str:
    return io.mrid if io else ""
