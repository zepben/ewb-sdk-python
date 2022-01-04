#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from zepben.protobuf.cim.iec61970.base.domain.UnitSymbol_pb2 import UnitSymbol as PBUnitSymbol

from test.cim.enum_verifier import verify_enum
from zepben.evolve import UnitSymbol


def test_unit_symbol_enum():
    verify_enum(UnitSymbol, PBUnitSymbol)
