#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from zepben.protobuf.cim.iec61970.base.wires.WindingConnection_pb2 import WindingConnection as PBWindingConnection

from cim.enum_validator import validate_enum
from zepben.evolve import WindingConnection


def test_winding_connection_enum():
    validate_enum(WindingConnection, PBWindingConnection)
