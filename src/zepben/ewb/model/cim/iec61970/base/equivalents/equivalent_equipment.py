#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["EquivalentEquipment"]

from zepben.ewb.collections.autoslot import autoslot_dataclass
from zepben.ewb.model.cim.iec61970.base.core.conducting_equipment import ConductingEquipment


@autoslot_dataclass
class EquivalentEquipment(ConductingEquipment):
    """
    The class represents equivalent objects that are the result of a network reduction. The class is the base for equivalent objects of different types.
    """
    pass
