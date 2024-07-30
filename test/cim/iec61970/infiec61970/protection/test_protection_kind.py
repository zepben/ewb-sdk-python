#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from zepben.protobuf.cim.iec61970.infiec61970.protection.ProtectionKind_pb2 import ProtectionKind as PBProtectionKind

from cim.enum_validator import validate_enum
from zepben.evolve import ProtectionKind


def test_protection_kind_enum():
    validate_enum(ProtectionKind, PBProtectionKind)
