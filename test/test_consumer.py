#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from unittest.mock import MagicMock, call

import pytest
from hypothesis import given, settings, Phase
from zepben.protobuf.nc.nc_data_pb2 import NetworkIdentifiedObject
from zepben.protobuf.nc.nc_requests_pb2 import GetIdentifiedObjectsRequest, GetEquipmentForContainerRequest, GetCurrentEquipmentForFeederRequest, \
    GetEquipmentForRestrictionRequest, GetTerminalsForNodeRequest
from zepben.protobuf.nc.nc_responses_pb2 import GetIdentifiedObjectsResponse, GetEquipmentForContainerResponse, GetCurrentEquipmentForFeederResponse, \
    GetEquipmentForRestrictionResponse, GetTerminalsForNodeResponse

from test.pb_creators import networkidentifiedobjects, aclinesegment
from zepben.evolve import NetworkConsumerClient, NetworkService, IdentifiedObject, CableInfo, AcLineSegment, Breaker, EnergySource, \
    EnergySourcePhase, Junction, PowerTransformer, PowerTransformerEnd, ConnectivityNode, Feeder, Location, OverheadWireInfo, PerLengthSequenceImpedance, \
    Substation, Terminal, EquipmentContainer, Equipment, BaseService, OperationalRestriction, TransformerStarImpedance


# TODO: Test behaviour of "failures" with get_feeder/get_identified_objects

@pytest.mark.asyncio
@given(networkidentifiedobjects())
@settings(max_examples=1, phases=(Phase.explicit, Phase.reuse, Phase.generate))
async def test_retrieve_supported_types(network_identified_objects):
    network_service = NetworkService()
    for nio in network_identified_objects:
        response = GetIdentifiedObjectsResponse(identifiedObject=nio)
        stub = MagicMock(**{"getIdentifiedObjects.return_value": [response]})
        client = NetworkConsumerClient(stub=stub)
        pbio = getattr(nio, nio.WhichOneof("identifiedObject"), None)
        result = (await client.get_identified_objects(network_service, [pbio.mrid()])).throw_on_error()
        assert result.was_successful
        if pbio.mrid():
            assert result.result.objects[pbio.mrid()] is not None, f"type: {nio.WhichOneof('identifiedObject')} mrid: {pbio.mrid()}"
            assert network_service.get(pbio.mrid()) is result.result.objects[pbio.mrid()]
        else:
            assert pbio.mrid() in result.result.failed


@pytest.mark.asyncio
@given(aclinesegment())
async def test_get_identifiedobject(acls):
    network_service = NetworkService()
    nio = NetworkIdentifiedObject(acLineSegment=acls)
    response = GetIdentifiedObjectsResponse(identifiedObject=nio)
    stub = MagicMock(**{"getIdentifiedObjects.return_value": [response]})
    client = NetworkConsumerClient(stub=stub)
    pbio = getattr(nio, nio.WhichOneof("identifiedObject"), None)
    result = await client.get_identified_object(network_service, pbio.mrid())
    assert result.was_successful
    assert result.result is not None
    assert result.result.mrid == pbio.mrid()

    stub = MagicMock(**{"getIdentifiedObjects.return_value": []})
    client = NetworkConsumerClient(stub=stub)
    result = await client.get_identified_object(network_service, "fakemrid")
    assert result.was_failure
    assert isinstance(result.thrown, ValueError)
    assert str(result.thrown) == "No object with mRID fakemrid could be found."


@pytest.mark.asyncio
async def test_get_network_hierarchy(feeder_network: NetworkService):
    pass


@pytest.mark.asyncio
async def test_retrieve_network():
    pass


@pytest.mark.asyncio
async def test_get_feeder(feeder_network: NetworkService):
    ns = NetworkService()
    feeder_mrid = "f001"

    def create_feeder_response(request: GetIdentifiedObjectsRequest):
        for mrid in request.mrids:
            yield response_of(feeder_network.get(mrid), GetIdentifiedObjectsResponse)

    stub = MagicMock(
        **{"getIdentifiedObjects.side_effect": create_feeder_response, "getEquipmentForContainer.side_effect": create_container_equipment_func(feeder_network)})
    client = NetworkConsumerClient(stub=stub)
    response = await client.get_equipment_container(ns, feeder_mrid, Feeder)
    stub.assert_has_calls([call.getIdentifiedObjects(GetIdentifiedObjectsRequest(mrids=["f001"]))])
    assert stub.getIdentifiedObjects.call_count == 3
    assert len(response.result.objects) == ns.len_of() == 21
    assert response.was_successful
    assert feeder_mrid in response.result.objects
    for io in response.result.objects.values():
        assert ns.get(io.mrid) == io

    for io in ns.objects():
        assert response.result.objects[io.mrid] == io
    assert len(response.result.failed) == 0


