#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["NoLoadTest"]

from typing import Optional

from zepben.ewb.dataslot import custom_len, MRIDListRouter, MRIDDictRouter, boilermaker, TypeRestrictedDescriptor, WeakrefDescriptor, dataslot, BackedDescriptor, ListAccessor, ValidatedDescriptor, MRIDListAccessor, custom_get, custom_remove, override_boilerplate, ListActions, MRIDDictAccessor, BackingValue, custom_clear, custom_get_by_mrid, custom_add, NoResetDescriptor, ListRouter, validate
from typing_extensions import deprecated
from zepben.ewb.model.cim.iec61968.assetinfo.transformer_test import TransformerTest


@dataslot
class NoLoadTest(TransformerTest):
    """
    No-load test results determine core admittance parameters. They include exciting current and core loss measurements from applying voltage to one
    winding. The excitation may be positive sequence or zero sequence. The test may be repeated at different voltages to measure saturation.
    """

    energised_end_voltage: int | None = None
    """
    Voltage applied to the winding (end) during test in volts.
    """

    exciting_current: float | None = None
    """
    Exciting current measured from a positive-sequence or single-phase excitation test as a percentage.
    """

    exciting_current_zero: float | None = None
    """
    Exciting current measured from a zero-sequence open-circuit excitation test as a percentage.
    """

    loss: int | None = None
    """
    Losses measured from a positive-sequence or single-phase excitation test in watts.
    """

    loss_zero: int | None = None
    """
    Losses measured from a zero-sequence excitation test in watts.
    """
