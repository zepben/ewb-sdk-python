#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from cim.enum_validator import validate_enum
from zepben.evolve import EndDeviceFunctionKind
from zepben.protobuf.cim.iec61968.metering.EndDeviceFunctionKind_pb2 import EndDeviceFunctionKind as PBEndDeviceFunctionKind


def test_versus_pb():
    validate_enum(EndDeviceFunctionKind, PBEndDeviceFunctionKind)
