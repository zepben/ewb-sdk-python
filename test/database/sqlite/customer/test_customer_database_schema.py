#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from sqlite3 import Connection
from typing import TypeVar

from hypothesis import given, settings, HealthCheck

from cim.cim_creators import create_organisation, create_customer, create_customer_agreement, create_pricing_structure, create_tariffs
from database.sqlite.common.cim_database_schema_common_tests import CimDatabaseSchemaCommonTests, TComparator, TService, TReader, TWriter
from database.sqlite.schema_utils import SchemaNetworks
from zepben.evolve import IdentifiedObject, CustomerAgreement, PricingStructure, Tariff, Organisation, Customer, CustomerDatabaseReader, \
    CustomerDatabaseWriter, CustomerService
from zepben.evolve.services.customer.customer_service_comparator import CustomerServiceComparator

T = TypeVar("T", bound=IdentifiedObject)


# pylint: disable=too-many-public-methods
class TestCustomerDatabaseSchema(CimDatabaseSchemaCommonTests[CustomerService, CustomerDatabaseWriter, CustomerDatabaseReader, CustomerServiceComparator]):

    def create_service(self) -> TService:
        return CustomerService()

    def create_writer(self, filename: str, service: TService) -> TWriter:
        return CustomerDatabaseWriter(filename, service)

    def create_reader(self, connection: Connection, service: TService, database_description: str) -> TReader:
        return CustomerDatabaseReader(connection, service, database_description)

    def create_comparator(self) -> TComparator:
        return CustomerServiceComparator()

    def create_identified_object(self) -> IdentifiedObject:
        return Customer()

    ######################
    # IEC61968 CUSTOMERS #
    ######################

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(customer=create_customer(False))
    async def test_schema_customer(self, customer):
        await self._validate_schema(SchemaNetworks().customer_services_of(Customer, customer))

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(customer_agreement=create_customer_agreement(False))
    async def test_schema_customer_agreement(self, customer_agreement):
        await self._validate_schema(SchemaNetworks().customer_services_of(CustomerAgreement, customer_agreement))

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(pricing_structure=create_pricing_structure(False))
    async def test_schema_pricing_structure(self, pricing_structure):
        await self._validate_schema(SchemaNetworks().customer_services_of(PricingStructure, pricing_structure))

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(tariffs=create_tariffs(False))
    async def test_schema_tariffs(self, tariffs):
        await self._validate_schema(SchemaNetworks().customer_services_of(Tariff, tariffs))

    ###################
    # IEC61968 COMMON #
    ###################

    @settings(deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow])
    @given(organisation=create_organisation(False))
    async def test_schema_organisation_customer(self, organisation):
        await self._validate_schema(SchemaNetworks().customer_services_of(Organisation, organisation))
