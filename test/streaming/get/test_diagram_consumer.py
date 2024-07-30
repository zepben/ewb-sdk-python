#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import TypeVar
from unittest.mock import MagicMock

import grpc_testing
import pytest
# noinspection PyPackageRequirements
from hypothesis import given, settings, Phase
from zepben.protobuf.dc import dc_pb2
from zepben.protobuf.dc.dc_data_pb2 import DiagramIdentifiedObject
from zepben.protobuf.dc.dc_responses_pb2 import GetIdentifiedObjectsResponse, GetDiagramObjectsResponse

from streaming.get.data.metadata import create_metadata, create_metadata_response
from streaming.get.pb_creators import diagram_identified_objects, diagram, diagram_object
from zepben.evolve import DiagramConsumerClient, BaseService, IdentifiedObject, DiagramObject, Diagram

from streaming.get.grpcio_aio_testing.mock_async_channel import async_testing_channel
from streaming.get.mock_server import MockServer, StreamGrpc, stream_from_fixed, UnaryGrpc, unary_from_fixed

PBRequest = TypeVar('PBRequest')
GrpcResponse = TypeVar('GrpcResponse')


class TestDiagramConsumer:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.channel = async_testing_channel(dc_pb2.DESCRIPTOR.services_by_name.values(), grpc_testing.strict_real_time())
        self.mock_server = MockServer(self.channel, dc_pb2.DESCRIPTOR.services_by_name['DiagramConsumer'])
        self.client = DiagramConsumerClient(channel=self.channel)
        self.service = self.client.service

    def test_constructor(self):
        DiagramConsumerClient(channel=MagicMock())
        DiagramConsumerClient(stub=MagicMock())

        with pytest.raises(ValueError, match="Must provide either a channel or a stub"):
            DiagramConsumerClient()

    @pytest.mark.asyncio
    @given(diagram_identified_objects())
    @settings(max_examples=1, phases=(Phase.explicit, Phase.reuse, Phase.generate))
    async def test_get_identified_objects_supported_types(self, dios):
        requested = []
        for dio in dios:
            mrid = getattr(dio, dio.WhichOneof("identifiedObject"), None).mrid()
            requested.append(mrid)

            async def client_test():
                result = await self.client.get_identified_objects([mrid])
                if not mrid:
                    assert result.was_failure
                    assert isinstance(result.thrown, KeyError)
                    return
                mor = result.throw_on_error().value

                assert mrid in self.service, f"type: {dio.WhichOneof('identifiedObject')} mrid: {mrid}"
                assert mor.objects[mrid] is not None, f"type: {dio.WhichOneof('identifiedObject')} mrid: {mrid}"
                assert self.service[mrid] is mor.objects[mrid], f"type: {dio.WhichOneof('identifiedObject')} mrid: {mrid}"

            response = GetIdentifiedObjectsResponse(identifiedObjects=[dio])
            await self.mock_server.validate(client_test, [StreamGrpc('getIdentifiedObjects', stream_from_fixed([mrid], [response]))])

        assert len(requested) == len(dios) == self.service.len_of()

    @pytest.mark.asyncio
    async def test_get_identified_objects_not_found(self):
        mrid = "unknown"

        async def client_test():
            mor = (await self.client.get_identified_objects([mrid])).throw_on_error().value

            assert mor.objects == {}
            assert mor.failed == {mrid}

        await self.mock_server.validate(client_test, [StreamGrpc('getIdentifiedObjects', stream_from_fixed([mrid], []))])

    # noinspection PyUnresolvedReferences
    @pytest.mark.asyncio
    async def test_get_identified_objects_partial_not_found(self):
        async def client_test():
            mor = (await self.client.get_identified_objects(["diagram1", "diagram2", "diagram3"])).throw_on_error().value

            assert mor.objects.keys() == {"diagram1", "diagram2"}
            assert mor.failed == {"diagram3"}

        response1 = GetIdentifiedObjectsResponse(identifiedObjects=[DiagramIdentifiedObject(diagram=Diagram(mrid="diagram1").to_pb())])
        response2 = GetIdentifiedObjectsResponse(identifiedObjects=[DiagramIdentifiedObject(diagram=Diagram(mrid="diagram2").to_pb())])

        await self.mock_server.validate(client_test,
                                        [StreamGrpc('getIdentifiedObjects', stream_from_fixed(["diagram1", "diagram2", "diagram3"], [response1, response2]))])

    @pytest.mark.asyncio
    @given(diagram())
    async def test_get_identified_object(self, diagram_):
        mrid = diagram_.mrid()

        async def client_test():
            io = (await self.client.get_identified_object(mrid)).throw_on_error().value

            assert mrid in self.service
            assert io is not None
            assert self.service[mrid] is io

        response = GetIdentifiedObjectsResponse(identifiedObjects=[DiagramIdentifiedObject(diagram=diagram_)])
        await self.mock_server.validate(client_test, [StreamGrpc('getIdentifiedObjects', stream_from_fixed([mrid], [response]))])

    @pytest.mark.asyncio
    async def test_get_identified_object_not_found(self):
        mrid = "unknown"

        async def client_test():
            result = (await self.client.get_identified_object(mrid))

            assert result.was_failure
            assert isinstance(result.thrown, ValueError)
            assert str(result.thrown) == f"No object with mRID {mrid} could be found."

        await self.mock_server.validate(client_test, [StreamGrpc('getIdentifiedObjects', stream_from_fixed([mrid], []))])

    @pytest.mark.asyncio
    @given(diagram_object())
    @settings(max_examples=2, phases=(Phase.explicit, Phase.reuse, Phase.generate))
    async def test_get_diagram_objects_returns_objects_for_a_given_id(self, dio):
        mrid = dio.mrid()

        async def client_test():
            mor = (await self.client.get_diagram_objects(mrid)).throw_on_error().value
            assert mrid in mor.objects
            assert mrid in self.service

            io = mor.objects[mrid]
            assert io is not None
            assert self.service[mrid] is io

        response = GetDiagramObjectsResponse(identifiedObjects=[DiagramIdentifiedObject(diagramObject=dio)])
        await self.mock_server.validate(client_test, [StreamGrpc('getDiagramObjects', stream_from_fixed([mrid], [response]))])

    @pytest.mark.asyncio
    async def test_get_metadata(self):
        expected_metadata = create_metadata()

        async def client_test():
            metadata = (await self.client.get_metadata()).throw_on_error().value
            assert metadata == expected_metadata

        await self.mock_server.validate(client_test, [UnaryGrpc('getMetadata', unary_from_fixed(None, create_metadata_response(expected_metadata)))])

    @pytest.mark.asyncio
    async def test_get_metadata_is_cached(self):
        expected_metadata = create_metadata()

        async def client_test():
            metadata1 = (await self.client.get_metadata()).throw_on_error().value
            metadata2 = (await self.client.get_metadata()).throw_on_error().value
            assert metadata1 is metadata2

        await self.mock_server.validate(client_test, [UnaryGrpc('getMetadata', unary_from_fixed(None, create_metadata_response(expected_metadata)))])


def _assert_contains_mrids(service: BaseService, *mrids):
    for mrid in mrids:
        assert service.get(mrid)


def _response_of(io: IdentifiedObject, response_type):
    return response_type(identifiedObjects=[_to_diagram_identified_object(io)])


# noinspection PyUnresolvedReferences
def _to_diagram_identified_object(obj) -> DiagramIdentifiedObject:
    if isinstance(obj, Diagram):
        dio = DiagramIdentifiedObject(diagram=obj.to_pb())
    elif isinstance(obj, DiagramObject):
        dio = DiagramIdentifiedObject(diagramObject=obj.to_pb())
    else:
        raise Exception(f"Missing class in create response - you should implement it: {str(obj)}")
    return dio
