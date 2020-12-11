#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve.model.cim.iec61970.base.core.identified_object import IdentifiedObject

__all__ = ["RemotePoint"]


class RemotePoint(IdentifiedObject):
    """
    For a RTU remote points correspond to telemetered values or control outputs. Other units (e.g. control centers)
    usually also contain calculated values.
    """
    pass
