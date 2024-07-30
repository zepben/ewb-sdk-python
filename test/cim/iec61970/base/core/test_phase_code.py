#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

# The IDE auto format puts the imports in an order that pylint does not like, so disable the warnings.
# pylint: disable=wrong-import-order,ungrouped-imports

from zepben.protobuf.cim.iec61970.base.core.PhaseCode_pb2 import PhaseCode as PBPhaseCode

from cim.enum_validator import validate_enum
from zepben.evolve import PhaseCode, phase_code_by_id, SinglePhaseKind


# pylint: enable=wrong-import-order,ungrouped-imports


class TestPhaseCode:

    def test_phase_code_enum(self):
        validate_enum(PhaseCode, PBPhaseCode)

    def test_single_phases(self):
        for pc in PhaseCode:
            if pc == PhaseCode.NONE:
                assert pc.single_phases == [SinglePhaseKind.NONE]
            else:
                # We need to strip the 's' off secondary phases for the following checks to work correctly.
                assert len(pc.single_phases) == len(pc.name.lstrip('s'))

                single_phases = {it.short_name.lstrip('s') for it in pc}
                name_phases = set(pc.short_name.lstrip('s'))

                assert single_phases == name_phases

    def test_num_phases(self):
        for pc in PhaseCode:
            if pc == PhaseCode.NONE:
                assert pc.num_phases == 0
            else:
                assert pc.num_phases == len(pc.single_phases)

    def test_without_neutral(self):
        assert PhaseCode.ABCN.without_neutral == PhaseCode.ABC
        assert PhaseCode.ABC.without_neutral == PhaseCode.ABC
        assert PhaseCode.BCN.without_neutral == PhaseCode.BC
        assert PhaseCode.XYN.without_neutral == PhaseCode.XY
        assert PhaseCode.NONE.without_neutral == PhaseCode.NONE
        assert PhaseCode.N.without_neutral == PhaseCode.NONE

    def test_phase_code_value_lookup(self):
        for pc in PhaseCode:
            assert phase_code_by_id(pc.value[0]) == pc, f"value lookup of {pc.name} resulted in {phase_code_by_id(pc.value[0]).name}"

    def test_contains(self):
        assert SinglePhaseKind.A in PhaseCode.ABCN, "ABCN should contain A"
        assert SinglePhaseKind.B in PhaseCode.ABCN, "ABCN should contain B"
        assert SinglePhaseKind.C in PhaseCode.ABCN, "ABCN should contain C"
        assert SinglePhaseKind.N in PhaseCode.ABCN, "ABCN should contain N"
        assert SinglePhaseKind.X not in PhaseCode.ABCN, "ABCN should not contain X"
        assert SinglePhaseKind.Y not in PhaseCode.ABCN, "ABCN should not contain Y"

        assert SinglePhaseKind.A not in PhaseCode.XY, "XY should not contain A"
        assert SinglePhaseKind.B not in PhaseCode.XY, "XY should not contain B"
        assert SinglePhaseKind.C not in PhaseCode.XY, "XY should not contain C"
        assert SinglePhaseKind.N not in PhaseCode.XY, "XY should not contain N"
        assert SinglePhaseKind.X in PhaseCode.XY, "XY should contain X"
        assert SinglePhaseKind.Y in PhaseCode.XY, "XY should contain Y"

    def test_for_each(self):
        assert list(PhaseCode.ABCN) == [SinglePhaseKind.A, SinglePhaseKind.B, SinglePhaseKind.C, SinglePhaseKind.N]

    def test_plus(self):
        assert PhaseCode.A + SinglePhaseKind.B == PhaseCode.AB
        assert PhaseCode.BC + PhaseCode.AN == PhaseCode.ABCN
        assert PhaseCode.X + SinglePhaseKind.Y == PhaseCode.XY
        assert PhaseCode.N + PhaseCode.XY == PhaseCode.XYN

        # Can add existing phases.
        assert PhaseCode.ABCN + SinglePhaseKind.A == PhaseCode.ABCN
        assert PhaseCode.ABCN + SinglePhaseKind.B == PhaseCode.ABCN
        assert PhaseCode.A + PhaseCode.ABCN == PhaseCode.ABCN

        # Returns NONE for invalid additions.
        assert PhaseCode.ABCN + SinglePhaseKind.X == PhaseCode.NONE
        assert PhaseCode.ABCN + PhaseCode.X == PhaseCode.NONE

    def test_minus(self):
        assert PhaseCode.ABCN - SinglePhaseKind.B == PhaseCode.ACN
        assert PhaseCode.ABCN - PhaseCode.AN == PhaseCode.BC
        assert PhaseCode.BC - SinglePhaseKind.C == PhaseCode.B
        assert PhaseCode.XY - PhaseCode.X == PhaseCode.Y

        assert PhaseCode.X - SinglePhaseKind.Y == PhaseCode.X
        assert PhaseCode.AB - PhaseCode.C == PhaseCode.AB

        assert PhaseCode.ABCN - PhaseCode.ABCN == PhaseCode.NONE
