#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["PerLengthLineParameter"]

from abc import ABCMeta

from zepben.ewb.dataclass_descriptors import zb_dataclass
from zepben.ewb.model.cim.iec61970.base.core.identified_object import IdentifiedObject


@zb_dataclass
class PerLengthLineParameter(IdentifiedObject, metaclass=ABCMeta):
    """Common type for per-length electrical catalogues describing line parameters."""
    pass
