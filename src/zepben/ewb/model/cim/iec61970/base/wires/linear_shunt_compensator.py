#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["LinearShuntCompensator"]

from typing import Optional

from zepben.ewb.model.cim.iec61970.base.wires.shunt_compensator import ShuntCompensator


class LinearShuntCompensator(ShuntCompensator):
    """A linear shunt compensator has banks or sections with equal admittance values."""

    b0_per_section: Optional[float] = None
    """Zero sequence shunt (charging) susceptance per section"""

    b_per_section: Optional[float] = None
    """Positive sequence shunt (charging) susceptance per section"""

    g0_per_section: Optional[float] = None
    """Zero sequence shunt (charging) conductance per section"""

    g_per_section: Optional[float] = None
    """Positive sequence shunt (charging) conductance per section"""
