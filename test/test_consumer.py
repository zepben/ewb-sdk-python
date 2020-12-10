#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import pytest
from hypothesis import given, settings, Phase
from zepben.protobuf.nc.nc_data_pb2 import NetworkIdentifiedObject, IdentifiedObjectGroup
from zepben.protobuf.nc.nc_responses_pb2 import GetIdentifiedObjectsResponse
from unittest.mock import MagicMock

from test.pb_creators import networkidentifiedobjects, aclinesegment
from zepben.evolve import NetworkConsumerClient, NetworkService


class TestConsumer(object):

    @pytest.mark.asyncio
    @given(networkidentifiedobjects())
    @settings(max_examples=1, phases=(Phase.explicit, Phase.reuse, Phase.generate))
    async def test_retrieve_supported_types(self, networkidentifiedobjects):
        network_service = NetworkService()
        for nio in networkidentifiedobjects:
            response = GetIdentifiedObjectsResponse(objectGroup=IdentifiedObjectGroup(identifiedObject=nio))
            stub = MagicMock(**{"getIdentifiedObjects.return_value": [response]})
            client = NetworkConsumerClient(stub=stub)
            pbio = getattr(nio, nio.WhichOneof("identifiedObject"), None)
            result = await client.get_identified_objects(network_service, [pbio.mrid()])
            assert result.was_successful
            if pbio.mrid():
                assert result.result.value[pbio.mrid()] is not None, f"type: {nio.WhichOneof('identifiedObject')} mrid: {pbio.mrid()}"
                assert network_service.get(pbio.mrid()) is result.result.value[pbio.mrid()]
            else:
                assert pbio.mrid() in result.result.failed

    @pytest.mark.asyncio
    @given(aclinesegment())
    async def test_get_identifiedobject(self, aclinesegment):
        network_service = NetworkService()
        nio = NetworkIdentifiedObject(acLineSegment=aclinesegment)
        response = GetIdentifiedObjectsResponse(objectGroup=IdentifiedObjectGroup(identifiedObject=nio))
        stub = MagicMock(**{"getIdentifiedObjects.return_value": [response]})
        client = NetworkConsumerClient(stub=stub)
        pbio = getattr(nio, nio.WhichOneof("identifiedObject"), None)
        result = await client.get_identified_object(network_service, pbio.mrid())
        assert result.was_successful
        assert result.result is not None
        assert result.result.mrid == pbio.mrid()

        stub = MagicMock(**{"getIdentifiedObjects.return_value": []})
        client = NetworkConsumerClient(stub=stub)
        pbio = getattr(nio, nio.WhichOneof("identifiedObject"), None)
        result = await client.get_identified_object(network_service, "fakemrid")
        assert result.was_successful
        assert result.result is None



