#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["RemoteSource"]

from typing import Optional, TYPE_CHECKING

from zepben.ewb.model.cim.iec61970.base.scada.remote_point import RemotePoint

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61970.base.meas.measurement import Measurement


class RemoteSource(RemotePoint):
    """
    Remote sources are state variables that are telemetered or calculated within the remote unit.
    """

    measurement: Optional['Measurement'] = None
    """The `meas.measurement.Measurement` for the `RemoteSource` point."""
