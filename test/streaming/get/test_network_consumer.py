#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import itertools
import warnings
from collections import Counter
from typing import Dict, Iterable, List
from unittest.mock import MagicMock, call

import pytest
from google.protobuf.any_pb2 import Any
from hypothesis import given, settings, Phase
from zepben.protobuf.nc.nc_data_pb2 import NetworkIdentifiedObject
from zepben.protobuf.nc.nc_requests_pb2 import GetIdentifiedObjectsRequest, GetEquipmentForContainerRequest, GetCurrentEquipmentForFeederRequest, \
    GetEquipmentForRestrictionRequest, GetTerminalsForNodeRequest, GetNetworkHierarchyRequest
from zepben.protobuf.nc.nc_responses_pb2 import GetIdentifiedObjectsResponse, GetEquipmentForContainerResponse, GetCurrentEquipmentForFeederResponse, \
    GetEquipmentForRestrictionResponse, GetTerminalsForNodeResponse, GetNetworkHierarchyResponse

from test.pb_creators import networkidentifiedobjects, aclinesegment
from test.streaming.get.data.hierarchy import create_hierarchy_network
from test.streaming.get.data.loops import create_loops_network
from zepben.evolve import NetworkConsumerClient, NetworkService, IdentifiedObject, CableInfo, AcLineSegment, Breaker, EnergySource, \
    EnergySourcePhase, Junction, PowerTransformer, PowerTransformerEnd, ConnectivityNode, Feeder, Location, OverheadWireInfo, PerLengthSequenceImpedance, \
    Substation, Terminal, EquipmentContainer, Equipment, BaseService, OperationalRestriction, TransformerStarImpedance, GeographicalRegion, \
    SubGeographicalRegion, Circuit, Loop, Diagram, UnsupportedOperationException


# TODO: Test behaviour of "failures" with get_feeder

def test_constructor():
    NetworkConsumerClient(channel=MagicMock())
    NetworkConsumerClient(stub=MagicMock())

    try:
        NetworkConsumerClient()
        raise AssertionError("Should have thrown")
    except ValueError as e:
        assert str(e) == "Must provide either a channel or a stub"
    except Exception as e:
        raise e


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
async def test_get_identified_object(acls):
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


# noinspection PyUnresolvedReferences
@pytest.mark.asyncio
async def test_get_identified_objects():
    network_service = NetworkService()
    nio1 = NetworkIdentifiedObject(acLineSegment=AcLineSegment(mrid="acls1").to_pb())
    nio2 = NetworkIdentifiedObject(acLineSegment=AcLineSegment(mrid="acls2").to_pb())
    response1 = GetIdentifiedObjectsResponse(identifiedObject=nio1)
    response2 = GetIdentifiedObjectsResponse(identifiedObject=nio2)
    stub = MagicMock(**{"getIdentifiedObjects.return_value": [response1, response2]})
    client = NetworkConsumerClient(stub=stub)
    result = await client.get_identified_objects(network_service, ["acls1", "acls2", "acls3"])
    assert result.was_successful
    assert result.value.objects.keys() == {"acls1", "acls2"}
    assert result.value.failed == {"acls3"}


@pytest.mark.asyncio
async def test_get_network_hierarchy(feeder_network: NetworkService):
    expected_ns = create_hierarchy_network()
    ns = NetworkService()
    stub = MagicMock(**{"getNetworkHierarchy.return_value": _create_hierarchy_response(expected_ns)})
    client = NetworkConsumerClient(stub=stub)

    response = await client.get_network_hierarchy(ns)
    stub.assert_has_calls([call.getNetworkHierarchy(GetNetworkHierarchyRequest())])

    assert response.was_successful
    assert response.value.geographical_regions.keys() == set(map(lambda it: it.mrid, expected_ns.objects(GeographicalRegion)))


@pytest.mark.asyncio
async def test_get_network_hierarchy_with_existing_items(feeder_network: NetworkService):
    expected_ns = create_hierarchy_network()
    ns = NetworkService()
    ns.add(expected_ns["g1"])
    stub = MagicMock(**{"getNetworkHierarchy.return_value": _create_hierarchy_response(expected_ns)})
    client = NetworkConsumerClient(stub=stub)

    response = await client.get_network_hierarchy(ns)
    stub.assert_has_calls([call.getNetworkHierarchy(GetNetworkHierarchyRequest())])

    assert response.was_successful
    assert response.value.geographical_regions.keys() == set(map(lambda it: it.mrid, expected_ns.objects(GeographicalRegion)))


