#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https:#mozilla.org/MPL/2.0/.
# PROJ-1945
# from _pytest.python_api import raises
#
# from zepben.evolve import SinglePhaseKind, PhaseDirection, TracedPhases
# from zepben.evolve.exceptions import PhaseException
#
#
# def test_get_phase():
#     tp = _new_test_phase_object()
#
#     assert tp.phase_normal(SinglePhaseKind.A) == SinglePhaseKind.A
#     assert tp.phase_normal(SinglePhaseKind.B) == SinglePhaseKind.B
#     assert tp.phase_normal(SinglePhaseKind.C) == SinglePhaseKind.C
#     assert tp.phase_normal(SinglePhaseKind.N) == SinglePhaseKind.N
#
#     assert tp.phase_current(SinglePhaseKind.A) == SinglePhaseKind.N
#     assert tp.phase_current(SinglePhaseKind.B) == SinglePhaseKind.C
#     assert tp.phase_current(SinglePhaseKind.C) == SinglePhaseKind.B
#     assert tp.phase_current(SinglePhaseKind.N) == SinglePhaseKind.A
#
#
# def test_get_direction():
#     tp = _new_test_phase_object()
#
#     assert tp.direction_normal(SinglePhaseKind.A) == PhaseDirection.IN
#     assert tp.direction_normal(SinglePhaseKind.B) == PhaseDirection.OUT
#     assert tp.direction_normal(SinglePhaseKind.C) == PhaseDirection.BOTH
#     assert tp.direction_normal(SinglePhaseKind.N) == PhaseDirection.BOTH
#
#     assert tp.direction_current(SinglePhaseKind.A) == PhaseDirection.BOTH
#     assert tp.direction_current(SinglePhaseKind.B) == PhaseDirection.BOTH
#     assert tp.direction_current(SinglePhaseKind.C) == PhaseDirection.OUT
#     assert tp.direction_current(SinglePhaseKind.N) == PhaseDirection.IN
#
#
# def test_set():
#     tp = _new_test_phase_object()
#
#     # -- Setting --
#     assert tp.set_normal(SinglePhaseKind.N, SinglePhaseKind.A, PhaseDirection.BOTH)
#     assert tp.set_normal(SinglePhaseKind.C, SinglePhaseKind.B, PhaseDirection.BOTH)
#     assert tp.set_normal(SinglePhaseKind.B, SinglePhaseKind.C, PhaseDirection.OUT)
#     assert tp.set_normal(SinglePhaseKind.A, SinglePhaseKind.N, PhaseDirection.IN)
#
#     assert tp.set_current(SinglePhaseKind.A, SinglePhaseKind.A, PhaseDirection.IN)
#     assert tp.set_current(SinglePhaseKind.B, SinglePhaseKind.B, PhaseDirection.OUT)
#     assert tp.set_current(SinglePhaseKind.C, SinglePhaseKind.C, PhaseDirection.BOTH)
#     assert tp.set_current(SinglePhaseKind.N, SinglePhaseKind.N, PhaseDirection.BOTH)
#
#     # Returns false if no changes were done.
#     assert not tp.set_normal(SinglePhaseKind.N, SinglePhaseKind.A, PhaseDirection.BOTH)
#     assert not tp.set_normal(SinglePhaseKind.C, SinglePhaseKind.B, PhaseDirection.BOTH)
#     assert not tp.set_normal(SinglePhaseKind.B, SinglePhaseKind.C, PhaseDirection.OUT)
#     assert not tp.set_normal(SinglePhaseKind.A, SinglePhaseKind.N, PhaseDirection.IN)
#
#     assert not tp.set_current(SinglePhaseKind.A, SinglePhaseKind.A, PhaseDirection.IN)
#     assert not tp.set_current(SinglePhaseKind.B, SinglePhaseKind.B, PhaseDirection.OUT)
#     assert not tp.set_current(SinglePhaseKind.C, SinglePhaseKind.C, PhaseDirection.BOTH)
#     assert not tp.set_current(SinglePhaseKind.N, SinglePhaseKind.N, PhaseDirection.BOTH)
#
#     # -- Getting Phase--
#     assert tp.phase_normal(SinglePhaseKind.A) == SinglePhaseKind.N
#     assert tp.phase_normal(SinglePhaseKind.B) == SinglePhaseKind.C
#     assert tp.phase_normal(SinglePhaseKind.C) == SinglePhaseKind.B
#     assert tp.phase_normal(SinglePhaseKind.N) == SinglePhaseKind.A
#
#     assert tp.phase_current(SinglePhaseKind.A) == SinglePhaseKind.A
#     assert tp.phase_current(SinglePhaseKind.B) == SinglePhaseKind.B
#     assert tp.phase_current(SinglePhaseKind.C) == SinglePhaseKind.C
#     assert tp.phase_current(SinglePhaseKind.N) == SinglePhaseKind.N
#
#     # -- Getting Direction--
#     assert tp.direction_normal(SinglePhaseKind.A) == PhaseDirection.BOTH
#     assert tp.direction_normal(SinglePhaseKind.B) == PhaseDirection.BOTH
#     assert tp.direction_normal(SinglePhaseKind.C) == PhaseDirection.OUT
#     assert tp.direction_normal(SinglePhaseKind.N) == PhaseDirection.IN
#
#     assert tp.direction_current(SinglePhaseKind.A) == PhaseDirection.IN
#     assert tp.direction_current(SinglePhaseKind.B) == PhaseDirection.OUT
#     assert tp.direction_current(SinglePhaseKind.C) == PhaseDirection.BOTH
#     assert tp.direction_current(SinglePhaseKind.N) == PhaseDirection.BOTH
#
#     # -- Setting --
#     assert tp.set_normal(SinglePhaseKind.N, SinglePhaseKind.A, PhaseDirection.IN)
#     assert tp.set_normal(SinglePhaseKind.C, SinglePhaseKind.B, PhaseDirection.OUT)
#     assert tp.set_normal(SinglePhaseKind.B, SinglePhaseKind.C, PhaseDirection.BOTH)
#     assert tp.set_normal(SinglePhaseKind.A, SinglePhaseKind.N, PhaseDirection.BOTH)
#
#     assert tp.set_current(SinglePhaseKind.A, SinglePhaseKind.A, PhaseDirection.BOTH)
#     assert tp.set_current(SinglePhaseKind.B, SinglePhaseKind.B, PhaseDirection.BOTH)
#     assert tp.set_current(SinglePhaseKind.C, SinglePhaseKind.C, PhaseDirection.OUT)
#     assert tp.set_current(SinglePhaseKind.N, SinglePhaseKind.N, PhaseDirection.IN)
#
#     # -- Getting Phase--
#     assert tp.phase_normal(SinglePhaseKind.A) == SinglePhaseKind.N
#     assert tp.phase_normal(SinglePhaseKind.B) == SinglePhaseKind.C
#     assert tp.phase_normal(SinglePhaseKind.C) == SinglePhaseKind.B
#     assert tp.phase_normal(SinglePhaseKind.N) == SinglePhaseKind.A
#
#     assert tp.phase_current(SinglePhaseKind.A) == SinglePhaseKind.A
#     assert tp.phase_current(SinglePhaseKind.B) == SinglePhaseKind.B
#     assert tp.phase_current(SinglePhaseKind.C) == SinglePhaseKind.C
#     assert tp.phase_current(SinglePhaseKind.N) == SinglePhaseKind.N
#
#     # -- Getting Direction--
#     assert tp.direction_normal(SinglePhaseKind.A) == PhaseDirection.IN
#     assert tp.direction_normal(SinglePhaseKind.B) == PhaseDirection.OUT
#     assert tp.direction_normal(SinglePhaseKind.C) == PhaseDirection.BOTH
#     assert tp.direction_normal(SinglePhaseKind.N) == PhaseDirection.BOTH
#
#     assert tp.direction_current(SinglePhaseKind.A) == PhaseDirection.BOTH
#     assert tp.direction_current(SinglePhaseKind.B) == PhaseDirection.BOTH
#     assert tp.direction_current(SinglePhaseKind.C) == PhaseDirection.OUT
#     assert tp.direction_current(SinglePhaseKind.N) == PhaseDirection.IN
#
#     # Setting NONE to the direction clears the whole phase
#     tp.set_normal(SinglePhaseKind.N, SinglePhaseKind.A, PhaseDirection.NONE)
#     tp.set_current(SinglePhaseKind.A, SinglePhaseKind.A, PhaseDirection.NONE)
#
#     assert tp.direction_normal(SinglePhaseKind.A) == PhaseDirection.NONE
#     assert tp.direction_current(SinglePhaseKind.A) == PhaseDirection.NONE
#     assert tp.phase_normal(SinglePhaseKind.A) == SinglePhaseKind.NONE
#     assert tp.phase_current(SinglePhaseKind.A) == SinglePhaseKind.NONE
#
#     # Setting NONE to the phase clears the whole phase
#     assert tp.set_normal(SinglePhaseKind.NONE, SinglePhaseKind.B, PhaseDirection.NONE)
#     assert tp.set_current(SinglePhaseKind.NONE, SinglePhaseKind.B, PhaseDirection.NONE)
#
#     assert tp.direction_normal(SinglePhaseKind.B) == PhaseDirection.NONE
#     assert tp.direction_current(SinglePhaseKind.B) == PhaseDirection.NONE
#     assert tp.phase_normal(SinglePhaseKind.B) == SinglePhaseKind.NONE
#     assert tp.phase_current(SinglePhaseKind.B) == SinglePhaseKind.NONE
#
#
# def test_add():
#     tp = TracedPhases()
#
#     # -- Adding --
#     assert tp.add_normal(SinglePhaseKind.N, SinglePhaseKind.A, PhaseDirection.BOTH)
#     assert tp.add_normal(SinglePhaseKind.C, SinglePhaseKind.B, PhaseDirection.BOTH)
#     assert tp.add_normal(SinglePhaseKind.B, SinglePhaseKind.C, PhaseDirection.OUT)
#     assert tp.add_normal(SinglePhaseKind.A, SinglePhaseKind.N, PhaseDirection.IN)
#
#     assert tp.add_current(SinglePhaseKind.A, SinglePhaseKind.A, PhaseDirection.IN)
#     assert tp.add_current(SinglePhaseKind.B, SinglePhaseKind.B, PhaseDirection.OUT)
#     assert tp.add_current(SinglePhaseKind.C, SinglePhaseKind.C, PhaseDirection.BOTH)
#     assert tp.add_current(SinglePhaseKind.N, SinglePhaseKind.N, PhaseDirection.BOTH)
#
#     # Returns false if no changes were done.
#     assert not tp.add_normal(SinglePhaseKind.N, SinglePhaseKind.A, PhaseDirection.BOTH)
#     assert not tp.add_normal(SinglePhaseKind.C, SinglePhaseKind.B, PhaseDirection.BOTH)
#     assert not tp.add_normal(SinglePhaseKind.B, SinglePhaseKind.C, PhaseDirection.OUT)
#     assert not tp.add_normal(SinglePhaseKind.A, SinglePhaseKind.N, PhaseDirection.IN)
#
#     assert not tp.add_current(SinglePhaseKind.A, SinglePhaseKind.A, PhaseDirection.IN)
#     assert not tp.add_current(SinglePhaseKind.B, SinglePhaseKind.B, PhaseDirection.OUT)
#     assert not tp.add_current(SinglePhaseKind.C, SinglePhaseKind.C, PhaseDirection.BOTH)
#     assert not tp.add_current(SinglePhaseKind.N, SinglePhaseKind.N, PhaseDirection.BOTH)
#
#     # -- Getting Phase--
#     assert tp.phase_normal(SinglePhaseKind.A) == SinglePhaseKind.N
#     assert tp.phase_normal(SinglePhaseKind.B) == SinglePhaseKind.C
#     assert tp.phase_normal(SinglePhaseKind.C) == SinglePhaseKind.B
#     assert tp.phase_normal(SinglePhaseKind.N) == SinglePhaseKind.A
#
#     assert tp.phase_current(SinglePhaseKind.A) == SinglePhaseKind.A
#     assert tp.phase_current(SinglePhaseKind.B) == SinglePhaseKind.B
#     assert tp.phase_current(SinglePhaseKind.C) == SinglePhaseKind.C
#     assert tp.phase_current(SinglePhaseKind.N) == SinglePhaseKind.N
#
#     # -- Getting Direction--
#     assert tp.direction_normal(SinglePhaseKind.A) == PhaseDirection.BOTH
#     assert tp.direction_normal(SinglePhaseKind.B) == PhaseDirection.BOTH
#     assert tp.direction_normal(SinglePhaseKind.C) == PhaseDirection.OUT
#     assert tp.direction_normal(SinglePhaseKind.N) == PhaseDirection.IN
#
#     assert tp.direction_current(SinglePhaseKind.A) == PhaseDirection.IN
#     assert tp.direction_current(SinglePhaseKind.B) == PhaseDirection.OUT
#     assert tp.direction_current(SinglePhaseKind.C) == PhaseDirection.BOTH
#     assert tp.direction_current(SinglePhaseKind.N) == PhaseDirection.BOTH
#
#     # -- Adding --
#     assert not tp.add_normal(SinglePhaseKind.N, SinglePhaseKind.A, PhaseDirection.NONE)
#     assert not tp.add_normal(SinglePhaseKind.C, SinglePhaseKind.B, PhaseDirection.IN)
#     assert tp.add_normal(SinglePhaseKind.B, SinglePhaseKind.C, PhaseDirection.IN)
#     assert tp.add_normal(SinglePhaseKind.A, SinglePhaseKind.N, PhaseDirection.OUT)
#
#     assert tp.add_current(SinglePhaseKind.A, SinglePhaseKind.A, PhaseDirection.OUT)
#     assert tp.add_current(SinglePhaseKind.B, SinglePhaseKind.B, PhaseDirection.IN)
#     assert not tp.add_current(SinglePhaseKind.C, SinglePhaseKind.C, PhaseDirection.NONE)
#     assert not tp.add_current(SinglePhaseKind.N, SinglePhaseKind.N, PhaseDirection.OUT)
#
#     # -- Getting Phase--
#     assert tp.phase_normal(SinglePhaseKind.A) == SinglePhaseKind.N
#     assert tp.phase_normal(SinglePhaseKind.B) == SinglePhaseKind.C
#     assert tp.phase_normal(SinglePhaseKind.C) == SinglePhaseKind.B
#     assert tp.phase_normal(SinglePhaseKind.N) == SinglePhaseKind.A
#
#     assert tp.phase_current(SinglePhaseKind.A) == SinglePhaseKind.A
#     assert tp.phase_current(SinglePhaseKind.B) == SinglePhaseKind.B
#     assert tp.phase_current(SinglePhaseKind.C) == SinglePhaseKind.C
#     assert tp.phase_current(SinglePhaseKind.N) == SinglePhaseKind.N
#
#     # -- Getting Direction--
#     assert tp.direction_normal(SinglePhaseKind.A) == PhaseDirection.BOTH
#     assert tp.direction_normal(SinglePhaseKind.B) == PhaseDirection.BOTH
#     assert tp.direction_normal(SinglePhaseKind.C) == PhaseDirection.BOTH
#     assert tp.direction_normal(SinglePhaseKind.N) == PhaseDirection.BOTH
#
#     assert tp.direction_current(SinglePhaseKind.A) == PhaseDirection.BOTH
#     assert tp.direction_current(SinglePhaseKind.B) == PhaseDirection.BOTH
#     assert tp.direction_current(SinglePhaseKind.C) == PhaseDirection.BOTH
#     assert tp.direction_current(SinglePhaseKind.N) == PhaseDirection.BOTH
#
#     with raises(PhaseException, match="Crossing phases"):
#         tp.add_normal(SinglePhaseKind.A, SinglePhaseKind.A, PhaseDirection.BOTH)
#
#
# def test_remove_direction():
#     tp = _new_test_phase_object()
#
#     tp.add_normal(SinglePhaseKind.A, SinglePhaseKind.A, PhaseDirection.OUT)
#     tp.add_normal(SinglePhaseKind.B, SinglePhaseKind.B, PhaseDirection.IN)
#
#     tp.add_current(SinglePhaseKind.B, SinglePhaseKind.C, PhaseDirection.IN)
#     tp.add_current(SinglePhaseKind.A, SinglePhaseKind.N, PhaseDirection.OUT)
#
#     tp.remove_normal(SinglePhaseKind.A, SinglePhaseKind.A, PhaseDirection.IN)
#     tp.remove_normal(SinglePhaseKind.B, SinglePhaseKind.B, PhaseDirection.OUT)
#     tp.remove_normal(SinglePhaseKind.C, SinglePhaseKind.C, PhaseDirection.BOTH)
#     tp.remove_normal(SinglePhaseKind.N, SinglePhaseKind.N, PhaseDirection.BOTH)
#
#     tp.remove_current(SinglePhaseKind.N, SinglePhaseKind.A, PhaseDirection.BOTH)
#     tp.remove_current(SinglePhaseKind.C, SinglePhaseKind.B, PhaseDirection.BOTH)
#     tp.remove_current(SinglePhaseKind.B, SinglePhaseKind.C, PhaseDirection.OUT)
#     tp.remove_current(SinglePhaseKind.A, SinglePhaseKind.N, PhaseDirection.IN)
#
#     assert tp.direction_normal(SinglePhaseKind.A) == PhaseDirection.OUT
#     assert tp.direction_normal(SinglePhaseKind.B) == PhaseDirection.IN
#     assert tp.direction_normal(SinglePhaseKind.C) == PhaseDirection.NONE
#     assert tp.direction_normal(SinglePhaseKind.N) == PhaseDirection.NONE
#
#     assert tp.direction_current(SinglePhaseKind.A) == PhaseDirection.NONE
#     assert tp.direction_current(SinglePhaseKind.B) == PhaseDirection.NONE
#     assert tp.direction_current(SinglePhaseKind.C) == PhaseDirection.IN
#     assert tp.direction_current(SinglePhaseKind.N) == PhaseDirection.OUT
#
#     assert tp.remove_normal(SinglePhaseKind.A, SinglePhaseKind.A)
#     assert tp.remove_normal(SinglePhaseKind.B, SinglePhaseKind.B)
#     assert not tp.remove_normal(SinglePhaseKind.C, SinglePhaseKind.C)
#     assert not tp.remove_normal(SinglePhaseKind.N, SinglePhaseKind.N)
#
#     assert not tp.remove_current(SinglePhaseKind.N, SinglePhaseKind.A)
#     assert not tp.remove_current(SinglePhaseKind.C, SinglePhaseKind.B)
#     assert tp.remove_current(SinglePhaseKind.B, SinglePhaseKind.C)
#     assert tp.remove_current(SinglePhaseKind.A, SinglePhaseKind.N)
#
#     assert tp.direction_normal(SinglePhaseKind.A) == PhaseDirection.NONE
#     assert tp.direction_normal(SinglePhaseKind.B) == PhaseDirection.NONE
#     assert tp.direction_normal(SinglePhaseKind.C) == PhaseDirection.NONE
#     assert tp.direction_normal(SinglePhaseKind.N) == PhaseDirection.NONE
#
#     assert tp.direction_current(SinglePhaseKind.A) == PhaseDirection.NONE
#     assert tp.direction_current(SinglePhaseKind.B) == PhaseDirection.NONE
#     assert tp.direction_current(SinglePhaseKind.C) == PhaseDirection.NONE
#     assert tp.direction_current(SinglePhaseKind.N) == PhaseDirection.NONE
#
#
# def test_invalid_nominal_normal():
#     with raises(ValueError, match="INTERNAL ERROR: Phase SinglePhaseKind.INVALID is invalid. Must be one of [[].*[]]"):
#         _new_test_phase_object().phase_normal(SinglePhaseKind.INVALID)
#
#
# def test_crossing_phases_exception_normal():
#     with raises(PhaseException, match="Crossing phases"):
#         _new_test_phase_object().add_normal(SinglePhaseKind.B, SinglePhaseKind.A, PhaseDirection.BOTH)
#
#
# def test_invalid_nominal_current():
#     with raises(ValueError, match="INTERNAL ERROR: Phase SinglePhaseKind.INVALID is invalid. Must be one of [[].*[]]"):
#         _new_test_phase_object().phase_current(SinglePhaseKind.INVALID)
#
#
# def test_crossing_phases_exception_current():
#     with raises(PhaseException, match="Crossing phases"):
#         _new_test_phase_object().add_current(SinglePhaseKind.B, SinglePhaseKind.A, PhaseDirection.BOTH)
#
#
# def test_removing_something_not_present_normal():
#     tp = _new_test_phase_object()
#     assert not tp.remove_normal(SinglePhaseKind.B, SinglePhaseKind.A, PhaseDirection.OUT)
#
#
# def test_removing_something_not_present_current():
#     tp = _new_test_phase_object()
#     assert not tp.remove_current(SinglePhaseKind.A, SinglePhaseKind.N, PhaseDirection.OUT)
#
#
# def _new_test_phase_object() -> TracedPhases:
#     tp = TracedPhases()
#     tp.set_normal(SinglePhaseKind.A, SinglePhaseKind.A, PhaseDirection.IN)
#     tp.set_normal(SinglePhaseKind.B, SinglePhaseKind.B, PhaseDirection.OUT)
#     tp.set_normal(SinglePhaseKind.C, SinglePhaseKind.C, PhaseDirection.BOTH)
#     tp.set_normal(SinglePhaseKind.N, SinglePhaseKind.N, PhaseDirection.BOTH)
#
#     tp.set_current(SinglePhaseKind.N, SinglePhaseKind.A, PhaseDirection.BOTH)
#     tp.set_current(SinglePhaseKind.C, SinglePhaseKind.B, PhaseDirection.BOTH)
#     tp.set_current(SinglePhaseKind.B, SinglePhaseKind.C, PhaseDirection.OUT)
#     tp.set_current(SinglePhaseKind.A, SinglePhaseKind.N, PhaseDirection.IN)
#
#     return tp
