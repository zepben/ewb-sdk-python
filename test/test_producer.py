#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from datetime import datetime
from unittest.mock import MagicMock

import pytest
from google.protobuf.timestamp_pb2 import Timestamp
from zepben.protobuf.mp.mp_pb2_grpc import MeasurementProducerStub
from zepben.protobuf.mp.mp_requests_pb2 import CreateAnalogValueRequest
from zepben.protobuf.cim.iec61970.base.meas.AnalogValue_pb2 import AnalogValue as PBAnalogValue

from zepben.evolve import CableInfo, NetworkService, MeasurementService, AnalogValue
from zepben.evolve.streaming.put.producer import NetworkProducerClient, ProducerClient, SyncNetworkProducerClient, SyncMeasurementProducerClient
from zepben.protobuf.np.np_pb2_grpc import NetworkProducerStub


class TestProducer(object):

    def test_send(self):
        stub: NetworkProducerStub = MagicMock(["CreateNetwork", "CompleteNetwork", "CreateCableInfo"])
        producer_client: SyncNetworkProducerClient = SyncNetworkProducerClient(stub=stub)
        service: NetworkService = NetworkService()

        cable_info = CableInfo("id1")
        service.add(cable_info)
        producer_client.send(service)
        stub.CreateNetwork.assert_called_once()
        stub.CreateCableInfo.assert_called_once()
        stub.CompleteNetwork.assert_called_once()

    @pytest.mark.asyncio
    async def test_send_all_services(self):
        pass
        # network_stub = MagicMock(["CreateNetwork", "CompleteNetwork", "CreateCableInfo"])
        # diagram_stub = MagicMock(["CreateDiagramService", "CompleteDiagramService", "CreateDiagram"])
        # customer_stub = MagicMock(["CreateCustomerService", "CompleteCustomerService", "CreateCustomer"])
        #
        # producer_client = ProducerClient(stub=stub)
        # service: NetworkService = NetworkService()

    def test_send_measurement(self):
        stub: MeasurementProducerStub = MagicMock(["CreateAnalogValue"])
        producer_client = SyncMeasurementProducerClient(stub=stub)
        service = MeasurementService()

        av = AnalogValue(time_stamp=datetime.utcnow(), value=1.0, analog_mrid="test_analog")
        service.add(av)
        producer_client.send(service)
        stub.CreateAnalogValue.assert_called_once()
        t = Timestamp()
        t.FromDatetime(av.time_stamp)
        request = CreateAnalogValueRequest(analogValue=av.to_pb())
        stub.CreateAnalogValue.assert_called_with(request)
