#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["transformer_phase_paths", "add_neutral"]

from typing import Dict, List

from zepben.ewb import SinglePhaseKind as Phase, NominalPhasePath, PhaseCode


def _path(from_phase: Phase, to_phase: Phase) -> NominalPhasePath:
    # noinspection PyArgumentList
    return NominalPhasePath(from_phase, to_phase)


# This is used to indicate that a transformer adds a neutral, and it should be energised from the transformer.
add_neutral = _path(Phase.NONE, Phase.N)

transformer_phase_paths: Dict[PhaseCode, Dict[PhaseCode, List[NominalPhasePath]]] = {
    PhaseCode.ABCN: {
        PhaseCode.ABCN: [_path(Phase.A, Phase.A), _path(Phase.B, Phase.B), _path(Phase.C, Phase.C), _path(Phase.N, Phase.N)],
        PhaseCode.ABC: [_path(Phase.A, Phase.A), _path(Phase.B, Phase.B), _path(Phase.C, Phase.C)],
    },
    PhaseCode.AN: {
        PhaseCode.AN: [_path(Phase.A, Phase.A), _path(Phase.N, Phase.N)],
        PhaseCode.XN: [_path(Phase.A, Phase.X), _path(Phase.N, Phase.N)],
        PhaseCode.AB: [_path(Phase.A, Phase.A), _path(Phase.NONE, Phase.B)],
        PhaseCode.XY: [_path(Phase.A, Phase.X), _path(Phase.NONE, Phase.Y)],
        PhaseCode.X: [_path(Phase.A, Phase.X)],
        PhaseCode.A: [_path(Phase.A, Phase.A)],
    },
    PhaseCode.BN: {
        PhaseCode.BN: [_path(Phase.B, Phase.B), _path(Phase.N, Phase.N)],
        PhaseCode.XN: [_path(Phase.B, Phase.X), _path(Phase.N, Phase.N)],
        PhaseCode.BC: [_path(Phase.B, Phase.B), _path(Phase.NONE, Phase.C)],
        PhaseCode.XY: [_path(Phase.B, Phase.X), _path(Phase.NONE, Phase.Y)],
        PhaseCode.B: [_path(Phase.B, Phase.B)],
        PhaseCode.X: [_path(Phase.B, Phase.X)],
    },
    PhaseCode.CN: {
        PhaseCode.CN: [_path(Phase.C, Phase.C), _path(Phase.N, Phase.N)],
        PhaseCode.XN: [_path(Phase.C, Phase.X), _path(Phase.N, Phase.N)],
        PhaseCode.AC: [_path(Phase.C, Phase.C), _path(Phase.NONE, Phase.A)],
        PhaseCode.XY: [_path(Phase.C, Phase.X), _path(Phase.NONE, Phase.Y)],
        PhaseCode.C: [_path(Phase.C, Phase.C)],
        PhaseCode.X: [_path(Phase.C, Phase.X)],
    },
    PhaseCode.XN: {
        PhaseCode.AN: [_path(Phase.X, Phase.A), _path(Phase.N, Phase.N)],
        PhaseCode.BN: [_path(Phase.X, Phase.B), _path(Phase.N, Phase.N)],
        PhaseCode.CN: [_path(Phase.X, Phase.C), _path(Phase.N, Phase.N)],
        PhaseCode.XN: [_path(Phase.X, Phase.X), _path(Phase.N, Phase.N)],
        PhaseCode.AB: [_path(Phase.X, Phase.A), _path(Phase.NONE, Phase.B)],
        PhaseCode.BC: [_path(Phase.X, Phase.B), _path(Phase.NONE, Phase.C)],
        PhaseCode.AC: [_path(Phase.X, Phase.C), _path(Phase.NONE, Phase.A)],
        PhaseCode.XY: [_path(Phase.X, Phase.X), _path(Phase.NONE, Phase.Y)],
        PhaseCode.A: [_path(Phase.X, Phase.A)],
        PhaseCode.B: [_path(Phase.X, Phase.B)],
        PhaseCode.C: [_path(Phase.X, Phase.C)],
        PhaseCode.X: [_path(Phase.X, Phase.X)],
    },
    PhaseCode.ABC: {
        PhaseCode.ABCN: [_path(Phase.A, Phase.A), _path(Phase.B, Phase.B), _path(Phase.C, Phase.C), add_neutral],
        PhaseCode.ABC: [_path(Phase.A, Phase.A), _path(Phase.B, Phase.B), _path(Phase.C, Phase.C)],
    },
    PhaseCode.ABN: {
        PhaseCode.ABN: [_path(Phase.A, Phase.A), _path(Phase.B, Phase.B), _path(Phase.N, Phase.N)],
        PhaseCode.XYN: [_path(Phase.A, Phase.X), _path(Phase.B, Phase.Y), _path(Phase.N, Phase.N)],
        PhaseCode.AB: [_path(Phase.A, Phase.A), _path(Phase.B, Phase.B)],
        PhaseCode.XY: [_path(Phase.A, Phase.X), _path(Phase.B, Phase.Y)],
        PhaseCode.A: [_path(Phase.A, Phase.A)],
        PhaseCode.X: [_path(Phase.A, Phase.X)],
    },
    PhaseCode.BCN: {
        PhaseCode.BCN: [_path(Phase.B, Phase.B), _path(Phase.C, Phase.C), _path(Phase.N, Phase.N)],
        PhaseCode.XYN: [_path(Phase.B, Phase.X), _path(Phase.C, Phase.Y), _path(Phase.N, Phase.N)],
        PhaseCode.BC: [_path(Phase.B, Phase.B), _path(Phase.C, Phase.C)],
        PhaseCode.XY: [_path(Phase.B, Phase.X), _path(Phase.C, Phase.Y)],
        PhaseCode.B: [_path(Phase.B, Phase.B)],
        PhaseCode.X: [_path(Phase.B, Phase.X)],
    },
    PhaseCode.ACN: {
        PhaseCode.ACN: [_path(Phase.A, Phase.A), _path(Phase.C, Phase.C), _path(Phase.N, Phase.N)],
        PhaseCode.XYN: [_path(Phase.A, Phase.X), _path(Phase.C, Phase.Y), _path(Phase.N, Phase.N)],
        PhaseCode.AC: [_path(Phase.A, Phase.A), _path(Phase.C, Phase.C)],
        PhaseCode.XY: [_path(Phase.A, Phase.X), _path(Phase.C, Phase.Y)],
        PhaseCode.C: [_path(Phase.C, Phase.C)],
        PhaseCode.X: [_path(Phase.C, Phase.X)],
    },
    PhaseCode.XYN: {
        PhaseCode.ABN: [_path(Phase.X, Phase.A), _path(Phase.Y, Phase.B), _path(Phase.N, Phase.N)],
        PhaseCode.BCN: [_path(Phase.X, Phase.B), _path(Phase.Y, Phase.C), _path(Phase.N, Phase.N)],
        PhaseCode.ACN: [_path(Phase.X, Phase.A), _path(Phase.Y, Phase.C), _path(Phase.N, Phase.N)],
        PhaseCode.XYN: [_path(Phase.X, Phase.X), _path(Phase.Y, Phase.Y), _path(Phase.N, Phase.N)],
        PhaseCode.AB: [_path(Phase.X, Phase.A), _path(Phase.Y, Phase.B)],
        PhaseCode.BC: [_path(Phase.X, Phase.B), _path(Phase.Y, Phase.C)],
        PhaseCode.AC: [_path(Phase.X, Phase.A), _path(Phase.Y, Phase.C)],
        PhaseCode.XY: [_path(Phase.X, Phase.X), _path(Phase.Y, Phase.Y)],
        PhaseCode.A: [_path(Phase.X, Phase.A)],
        PhaseCode.B: [_path(Phase.X, Phase.B)],
        PhaseCode.C: [_path(Phase.X, Phase.C)],
        PhaseCode.X: [_path(Phase.X, Phase.X)],
    },
    PhaseCode.AB: {
        PhaseCode.ABN: [_path(Phase.A, Phase.A), _path(Phase.B, Phase.B), add_neutral],
        PhaseCode.XYN: [_path(Phase.A, Phase.X), _path(Phase.B, Phase.Y), add_neutral],
        PhaseCode.AN: [_path(Phase.A, Phase.A), add_neutral],
        PhaseCode.XN: [_path(Phase.A, Phase.X), add_neutral],
        PhaseCode.AB: [_path(Phase.A, Phase.A), _path(Phase.B, Phase.B)],
        PhaseCode.XY: [_path(Phase.A, Phase.X), _path(Phase.B, Phase.Y)],
        PhaseCode.A: [_path(Phase.A, Phase.A)],
        PhaseCode.X: [_path(Phase.A, Phase.X)],
    },
    PhaseCode.BC: {
        PhaseCode.BCN: [_path(Phase.B, Phase.B), _path(Phase.C, Phase.C), add_neutral],
        PhaseCode.XYN: [_path(Phase.B, Phase.X), _path(Phase.C, Phase.Y), add_neutral],
        PhaseCode.BN: [_path(Phase.B, Phase.B), add_neutral],
        PhaseCode.XN: [_path(Phase.B, Phase.X), add_neutral],
        PhaseCode.BC: [_path(Phase.B, Phase.B), _path(Phase.C, Phase.C)],
        PhaseCode.XY: [_path(Phase.B, Phase.X), _path(Phase.C, Phase.Y)],
        PhaseCode.B: [_path(Phase.B, Phase.B)],
        PhaseCode.X: [_path(Phase.B, Phase.X)],
    },
    PhaseCode.AC: {
        PhaseCode.ACN: [_path(Phase.A, Phase.A), _path(Phase.C, Phase.C), add_neutral],
        PhaseCode.XYN: [_path(Phase.A, Phase.X), _path(Phase.C, Phase.Y), add_neutral],
        PhaseCode.CN: [_path(Phase.C, Phase.C), add_neutral],
        PhaseCode.XN: [_path(Phase.C, Phase.X), add_neutral],
        PhaseCode.AC: [_path(Phase.A, Phase.A), _path(Phase.C, Phase.C)],
        PhaseCode.XY: [_path(Phase.A, Phase.X), _path(Phase.C, Phase.Y)],
        PhaseCode.C: [_path(Phase.C, Phase.C)],
        PhaseCode.X: [_path(Phase.C, Phase.X)],
    },
    PhaseCode.XY: {
        PhaseCode.ABN: [_path(Phase.X, Phase.A), _path(Phase.Y, Phase.B), add_neutral],
        PhaseCode.BCN: [_path(Phase.X, Phase.B), _path(Phase.Y, Phase.C), add_neutral],
        PhaseCode.ACN: [_path(Phase.X, Phase.A), _path(Phase.Y, Phase.C), add_neutral],
        PhaseCode.XYN: [_path(Phase.X, Phase.X), _path(Phase.Y, Phase.Y), add_neutral],
        PhaseCode.AN: [_path(Phase.X, Phase.A), add_neutral],
        PhaseCode.BN: [_path(Phase.X, Phase.B), add_neutral],
        PhaseCode.CN: [_path(Phase.X, Phase.C), add_neutral],
        PhaseCode.XN: [_path(Phase.X, Phase.X), add_neutral],
        PhaseCode.AB: [_path(Phase.X, Phase.A), _path(Phase.Y, Phase.B)],
        PhaseCode.BC: [_path(Phase.X, Phase.B), _path(Phase.Y, Phase.C)],
        PhaseCode.AC: [_path(Phase.X, Phase.A), _path(Phase.Y, Phase.C)],
        PhaseCode.XY: [_path(Phase.X, Phase.X), _path(Phase.Y, Phase.Y)],
        PhaseCode.A: [_path(Phase.X, Phase.A)],
        PhaseCode.B: [_path(Phase.X, Phase.B)],
        PhaseCode.C: [_path(Phase.X, Phase.C)],
        PhaseCode.X: [_path(Phase.X, Phase.X)],
    },
    PhaseCode.A: {
        PhaseCode.AN: [_path(Phase.A, Phase.A), add_neutral],
        PhaseCode.XN: [_path(Phase.A, Phase.X), add_neutral],
        PhaseCode.AB: [_path(Phase.A, Phase.A), _path(Phase.NONE, Phase.B)],
        PhaseCode.XY: [_path(Phase.A, Phase.X), _path(Phase.NONE, Phase.Y)],
        PhaseCode.A: [_path(Phase.A, Phase.A)],
        PhaseCode.X: [_path(Phase.A, Phase.X)],
        PhaseCode.ABN: [_path(Phase.A, Phase.A), _path(Phase.NONE, Phase.B), add_neutral],
        PhaseCode.XYN: [_path(Phase.A, Phase.X), _path(Phase.NONE, Phase.Y), add_neutral],
    },
    PhaseCode.B: {
        PhaseCode.BN: [_path(Phase.B, Phase.B), add_neutral],
        PhaseCode.XN: [_path(Phase.B, Phase.X), add_neutral],
        PhaseCode.BC: [_path(Phase.B, Phase.B), _path(Phase.NONE, Phase.C)],
        PhaseCode.XY: [_path(Phase.B, Phase.X), _path(Phase.NONE, Phase.Y)],
        PhaseCode.B: [_path(Phase.B, Phase.B)],
        PhaseCode.X: [_path(Phase.B, Phase.X)],
        PhaseCode.BCN: [_path(Phase.B, Phase.B), _path(Phase.NONE, Phase.C), add_neutral],
        PhaseCode.XYN: [_path(Phase.B, Phase.X), _path(Phase.NONE, Phase.Y), add_neutral],
    },
    PhaseCode.C: {
        PhaseCode.CN: [_path(Phase.C, Phase.C), add_neutral],
        PhaseCode.XN: [_path(Phase.C, Phase.X), add_neutral],
        PhaseCode.AC: [_path(Phase.C, Phase.C), _path(Phase.NONE, Phase.A)],
        PhaseCode.XY: [_path(Phase.C, Phase.X), _path(Phase.NONE, Phase.Y)],
        PhaseCode.C: [_path(Phase.C, Phase.C)],
        PhaseCode.X: [_path(Phase.C, Phase.X)],
        PhaseCode.ACN: [_path(Phase.C, Phase.C), _path(Phase.NONE, Phase.A), add_neutral],
        PhaseCode.XYN: [_path(Phase.C, Phase.X), _path(Phase.NONE, Phase.Y), add_neutral],
    },
    PhaseCode.X: {
        PhaseCode.AN: [_path(Phase.X, Phase.A), add_neutral],
        PhaseCode.BN: [_path(Phase.X, Phase.B), add_neutral],
        PhaseCode.CN: [_path(Phase.X, Phase.C), add_neutral],
        PhaseCode.XN: [_path(Phase.X, Phase.X), add_neutral],
        PhaseCode.AB: [_path(Phase.X, Phase.A), _path(Phase.NONE, Phase.B)],
        PhaseCode.BC: [_path(Phase.X, Phase.B), _path(Phase.NONE, Phase.C)],
        PhaseCode.AC: [_path(Phase.X, Phase.C), _path(Phase.NONE, Phase.A)],
        PhaseCode.XY: [_path(Phase.X, Phase.X), _path(Phase.NONE, Phase.Y)],
        PhaseCode.A: [_path(Phase.X, Phase.A)],
        PhaseCode.B: [_path(Phase.X, Phase.B)],
        PhaseCode.C: [_path(Phase.X, Phase.C)],
        PhaseCode.X: [_path(Phase.X, Phase.X)],
        PhaseCode.ABN: [_path(Phase.X, Phase.A), _path(Phase.NONE, Phase.B), add_neutral],
        PhaseCode.BCN: [_path(Phase.X, Phase.B), _path(Phase.NONE, Phase.C), add_neutral],
        PhaseCode.ACN: [_path(Phase.X, Phase.C), _path(Phase.NONE, Phase.A), add_neutral],
        PhaseCode.XYN: [_path(Phase.X, Phase.X), _path(Phase.NONE, Phase.Y), add_neutral],
    },
}
