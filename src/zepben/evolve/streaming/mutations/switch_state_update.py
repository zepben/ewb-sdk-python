#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from datetime import datetime
from dataclassy import dataclass


@dataclass()
class SwitchStateUpdate:
    """
    Class to hold details for setting a new switch state.
    """

    mrid: str
    """The MRID of the switch to be updated."""

    set_open: bool
    """True if the switch should be opened, false if it should be closed."""

    timestamp: datetime = datetime.now()
    """The time recorded of the actual switch state change occurring. Defaults to now if not provided."""