@pytest.mark.asyncio
async def test_retrieve_network():
    pass


@pytest.mark.asyncio
async def test_get_feeder_deprecated(feeder_network: NetworkService):
    client = NetworkConsumerClient(stub=MagicMock())
    with pytest.warns(DeprecationWarning):
        warnings.warn("`get_feeder` is deprecated, prefer the more generic `get_equipment_container`")
        # noinspection PyDeprecation
        await client.get_feeder(NetworkService(), "feeder")


@pytest.mark.asyncio
async def test_get_feeder_as_equipment_container(feeder_network: NetworkService):
    ns = NetworkService()
    feeder_mrid = "f001"

    def create_feeder_response(request: GetIdentifiedObjectsRequest):
        for mrid in request.mrids:
            yield _response_of(feeder_network.get(mrid), GetIdentifiedObjectsResponse)

    stub = MagicMock(**{"getIdentifiedObjects.side_effect": create_feeder_response,
                        "getEquipmentForContainer.side_effect": _create_container_equipment_func(feeder_network)})
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
async def test_get_equipment_container_validates_type(feeder_network: NetworkService):
    ns = NetworkService()
    feeder_mrid = "f001"

    stub = MagicMock(**{"getIdentifiedObjects.side_effect": _create_objects_response(feeder_network, [feeder_mrid]),
                        "getEquipmentForContainer.side_effect": _create_container_equipment_func(feeder_network)})

    client = NetworkConsumerClient(stub=stub)

    response = await client.get_equipment_container(ns, feeder_mrid, Circuit)

    stub.assert_has_calls([call.getIdentifiedObjects(GetIdentifiedObjectsRequest(mrids=["f001"]))])
    assert response.was_failure
    assert isinstance(response.thrown, ValueError)
    assert str(response.thrown) == "Requested mrid f001 was not a Circuit, was Feeder"


@pytest.mark.asyncio
async def test_get_equipment_for_container(feeder_network: NetworkService):
    ns = NetworkService()
    feeder_mrid = "f001"

    stub = MagicMock(**{"getEquipmentForContainer.side_effect": _create_container_equipment_func(feeder_network)})
    client = NetworkConsumerClient(stub=stub)
    objects = await client.get_equipment_for_container(ns, feeder_mrid)
    assert len(objects.result.objects) == ns.len_of(Equipment) == 3
    _assert_contains_mrids(ns, "fsp", "c2", "tx")


@pytest.mark.asyncio
async def test_get_current_equipment_for_feeder(feeder_with_current: NetworkService):
    ns = NetworkService()
    feeder_mrid = "f001"
    stub = MagicMock(**{"getEquipmentForContainer.side_effect": _create_container_equipment_func(feeder_with_current),
                        "getCurrentEquipmentForFeeder.side_effect": _create_container_current_equipment_func(feeder_with_current)})
    client = NetworkConsumerClient(stub=stub)
    objects = await client.get_equipment_for_container(ns, feeder_mrid)
    assert len(objects.result.objects) == ns.len_of(Equipment) == 7
    _assert_contains_mrids(ns, "fsp", "c2", "tx", "c3", "sw", "c4", "tx2")
    ns2 = NetworkService()
    objects = await client.get_current_equipment_for_feeder(ns2, feeder_mrid)
    assert len(objects.result.objects) == ns2.len_of(Equipment) == 5
    _assert_contains_mrids(ns2, "fsp", "c2", "tx", "c3", "sw")


@pytest.mark.asyncio
async def test_get_equipment_for_operational_restriction(operational_restriction_with_equipment: NetworkService):
    ns = NetworkService()
    or_mrid = "or1"
    stub = MagicMock(**{"getEquipmentForRestriction.side_effect": _create_restriction_equipment_func(operational_restriction_with_equipment)})
    client = NetworkConsumerClient(stub=stub)
    objects = await client.get_equipment_for_restriction(ns, or_mrid)
    assert len(objects.result.objects) == ns.len_of(Equipment) == 3
    _assert_contains_mrids(ns, "fsp", "c2", "tx")


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


