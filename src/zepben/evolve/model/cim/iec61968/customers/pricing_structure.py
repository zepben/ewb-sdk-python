

#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from typing import Optional, Generator, List, TYPE_CHECKING

if TYPE_CHECKING:
    from zepben.evolve import Tariff

from zepben.evolve.model.cim.iec61968.common.document import Document
from zepben.evolve.util import get_by_mrid, nlen, ngen, safe_remove

__all__ = ["PricingStructure"]


class PricingStructure(Document):
    """
    Grouping of pricing components and prices used in the creation of customer charges and the eligibility
    criteria under which these terms may be offered to a customer. The reasons for grouping include state,
    customer classification, site characteristics, classification (i.e. fee price structure, deposit price
    structure, electric service price structure, etc.) and accounting requirements.
    """
    _tariffs: Optional[List[Tariff]] = None

    def __init__(self, tariffs: List[Tariff] = None, **kwargs):
        super(PricingStructure, self).__init__(**kwargs)
        if tariffs:
            for tariff in tariffs:
                self.add_tariff(tariff)

    def num_tariffs(self):
        """
        Returns The number of `Tariff`s associated with this `PricingStructure`
        """
        return nlen(self._tariffs)

    @property
    def tariffs(self) -> Generator[Tariff, None, None]:
        """
        The `Tariff`s of this `PricingStructure`.
        """
        return ngen(self._tariffs)

    def get_tariff(self, mrid: str) -> Tariff:
        """
        Get the `Tariff` for this `PricingStructure` identified by `mrid`

        `mrid` the mRID of the required `Tariff`
        Returns The `Tariff` with the specified `mrid` if it exists
        Raises `KeyError` if `mrid` wasn't present.
        """
        return get_by_mrid(self._tariffs, mrid)

    def add_tariff(self, tariff: Tariff) -> PricingStructure:
        """
        Associate a `Tariff` with this `PricingStructure`.

        `tariff` the `Tariff` to associate with this `PricingStructure`.
        Returns A reference to this `PricingStructure` to allow fluent use.
        Raises `ValueError` if another `Tariff` with the same `mrid` already exists for this `PricingStructure`.
        """
        if self._validate_reference(tariff, self.get_tariff, "A Tariff"):
            return self
        self._tariffs = list() if self._tariffs is None else self._tariffs
        self._tariffs.append(tariff)
        return self

    def remove_tariff(self, tariff: Tariff) -> PricingStructure:
        """
        Disassociate `tariff` from this `PricingStructure`.

        `tariff` the `Tariff` to disassociate from this `PricingStructure`.
        Returns A reference to this `PricingStructure` to allow fluent use.
        Raises `ValueError` if `tariff` was not associated with this `PricingStructure`.
        """
        self._tariffs = safe_remove(self._tariffs, tariff)
        return self

    def clear_tariffs(self) -> PricingStructure:
        """
        Clear all tariffs.
        Returns A reference to this `PricingStructure` to allow fluent use.
        """
        self._tariffs = None
        return self
