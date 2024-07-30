#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from collections import Counter

from zepben.evolve import Junction, Terminal, PhaseCode, SinglePhaseKind, NominalPhasePath, ConnectivityResult


class TestConnectivityResult:
    terminal11, terminal12 = Terminal(phases=PhaseCode.A), Terminal(phases=PhaseCode.A)
    terminal21, terminal22 = Terminal(phases=PhaseCode.A), Terminal(phases=PhaseCode.A)
    asset1 = Junction(mrid="asset1", name="asset 1", terminals=[terminal11, terminal12])
    asset2 = Junction(mrid="asset2", name="asset 2", terminals=[terminal21, terminal22])

    def test_accessors(self):
        expected_phase_map = {
            NominalPhasePath(SinglePhaseKind.A, SinglePhaseKind.A),
            NominalPhasePath(SinglePhaseKind.B, SinglePhaseKind.X)
        }
        cr = ConnectivityResult(from_terminal=self.terminal11, to_terminal=self.terminal21, nominal_phase_paths=expected_phase_map)

        assert cr.from_equip is self.asset1
        assert cr.from_terminal is self.terminal11
        assert cr.to_equip is self.asset2
        assert cr.to_terminal is self.terminal21
        assert Counter(cr.from_nominal_phases) == Counter([SinglePhaseKind.A, SinglePhaseKind.B])
        assert Counter(cr.to_nominal_phases) == Counter([SinglePhaseKind.A, SinglePhaseKind.X])
        assert Counter(cr.nominal_phase_paths) == Counter(expected_phase_map)

    def test_dunder_methods(self):
        cr1 = ConnectivityResult(from_terminal=self.terminal11, to_terminal=self.terminal21, nominal_phase_paths=[NominalPhasePath(SinglePhaseKind.A, SinglePhaseKind.A)])
        cr1Dup = ConnectivityResult(from_terminal=self.terminal11, to_terminal=self.terminal21, nominal_phase_paths=[NominalPhasePath(SinglePhaseKind.A, SinglePhaseKind.A)])
        cr2 = ConnectivityResult(from_terminal=self.terminal11, to_terminal=self.terminal21, nominal_phase_paths=[NominalPhasePath(SinglePhaseKind.B, SinglePhaseKind.B)])
        cr3 = ConnectivityResult(from_terminal=self.terminal11, to_terminal=self.terminal12, nominal_phase_paths=[NominalPhasePath(SinglePhaseKind.A, SinglePhaseKind.A)])
        cr4 = ConnectivityResult(from_terminal=self.terminal21, to_terminal=self.terminal11, nominal_phase_paths=[NominalPhasePath(SinglePhaseKind.A, SinglePhaseKind.A)])

        assert cr1 == cr1
        assert cr1 == cr1Dup
        assert cr1 != cr2
        assert cr1 != cr3
        assert cr1 != cr4
        assert hash(cr1) == hash(cr1Dup)
        assert str(cr1) != ""
