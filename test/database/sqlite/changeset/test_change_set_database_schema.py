#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from sqlite3 import Connection

from database.sqlite.common.cim_database_schema_common_tests import (CimDatabaseSchemaCommonTests, TComparator, TReader,
                                                                    TService, TWriter)
from zepben.ewb import Identifiable
from zepben.ewb.database.sqlite.changeset.change_set_database_reader import ChangeSetDatabaseReader
from zepben.ewb.database.sqlite.changeset.change_set_database_writer import ChangeSetDatabaseWriter
from zepben.ewb.model.cim.iec61970.infiec61970.part303.genericdataset.change_set import ChangeSet
from zepben.ewb.services.variant.variant_service import VariantService
from zepben.ewb.services.variant.variant_service_comparator import VariantServiceComparator


class TestChangeSetDatabaseSchema(CimDatabaseSchemaCommonTests[VariantService, ChangeSetDatabaseWriter, ChangeSetDatabaseReader,
                                                              VariantServiceComparator]):

    def create_service(self) -> TService:
        return VariantService()

    def create_writer(self, filename: str, service: TService) -> TWriter:
        return ChangeSetDatabaseWriter(filename, service)

    def create_reader(self, connection: Connection, service: TService, database_description: str) -> TReader:
        return ChangeSetDatabaseReader(connection, service, database_description)

    def create_comparator(self) -> TComparator:
        return VariantServiceComparator()

    def create_identifiable(self) -> Identifiable:
        return ChangeSet(mrid="test")
