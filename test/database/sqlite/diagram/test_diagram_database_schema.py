#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from sqlite3 import Connection
from typing import TypeVar

from hypothesis import given, settings, HealthCheck

from cim.cim_creators import create_diagram, create_diagram_object
from database.sqlite.common.cim_database_schema_common_tests import CimDatabaseSchemaCommonTests, TComparator, TService, TReader, TWriter
from database.sqlite.schema_utils import SchemaNetworks
from zepben.evolve import IdentifiedObject, DiagramDatabaseReader, DiagramDatabaseWriter, DiagramService
from zepben.evolve.model.cim.iec61970.base.diagramlayout.diagram import Diagram
from zepben.evolve.model.cim.iec61970.base.diagramlayout.diagram_object import DiagramObject
from zepben.evolve.services.diagram.diagram_service_comparator import DiagramServiceComparator

T = TypeVar("T", bound=IdentifiedObject)


# pylint: disable=too-many-public-methods
class TestDiagramDatabaseSchema(CimDatabaseSchemaCommonTests[DiagramService, DiagramDatabaseWriter, DiagramDatabaseReader, DiagramServiceComparator]):

    def create_service(self) -> TService:
        return DiagramService()

    def create_writer(self, filename: str, service: TService) -> TWriter:
        return DiagramDatabaseWriter(filename, service)

    def create_reader(self, connection: Connection, service: TService, database_description: str) -> TReader:
        return DiagramDatabaseReader(connection, service, database_description)

    def create_comparator(self) -> TComparator:
        return DiagramServiceComparator()

    def create_identified_object(self) -> IdentifiedObject:
        return DiagramObject()

    ################################
    # IEC61970 BASE DIAGRAM LAYOUT #
    ################################

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(diagram=create_diagram(False))
    async def test_schema_diagram(self, diagram):
        await self._validate_schema(SchemaNetworks().diagram_services_of(Diagram, diagram))

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(diagram_object=create_diagram_object(False))
    async def test_schema_diagram_object(self, diagram_object):
        await self._validate_schema(SchemaNetworks().diagram_services_of(DiagramObject, diagram_object))
