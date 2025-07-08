#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["Junction"]

from zepben.ewb.model.cim.iec61970.base.wires.connector import Connector


class Junction(Connector):
    """
    A point where one or more conducting equipments are connected with zero resistance.
    """
    pass
