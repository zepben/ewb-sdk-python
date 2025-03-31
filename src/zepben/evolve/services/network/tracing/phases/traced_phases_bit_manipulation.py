#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.


from zepben.evolve import SinglePhaseKind

_phase_masks = [0x1, 0x2, 0x4, 0x8]

_nominal_phase_masks = [0x000F, 0x00F0, 0x0F00, 0xF000]
"""Bitwise mask for selecting the specific phases from a nominal phase eg: A/B/C/N - `0x000F` will select Phase.A"""

_bit_to_phase_map = {
    0x8: SinglePhaseKind.N,
    0x4: SinglePhaseKind.C,
    0x2: SinglePhaseKind.B,
    0x1: SinglePhaseKind.A
}

SinglePhaseKind.byte_selector = lambda spk: spk.mask_index * 4
SinglePhaseKind.shifted_value = lambda spk, nominal_phase: _phase_masks[spk.mask_index] << nominal_phase.byte_selector()


class TracedPhaseBitManipulation:
    
    """
    Class that performs the bit manipulation for the input phase status.
    Each byte in an int is used to store all possible phases and directions for a nominal phase.
    Each byte has 2 bits that represent the direction for a phase. If none of those bits are set the direction is equal to NONE.
    Use the figures below as a reference.
    <p>
    Network state phase status:
                   |              16 bits              |
                   | 4 bits | 4 bits | 4 bits | 4 bits |
    Nominal phase: |   N    |    C   | B/Y/s2 | A/X/s1 |
    <p>
    Each nominal phase (actual phase):
                  |                 4 bits                |
                  |  1 bit  |  1 bit  |  1 bit  |  1 bit  |
    Actual Phase: |    N    |    C    |    B    |    A    |
    """
    
    @staticmethod
    def get(status: hex, nominal_phase: SinglePhaseKind) -> SinglePhaseKind:
        """
        get the selected phase from the `PhaseCode` represented by a 16-bit integer `status`

        eg:
            >>> tbm = TracedPhaseBitManipulation()
            >>> p = 0x0
            >>> p = tbm.set(p, SinglePhaseKind.A, SinglePhaseKind.A)
            >>> tbm.get(p, SinglePhaseKind.A)
            <SinglePhaseKind.A: (1, 0)>
            >>> p = tbm.set(p, SinglePhaseKind.B, SinglePhaseKind.C)
            >>> tbm.get(p, SinglePhaseKind.B)
            <SinglePhaseKind.C: (3, 2)>

        :param status: 16-bit integer used to store the current phase data
        :param nominal_phase: the nominal phase to return from the `PhaseCode`
        """
        return _bit_to_phase_map.get(status >> nominal_phase.byte_selector() & 15, SinglePhaseKind.NONE)

    @staticmethod
    def set(status: hex, nominal_phase: SinglePhaseKind, single_phase_kind: SinglePhaseKind) -> hex:
        """
        Set the `nominal_phase` in the `PhaseCode` represented by a 16-bit integer `status` to `single_phase_kind`

        eg:
            >>> tbm = TracedPhaseBitManipulation()
            >>> p = 0x0
            >>> p = tbm.set(p, SinglePhaseKind.A, SinglePhaseKind.A)
            >>> tbm.get(p, SinglePhaseKind.A)
            <SinglePhaseKind.A: (1, 0)>

        :param status: 16-bit integer used to store the current phase data
        :param nominal_phase:  the nominal phase to return from the `PhaseCode`
        :param single_phase_kind: the kind of phase to set it too
        """
        if single_phase_kind == SinglePhaseKind.NONE:
            return status & ~_nominal_phase_masks[nominal_phase.mask_index]
        else:
            return status & ~_nominal_phase_masks[nominal_phase.mask_index] | single_phase_kind.shifted_value(nominal_phase)

