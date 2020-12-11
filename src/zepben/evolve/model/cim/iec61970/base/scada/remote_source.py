#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import Optional

from zepben.evolve.model.cim.iec61970.base.meas.measurement import Measurement
from zepben.evolve.model.cim.iec61970.base.scada.remote_point import RemotePoint

__all__ = ["RemoteSource"]


class RemoteSource(RemotePoint):
    """
    Remote sources are state variables that are telemetered or calculated within the remote unit.
    """

    measurement: Optional[Measurement] = None
    """The `meas.measurement.Measurement` for the `RemoteSource` point."""
