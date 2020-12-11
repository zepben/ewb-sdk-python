#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve.model.cim.iec61970.base.core.identified_object import IdentifiedObject

__all__ = ["IoPoint"]


class IoPoint(IdentifiedObject):
    """
    This class describes a measurement or control value.
    The purpose is to enable having attributes and associations common for measurement and control.
    """
    pass
