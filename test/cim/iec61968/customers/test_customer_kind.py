#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from zepben.protobuf.cim.iec61968.customers.CustomerKind_pb2 import CustomerKind as PBCustomerKind

from cim.enum_validator import validate_enum
from zepben.evolve import CustomerKind


def test_customer_kind_enum():
    validate_enum(CustomerKind, PBCustomerKind)