@pytest.mark.asyncio
async def test_get_equipment_for_loop():
    ns = create_loops_network()
    fetch_ns = NetworkService()

    loop = "loop1"
    loop_containers = ["cir1", "cir2", "cir3", "sub1", "sub2", "sub3"]
    assoc_objs = [["loop2", "fdr1", "fdr2", "fdr3", "cir4"], ["sub4"], ["fdr4"], ["cir1-j-t", "cir2-j-t", "cir3-j-t", "sub1-j-t", "sub2-j-t", "sub3-j-t"]]
    valid_objects = [loop] + loop_containers + list(itertools.chain.from_iterable(assoc_objs))

    stub = MagicMock(**{"getEquipmentForContainer.side_effect": _create_containers_response(ns, loop_containers),
                        "getIdentifiedObjects.side_effect": _create_objects_response(ns, valid_objects)})
    client = NetworkConsumerClient(stub=stub)
    response = await client.get_equipment_for_loop(fetch_ns, loop)

    assert response.was_successful

    expected_calls = [call.getIdentifiedObjects(MatchRequest(GetIdentifiedObjectsRequest, [loop])),
                      call.getIdentifiedObjects(MatchRequest(GetIdentifiedObjectsRequest, loop_containers)),
                      call.getIdentifiedObjects(MatchRequest(GetIdentifiedObjectsRequest, assoc_objs[0])),
                      call.getIdentifiedObjects(MatchRequest(GetIdentifiedObjectsRequest, assoc_objs[1])),
                      call.getIdentifiedObjects(MatchRequest(GetIdentifiedObjectsRequest, assoc_objs[2]))]
    matcher = MatchRequest(GetEquipmentForContainerRequest, loop_containers)
    for _ in loop_containers:
        expected_calls.append(call.getEquipmentForContainer(matcher))
    expected_calls.append(call.getIdentifiedObjects(MatchRequest(GetIdentifiedObjectsRequest, assoc_objs[3])))

    stub.assert_has_calls(expected_calls)
    assert not matcher.expected_mrids


@pytest.mark.asyncio
async def test_get_all_loop():
    ns = create_loops_network()
    fetch_ns = NetworkService()

    containers = ["cir1", "cir2", "cir3", "cir4", "sub1", "sub2", "sub3", "sub4"]
    assoc_objs = ["cir1-j-t", "cir2-j-t", "cir3-j-t", "cir4-j-t", "sub1-j-t", "sub2-j-t", "sub3-j-t", "sub4-j-t"]

    stub = MagicMock(**{"getNetworkHierarchy.return_value": _create_hierarchy_response(ns),
                        "getEquipmentForContainer.side_effect": _create_containers_response(ns, containers),
                        "getIdentifiedObjects.side_effect": _create_objects_response(ns, assoc_objs)})
    client = NetworkConsumerClient(stub=stub)
    response = await client.get_all_loops(fetch_ns)

    assert response.was_successful

    expected_calls = [call.getNetworkHierarchy(GetNetworkHierarchyRequest())]
    matcher = MatchRequest(GetEquipmentForContainerRequest, containers)
    for _ in containers:
        expected_calls.append(call.getEquipmentForContainer(matcher))
    expected_calls.append(call.getIdentifiedObjects(MatchRequest(GetIdentifiedObjectsRequest, assoc_objs)))

    stub.assert_has_calls(expected_calls)
    assert not matcher.expected_mrids


@pytest.mark.asyncio
async def test_existing_equipment_used_for_repeats(feeder_network: NetworkService):
    ns = NetworkService()
    ns.add(feeder_network["tx"])
    feeder_mrid = "f001"

    stub = MagicMock(**{"getEquipmentForContainer.side_effect": _create_container_equipment_func(feeder_network)})
    client = NetworkConsumerClient(stub=stub)

    response = await client.get_equipment_for_container(ns, feeder_mrid)

    assert response.was_successful
    assert ns["tx"] is feeder_network["tx"]
    assert ns["fsp"] is not feeder_network["fsp"]


@pytest.mark.asyncio
async def test_unknown_types_are_reported(feeder_network: NetworkService):
    ns = NetworkService()
    ns.add(feeder_network["tx"])
    feeder_mrid = "f001"

    def responses(_):
        nio = Any()
        # noinspection PyUnresolvedReferences
        nio.Pack(Diagram().to_pb())
        it = GetIdentifiedObjectsResponse(identifiedObject=NetworkIdentifiedObject(other=nio))
        yield GetIdentifiedObjectsResponse(identifiedObject=NetworkIdentifiedObject(other=nio))

    stub = MagicMock(**{"getEquipmentForContainer.side_effect": responses})
    client = NetworkConsumerClient(stub=stub)

    response = await client.get_equipment_for_container(ns, feeder_mrid)

    assert response.was_failure
    assert isinstance(response.thrown, UnsupportedOperationException)
    assert str(response.thrown) == "Identified object type 'other' is not supported by the network service"


