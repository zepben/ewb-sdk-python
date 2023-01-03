#  Copyright 2023 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Optional

from zepben.evolve.model.cim.iec61970.base.core.identified_object import IdentifiedObject

__all__ = ["RecloseSequence"]


class RecloseSequence(IdentifiedObject):
    """A reclose sequence (open and close) is defined for each possible reclosure of a breaker."""

    reclose_delay: Optional[float] = None
    """Indicates the time lapse in seconds before the reclose step will execute a reclose."""

    reclose_step: Optional[int] = None
    """Indicates the ordinal position of the reclose step relative to other steps in the sequence."""
