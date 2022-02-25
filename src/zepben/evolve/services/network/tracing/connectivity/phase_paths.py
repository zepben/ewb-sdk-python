#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Dict, List

from zepben.evolve import SinglePhaseKind, PhaseCode, NominalPhasePath

__all__ = ["straight_phase_connectivity", "viable_inferred_phase_connectivity"]

# noinspection PyArgumentList
_STRAIGHT_PHASE_PATHS = {
    SinglePhaseKind.A: NominalPhasePath(SinglePhaseKind.A, SinglePhaseKind.A),
    SinglePhaseKind.B: NominalPhasePath(SinglePhaseKind.B, SinglePhaseKind.B),
    SinglePhaseKind.C: NominalPhasePath(SinglePhaseKind.C, SinglePhaseKind.C),
    SinglePhaseKind.N: NominalPhasePath(SinglePhaseKind.N, SinglePhaseKind.N),
    SinglePhaseKind.X: NominalPhasePath(SinglePhaseKind.X, SinglePhaseKind.X),
    SinglePhaseKind.Y: NominalPhasePath(SinglePhaseKind.Y, SinglePhaseKind.Y),
}

_KNOWN_PHASE_CODES = [pc for pc in PhaseCode if any(it in PhaseCode.ABC.single_phases for it in pc.single_phases) or (pc == PhaseCode.N)]
_UNKNOWN_PHASE_CODES = [pc for pc in PhaseCode if any(it in PhaseCode.XY.single_phases for it in pc.single_phases)]

straight_phase_connectivity: Dict[PhaseCode, Dict[PhaseCode, List[NominalPhasePath]]] = {
    from_phases: {
        to_phases: [
            _STRAIGHT_PHASE_PATHS[phase] for phase in from_phases.single_phases if phase in to_phases.single_phases
        ] for to_phases in _KNOWN_PHASE_CODES
    } for from_phases in _KNOWN_PHASE_CODES
}
straight_phase_connectivity.update({
    from_phases: {
        to_phases: [
            _STRAIGHT_PHASE_PATHS[phase] for phase in from_phases.single_phases if phase in to_phases.single_phases
        ] for to_phases in _UNKNOWN_PHASE_CODES
    } for from_phases in _UNKNOWN_PHASE_CODES
})

viable_inferred_phase_connectivity: Dict[PhaseCode, Dict[PhaseCode, Dict[SinglePhaseKind, List[SinglePhaseKind]]]] = {
    PhaseCode.XY: {
        PhaseCode.ABC: {SinglePhaseKind.X: [SinglePhaseKind.A, SinglePhaseKind.B, SinglePhaseKind.C],
                        SinglePhaseKind.Y: [SinglePhaseKind.B, SinglePhaseKind.C]},
        PhaseCode.AB: {SinglePhaseKind.X: [SinglePhaseKind.A, SinglePhaseKind.B], SinglePhaseKind.Y: [SinglePhaseKind.B]},
        PhaseCode.AC: {SinglePhaseKind.X: [SinglePhaseKind.A, SinglePhaseKind.C], SinglePhaseKind.Y: [SinglePhaseKind.C]},
        PhaseCode.BC: {SinglePhaseKind.X: [SinglePhaseKind.B, SinglePhaseKind.C], SinglePhaseKind.Y: [SinglePhaseKind.B, SinglePhaseKind.C]},
        PhaseCode.A: {SinglePhaseKind.X: [SinglePhaseKind.A]},
        PhaseCode.B: {SinglePhaseKind.X: [SinglePhaseKind.B], SinglePhaseKind.Y: [SinglePhaseKind.B]},
        PhaseCode.C: {SinglePhaseKind.X: [SinglePhaseKind.C], SinglePhaseKind.Y: [SinglePhaseKind.C]}
    },
    PhaseCode.X: {
        PhaseCode.ABC: {SinglePhaseKind.X: [SinglePhaseKind.A, SinglePhaseKind.B, SinglePhaseKind.C]},
        PhaseCode.AB: {SinglePhaseKind.X: [SinglePhaseKind.A, SinglePhaseKind.B]},
        PhaseCode.AC: {SinglePhaseKind.X: [SinglePhaseKind.A, SinglePhaseKind.C]},
        PhaseCode.BC: {SinglePhaseKind.X: [SinglePhaseKind.B, SinglePhaseKind.C]},
        PhaseCode.A: {SinglePhaseKind.X: [SinglePhaseKind.A]},
        PhaseCode.B: {SinglePhaseKind.X: [SinglePhaseKind.B]},
        PhaseCode.C: {SinglePhaseKind.X: [SinglePhaseKind.C]}
    },
    PhaseCode.Y: {
        PhaseCode.ABC: {SinglePhaseKind.Y: [SinglePhaseKind.B, SinglePhaseKind.C]},
        PhaseCode.AB: {SinglePhaseKind.Y: [SinglePhaseKind.B]},
        PhaseCode.AC: {SinglePhaseKind.Y: [SinglePhaseKind.C]},
        PhaseCode.BC: {SinglePhaseKind.Y: [SinglePhaseKind.B, SinglePhaseKind.C]},
        PhaseCode.A: {},
        PhaseCode.B: {SinglePhaseKind.Y: [SinglePhaseKind.B]},
        PhaseCode.C: {SinglePhaseKind.Y: [SinglePhaseKind.C]}
    }
}
