#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["Accumulator"]

from zepben.ewb.model.cim.iec61970.base.meas.measurement import Measurement


class Accumulator(Measurement):
    """Accumulator represents an accumulated (counted) Measurement, e.g. an energy value."""
    pass
