#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List

from zepben.evolve.database.sqlite.tables.column import Column, Nullable
from zepben.evolve.database.sqlite.tables.iec61968.common_tables import TableAgreements, TableOrganisationRoles, TableDocuments

__all__ = ["TableCustomerAgreements", "TableCustomers", "TablePricingStructures", "TableTariffs"]


class TableCustomerAgreements(TableAgreements):
    customer_mrid: Column = None

    def __init__(self):
        super(TableCustomerAgreements, self).__init__()
        self.customer_mrid = self._create_column("customer_mrid", "TEXT", Nullable.NULL)

    def name(self) -> str:
        return "customer_agreements"

    def non_unique_index_columns(self) -> List[List[Column]]:
        cols = super(TableCustomerAgreements, self).non_unique_index_columns()
        cols.append([self.customer_mrid])
        return cols


class TableCustomers(TableOrganisationRoles):
    kind: Column = None
    num_end_devices: Column = None

    def __init__(self):
        super(TableCustomers, self).__init__()
        self.kind = self._create_column("kind", "TEXT", Nullable.NOT_NULL)
        self.num_end_devices = self._create_column("num_end_devices", "INTEGER", Nullable.NOT_NULL)

    def name(self) -> str:
        return "customers"


class TablePricingStructures(TableDocuments):

    def name(self) -> str:
        return "pricing_structures"


class TableTariffs(TableDocuments):

    def name(self) -> str:
        return "tariffs"