@pytest.mark.asyncio
async def test_get_equipment_for_container(feeder_network: NetworkService):
    ns = NetworkService()
    feeder_mrid = "f001"

    stub = MagicMock(**{"getEquipmentForContainer.side_effect": create_container_equipment_func(feeder_network)})
    client = NetworkConsumerClient(stub=stub)
    objects = await client.get_equipment_for_container(ns, feeder_mrid)
    assert len(objects.result.objects) == ns.len_of(Equipment) == 3
    assert_contains_mrids(ns, "fsp", "c2", "tx")


@pytest.mark.asyncio
async def test_get_current_equipment_for_feeder(feeder_with_current: NetworkService):
    ns = NetworkService()
    feeder_mrid = "f001"
    stub = MagicMock(**{"getEquipmentForContainer.side_effect": create_container_equipment_func(feeder_with_current),
                        "getCurrentEquipmentForFeeder.side_effect": create_container_current_equipment_func(feeder_with_current)})
    client = NetworkConsumerClient(stub=stub)
    objects = await client.get_equipment_for_container(ns, feeder_mrid)
    assert len(objects.result.objects) == ns.len_of(Equipment) == 7
    assert_contains_mrids(ns, "fsp", "c2", "tx", "c3", "sw", "c4", "tx2")
    ns2 = NetworkService()
    objects = await client.get_current_equipment_for_feeder(ns2, feeder_mrid)
    assert len(objects.result.objects) == ns2.len_of(Equipment) == 5
    assert_contains_mrids(ns2, "fsp", "c2", "tx", "c3", "sw")


@pytest.mark.asyncio
async def test_get_equipment_for_operational_restriction(operational_restriction_with_equipment: NetworkService):
    ns = NetworkService()
    or_mrid = "or1"
    stub = MagicMock(**{"getEquipmentForRestriction.side_effect": create_restriction_equipment_func(operational_restriction_with_equipment)})
    client = NetworkConsumerClient(stub=stub)
    objects = await client.get_equipment_for_restriction(ns, or_mrid)
    assert len(objects.result.objects) == ns.len_of(Equipment) == 3
    assert_contains_mrids(ns, "fsp", "c2", "tx")


@pytest.mark.asyncio
async def test_get_terminals_for_connectivity_node(single_connectivitynode_network: NetworkService):
    ns = NetworkService()
    cn_mrid = "cn1"
    cn1 = single_connectivitynode_network.get(cn_mrid, ConnectivityNode)

    def create_cn_response(request: GetTerminalsForNodeRequest):
        cn = single_connectivitynode_network.get(request.mrid, ConnectivityNode)
        for terminal in cn.terminals:
            yield GetTerminalsForNodeResponse(terminal=terminal.to_pb())

    stub = MagicMock(**{"getTerminalsForNode.side_effect": create_cn_response})
    client = NetworkConsumerClient(stub=stub)
    response = await client.get_terminals_for_connectivity_node(ns, cn_mrid)
    assert len(response.result.objects) == ns.len_of(Terminal) == 3
    for term in cn1:
        assert ns.get(term.mrid)


def assert_contains_mrids(service: BaseService, *mrids):
    for mrid in mrids:
        assert service.get(mrid)


def response_of(io: IdentifiedObject, response_type):
    return response_type(identifiedObject=to_network_identified_object(io))


# noinspection PyUnresolvedReferences
def to_network_identified_object(obj) -> NetworkIdentifiedObject:
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
    elif isinstance(obj, Terminal):
        nio = NetworkIdentifiedObject(terminal=obj.to_pb())
    elif isinstance(obj, ConnectivityNode):
        nio = NetworkIdentifiedObject(connectivityNode=obj.to_pb())
    elif isinstance(obj, CableInfo):
        nio = NetworkIdentifiedObject(cableInfo=obj.to_pb())
    elif isinstance(obj, TransformerStarImpedance):
        nio = NetworkIdentifiedObject(transformerStarImpedance=obj.to_pb())
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
    else:
        raise Exception(f"Missing class in create response - you should implement it: {str(obj)}")
    return nio


def create_container_equipment_func(network: NetworkService):
    def create_equipment_response(request: GetEquipmentForContainerRequest):
        ec = network.get(request.mrid, EquipmentContainer)
        for equip in ec.equipment:
            yield response_of(equip, GetEquipmentForContainerResponse)

    return create_equipment_response


def create_restriction_equipment_func(network: NetworkService):
    def create_equipment_response(request: GetEquipmentForRestrictionRequest):
        or1 = network.get(request.mrid, OperationalRestriction)
        for equip in or1.equipment:
            yield response_of(equip, GetEquipmentForRestrictionResponse)

    return create_equipment_response


def create_container_current_equipment_func(network: NetworkService):
    def create_equipment_response(request: GetCurrentEquipmentForFeederRequest):
        ec = network.get(request.mrid, Feeder)
        for equip in ec.current_equipment:
            yield response_of(equip, GetCurrentEquipmentForFeederResponse)

    return create_equipment_response
