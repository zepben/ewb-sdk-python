#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["PricingStructure"]

from typing import Optional, List, TYPE_CHECKING
from dataclasses import field
from typing_extensions import deprecated

from zepben.ewb.model.cim.iec61968.common.document import Document
from zepben.ewb.boilerplate.dataclass_base import zb_dataclass
from zepben.ewb.boilerplate.collections.mrid_list import LazyMridList
from zepben.ewb.boilerplate.collections.mrid_collection import MridCollection

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61968.customers.tariff import Tariff


@zb_dataclass
class PricingStructure(Document):
    """
    Grouping of pricing components and prices used in the creation of customer charges and the eligibility
    criteria under which these terms may be offered to a customer. The reasons for grouping include state,
    customer classification, site characteristics, classification (i.e. fee price structure, deposit price
    structure, electric service price structure, etc.) and accounting requirements.

    :var tariffs: All tariffs used by this pricing structure
    :var code: Unique user-allocated key for this pricing structure, used by company representatives to identify the correct price structure for allocating to a
               customer. For rate schedules it is often prefixed by a state code.
    """
    _tariffs: Optional[List[Tariff]] = field(default=None)

    code: str | None = None

    tariffs: MridCollection[Tariff] = LazyMridList(
        _tariffs,
        "A Tariff",
    )


    # region deprecated list boilerplate
    # region tariffs boilerplate

    @deprecated("Use len(obj.tariffs) instead.")
    def num_tariffs(self):
        return len(self.tariffs)

    @deprecated("Use obj.tariffs.get_by_mrid(mrid) instead.")
    def get_tariff(self, mrid: str) -> Tariff:
        return self.tariffs.get_by_mrid(mrid)

    @deprecated("Use obj.tariffs.append(tariff) instead.")
    def add_tariff(self, tariff: Tariff) -> PricingStructure:
        self.tariffs.append(tariff)
        return self

    @deprecated("Use obj.tariffs.remove(tariff) instead.")
    def remove_tariff(self, tariff: Tariff) -> PricingStructure:
        self.tariffs.remove(tariff)
        return self

    @deprecated("Use obj.tariffs.clear() instead.")
    def clear_tariffs(self) -> PricingStructure:
        self.tariffs.clear()
        return self

    # endregion tariffs boilerplate

    # endregion deprecated list boilerplate