def _assert_contains_mrids(service: BaseService, *mrids):
    for mrid in mrids:
        assert service.get(mrid)


def _response_of(io: IdentifiedObject, response_type):
    return response_type(identifiedObject=_to_network_identified_object(io))


# noinspection PyUnresolvedReferences
def _to_network_identified_object(obj) -> NetworkIdentifiedObject:
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
    elif isinstance(obj, Loop):
        nio = NetworkIdentifiedObject(loop=obj.to_pb())
    elif isinstance(obj, Circuit):
        nio = NetworkIdentifiedObject(circuit=obj.to_pb())
    else:
        raise Exception(f"Missing class in create response - you should implement it: {str(obj)}")
    return nio


def _create_container_equipment_func(network: NetworkService):
    def create_equipment_response(request: GetEquipmentForContainerRequest):
        ec = network.get(request.mrid, EquipmentContainer)
        for equip in ec.equipment:
            yield _response_of(equip, GetEquipmentForContainerResponse)

    return create_equipment_response


def _create_restriction_equipment_func(network: NetworkService):
    def create_equipment_response(request: GetEquipmentForRestrictionRequest):
        or1 = network.get(request.mrid, OperationalRestriction)
        for equip in or1.equipment:
            yield _response_of(equip, GetEquipmentForRestrictionResponse)

    return create_equipment_response


def _create_container_current_equipment_func(network: NetworkService):
    def create_equipment_response(request: GetCurrentEquipmentForFeederRequest):
        ec = network.get(request.mrid, Feeder)
        for equip in ec.current_equipment:
            yield _response_of(equip, GetCurrentEquipmentForFeederResponse)

    return create_equipment_response


# noinspection PyUnresolvedReferences
def _create_hierarchy_response(service: NetworkService) -> GetNetworkHierarchyResponse:
    return GetNetworkHierarchyResponse(
        geographicalRegions=list(map(lambda it: it.to_pb(), service.objects(GeographicalRegion))),
        subGeographicalRegions=list(map(lambda it: it.to_pb(), service.objects(SubGeographicalRegion))),
        substations=list(map(lambda it: it.to_pb(), service.objects(Substation))),
        feeders=list(map(lambda it: it.to_pb(), service.objects(Feeder))),
        circuits=list(map(lambda it: it.to_pb(), service.objects(Circuit))),
        loops=list(map(lambda it: it.to_pb(), service.objects(Loop)))
    )


def _create_objects_response(ns: NetworkService, mrids: Iterable[str]):
    valid: Dict[str, IdentifiedObject] = {mrid: ns[mrid] for mrid in mrids}

    def responses(request: GetIdentifiedObjectsRequest):
        for mrid in request.mrids:
            obj = valid.get(mrid)
            if obj:
                yield _response_of(obj, GetIdentifiedObjectsResponse)
            else:
                raise AssertionError(f"Requested unexpected object {mrid}.")

    return responses


def _create_containers_response(ns: NetworkService, mrids: Iterable[str]):
    valid: Dict[str, EquipmentContainer] = {mrid: ns[mrid] for mrid in mrids}

    def responses(request: GetEquipmentForContainerRequest):
        container = valid.get(request.mrid)
        if container:
            for equipment in container.equipment:
                yield _response_of(equipment, GetEquipmentForContainerResponse)
        else:
            raise AssertionError(f"Requested unexpected container {request.mrid}.")

    return responses


class MatchRequest(object):

    def __init__(self, expected_type: type, expected_mrids: List[str]):
        self.expected_type = expected_type
        self.expected_mrids = expected_mrids.copy()

    # noinspection PyUnresolvedReferences
    def __eq__(self, other):
        if not isinstance(other, self.expected_type):
            return False

        if isinstance(other, GetEquipmentForContainerRequest):
            if other.mrid not in self.expected_mrids:
                return False

            self.expected_mrids.remove(other.mrid)
            return True

        elif isinstance(other, GetIdentifiedObjectsRequest):
            return Counter(self.expected_mrids) == Counter(other.mrids)

        return False
