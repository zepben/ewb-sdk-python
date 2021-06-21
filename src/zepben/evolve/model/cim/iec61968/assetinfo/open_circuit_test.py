#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Optional

from zepben.evolve import TransformerTest

__all__ = ["OpenCircuitTest"]


class OpenCircuitTest(TransformerTest):
    """
    Open-circuit test results verify winding turn ratios and phase shifts. They include induced voltage and phase shift measurements on open-circuit windings,
    with voltage applied to the energised end. For three-phase windings, the excitation can be a positive sequence (the default) or a zero sequence.
    """

    energised_end_step: Optional[int] = None
    """
    Tap step number for the energised end of the test pair.
    """

    energised_end_voltage: Optional[int] = None
    """
    Voltage applied to the winding (end) during test in volts.
    """

    open_end_step: Optional[int] = None
    """
    Tap step number for the open end of the test pair.
    """

    open_end_voltage: Optional[int] = None
    """
    Voltage measured at the open-circuited end, with the energised end set to rated voltage and all other ends open in volts.
    """

    phase_shift: Optional[float] = None
    """
    Phase shift measured at the open end with the energised end set to rated voltage and all other ends open in angle degrees.
    """
