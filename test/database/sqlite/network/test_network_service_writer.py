#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from unittest.mock import create_autospec, call

from capture_mock_sequence import CaptureMockSequence
from zepben.ewb import NetworkService, NetworkCimWriter, NetworkServiceWriter, NetworkDatabaseTables, Circuit


class TestNetworkServiceWriter:

    #
    # NOTE: We don't do an exhaustive test of saving objects as this is done via the schema test.
    #

    def setup_method(self):
        self.network_service = NetworkService()
        self.cim_writer = create_autospec(NetworkCimWriter)
        self.network_service_writer = NetworkServiceWriter(self.network_service, create_autospec(NetworkDatabaseTables), self.cim_writer)

        self.cim_writer.save_circuit.return_value = True

        self.mock_sequence = CaptureMockSequence(
            cim_writer=self.cim_writer,
        )

    def test_passes_objects_through_to_the_cim_writer(self):
        circuit = Circuit()
        self.network_service.add(circuit)

        # NOTE: the save method will fail due to the relaxed mock returning false for all save operations,
        #       but a save should still be attempted on every object
        self.network_service_writer.save()

        self.mock_sequence.verify_sequence([call.cim_writer.save_circuit(circuit)])
