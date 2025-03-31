#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.


from zepben.evolve import SinglePhaseKind

_phase_masks = [0x1, 0x2, 0x4, 0x8]

SinglePhaseKind.byte_selector = lambda spk: spk.mask_index * 4
SinglePhaseKind.shifted_value = lambda spk, nominal_phase: _phase_masks[spk.mask_index] << nominal_phase.byte_selector()


class TracedPhaseBitManipulation:
    _nominal_phase_masks = [0x000F, 0x00F0, 0x0F00, 0xF000]

    _bit_to_phase_map = {
        0x8: SinglePhaseKind.N,
        0x4: SinglePhaseKind.C,
        0x2: SinglePhaseKind.B,
        0x1: SinglePhaseKind.A
    }

    @classmethod
    def get(cls, status: hex, nominal_phase: SinglePhaseKind) -> SinglePhaseKind:
        return cls._bit_to_phase_map.get(status >> nominal_phase.byte_selector() & 15, SinglePhaseKind.NONE)

    @classmethod
    def set(cls, status: hex, nominal_phase: SinglePhaseKind, single_phase_kind: SinglePhaseKind) -> hex:
        if single_phase_kind == SinglePhaseKind.NONE:
            return status & ~cls._nominal_phase_masks[nominal_phase.mask_index]
        else:
            return status & ~cls._nominal_phase_masks[nominal_phase.mask_index] | single_phase_kind.shifted_value(nominal_phase)

