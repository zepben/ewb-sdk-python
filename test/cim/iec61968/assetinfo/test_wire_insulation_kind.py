#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from zepben.protobuf.cim.iec61968.assetinfo.WireMaterialKind_pb2 import WireMaterialKind as PBWireMaterialKind

from cim.enum_validator import validate_enum
from zepben.ewb.model.cim.iec61968.assetinfo.wire_insulation_kind import WireInsulationKind
from zepben.protobuf.cim.iec61968.assetinfo.WireInsulationKind_pb2 import WireInsulationKind as PBWireInsulationKind


def test_wire_material_kind_enum():
    validate_enum(WireInsulationKind, PBWireInsulationKind)
