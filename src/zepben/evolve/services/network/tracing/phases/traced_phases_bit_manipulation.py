#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.


"""
class Phases:
    N = 0xF000
    C = 0x0F00
    B = 0x00F0
    A = 0x000F
    
Phases.N + Phases.A
61455
hex(Phases.N + Phases.A)
'0xf00f'
hex(Phases.N + Phases.A + Phases.B)
'0xf0ff'
hex(Phases.C) in hex(Phases.N + Phases.A + Phases.B)
False
hex(Phases.B) in hex(Phases.N + Phases.A + Phases.B)
"""
from zepben.evolve import SinglePhaseKind


class TracedPhaseBitManipulation:
    _nominal_phase_masks = [0x000F, 0x00F0, 0x0F00, 0xF000]

    _mask_by_phase_map = {
        SinglePhaseKind.N: 0xF000,
        SinglePhaseKind.C: 0x0F00,
        SinglePhaseKind.B: 0x00F0,
        SinglePhaseKind.A: 0x000F
    }

    _phase_by_mask_map = {v: k for k, v in _mask_by_phase_map.items()}

    def get(self, status: hex, nominal_phase: SinglePhaseKind) -> SinglePhaseKind:
        return self._mask_by_phase_map.get(nominal_phase, SinglePhaseKind.NONE)