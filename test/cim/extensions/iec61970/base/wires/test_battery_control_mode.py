#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from cim.enum_validator import validate_enum
from zepben.ewb import BatteryControlMode
from zepben.protobuf.cim.extensions.iec61970.base.wires.BatteryControlMode_pb2 import BatteryControlMode as PBBatteryControlMode


def test_versus_pb():
    validate_enum(BatteryControlMode, PBBatteryControlMode)
