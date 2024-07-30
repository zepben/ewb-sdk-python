#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from zepben.protobuf.cim.iec61970.base.wires.SinglePhaseKind_pb2 import SinglePhaseKind as PBSinglePhaseKind

from cim.enum_validator import validate_enum
from zepben.evolve import SinglePhaseKind, single_phase_kind_by_id, PhaseCode


class TestSinglePhaseKind:

    def test_single_phase_kind_enum(self):
        validate_enum(SinglePhaseKind, PBSinglePhaseKind)

    def test_single_phase_kind_value_lookup(self):
        for spc in SinglePhaseKind:
            assert single_phase_kind_by_id(spc.value[0]) == spc, f"value lookup of {spc.name} resulted in {single_phase_kind_by_id(spc.value[0]).name}"

    def test_plus(self):
        assert SinglePhaseKind.A + SinglePhaseKind.B == PhaseCode.AB
        assert SinglePhaseKind.A + SinglePhaseKind.A == PhaseCode.A
        assert SinglePhaseKind.A + PhaseCode.BC == PhaseCode.ABC

    def test_minus(self):
        assert SinglePhaseKind.B - SinglePhaseKind.A == PhaseCode.B
        assert SinglePhaseKind.A - SinglePhaseKind.A == PhaseCode.NONE
        assert SinglePhaseKind.A - PhaseCode.BC == PhaseCode.A
        assert SinglePhaseKind.A - PhaseCode.ABC == PhaseCode.NONE
