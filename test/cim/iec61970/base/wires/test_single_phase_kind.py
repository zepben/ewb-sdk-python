#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from zepben.protobuf.cim.iec61970.base.wires.SinglePhaseKind_pb2 import SinglePhaseKind as PBSinglePhaseKind

from test.cim.enum_validator import validate_enum
from zepben.evolve import SinglePhaseKind, single_phase_kind_by_id


def test_single_phase_kind_enum():
    validate_enum(SinglePhaseKind, PBSinglePhaseKind)


def test_single_phase_kind_value_lookup():
    for spc in SinglePhaseKind:
        assert single_phase_kind_by_id(spc.value[0]) == spc, f"value lookup of {spc.name} resulted in {single_phase_kind_by_id(spc.value[0]).name}"
