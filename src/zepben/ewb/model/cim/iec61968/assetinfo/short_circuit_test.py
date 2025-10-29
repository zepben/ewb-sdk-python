#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["ShortCircuitTest"]

from typing import Optional

from zepben.ewb.dataslot import custom_len, MRIDListRouter, MRIDDictRouter, boilermaker, TypeRestrictedDescriptor, WeakrefDescriptor, dataslot, BackedDescriptor, ListAccessor, ValidatedDescriptor, MRIDListAccessor, custom_get, custom_remove, override_boilerplate, ListActions, MRIDDictAccessor, BackingValue, custom_clear, custom_get_by_mrid, custom_add, NoResetDescriptor, ListRouter, validate
from typing_extensions import deprecated
from zepben.ewb.model.cim.iec61968.assetinfo.transformer_test import TransformerTest


@dataslot
class ShortCircuitTest(TransformerTest):
    """
    Short-circuit test results determine mesh impedance parameters. They include load losses and leakage impedances. For three-phase windings, the excitation
    can be a positive sequence (the default) or a zero sequence. There shall be at least one grounded winding.
    """

    current: float | None = None
    """
    Short circuit current in amps.
    """

    energised_end_step: int | None = None
    """
    Tap step number for the energised end of the test pair.
    """

    grounded_end_step: int | None = None
    """
    Tap step number for the grounded end of the test pair.
    """

    leakage_impedance: float | None = None
    """
    Leakage impedance measured from a positive-sequence or single-phase short-circuit test in ohms.
    """

    leakage_impedance_zero: float | None = None
    """
    Leakage impedance measured from a zero-sequence short-circuit test in ohms.
    """

    loss: int | None = None
    """
    Load losses from a positive-sequence or single-phase short-circuit test in watts.
    """

    loss_zero: int | None = None
    """
    Load losses from a zero-sequence short-circuit test in watts.
    """

    power: int | None = None
    """
    Short circuit apparent power in VA.
    """

    voltage: float | None = None
    """
    Short circuit voltage as a percentage.
    """

    voltage_ohmic_part: float | None = None
    """
    Short Circuit Voltage – Ohmic Part as a percentage.
    """
