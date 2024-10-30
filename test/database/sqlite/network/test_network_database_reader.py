#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from sqlite3 import Connection
from unittest.mock import Mock, create_autospec, call

import pytest

from capture_mock_sequence import CaptureMockSequence
from zepben.evolve import NetworkDatabaseReader, NetworkService, MetadataCollectionReader, NetworkServiceReader, TableVersion, SetDirection, SetPhases, \
    PhaseInferrer, AssignToFeeders, AssignToLvFeeders, Equipment, Feeder, EnergySource


class TestNetworkDatabaseReader:

    def setup_method(self):
        self.database_file = "database_file"
        self.service = create_autospec(NetworkService)

        self.metadata_reader = create_autospec(MetadataCollectionReader)
        self.service_reader = create_autospec(NetworkServiceReader)
        self.cursor = Mock()
        self.connection = create_autospec(Connection)
        self.table_version = create_autospec(TableVersion)

        self.set_direction = create_autospec(SetDirection)
        self.set_phases = create_autospec(SetPhases)
        self.phase_inferrer = create_autospec(PhaseInferrer)
        self.assign_to_feeders = create_autospec(AssignToFeeders)
        self.assign_to_lv_feeders = create_autospec(AssignToLvFeeders)

        # NOTE: Setting SUPPORTED_VERSION via `.return_value` here means it is not read correctly by the class and the underlying mock is used for
        #       comparison, so set the value directly instead. This has the side effect that it won't be tracked by the mock manager.
        self.metadata_reader.load.return_value = True
        self.service_reader.load.return_value = True
        self.connection.cursor.return_value = self.cursor
        self.table_version.get_version.return_value = 1
        self.table_version.SUPPORTED_VERSION = 1

        self.reader = NetworkDatabaseReader(
            self.connection,
            self.service,
            self.database_file,
            Mock(),  # tables should not be used if we provide the rest of the parameters, so provide a mockk that will throw if used.
            self.metadata_reader,
            self.service_reader,
            self.table_version,
            self.set_direction,
            self.set_phases,
            self.phase_inferrer,
            self.assign_to_feeders,
            self.assign_to_lv_feeders
        )

        # Add the mocks to the mock manager, so we can verify the calls in order across the mocks.
        self.mock_sequence = CaptureMockSequence(
            service=self.service,
            metadata_reader=self.metadata_reader,
            service_reader=self.service_reader,
            cursor=self.cursor,
            connection=self.connection,
            table_version=self.table_version,
            set_direction=self.set_direction,
            set_phases=self.set_phases,
            phase_inferrer=self.phase_inferrer,
            assign_to_feeders=self.assign_to_feeders,
            assign_to_lv_feeders=self.assign_to_lv_feeders,
        )

    @pytest.fixture(autouse=True)
    def inject_fixtures(self, caplog):
        self.caplog = caplog

    #
    # NOTE: We don't do an exhaustive test of reading objects as this is done via the schema test.
    #

    async def test_calls_expected_processors_including_post_processes(self):
        assert await self.reader.load(), "Should have loaded"

        assert "Applying feeder direction to network..." in self.caplog.text, "Should contain log message."
        assert "Feeder direction applied to network." in self.caplog.text, "Should contain log message."

        assert "Applying phases to network..." in self.caplog.text, "Should contain log message."
        assert "Phasing applied to network." in self.caplog.text, "Should contain log message."

        assert "Assigning equipment to feeders..." in self.caplog.text, "Should contain log message."
        assert "Equipment assigned to feeders." in self.caplog.text, "Should contain log message."

        assert "Assigning equipment to LV feeders..." in self.caplog.text, "Should contain log message."
        assert "Equipment assigned to LV feeders." in self.caplog.text, "Should contain log message."

        assert "Validating that each equipment is assigned to a container..." in self.caplog.text, "Should contain log message."
        assert "Equipment containers validated." in self.caplog.text, "Should contain log message."

        assert "Validating primary sources vs feeders..." in self.caplog.text, "Should contain log message."
        assert "Sources vs feeders validated." in self.caplog.text, "Should contain log message."

        expected_calls = [
            # NOTE: The call to table_version.SUPPORTED_VERSION is not tracked because of how we register the return value.
            # call.table_version.SUPPORTED_VERSION,
            call.connection.cursor(),
            call.table_version.get_version(self.cursor),
            call.cursor.close(),

            call.metadata_reader.load(),
            call.service_reader.load(),

            call.service.unresolved_references(),
            call.service.unresolved_references().__iter__,

            call.set_direction.run(self.service),
            call.set_phases.run(self.service),
            call.phase_inferrer.run(self.service),
            call.assign_to_feeders.run(self.service),
            call.assign_to_lv_feeders.run(self.service),

            # calls for _validate_equipment_containers()
            call.service.objects(Equipment),
            call.service.objects().__iter__(),

            # calls for _validate_sources()
            call.service.objects(Feeder),
            call.service.objects().__iter__(),
            call.service.objects(EnergySource),
            call.service.objects().__iter__(),
        ]

        self.mock_sequence.verify_sequence(expected_calls)
