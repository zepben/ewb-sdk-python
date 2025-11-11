#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["PricingStructure"]

from typing import Optional, Generator, List, TYPE_CHECKING

from zepben.ewb.dataslot import custom_len, MRIDListRouter, MRIDDictRouter, boilermaker, TypeRestrictedDescriptor, WeakrefDescriptor, dataslot, BackedDescriptor, ListAccessor, ValidatedDescriptor, MRIDListAccessor, custom_get, custom_remove, override_boilerplate, ListActions, MRIDDictAccessor, BackingValue, custom_clear, custom_get_by_mrid, custom_add, NoResetDescriptor, ListRouter, validate
from typing_extensions import deprecated
from zepben.ewb.model.cim.iec61968.common.document import Document
from zepben.ewb.util import get_by_mrid, nlen, ngen, safe_remove

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61968.customers.tariff import Tariff


@dataslot
@boilermaker
class PricingStructure(Document):
    """
    Grouping of pricing components and prices used in the creation of customer charges and the eligibility
    criteria under which these terms may be offered to a customer. The reasons for grouping include state,
    customer classification, site characteristics, classification (i.e. fee price structure, deposit price
    structure, electric service price structure, etc.) and accounting requirements.
    """
    tariffs: List[Tariff] | None = MRIDListAccessor()

    def _retype(self):
        self.tariffs: MRIDListRouter = ...
    
    @deprecated("BOILERPLATE: Use len(tariffs) instead")
    def num_tariffs(self):
        return len(self.tariffs)

    @deprecated("BOILERPLATE: Use tariffs.get_by_mrid(mrid) instead")
    def get_tariff(self, mrid: str) -> Tariff:
        return self.tariffs.get_by_mrid(mrid)

    @deprecated("Boilerplate: Use tariffs.append(tariff) instead")
    def add_tariff(self, tariff: Tariff) -> PricingStructure:
        self.tariffs.append(tariff)
        return self

    @deprecated("Boilerplate: Use tariffs.remove(tariff) instead")
    def remove_tariff(self, tariff: Tariff) -> PricingStructure:
        self.tariffs.remove(tariff)
        return self

    @deprecated("BOILERPLATE: Use tariffs.clear() instead")
    def clear_tariffs(self) -> PricingStructure:
        self.tariffs.clear()
        return self

