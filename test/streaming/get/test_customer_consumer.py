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
from zepben.protobuf.cc import cc_pb2
from zepben.protobuf.cc.cc_data_pb2 import CustomerIdentifiedObject
from zepben.protobuf.cc.cc_responses_pb2 import GetIdentifiedObjectsResponse, GetCustomersForContainerResponse

from streaming.get.data.metadata import create_metadata, create_metadata_response
from streaming.get.pb_creators import customer_identified_objects, customer
from zepben.evolve import CustomerConsumerClient, BaseService, IdentifiedObject, Customer

from streaming.get.grpcio_aio_testing.mock_async_channel import async_testing_channel
from streaming.get.mock_server import MockServer, StreamGrpc, stream_from_fixed, UnaryGrpc, unary_from_fixed

PBRequest = TypeVar('PBRequest')
GrpcResponse = TypeVar('GrpcResponse')


class TestCustomerConsumer:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.channel = async_testing_channel(cc_pb2.DESCRIPTOR.services_by_name.values(), grpc_testing.strict_real_time())
        self.mock_server = MockServer(self.channel, cc_pb2.DESCRIPTOR.services_by_name['CustomerConsumer'])
        self.client = CustomerConsumerClient(channel=self.channel)
        self.service = self.client.service

    def test_constructor(self):
        CustomerConsumerClient(channel=MagicMock())
        CustomerConsumerClient(stub=MagicMock())

        with pytest.raises(ValueError, match="Must provide either a channel or a stub"):
            CustomerConsumerClient()

    @pytest.mark.asyncio
    @given(customer_identified_objects())
    @settings(max_examples=1, phases=(Phase.explicit, Phase.reuse, Phase.generate))
    async def test_get_identified_objects_supported_types(self, cios):
        requested = []
        for cio in cios:
            mrid = getattr(cio, cio.WhichOneof("identifiedObject"), None).mrid()
            requested.append(mrid)

            async def client_test():
                result = await self.client.get_identified_objects([mrid])
                if not mrid:
                    assert result.was_failure
                    assert isinstance(result.thrown, KeyError)
                    return
                mor = result.throw_on_error().value

                assert mrid in self.service, f"type: {cio.WhichOneof('identifiedObject')} mrid: {mrid}"
                assert mor.objects[mrid] is not None, f"type: {cio.WhichOneof('identifiedObject')} mrid: {mrid}"
                assert self.service[mrid] is mor.objects[mrid], f"type: {cio.WhichOneof('identifiedObject')} mrid: {mrid}"

            response = GetIdentifiedObjectsResponse(identifiedObjects=[cio])
            await self.mock_server.validate(client_test, [StreamGrpc('getIdentifiedObjects', stream_from_fixed([mrid], [response]))])

        assert len(requested) == len(cios) == self.service.len_of()

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
            mor = (await self.client.get_identified_objects(["customer1", "customer2", "customer3"])).throw_on_error().value

            assert mor.objects.keys() == {"customer1", "customer2"}
            assert mor.failed == {"customer3"}

        response1 = GetIdentifiedObjectsResponse(identifiedObjects=[CustomerIdentifiedObject(customer=Customer(mrid="customer1").to_pb())])
        response2 = GetIdentifiedObjectsResponse(identifiedObjects=[CustomerIdentifiedObject(customer=Customer(mrid="customer2").to_pb())])

        await self.mock_server.validate(client_test,
                                        [StreamGrpc('getIdentifiedObjects',
                                                    stream_from_fixed(["customer1", "customer2", "customer3"], [response1, response2]))])

    @pytest.mark.asyncio
    @given(customer())
    async def test_get_identified_object(self, customer_):
        mrid = customer_.mrid()

        async def client_test():
            io = (await self.client.get_identified_object(mrid)).throw_on_error().value

            assert mrid in self.service
            assert io is not None
            assert self.service[mrid] is io

        response = GetIdentifiedObjectsResponse(identifiedObjects=[CustomerIdentifiedObject(customer=customer_)])
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
    @given(customer())
    @settings(max_examples=2, phases=(Phase.explicit, Phase.reuse, Phase.generate))
    async def test_get_customers_for_container_returns_results(self, c):
        mrid = c.mrid()

        async def client_test():
            mor = (await self.client.get_customers_for_container(mrid)).throw_on_error().value
            assert mrid in mor.objects
            assert mrid in self.service

            io = mor.objects[mrid]
            assert io is not None
            assert self.service[mrid] is io

        response = GetCustomersForContainerResponse(identifiedObjects=[CustomerIdentifiedObject(customer=c)])
        await self.mock_server.validate(client_test, [StreamGrpc('getCustomersForContainer', stream_from_fixed([mrid], [response]))])

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
    return response_type(identifiedObjects=[_to_customer_identified_object(io)])


# noinspection PyUnresolvedReferences
def _to_customer_identified_object(obj) -> CustomerIdentifiedObject:
    if isinstance(obj, Customer):
        cio = CustomerIdentifiedObject(customer=obj.to_pb())
    elif isinstance(obj, CustomerAgreement):
        cio = CustomerIdentifiedObject(customerAgreement=obj.to_pb())
    elif isinstance(obj, Organisation):
        cio = CustomerIdentifiedObject(organisation=obj.to_pb())
    elif isinstance(obj, PricingStructure):
        cio = CustomerIdentifiedObject(pricingStructure=obj.to_pb())
    elif isinstance(obj, Tariff):
        cio = CustomerIdentifiedObject(tariff=obj.to_pb())
    else:
        raise Exception(f"Missing class in create response - you should implement it: {str(obj)}")
    return cio
