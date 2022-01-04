#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from zepben.protobuf.cim.iec61970.base.wires.generation.production.BatteryStateKind_pb2 import BatteryStateKind as PBBatteryStateKind

from test.cim.enum_verifier import verify_enum
from zepben.evolve import BatteryStateKind


def test_battery_state_kind_eum():
    verify_enum(BatteryStateKind, PBBatteryStateKind)
