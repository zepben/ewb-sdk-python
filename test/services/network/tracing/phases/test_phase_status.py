#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve import NormalPhases, CurrentPhases, Terminal, SinglePhaseKind, PhaseCode


def test_normal_and_current_phases():
    terminal = Terminal(phases=PhaseCode.ABCN)
    normal_phases = NormalPhases(terminal)
    current_phases = CurrentPhases(terminal)

    normal_phases[SinglePhaseKind.A] = SinglePhaseKind.A
    normal_phases[SinglePhaseKind.B] = SinglePhaseKind.B
    normal_phases[SinglePhaseKind.C] = SinglePhaseKind.C
    normal_phases[SinglePhaseKind.N] = SinglePhaseKind.N

    current_phases[SinglePhaseKind.A] = SinglePhaseKind.N
    current_phases[SinglePhaseKind.B] = SinglePhaseKind.C
    current_phases[SinglePhaseKind.C] = SinglePhaseKind.B
    current_phases[SinglePhaseKind.N] = SinglePhaseKind.A

    assert normal_phases[SinglePhaseKind.A] == SinglePhaseKind.A
    assert normal_phases[SinglePhaseKind.B] == SinglePhaseKind.B
    assert normal_phases[SinglePhaseKind.C] == SinglePhaseKind.C
    assert normal_phases[SinglePhaseKind.N] == SinglePhaseKind.N

    assert current_phases[SinglePhaseKind.A] == SinglePhaseKind.N
    assert current_phases[SinglePhaseKind.B] == SinglePhaseKind.C
    assert current_phases[SinglePhaseKind.C] == SinglePhaseKind.B
    assert current_phases[SinglePhaseKind.N] == SinglePhaseKind.A


def test_normal_and_current_phase_codes_three():
    terminal = Terminal(phases=PhaseCode.ABCN)
    normal_phases = NormalPhases(terminal)
    current_phases = CurrentPhases(terminal)

    assert normal_phases.as_phase_code() == PhaseCode.NONE
    assert current_phases.as_phase_code() == PhaseCode.NONE

    normal_phases[SinglePhaseKind.A] = SinglePhaseKind.A

    assert normal_phases.as_phase_code() is None
    assert current_phases.as_phase_code() == PhaseCode.NONE

    current_phases[SinglePhaseKind.A] = SinglePhaseKind.A

    assert normal_phases.as_phase_code() is None
    assert current_phases.as_phase_code() is None

    normal_phases[SinglePhaseKind.B] = SinglePhaseKind.B
    normal_phases[SinglePhaseKind.C] = SinglePhaseKind.C
    normal_phases[SinglePhaseKind.N] = SinglePhaseKind.N

    assert normal_phases.as_phase_code() == PhaseCode.ABCN
    assert current_phases.as_phase_code() is None

    current_phases[SinglePhaseKind.B] = SinglePhaseKind.B
    current_phases[SinglePhaseKind.C] = SinglePhaseKind.C
    current_phases[SinglePhaseKind.N] = SinglePhaseKind.N

    assert normal_phases.as_phase_code() == PhaseCode.ABCN
    assert current_phases.as_phase_code() == PhaseCode.ABCN


def test_normal_and_current_phase_codes_single():
    terminal = Terminal(phases=PhaseCode.BC)
    normal_phases = NormalPhases(terminal)
    current_phases = CurrentPhases(terminal)

    assert normal_phases.as_phase_code() == PhaseCode.NONE
    assert current_phases.as_phase_code() == PhaseCode.NONE

    normal_phases[SinglePhaseKind.A] = SinglePhaseKind.A
    current_phases[SinglePhaseKind.A] = SinglePhaseKind.A

    assert normal_phases.as_phase_code() == PhaseCode.NONE
    assert current_phases.as_phase_code() == PhaseCode.NONE

    normal_phases[SinglePhaseKind.B] = SinglePhaseKind.B
    current_phases[SinglePhaseKind.B] = SinglePhaseKind.B

    assert normal_phases.as_phase_code() is None
    assert current_phases.as_phase_code() is None

    normal_phases[SinglePhaseKind.C] = SinglePhaseKind.C
    current_phases[SinglePhaseKind.C] = SinglePhaseKind.C

    assert normal_phases.as_phase_code() == PhaseCode.BC
    assert current_phases.as_phase_code() == PhaseCode.BC


def test_normal_and_current_phase_codes_none():
    terminal = Terminal(phases=PhaseCode.NONE)
    normal_phases = NormalPhases(terminal)
    current_phases = CurrentPhases(terminal)

    assert normal_phases.as_phase_code() == PhaseCode.NONE
    assert current_phases.as_phase_code() == PhaseCode.NONE

    for spk in PhaseCode.ABCN.single_phases:
        normal_phases[spk] = spk
        current_phases[spk] = spk

    assert normal_phases.as_phase_code() == PhaseCode.NONE
    assert current_phases.as_phase_code() == PhaseCode.NONE
