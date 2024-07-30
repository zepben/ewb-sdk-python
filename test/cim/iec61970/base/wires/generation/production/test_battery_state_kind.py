#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from zepben.protobuf.cim.iec61970.base.wires.generation.production.BatteryStateKind_pb2 import BatteryStateKind as PBBatteryStateKind

from cim.enum_validator import validate_enum
from zepben.evolve import BatteryStateKind


def test_battery_state_kind_eum():
    validate_enum(BatteryStateKind, PBBatteryStateKind)
