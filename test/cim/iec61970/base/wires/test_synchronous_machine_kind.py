#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.protobuf.cim.iec61970.base.wires.SynchronousMachineKind_pb2 import SynchronousMachineKind as PBSynchronousMachineKind

from cim.enum_validator import validate_enum
from zepben.evolve import SynchronousMachineKind


def test_synchronous_machine_kind_enum():
    validate_enum(SynchronousMachineKind, PBSynchronousMachineKind)
