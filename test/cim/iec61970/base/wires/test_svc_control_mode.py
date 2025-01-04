#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from cim.enum_validator import validate_enum
from zepben.evolve import SVCControlMode
from zepben.protobuf.cim.iec61970.base.wires.SVCControlMode_pb2 import SVCControlMode as PBSVCControlMode


def test_versus_pb():
    validate_enum(SVCControlMode, PBSVCControlMode.Enum)
