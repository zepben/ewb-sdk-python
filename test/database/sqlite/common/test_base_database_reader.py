#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from sqlite3 import Connection
from unittest.mock import Mock, create_autospec, call

import pytest

from capture_mock_sequence import CaptureMockSequence
from zepben.evolve import MissingTableConfigException, MetadataCollectionReader, BaseServiceReader, TableVersion
from zepben.evolve.database.sqlite.common.base_database_reader import BaseDatabaseReader


class TestBaseDatabaseReader:
    database_file = "database_file"

    class SampleReader(BaseDatabaseReader):
        post_load_result = True
        post_load_called = False

        async def _post_load(self) -> bool:
            self.post_load_called = True
            return self.post_load_result

    def setup_method(self):
        self.metadata_reader = create_autospec(MetadataCollectionReader)
        self.metadata_reader.load.return_value = True

        self.service_reader = create_autospec(BaseServiceReader)
        self.service_reader.load.return_value = True

        self.cursor = Mock()
        self.connection = create_autospec(Connection)
        self.connection.cursor.return_value = self.cursor

        # NOTE: Setting SUPPORTED_VERSION via `.return_value` here means it is not read correctly by the class and the underlying mock is used for
        #       comparison, so set the value directly instead. This has the side effect that it won't be tracked by the mock manager.
        self.table_version = create_autospec(TableVersion)
        self.table_version.get_version.return_value = 1
        self.table_version.SUPPORTED_VERSION = 1

        self.reader = TestBaseDatabaseReader.SampleReader(
            self.connection,
            self.metadata_reader,
            self.service_reader,
            Mock(),  # Services won't be used as we have replaced the post_load implementation. The real function is tested by each descendant class.
            self.database_file,
            self.table_version
        )

        # Add the mocks to the mock manager, so we can verify the calls in order across the mocks.
        self.mock_sequence = CaptureMockSequence(
            metadata_reader=self.metadata_reader,
            service_reader=self.service_reader,
            cursor=self.cursor,
            connection=self.connection,
            table_version=self.table_version,
        )

    #
    # NOTE: We need to grab a copy of the pytest `caplog` fixture as we can't inject it directly into our tests as we are using `unittest`. If we
    #       try to inject this directly into our test functions it breaks the `unittest` class such that declared class members go missing.
    #
    @pytest.fixture(autouse=True)
    def inject_fixtures(self, caplog):
        self.caplog = caplog

    async def test_can_load_from_valid_database(self):
        assert await self.reader.load(), "Should have loaded"

        self._verify_readers_called()
        assert self.reader.post_load_called, "post_load should have been called"

    async def test_can_only_run_once(self):
        assert await self.reader.load(), "Should have loaded the first time"
        assert not await self.reader.load(), "Shouldn't have loaded a second time"

        assert "You can only use the database reader once." in self.caplog.text, "Should have had the error message."

    async def test_detect_missing_databases(self):
        self.connection.cursor.side_effect = Exception("Test Error")

        assert not await self.reader.load(), "Should not have loaded"
        assert "Failed to connect to the database for reading: Test Error" in self.caplog.text, "Should have had the error message."

        self.connection.cursor.assert_called_once()

        assert len(self.connection.mock_calls) == 1, "Only the 1 call verified above should have happened."
        assert not self.metadata_reader.mock_calls, "metadata_reader shouldn't have been called"
        assert not self.service_reader.mock_calls, "service_reader shouldn't have been called"
        assert not self.reader.post_load_called, "post_load shouldn't have been called"

    async def test_detect_old_databases(self):
        self.table_version.get_version.return_value = 0

        assert not await self.reader.load(), "Should not have loaded"

        assert (f"Unable to load from database {self.database_file} [found v0, expected v1]. Consider using the UpgradeRunner if you wish to support this "
                f"database.") in self.caplog.text, "Should have had the error message."

        self._verify_readers_called(expect_metadata_read=False)

    async def test_detect_future_databases(self):
        self.table_version.get_version.return_value = 2

        assert not await self.reader.load(), "Should not have loaded"
        assert (f"Unable to load from database {self.database_file} [found v2, expected v1]. You need to use a newer version of the SDK to load this "
                "database.") in self.caplog.text, "Should have had the error message."

        self._verify_readers_called(expect_metadata_read=False)

    async def test_detect_invalid_databases(self):
        self.table_version.get_version.return_value = None

        assert not await self.reader.load(), "Should not have loaded"
        assert "Failed to read the version number form the selected database. Are you sure it is a EWB database?" in self.caplog.text, \
            "Should have had the error message."

        self._verify_readers_called(expect_metadata_read=False)

    async def test_detect_metadata_failure(self):
        self.metadata_reader.load.return_value = False

        assert not await self.reader.load(), "Should not have loaded"

        self._verify_readers_called(expect_service_read=False)
        assert not self.reader.post_load_called, "post_load shouldn't have been called"

    async def test_detect_reader_failure(self):
        self.service_reader.load.return_value = False

        assert not await self.reader.load(), "Should not have loaded"

        self._verify_readers_called(expect_post_load=False)
        assert not self.reader.post_load_called, "post_load shouldn't have been called"

    async def test_detect_post_load_failure(self):
        self.reader.post_load_result = False

        assert not await self.reader.load(), "Should not have loaded"

        self._verify_readers_called()
        assert self.reader.post_load_called, "post_load should have been called"

    async def test_detect_missing_tables(self):
        self.service_reader.load.side_effect = MissingTableConfigException("Test Error")

        assert not await self.reader.load(), "Should not have loaded"

        assert "Unable to load database: Test Error" in self.caplog.text, "Should have had the error message."

    def _verify_readers_called(
        self,
        expect_metadata_read: bool = True,
        expect_service_read: bool = True,
        expect_post_load: bool = True
    ):
        expected_calls = [
            # NOTE: The call to table_version.SUPPORTED_VERSION is not tracked because of how we register the return value.
            # call.table_version.SUPPORTED_VERSION,
            call.connection.cursor(),
            call.table_version.get_version(self.cursor),
            call.cursor.close()
        ]
        if expect_metadata_read:
            expected_calls += [call.metadata_reader.load()]
        if expect_metadata_read and expect_service_read:
            expected_calls += [call.service_reader.load()]

        self.mock_sequence.verify_sequence(expected_calls)
        assert self.reader.post_load_called == (expect_metadata_read and expect_service_read and expect_post_load), \
            f"post_load call mismatch, expected {expect_post_load}."
