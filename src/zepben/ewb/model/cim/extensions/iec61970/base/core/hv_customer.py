#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ['HvCustomer']

from zepben.ewb.model.cim.iec61970.base.core.equipment_container import EquipmentContainer
from zepben.ewb.model.cim.extensions.zbex import zbex


@zbex
class HvCustomer(EquipmentContainer):
    """
    [ZBEX] A collection of equipment for organizational purposes, used for grouping distribution resources located at a HV customer site.
    """