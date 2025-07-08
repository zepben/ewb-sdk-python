#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["BaseVoltage"]

from zepben.ewb.model.cim.iec61970.base.core.identified_object import IdentifiedObject


class BaseVoltage(IdentifiedObject):
    """
    Defines a system base voltage which is referenced.
    """

    nominal_voltage: int = 0
    """The power system resource's base voltage."""
