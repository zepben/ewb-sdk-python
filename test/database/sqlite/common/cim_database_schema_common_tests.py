#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import contextlib
import os
import sqlite3
import tempfile
from abc import ABC, abstractmethod
from collections import Counter
from sqlite3 import Connection
from typing import TypeVar, Optional, Callable, Generic

import pytest

from database.sqlite.schema_utils import SchemaNetworks, assume_non_blank_street_address_details
from zepben.ewb import MetadataCollection, IdentifiedObject, Location, BaseService, BaseServiceComparator
from zepben.ewb.database.sqlite.common.base_database_reader import BaseDatabaseReader
from zepben.ewb.database.sqlite.common.base_database_writer import BaseDatabaseWriter
from zepben.ewb.database.sqlite.tables.table_version import TableVersion

TService = TypeVar("TService", bound=BaseService)
TWriter = TypeVar("TWriter", bound=BaseDatabaseWriter)
TReader = TypeVar("TReader", bound=BaseDatabaseReader)
TComparator = TypeVar("TComparator", bound=BaseServiceComparator)


# class CimDatabaseSchemaTestCases:
class CimDatabaseSchemaCommonTests(Generic[TService, TWriter, TReader, TComparator], ABC):
    """
    A collection of base tests and validations to be used for testing the schema of a cim service database.

    NOTE: This is deliberately named to avoid being detected by pytest. The contained tests should be included by creating child classes.
    """

    @abstractmethod
    def create_service(self) -> TService:
        pass

    @abstractmethod
    def create_writer(self, filename: str, service: TService) -> TWriter:
        pass

    @abstractmethod
    def create_reader(self, connection: Connection, service: TService, database_description: str) -> TReader:
        pass

    @abstractmethod
    def create_comparator(self) -> TComparator:
        pass

    @abstractmethod
    def create_identified_object(self) -> IdentifiedObject:
        pass

    @pytest.fixture(autouse=True)
    def inject_fixtures(self, caplog):
        # noinspection PyAttributeOutsideInit
        self.caplog = caplog

    @pytest.mark.asyncio
    async def test_metadata_data_source_schema(self):
        service = self.create_service()
        for data_source in SchemaNetworks().create_data_source_test_services().data_sources:
            service.metadata.add(data_source)

        await self._validate_schema(service)

    @pytest.mark.asyncio
    async def test_check_for_error_on_duplicate_id(self):
        write_service = self.create_service()
        read_service = self.create_service()

        # We add a copy of the junction to the read services to create an mRID conflict.
        identified_object = self.create_identified_object()
        write_service.add(identified_object)
        read_service.add(identified_object)

        await self._validate_write_read(write_service, read_service=read_service)

        assert f"Failed to load {identified_object}. Unable to add to service '{read_service.name}': duplicate MRID" in self.caplog.text

    async def _validate_schema(self, expected_service: TService):
        #
        # NOTE: We need to stop hypothesis from generating empty location addresses as the database load will throw these away, removing the test of
        #       those tables/fields.
        #
        for location in expected_service.objects(Location):
            assume_non_blank_street_address_details(location.main_address)

        def validate(service: TService):
            self._validate_metadata(service.metadata, expected_service.metadata)
            self._validate_service(service, expected_service, self.create_comparator())

        await self._validate_write_read(expected_service, validate_read=validate)

    async def _validate_write_read(
        self,
        write_service: Optional[TService] = None,
        read_service: Optional[TService] = None,
        validate_read: Optional[Callable[[TService], None]] = None,
    ):
        write_service = write_service or self.create_service()
        read_service = read_service or self.create_service()

        with tempfile.NamedTemporaryFile() as schema_test_file_temp:
            schema_test_file = schema_test_file_temp.name
            assert self.create_writer(schema_test_file, write_service).save(), "Database should have been saved"

            assert f"Creating database schema v{TableVersion.SUPPORTED_VERSION}" in self.caplog.text
            assert os.path.isfile(schema_test_file), "Database should now exist"

            self.caplog.clear()
            with contextlib.closing(sqlite3.connect(schema_test_file)) as connection:
                status = await self.create_reader(connection, read_service, schema_test_file).load()

            if validate_read:
                assert status, "Database read should have succeeded"
                validate_read(read_service)
            else:
                assert not status, "Database read should have failed"

    async def _validate_unresolved_failure(self, expected_source: str, expected_target: str, add_deferred_reference: Callable[[TService], None]):
        service = self.create_service()
        # Add an unresolved reference that should trigger the post load check.
        add_deferred_reference(service)

        await self._validate_write_read(read_service=service)

        assert (f"Unresolved references found in {service.name} service after load - this should not occur. "
                f"Failing reference was from {expected_source} resolving {expected_target}") in self.caplog.text, "Expected exception message to match"

    @staticmethod
    def _validate_metadata(metadata: MetadataCollection, expected_metadata_collection: MetadataCollection):
        assert Counter(metadata.data_sources) == Counter(expected_metadata_collection.data_sources)

    @staticmethod
    def _validate_service(service: BaseService, expected_service: BaseService, service_comparator: BaseServiceComparator):
        differences = service_comparator.compare_services(service, expected_service)

        if list(differences.modifications()):
            print(str(differences))

        assert not list(differences.missing_from_target()), "unexpected objects found in loaded service"
        if differences.modifications():
            print(sorted(list(service.objects()), key=lambda o: str(type(o))))
            print(sorted(list(expected_service.objects()), key=lambda o: str(type(o))))
        assert not list(differences.modifications()), ("unexpected modifications", service, expected_service)
        assert not list(differences.missing_from_source()), "objects missing from loaded service"
