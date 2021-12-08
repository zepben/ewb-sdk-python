#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List

from zepben.evolve import *


def create_nominal_phase_path(from_phase: SinglePhaseKind, to_phase: SinglePhaseKind) -> NominalPhasePath:
    """
    NominalPhasePath()
    NominalPhasePath: from_phase, to_phase
    """
    args = locals()
    # noinspection PyArgumentList
    return NominalPhasePath(**args)


def create_resistance_reactance(r: float = None, x: float = None, r0: float = None, x0: float = None) -> ResistanceReactance:
    """
    ResistanceReactance()
    ResistanceReactance: r, x, r0, x0
    """
    args = locals()
    # noinspection PyArgumentList
    return ResistanceReactance(**args)


def create_traced_phases() -> TracedPhases:
    """
    TracedPhases()
    TracedPhases: normal_status, current_status
    """
    args = locals()
    # noinspection PyArgumentList
    return TracedPhases(**args)
