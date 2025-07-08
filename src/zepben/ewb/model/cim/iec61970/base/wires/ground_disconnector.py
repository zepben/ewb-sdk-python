#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["GroundDisconnector"]

from zepben.ewb.model.cim.iec61970.base.wires.switch import Switch


class GroundDisconnector(Switch):
    """
    A manually operated or motor operated mechanical switching device used for isolating a circuit or equipment from ground.
    """
    pass
