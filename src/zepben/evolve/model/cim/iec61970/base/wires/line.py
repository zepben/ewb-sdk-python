#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve.model.cim.iec61970.base.core.equipment_container import EquipmentContainer

__all__ = ["Line"]


class Line(EquipmentContainer):
    """Contains equipment beyond a substation belonging to a power transmission line."""
    pass
