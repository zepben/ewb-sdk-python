#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["RemotePoint"]

from zepben.ewb.model.cim.iec61970.base.core.identified_object import IdentifiedObject


class RemotePoint(IdentifiedObject):
    """
    For a RTU remote points correspond to telemetered values or control outputs. Other units (e.g. control centers)
    usually also contain calculated values.
    """
    pass
