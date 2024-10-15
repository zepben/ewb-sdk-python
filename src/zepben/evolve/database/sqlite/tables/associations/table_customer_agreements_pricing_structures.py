#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List, Generator

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.sqlite_table import SqliteTable


__all__ = ["TableCustomerAgreementsPricingStructures"]


class TableCustomerAgreementsPricingStructures(SqliteTable):
    """
    A class representing the association between CustomerAgreements and PricingStructures.
    """

    def __init__(self):
        super().__init__()
        self.customer_agreement_mrid: Column = self._create_column("customer_agreement_mrid", "TEXT", Nullable.NOT_NULL)
        """A column storing the mRID of CustomerAgreements."""

        self.pricing_structure_mrid: Column = self._create_column("pricing_structure_mrid", "TEXT", Nullable.NOT_NULL)
        """A column storing the mRID of PricingStructures."""

    @property
    def name(self) -> str:
        return "customer_agreements_pricing_structures"

    @property
    def unique_index_columns(self) -> Generator[List[Column], None, None]:
        yield from super().unique_index_columns
        yield [self.customer_agreement_mrid, self.pricing_structure_mrid]

    @property
    def non_unique_index_columns(self) -> Generator[List[Column], None, None]:
        yield from super().non_unique_index_columns
        yield [self.customer_agreement_mrid]
        yield [self.pricing_structure_mrid]
