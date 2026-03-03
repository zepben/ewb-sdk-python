#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["TracedPhasesBitManipulation"]

from zepben.ewb.model.cim.iec61970.base.wires.single_phase_kind import SinglePhaseKind


_nominal_phase_masks = [0x000F, 0x00F0, 0x0F00, 0xF000]
"""Bitwise mask for selecting the actual phases from a nominal phase A/B/C/N, X/Y/N or s1/s2/N"""

_phase_masks = [1, 2, 4, 8]
"""Bitwise mask for setting the presence of an actual phase"""


class TracedPhasesBitManipulation:
    """
    Class that performs the bit manipulation for the traced phase statuses.
    Each byte in an int is used to store all possible phases and directions for a nominal phase.
    Each byte has 2 bits that represent the direction for a phase. If none of those bits are set the direction is equal to NONE.
    Use the figures below as a reference.

    ::

        Network state phase status:
                       |              16 bits              |
                       | 4 bits | 4 bits | 4 bits | 4 bits |
        Nominal phase: |   N    |    C   | B/Y/s2 | A/X/s1 |

    ::

        Each nominal phase (actual phase):
                      |                 4 bits                |
                      |  1 bit  |  1 bit  |  1 bit  |  1 bit  |
        Actual Phase: |    N    |    C    |    B    |    A    |
    """

    @staticmethod
    def get(status: int, nominal_phase: SinglePhaseKind) -> SinglePhaseKind:
        match ((status >> nominal_phase.byte_selector()) & 15):
            case 1: return SinglePhaseKind.A
            case 2: return SinglePhaseKind.B
            case 4: return SinglePhaseKind.C
            case 8: return SinglePhaseKind.N
            case _: return SinglePhaseKind.NONE

    @staticmethod
    def set(status: int, nominal_phase: SinglePhaseKind, single_phase_kind: SinglePhaseKind) -> int:
        if single_phase_kind == SinglePhaseKind.NONE:
            return status & (~_nominal_phase_masks[nominal_phase.mask_index])
        else:
            return (status & (~_nominal_phase_masks[nominal_phase.mask_index])) | single_phase_kind.shifted_value(nominal_phase)


SinglePhaseKind.byte_selector = lambda self: self.mask_index * 4
SinglePhaseKind.shifted_value = lambda self, nominal_phase: _phase_masks[self.mask_index] << nominal_phase.byte_selector()
