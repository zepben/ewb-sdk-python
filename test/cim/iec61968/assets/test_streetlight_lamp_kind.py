#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from zepben.protobuf.cim.iec61968.assets.StreetlightLampKind_pb2 import StreetlightLampKind as PBStreetlightLampKind

from cim.enum_validator import validate_enum
from zepben.evolve import StreetlightLampKind


def test_streetlight_lamp_kind_enum():
    validate_enum(StreetlightLampKind, PBStreetlightLampKind)
