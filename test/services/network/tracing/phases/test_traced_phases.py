#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import pytest

from zepben.evolve import TracedPhases, SinglePhaseKind as SPK
from zepben.evolve.exceptions import PhaseException

traced_phases = TracedPhases()


def test_set_and_get():
    # -- Setting --
    assert traced_phases.set_normal(SPK.A, SPK.N)
    assert traced_phases.set_normal(SPK.B, SPK.C)
    assert traced_phases.set_normal(SPK.C, SPK.B)
    assert traced_phases.set_normal(SPK.N, SPK.A)

    assert traced_phases.set_current(SPK.A, SPK.A)
    assert traced_phases.set_current(SPK.B, SPK.B)
    assert traced_phases.set_current(SPK.C, SPK.C)
    assert traced_phases.set_current(SPK.N, SPK.N)

    # -- Getting Phase--
    assert traced_phases.normal(SPK.A) == SPK.N
    assert traced_phases.normal(SPK.B) == SPK.C
    assert traced_phases.normal(SPK.C) == SPK.B
    assert traced_phases.normal(SPK.N) == SPK.A

    assert traced_phases.current(SPK.A) == SPK.A
    assert traced_phases.current(SPK.B) == SPK.B
    assert traced_phases.current(SPK.C) == SPK.C
    assert traced_phases.current(SPK.N) == SPK.N

    # -- Setting Unchanged --
    assert not traced_phases.set_normal(SPK.A, SPK.N)
    assert not traced_phases.set_normal(SPK.B, SPK.C)
    assert not traced_phases.set_normal(SPK.C, SPK.B)
    assert not traced_phases.set_normal(SPK.N, SPK.A)

    assert not traced_phases.set_current(SPK.A, SPK.A)
    assert not traced_phases.set_current(SPK.B, SPK.B)
    assert not traced_phases.set_current(SPK.C, SPK.C)
    assert not traced_phases.set_current(SPK.N, SPK.N)


def test_invalid_nominal_phase_normal():
    with pytest.raises(ValueError) as e_info:
        traced_phases.normal(SPK.INVALID)

    assert str(e_info.value) == "INTERNAL ERROR: Phase INVALID is invalid. Must not be NONE or INVALID."


def test_crossing_phases_exception_normal():
    with pytest.raises(PhaseException) as e_info:
        traced_phases.set_normal(SPK.A, SPK.A)
        traced_phases.set_normal(SPK.A, SPK.B)

    assert str(e_info.value) == "Crossing Phases."


def test_invalid_nominal_phase_current():
    with pytest.raises(ValueError):
        traced_phases.current(SPK.INVALID)


def test_crossing_phases_exception_current():
    with pytest.raises(PhaseException):
        traced_phases.set_current(SPK.A, SPK.A)
        traced_phases.set_current(SPK.A, SPK.B)
