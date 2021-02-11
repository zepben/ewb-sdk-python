#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import List

import pytest
from hypothesis import given, settings, Phase
from zepben.protobuf.nc.nc_data_pb2 import NetworkIdentifiedObject, IdentifiedObjectGroup
from zepben.protobuf.nc.nc_requests_pb2 import GetIdentifiedObjectsRequest
from zepben.protobuf.nc.nc_responses_pb2 import GetIdentifiedObjectsResponse
from unittest.mock import MagicMock

from test.pb_creators import networkidentifiedobjects, aclinesegment
from zepben.evolve import NetworkConsumerClient, NetworkService, IdentifiedObject, CableInfo, ConductingEquipment, AcLineSegment, Breaker, EnergySource, \
    EnergySourcePhase, Junction, PowerTransformer, PowerTransformerEnd, ConnectivityNode, Feeder, Location, OverheadWireInfo, PerLengthSequenceImpedance, \
    Substation, Terminal


# TODO: Test behaviour of "failures" with get_feeder/get_identified_objects

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

    @pytest.mark.asyncio
    async def test_get_network_hierarchy(self, feeder_network):
        pass

    @pytest.mark.asyncio
    async def test_retrieve_network(self):
        pass

    @pytest.mark.asyncio
    async def test_get_feeder(self, feeder_network):
        ns = NetworkService()
        feeder_mrid = "f001"

        def create_feeder_responses(request: GetIdentifiedObjectsRequest, *args, **kwargs):
            objects = []
            for mrid in request.mrids:
                io = feeder_network.get(mrid)
                if io:
                    objects.append(io)
            return response_of(objects)

        stub = MagicMock(**{"getIdentifiedObjects.side_effect": create_feeder_responses})
        client = NetworkConsumerClient(stub=stub)
        objects = await client.get_feeder(ns, feeder_mrid)
        assert len(objects.result.value) == ns.len_of() == feeder_network.len_of()
        assert objects.was_successful
        assert feeder_mrid in objects.result.value
        for io in objects.result.value.values():
            assert ns.get(io.mrid) == io

        for io in ns.objects():
            assert objects.result.value[io.mrid] == io
        assert len(objects.result.failed) == 0


def response_of(objects: List[IdentifiedObject]):
    responses = []
    for obj in objects:
        og = IdentifiedObjectGroup()
        if isinstance(obj, CableInfo):
            nio = NetworkIdentifiedObject(cableInfo=obj.to_pb())
        elif isinstance(obj, ConductingEquipment):
            # og.ownedIdentifiedObject.extend([NetworkIdentifiedObject(terminal=t.to_pb()) for t in obj.terminals])
            if isinstance(obj, AcLineSegment):
                nio = NetworkIdentifiedObject(acLineSegment=obj.to_pb())
            elif isinstance(obj, Breaker):
                nio = NetworkIdentifiedObject(breaker=obj.to_pb())
            elif isinstance(obj, EnergySource):
                nio = NetworkIdentifiedObject(energySource=obj.to_pb())
            elif isinstance(obj, EnergySourcePhase):
                nio = NetworkIdentifiedObject(energySourcePhase=obj.to_pb())
            elif isinstance(obj, Junction):
                nio = NetworkIdentifiedObject(junction=obj.to_pb())
            elif isinstance(obj, PowerTransformer):
                nio = NetworkIdentifiedObject(powerTransformer=obj.to_pb())
            else:
                raise Exception(f"Missing class in create response - you should implement it: {str(obj)}")
        elif isinstance(obj, ConnectivityNode):
            nio = NetworkIdentifiedObject(connectivityNode=obj.to_pb())
        elif isinstance(obj, EnergySourcePhase):
            nio = NetworkIdentifiedObject(energySourcePhase=obj.to_pb())
        elif isinstance(obj, Feeder):
            nio = NetworkIdentifiedObject(feeder=obj.to_pb())
        elif isinstance(obj, Location):
            nio = NetworkIdentifiedObject(location=obj.to_pb())
        elif isinstance(obj, OverheadWireInfo):
            nio = NetworkIdentifiedObject(overheadWireInfo=obj.to_pb())
        elif isinstance(obj, PerLengthSequenceImpedance):
            nio = NetworkIdentifiedObject(perLengthSequenceImpedance=obj.to_pb())
        elif isinstance(obj, PowerTransformerEnd):
            nio = NetworkIdentifiedObject(powerTransformerEnd=obj.to_pb())
        elif isinstance(obj, Substation):
            nio = NetworkIdentifiedObject(substation=obj.to_pb())
        elif isinstance(obj, Terminal):
            nio = NetworkIdentifiedObject(terminal=obj.to_pb())
        else:
            raise Exception(f"Missing class in create response - you should implement it: {str(obj)}")
        og.identifiedObject.CopyFrom(nio)
        responses.append(GetIdentifiedObjectsResponse(objectGroup=og))
    return responses
