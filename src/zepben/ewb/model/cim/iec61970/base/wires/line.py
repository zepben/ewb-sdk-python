#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["Line"]

from zepben.ewb.model.cim.iec61970.base.core.equipment_container import EquipmentContainer


class Line(EquipmentContainer):
    """Contains equipment beyond a substation belonging to a power transmission line."""
    pass
