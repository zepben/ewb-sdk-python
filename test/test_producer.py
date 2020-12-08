#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from unittest.mock import MagicMock

import pytest
from zepben.cimbend import CableInfo, NetworkService
from zepben.cimbend.streaming.producer import NetworkProducerClient, ProducerClient
from zepben.protobuf.np.np_pb2_grpc import NetworkProducerStub


class TestProducer(object):

    @pytest.mark.asyncio
    async def test_send(self):
        stub: NetworkProducerStub = MagicMock(["CreateNetwork", "CompleteNetwork", "CreateCableInfo"])
        producer_client: NetworkProducerClient = NetworkProducerClient(stub=stub)
        service: NetworkService = NetworkService()

        cable_info = CableInfo("id1")
        service.add(cable_info)
        await producer_client.send(service)
        stub.CreateNetwork.assert_called_once()
        stub.CreateCableInfo.assert_called_once()
        stub.CompleteNetwork.assert_called_once()


    async def test_send_all_services(self):
        network_stub = MagicMock(["CreateNetwork", "CompleteNetwork", "CreateCableInfo"])
        diagram_stub = MagicMock(["CreateDiagramService", "CompleteDiagramService", "CreateDiagram"])
        customer_stub = MagicMock(["CreateCustomerService", "CompleteCustomerService", "CreateCustomer"])

        producer_client = ProducerClient(stub=stub)
        service: NetworkService = NetworkService()
