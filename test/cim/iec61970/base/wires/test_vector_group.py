#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from zepben.protobuf.cim.iec61970.base.wires.VectorGroup_pb2 import VectorGroup as PBVectorGroup

from test.cim.enum_verifier import verify_enum
from zepben.evolve import VectorGroup


def test_vector_group_enum():
    verify_enum(VectorGroup, PBVectorGroup)
