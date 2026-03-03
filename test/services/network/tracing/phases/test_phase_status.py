#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import pytest

from zepben.ewb import Terminal, SinglePhaseKind, PhaseCode, NetworkStateOperators, generate_id, PhaseStatus, PhaseException


def test_normal_and_current_phases():
    terminal = Terminal(mrid=generate_id(), phases=PhaseCode.ABCN)
    normal_phases = NetworkStateOperators.NORMAL.phase_status(terminal)
    current_phases = NetworkStateOperators.CURRENT.phase_status(terminal)

    normal_phases[SinglePhaseKind.A] = SinglePhaseKind.A
    normal_phases[SinglePhaseKind.B] = SinglePhaseKind.B
    normal_phases[SinglePhaseKind.C] = SinglePhaseKind.C
    normal_phases[SinglePhaseKind.N] = SinglePhaseKind.N

    assert normal_phases[SinglePhaseKind.A] == SinglePhaseKind.A
    assert normal_phases[SinglePhaseKind.B] == SinglePhaseKind.B
    assert normal_phases[SinglePhaseKind.C] == SinglePhaseKind.C
    assert normal_phases[SinglePhaseKind.N] == SinglePhaseKind.N

    current_phases[SinglePhaseKind.A] = SinglePhaseKind.N
    current_phases[SinglePhaseKind.B] = SinglePhaseKind.C
    current_phases[SinglePhaseKind.C] = SinglePhaseKind.B
    current_phases[SinglePhaseKind.N] = SinglePhaseKind.A

    assert current_phases[SinglePhaseKind.A] == SinglePhaseKind.N
    assert current_phases[SinglePhaseKind.B] == SinglePhaseKind.C
    assert current_phases[SinglePhaseKind.C] == SinglePhaseKind.B
    assert current_phases[SinglePhaseKind.N] == SinglePhaseKind.A


def test_normal_and_current_phase_codes_three():
    terminal = Terminal(mrid=generate_id(), phases=PhaseCode.ABCN)
    normal_phases = PhaseStatus(terminal)
    current_phases = PhaseStatus(terminal)

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
    terminal = Terminal(mrid=generate_id(), phases=PhaseCode.BC)
    normal_phases = PhaseStatus(terminal)
    current_phases = PhaseStatus(terminal)

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
    terminal = Terminal(mrid=generate_id(), phases=PhaseCode.NONE)
    normal_phases = PhaseStatus(terminal)
    current_phases = PhaseStatus(terminal)

    assert normal_phases.as_phase_code() == PhaseCode.NONE
    assert current_phases.as_phase_code() == PhaseCode.NONE

    for spk in PhaseCode.ABCN.single_phases:
        normal_phases[spk] = spk
        current_phases[spk] = spk

    assert normal_phases.as_phase_code() == PhaseCode.NONE
    assert current_phases.as_phase_code() == PhaseCode.NONE


def as_phase_code_handles_changing_terminal_phases():
    terminal = Terminal(mrid=generate_id(), phases=PhaseCode.ABN)
    phase_status = PhaseStatus(terminal)

    phase_status[SinglePhaseKind.A] = SinglePhaseKind.A
    phase_status[SinglePhaseKind.B] = SinglePhaseKind.B
    phase_status[SinglePhaseKind.C] = SinglePhaseKind.C
    phase_status[SinglePhaseKind.N] = SinglePhaseKind.N

    assert phase_status[SinglePhaseKind.A] == SinglePhaseKind.A
    assert phase_status[SinglePhaseKind.B] == SinglePhaseKind.B
    assert phase_status[SinglePhaseKind.C] == SinglePhaseKind.C
    assert phase_status[SinglePhaseKind.N] == SinglePhaseKind.N
    assert phase_status.as_phase_code() == PhaseCode.ABN

    terminal.phases = PhaseCode.AC

    assert phase_status[SinglePhaseKind.A] == SinglePhaseKind.A
    assert phase_status[SinglePhaseKind.B] == SinglePhaseKind.B
    assert phase_status[SinglePhaseKind.C] == SinglePhaseKind.C
    assert phase_status[SinglePhaseKind.N] == SinglePhaseKind.N
    assert phase_status.as_phase_code() == PhaseCode.AC

    terminal.phases = PhaseCode.ABN

    assert phase_status.as_phase_code() == PhaseCode.ABN


def as_phase_code_does_not_drop_phases():
    terminal = Terminal(mrid=generate_id(), phases=PhaseCode.ABCN)
    phase_status = PhaseStatus(terminal)

    phase_status[SinglePhaseKind.B] = SinglePhaseKind.A
    phase_status[SinglePhaseKind.C] = SinglePhaseKind.A

    assert phase_status.as_phase_code() is None


def test_invalid_nominal_phase():
    terminal = Terminal(mrid=generate_id(), phases=PhaseCode.ABCN)
    phase_status = PhaseStatus(terminal)

    with pytest.raises(ValueError, match="INTERNAL ERROR: Phase INVALID is invalid"):
        phase_status[SinglePhaseKind.INVALID]


def test_crossing_phases_exception():
    terminal = Terminal(mrid=generate_id(), phases=PhaseCode.ABCN)
    phase_status = PhaseStatus(terminal)

    with pytest.raises(PhaseException, match="Crossing Phases"):
        phase_status[SinglePhaseKind.A] = SinglePhaseKind.A
        phase_status[SinglePhaseKind.A] = SinglePhaseKind.B
