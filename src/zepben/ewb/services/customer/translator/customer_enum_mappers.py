#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = []

from zepben.protobuf.cim.iec61968.customers.CustomerKind_pb2 import CustomerKind as PBCustomerKind

from zepben.ewb.model.cim.iec61968.customers.customer_kind import CustomerKind
# noinspection PyProtectedMember
from zepben.ewb.services.common.enum_mapper import EnumMapper

#
# NOTE: These are deliberately excluded from the module export, as they aren't part of the public api.
#

_map_customer_kind = EnumMapper(CustomerKind, PBCustomerKind)
