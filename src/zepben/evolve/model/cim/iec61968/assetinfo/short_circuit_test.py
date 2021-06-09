#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve import TransformerTest

__all__ = ["ShortCircuitTest"]


class ShortCircuitTest(TransformerTest):
    """
    Short-circuit test results determine mesh impedance parameters. They include load losses and leakage impedances. For three-phase windings, the excitation
    can be a positive sequence (the default) or a zero sequence. There shall be at least one grounded winding.
    """

    current: float = 0.0
    """
    Short circuit current in amps.
    """

    energised_end_step: int = 0
    """
    Tap step number for the energised end of the test pair.
    """

    grounded_end_step: int = 0
    """
    Tap step number for the grounded end of the test pair.
    """

    leakage_impedance: float = 0.0
    """
    Leakage impedance measured from a positive-sequence or single-phase short-circuit test in ohms.
    """

    leakage_impedance_zero: float = 0.0
    """
    Leakage impedance measured from a zero-sequence short-circuit test in ohms.
    """

    loss: int = 0
    """
    Load losses from a positive-sequence or single-phase short-circuit test in watts.
    """

    loss_zero: int = 0
    """
    Load losses from a zero-sequence short-circuit test in watts.
    """

    power: int = 0
    """
    Short circuit apparent power in VA.
    """

    voltage: float = 0.0
    """
    Short circuit voltage as a percentage.
    """

    voltage_ohmic_part: float = 0.0
    """
    Short Circuit Voltage – Ohmic Part as a percentage.
    """
