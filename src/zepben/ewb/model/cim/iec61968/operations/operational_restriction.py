#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["OperationalRestriction"]

from typing import Optional, Generator, List, TYPE_CHECKING

from zepben.ewb.dataslot import custom_len, MRIDListRouter, MRIDDictRouter, boilermaker, TypeRestrictedDescriptor, WeakrefDescriptor, dataslot, BackedDescriptor, ListAccessor, ValidatedDescriptor, MRIDListAccessor, custom_get, custom_remove, override_boilerplate, ListActions, MRIDDictAccessor, BackingValue, custom_clear, custom_get_by_mrid, custom_add, NoResetDescriptor, ListRouter, validate
from typing_extensions import deprecated
from zepben.ewb.model.cim.iec61968.common.document import Document
from zepben.ewb.util import get_by_mrid, nlen, ngen, safe_remove

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61970.base.core.equipment import Equipment


@dataslot
@boilermaker
class OperationalRestriction(Document):
    """
    A document that can be associated with equipment to describe any sort of restrictions compared with the
    original manufacturer's specification or with the usual operational practice e.g.
    temporary maximum loadings, maximum switching current, do not operate if bus couplers are open, etc.

    In the UK, for example, if a breaker or switch ever mal-operates, this is reported centrally and utilities
    use their asset systems to identify all the installed devices of the same manufacturer's type.
    They then apply operational restrictions in the operational systems to warn operators of potential problems.
    After appropriate inspection and maintenance, the operational restrictions may be removed.
    """
    equipment: List[Equipment] | None = MRIDListAccessor()

    def _retype(self):
        self.equipment: MRIDListRouter = ...
    
    @deprecated("BOILERPLATE: Use len(equipment) instead")
    def num_equipment(self):
        return len(self.equipment)

    @deprecated("BOILERPLATE: Use equipment.get_by_mrid(mrid) instead")
    def get_equipment(self, mrid: str) -> Equipment:
        return self.equipment.get_by_mrid(mrid)

    @deprecated("Boilerplate: Use equipment.append(equipment) instead")
    def add_equipment(self, equipment: Equipment) -> OperationalRestriction:
        self.equipment.append(equipment)
        return self

    @deprecated("Boilerplate: Use equipment.remove(equipment) instead")
    def remove_equipment(self, equipment: Equipment) -> OperationalRestriction:
        self.equipment.remove(equipment)
        return self

    @deprecated("BOILERPLATE: Use equipment.clear() instead")
    def clear_equipment(self) -> OperationalRestriction:
        self.equipment.clear()
        return self

