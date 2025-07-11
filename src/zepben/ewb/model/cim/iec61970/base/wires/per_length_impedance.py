#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["PerLengthImpedance"]

from zepben.ewb.model.cim.iec61970.base.wires.per_length_line_parameter import PerLengthLineParameter


class PerLengthImpedance(PerLengthLineParameter):
    """Common type for per-length impedance electrical catalogues."""
    pass
