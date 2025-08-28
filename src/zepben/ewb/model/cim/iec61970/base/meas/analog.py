#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["Analog"]

from typing import Optional

from zepben.ewb.model.cim.iec61970.base.meas.measurement import Measurement


class Analog(Measurement):
    """Analog represents an analog Measurement."""

    positive_flow_in: Optional[bool] = None
    """If true then this measurement is an active power, reactive power or current with the convention that a positive value measured at the 
    Terminal means power is flowing into the related PowerSystemResource."""
