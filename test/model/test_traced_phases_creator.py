#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https:#mozilla.org/MPL/2.0/.
from _pytest.python_api import raises

from zepben.evolve import SinglePhaseKind, TracedPhases
from zepben.evolve.model.create_basic_model_components import create_traced_phases


"""
Duplication of test_traced_phases.py but using the create_traced_phases method instead of the class initiator
"""


def test_get_normal():
    tp = _new_test_phase_object()

    assert tp.normal(SinglePhaseKind.A) == SinglePhaseKind.A
    assert tp.normal(SinglePhaseKind.B) == SinglePhaseKind.B
    assert tp.normal(SinglePhaseKind.C) == SinglePhaseKind.C
    assert tp.normal(SinglePhaseKind.N) == SinglePhaseKind.N


def test_get_current():
    tp = _new_test_phase_object()

    assert tp.current(SinglePhaseKind.A) == SinglePhaseKind.B
    assert tp.current(SinglePhaseKind.B) == SinglePhaseKind.C
    assert tp.current(SinglePhaseKind.C) == SinglePhaseKind.N
    assert tp.current(SinglePhaseKind.N) == SinglePhaseKind.A


def test_set_normal():
    tp = _new_test_phase_object()

    # Testing removal of normal phase as setting phases to empty traced phase is covered in creation
    tp.set_normal(SinglePhaseKind.A, SinglePhaseKind.NONE)
    tp.set_normal(SinglePhaseKind.B, SinglePhaseKind.NONE)
    tp.set_normal(SinglePhaseKind.C, SinglePhaseKind.NONE)
    tp.set_normal(SinglePhaseKind.N, SinglePhaseKind.NONE)

    assert tp.normal(SinglePhaseKind.A) == SinglePhaseKind.NONE
    assert tp.normal(SinglePhaseKind.B) == SinglePhaseKind.NONE
    assert tp.normal(SinglePhaseKind.C) == SinglePhaseKind.NONE
    assert tp.normal(SinglePhaseKind.N) == SinglePhaseKind.NONE


def test_set_current():
    tp = TracedPhases()

    # Testing changes to already set current traced phase
    tp.set_current(SinglePhaseKind.A, SinglePhaseKind.C)
    tp.set_current(SinglePhaseKind.B, SinglePhaseKind.N)
    tp.set_current(SinglePhaseKind.C, SinglePhaseKind.A)
    tp.set_current(SinglePhaseKind.N, SinglePhaseKind.B)

    assert tp.current(SinglePhaseKind.A) == SinglePhaseKind.C
    assert tp.current(SinglePhaseKind.B) == SinglePhaseKind.N
    assert tp.current(SinglePhaseKind.C) == SinglePhaseKind.A
    assert tp.current(SinglePhaseKind.N) == SinglePhaseKind.B


def _new_test_phase_object() -> TracedPhases:
    tp = create_traced_phases()

    tp.set_normal(SinglePhaseKind.A, SinglePhaseKind.A)
    tp.set_normal(SinglePhaseKind.B, SinglePhaseKind.B)
    tp.set_normal(SinglePhaseKind.C, SinglePhaseKind.C)
    tp.set_normal(SinglePhaseKind.N, SinglePhaseKind.N)

    tp.set_current(SinglePhaseKind.A, SinglePhaseKind.B)
    tp.set_current(SinglePhaseKind.B, SinglePhaseKind.C)
    tp.set_current(SinglePhaseKind.C, SinglePhaseKind.N)
    tp.set_current(SinglePhaseKind.N, SinglePhaseKind.A)

    return tp
