#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve import TransformerTest

__all__ = ["NoLoadTest"]


class NoLoadTest(TransformerTest):
    """
    No-load test results determine core admittance parameters. They include exciting current and core loss measurements from applying voltage to one
    winding. The excitation may be positive sequence or zero sequence. The test may be repeated at different voltages to measure saturation.
    """

    energised_end_voltage: int = 0
    """
    Voltage applied to the winding (end) during test in volts.
    """

    exciting_current: float = 0.0
    """
    Exciting current measured from a positive-sequence or single-phase excitation test as a percentage.
    """

    exciting_current_zero: float = 0.0
    """
    Exciting current measured from a zero-sequence open-circuit excitation test as a percentage.
    """

    loss: int = 0
    """
    Losses measured from a positive-sequence or single-phase excitation test in watts.
    """

    loss_zero: int = 0
    """
    Losses measured from a zero-sequence excitation test in watts.
    """
