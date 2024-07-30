#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Dict, Iterable, TypeVar, Generator, Callable, Optional
from unittest.mock import MagicMock

import grpc_testing
import pytest
# noinspection PyPackageRequirements
from google.protobuf.any_pb2 import Any
from hypothesis import given, settings, Phase

from zepben.evolve import NetworkConsumerClient, NetworkService, IdentifiedObject, CableInfo, AcLineSegment, Breaker, EnergySource, \
    EnergySourcePhase, Junction, PowerTransformer, PowerTransformerEnd, ConnectivityNode, Feeder, Location, OverheadWireInfo, PerLengthSequenceImpedance, \
    Substation, Terminal, EquipmentContainer, Equipment, BaseService, OperationalRestriction, TransformerStarImpedance, GeographicalRegion, \
    SubGeographicalRegion, Circuit, Loop, Diagram, UnsupportedOperationException, LvFeeder, TestNetworkBuilder
from zepben.protobuf.nc import nc_pb2
from zepben.protobuf.nc.nc_data_pb2 import NetworkIdentifiedObject
from zepben.protobuf.nc.nc_requests_pb2 import GetIdentifiedObjectsRequest, GetEquipmentForContainersRequest, GetCurrentEquipmentForFeederRequest, \
    GetEquipmentForRestrictionRequest, GetTerminalsForNodeRequest, IncludedEnergizingContainers, IncludedEnergizedContainers
from zepben.protobuf.nc.nc_responses_pb2 import GetIdentifiedObjectsResponse, GetEquipmentForContainersResponse, GetCurrentEquipmentForFeederResponse, \
    GetEquipmentForRestrictionResponse, GetTerminalsForNodeResponse, GetNetworkHierarchyResponse

from time import sleep
from streaming.get.data.metadata import create_metadata, create_metadata_response
from streaming.get.grpcio_aio_testing.mock_async_channel import async_testing_channel
from streaming.get.pb_creators import network_identified_objects, ac_line_segment
from streaming.get.data.hierarchy import create_hierarchy_network
from streaming.get.data.loops import create_loops_network
from streaming.get.mock_server import MockServer, StreamGrpc, UnaryGrpc, stream_from_fixed, unary_from_fixed

PBRequest = TypeVar('PBRequest')
GrpcResponse = TypeVar('GrpcResponse')


class TestNetworkConsumer:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.channel = async_testing_channel(nc_pb2.DESCRIPTOR.services_by_name.values(), grpc_testing.strict_real_time())
        self.mock_server = MockServer(self.channel, nc_pb2.DESCRIPTOR.services_by_name['NetworkConsumer'])
        self.client = NetworkConsumerClient(channel=self.channel)
        self.service = self.client.service

    def test_constructor(self):
        NetworkConsumerClient(channel=MagicMock())
        NetworkConsumerClient(stub=MagicMock())

        with pytest.raises(ValueError, match="Must provide either a channel or a stub"):
            NetworkConsumerClient()

    @pytest.mark.asyncio
    @given(network_identified_objects())
    @settings(max_examples=1, phases=(Phase.explicit, Phase.reuse, Phase.generate))
    async def test_get_identified_objects_supported_types(self, nios):
        requested = []
        for nio in nios:
            mrid = getattr(nio, nio.WhichOneof("identifiedObject"), None).mrid()
            requested.append(mrid)

            async def client_test():
                mor = (await self.client.get_identified_objects([mrid])).throw_on_error().value

                assert mrid in self.service, f"type: {nio.WhichOneof('identifiedObject')} mrid: {mrid}"
                assert mor.objects[mrid] is not None, f"type: {nio.WhichOneof('identifiedObject')} mrid: {mrid}"
                assert self.service[mrid] is mor.objects[mrid], f"type: {nio.WhichOneof('identifiedObject')} mrid: {mrid}"

            response = GetIdentifiedObjectsResponse(identifiedObjects=[nio])
            await self.mock_server.validate(client_test, [StreamGrpc('getIdentifiedObjects', stream_from_fixed([mrid], [response]))])

        assert len(requested) == len(nios) == self.service.len_of()

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
            mor = (await self.client.get_identified_objects(["acls1", "acls2", "acls3"])).throw_on_error().value

            assert mor.objects.keys() == {"acls1", "acls2"}
            assert mor.failed == {"acls3"}

        response1 = GetIdentifiedObjectsResponse(identifiedObjects=[NetworkIdentifiedObject(acLineSegment=AcLineSegment(mrid="acls1").to_pb())])
        response2 = GetIdentifiedObjectsResponse(identifiedObjects=[NetworkIdentifiedObject(acLineSegment=AcLineSegment(mrid="acls2").to_pb())])

        await self.mock_server.validate(client_test,
                                        [StreamGrpc('getIdentifiedObjects', stream_from_fixed(["acls1", "acls2", "acls3"], [response1, response2]))])

    @pytest.mark.asyncio
    @given(ac_line_segment())
    async def test_get_identified_object(self, acls):
        mrid = acls.mrid()

        async def client_test():
            io = (await self.client.get_identified_object(mrid)).throw_on_error().value

            assert mrid in self.service
            assert io is not None
            assert self.service[mrid] is io

        response = GetIdentifiedObjectsResponse(identifiedObjects=[NetworkIdentifiedObject(acLineSegment=acls)])
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

    @pytest.mark.asyncio
    async def test_get_network_hierarchy(self):
        expected_ns = create_hierarchy_network()

        async def client_test():
            hierarchy = (await self.client.get_network_hierarchy()).throw_on_error().value

            _validate_hierarchy(hierarchy, expected_ns)
            _validate_hierarchy(hierarchy, self.service)

        await self.mock_server.validate(client_test, [UnaryGrpc('getNetworkHierarchy', unary_from_fixed(None, _create_hierarchy_response(expected_ns)))])

    @pytest.mark.asyncio
    async def test_get_network_hierarchy_is_cached(self):
        expected_ns = create_hierarchy_network()

        async def client_test():
            hierarchy1 = (await self.client.get_network_hierarchy()).throw_on_error().value
            hierarchy2 = (await self.client.get_network_hierarchy()).throw_on_error().value

            assert hierarchy1 is hierarchy2

        await self.mock_server.validate(client_test, [UnaryGrpc('getNetworkHierarchy', unary_from_fixed(None, _create_hierarchy_response(expected_ns)))])

    @pytest.mark.asyncio
    async def test_get_network_hierarchy_with_existing_items(self):
        expected_ns = create_hierarchy_network()
        self.service.add(expected_ns["g1"])

        async def client_test():
            hierarchy = (await self.client.get_network_hierarchy()).throw_on_error().value

            assert hierarchy.geographical_regions["g1"] is expected_ns["g1"]
            assert hierarchy.geographical_regions["g2"] is not expected_ns["g2"]

        await self.mock_server.validate(client_test, [UnaryGrpc('getNetworkHierarchy', unary_from_fixed(None, _create_hierarchy_response(expected_ns)))])

    @pytest.mark.asyncio
    async def test_retrieve_network(self):
        ns = create_loops_network()
        containers = ["cir1", "cir2", "cir3", "cir4", "sub1", "sub2", "sub3", "sub4", "fdr1", "fdr2", "fdr3", "fdr4"]
        assoc_objs = [
            "cir1-j-t", "cir2-j-t", "cir3-j-t", "cir4-j-t",
            "sub1-j-t", "sub2-j-t", "sub3-j-t", "sub4-j-t",
            "fdr1-j-t", "fdr2-j-t", "fdr3-j-t", "fdr4-j-t"
        ]

        async def client_test():
            (await self.client.retrieve_network()).throw_on_error()

            assert self.service.len_of() == ns.len_of()
            for io in self.service.objects():
                assert io.mrid in ns

        interactions = [UnaryGrpc('getNetworkHierarchy', unary_from_fixed(None, _create_hierarchy_response(ns)))]

        for _ in ns.objects(EquipmentContainer):
            interactions.extend([
                StreamGrpc('getEquipmentForContainers', [_create_container_equipment_responses(ns, containers)]),
                StreamGrpc('getIdentifiedObjects', [_create_object_responses(ns, assoc_objs)])
            ])

        await self.mock_server.validate(client_test, interactions)

    @pytest.mark.asyncio
    async def test_get_feeder_as_equipment_container(self, feeder_network: NetworkService):
        feeder_mrid = "f001"

        async def client_test():
            mor = (await self.client.get_equipment_container(feeder_mrid, Feeder)).throw_on_error().value

            assert self.service.len_of() == 21
            assert len(mor.objects) == 20  # we do not include the substation in the results
            assert feeder_mrid in mor.objects
            for io in mor.objects.values():
                assert self.service.get(io.mrid) == io

            for io in self.service.objects():
                if not isinstance(io, Substation):
                    assert mor.objects[io.mrid] == io
            assert len(mor.failed) == 0

        object_responses = _create_object_responses(feeder_network)

        await self.mock_server.validate(client_test,
                                        [
                                            UnaryGrpc('getNetworkHierarchy', unary_from_fixed(None, _create_hierarchy_response(feeder_network))),
                                            StreamGrpc('getEquipmentForContainers', [_create_container_responses(feeder_network)]),
                                            StreamGrpc('getIdentifiedObjects', [object_responses, object_responses])
                                        ])

    @pytest.mark.asyncio
    async def test_resolve_references_skips_resolvers_referencing_equipment_containers(self):
        """
        lvf5:[     c1  {  ]  c3     }:lvf6
        lvf5:[tx0------{b2]------tx4}:lvf6
        """
        lv_feeders_with_open_point = (await TestNetworkBuilder()
                                      .from_power_transformer()  # tx0
                                      .to_acls()  # c1
                                      .to_breaker(action=lambda it: it.set_normally_open(True))  # b2
                                      .to_acls()  # c3
                                      .to_power_transformer()  # tx4
                                      .add_lv_feeder("tx0", 2)
                                      .add_lv_feeder("tx4", 1)
                                      .build())

        feeder_mrid = "lvf5"

        async def client_test():
            mor = (await self.client.get_equipment_container(feeder_mrid, LvFeeder)).throw_on_error().value

            assert self.service.len_of() == 16
            assert len(mor.objects) == 16
            assert len({"lvf5", "tx0", "c1", "b2", "tx0-t2", "tx0-e1", "tx0-e2", "tx0-t1", "c1-t1", "c1-t2", "b2-t1",
                        "b2-t2", "lvf6", "generated_cn_0", "generated_cn_1", "generated_cn_2"}.difference(mor.objects.keys())) == 0
            assert "tx4" not in mor.objects
            with pytest.raises(KeyError):
                self.service.get("tx4")
            assert self.service.get("tx0") == mor.objects["tx0"]

        object_responses = _create_object_responses(lv_feeders_with_open_point)

        await self.mock_server.validate(client_test,
                                        [
                                            UnaryGrpc('getNetworkHierarchy', unary_from_fixed(None, _create_hierarchy_response(lv_feeders_with_open_point))),
                                            StreamGrpc('getIdentifiedObjects', [object_responses]),
                                            StreamGrpc('getEquipmentForContainers', [_create_container_equipment_responses(lv_feeders_with_open_point)]),
                                            StreamGrpc('getIdentifiedObjects', [object_responses, object_responses])
                                        ])

    @pytest.mark.asyncio
    async def test_get_equipment_container_validates_type(self, feeder_network: NetworkService):
        feeder_mrid = "f001"

        async def client_test():
            response = (await self.client.get_equipment_container(feeder_mrid, Circuit))

            assert response.was_failure
            assert isinstance(response.thrown, ValueError)
            assert str(response.thrown) == f"Requested mrid {feeder_mrid} was not a Circuit, was Feeder"

        await self.mock_server.validate(client_test, [UnaryGrpc('getNetworkHierarchy', unary_from_fixed(None, _create_hierarchy_response(feeder_network)))])

    @pytest.mark.asyncio
    async def test_get_equipment_container_sends_linked_container_params(self, feeder_network: NetworkService):
        feeder_mrid = "f001"

        async def client_test():
            await self.client.get_equipment_container(
                feeder_mrid,
                Feeder,
                IncludedEnergizingContainers.INCLUDE_ENERGIZING_SUBSTATIONS,
                IncludedEnergizedContainers.INCLUDE_ENERGIZED_LV_FEEDERS
            )

        object_responses = _create_object_responses(feeder_network)

        await self.mock_server.validate(client_test,
                                        [
                                            UnaryGrpc('getNetworkHierarchy', unary_from_fixed(None, _create_hierarchy_response(feeder_network))),
                                            StreamGrpc('getEquipmentForContainers', [
                                                _create_container_responses(
                                                    feeder_network,
                                                    expected_include_energizing_containers=IncludedEnergizingContainers.INCLUDE_ENERGIZING_SUBSTATIONS,
                                                    expected_include_energized_containers=IncludedEnergizedContainers.INCLUDE_ENERGIZED_LV_FEEDERS
                                                )
                                            ]),
                                            StreamGrpc('getIdentifiedObjects', [object_responses, object_responses])
                                        ])

    @pytest.mark.asyncio
    async def test_get_equipment_for_container(self, feeder_network: NetworkService):
        async def client_test():
            mor = (await self.client.get_equipment_for_container("f001")).throw_on_error().value

            assert len(mor.objects) == self.service.len_of(Equipment) == 3
            _assert_contains_mrids(self.service, "fsp", "c2", "tx")

        await self.mock_server.validate(client_test, [StreamGrpc('getEquipmentForContainers', [_create_container_equipment_responses(feeder_network)])])

    @pytest.mark.asyncio
    async def test_get_equipment_for_container_supports_linked_containers(self, feeder_network: NetworkService):
        async def client_test():
            mor = (
                await self.client.get_equipment_for_container(
                    "f001",
                    IncludedEnergizingContainers.INCLUDE_ENERGIZING_SUBSTATIONS,
                    IncludedEnergizedContainers.INCLUDE_ENERGIZED_LV_FEEDERS
                )
            ).throw_on_error().value

            assert len(mor.objects) == self.service.len_of(Equipment) == 3
            _assert_contains_mrids(self.service, "fsp", "c2", "tx")

        await self.mock_server.validate(client_test, [StreamGrpc('getEquipmentForContainers', [_create_container_equipment_responses(feeder_network)])])

    @pytest.mark.asyncio
    async def test_get_equipment_for_containers(self, feeder_network: NetworkService):
        async def client_test():
            mor = (await self.client.get_equipment_for_containers(["f001"])).throw_on_error().value

            assert len(mor.objects) == self.service.len_of(Equipment) == 3
            _assert_contains_mrids(self.service, "fsp", "c2", "tx")

        await self.mock_server.validate(client_test, [StreamGrpc('getEquipmentForContainers', [_create_container_equipment_responses(feeder_network)])])

    @pytest.mark.asyncio
    async def test_get_equipment_for_containers_supports_linked_containers(self, feeder_network: NetworkService):
        async def client_test():
            mor = (
                await self.client.get_equipment_for_containers(
                    ["f001"],
                    IncludedEnergizingContainers.INCLUDE_ENERGIZING_SUBSTATIONS,
                    IncludedEnergizedContainers.INCLUDE_ENERGIZED_LV_FEEDERS
                )
            ).throw_on_error().value

            assert len(mor.objects) == self.service.len_of(Equipment) == 3
            _assert_contains_mrids(self.service, "fsp", "c2", "tx")

        await self.mock_server.validate(client_test, [StreamGrpc('getEquipmentForContainers', [_create_container_equipment_responses(feeder_network)])])

    @pytest.mark.asyncio
    async def test_get_current_equipment_for_feeder(self, feeder_with_current: NetworkService):
        async def client_test():
            mor = (await self.client.get_current_equipment_for_feeder("f001")).throw_on_error().value

            assert len(mor.objects) == self.service.len_of(Equipment) == 5
            _assert_contains_mrids(self.service, "fsp", "c2", "tx", "c3", "sw")

        await self.mock_server.validate(client_test,
                                        [StreamGrpc('getCurrentEquipmentForFeeder', [_create_container_current_equipment_responses(feeder_with_current)])])

    @pytest.mark.asyncio
    async def test_get_equipment_for_operational_restriction(self, operational_restriction_with_equipment: NetworkService):
        async def client_test():
            mor = (await self.client.get_equipment_for_restriction("or1")).throw_on_error().value

            assert len(mor.objects) == self.service.len_of(Equipment) == 3
            _assert_contains_mrids(self.service, "fsp", "c2", "tx")

        await self.mock_server.validate(client_test,
                                        [StreamGrpc('getEquipmentForRestriction',
                                                    [_create_restriction_equipment_responses(operational_restriction_with_equipment)])])

    @pytest.mark.asyncio
    async def test_get_terminals_for_connectivity_node(self, single_connectivitynode_network: NetworkService):
        cn_mrid = "cn1"
        cn1 = single_connectivitynode_network.get(cn_mrid, ConnectivityNode)

        async def client_test():
            mor = (await self.client.get_terminals_for_connectivity_node(cn_mrid)).throw_on_error().value

            assert len(mor.objects) == self.service.len_of(Terminal) == 3
            for term in cn1:
                assert self.service[term.mrid]

        await self.mock_server.validate(client_test, [StreamGrpc('getTerminalsForNode', [_create_cn_responses(single_connectivitynode_network)])])

    @pytest.mark.asyncio
    async def test_get_equipment_for_loop(self):
        ns = create_loops_network()
        loop = "loop1"
        loop_containers = ["cir1", "cir2", "cir3", "sub1", "sub2", "sub3"]
        hierarchy_objs = ["loop2", "fdr1", "fdr2", "fdr3", "cir4", "sub4", "fdr4"]
        container_equip = ["cir1-j", "cir2-j", "cir3-j", "sub1-j", "sub2-j", "sub3-j"]
        assoc_objs = ["cir1-j-t", "cir2-j-t", "cir3-j-t", "sub1-j-t", "sub2-j-t", "sub3-j-t"]

        async def client_test():
            mor = (await self.client.get_equipment_for_loop(loop)).throw_on_error().value

            assert self.service.len_of() == len([loop] + loop_containers + hierarchy_objs + container_equip + assoc_objs)
            assert len(mor.objects) == len([loop] + loop_containers + container_equip + assoc_objs)

        await self.mock_server.validate(client_test,
                                        [
                                            UnaryGrpc('getNetworkHierarchy', unary_from_fixed(None, _create_hierarchy_response(ns))),
                                            StreamGrpc('getEquipmentForContainers', [_create_container_equipment_responses(ns, loop_containers)]),
                                            StreamGrpc('getIdentifiedObjects', [_create_object_responses(ns, assoc_objs)])
                                        ])

    @pytest.mark.asyncio
    async def test_get_all_loops(self):
        ns = create_loops_network()
        loops = ["loop1", "loop2"]
        loop_containers = ["cir1", "cir2", "cir3", "cir4", "sub1", "sub2", "sub3", "sub4"]
        hierarchy_objs = ["fdr1", "fdr2", "fdr3", "fdr4"]
        container_equip = ["cir1-j", "cir2-j", "cir3-j", "cir4-j", "sub1-j", "sub2-j", "sub3-j", "sub4-j"]
        assoc_objs = ["cir1-j-t", "cir2-j-t", "cir3-j-t", "cir4-j-t", "sub1-j-t", "sub2-j-t", "sub3-j-t", "sub4-j-t"]

        async def client_test():
            mor = (await self.client.get_all_loops()).throw_on_error().value

            assert self.service.len_of() == len(mor.objects) == len(loops + loop_containers + hierarchy_objs + container_equip + assoc_objs)

        await self.mock_server.validate(client_test,
                                        [
                                            UnaryGrpc('getNetworkHierarchy', unary_from_fixed(None, _create_hierarchy_response(ns))),
                                            StreamGrpc('getEquipmentForContainers', [_create_container_equipment_responses(ns, loop_containers)]),
                                            StreamGrpc('getIdentifiedObjects', [_create_object_responses(ns, assoc_objs)])
                                        ])

    @pytest.mark.asyncio
    async def test_existing_equipment_used_for_repeats(self, feeder_network: NetworkService):
        self.service.add(feeder_network["tx"])

        async def client_test():
            (await self.client.get_equipment_for_container("f001")).throw_on_error()

            assert self.service["tx"] is feeder_network["tx"]
            assert self.service["fsp"] is not feeder_network["fsp"]

        await self.mock_server.validate(client_test, [StreamGrpc('getEquipmentForContainers', [_create_container_equipment_responses(feeder_network)])])

    @pytest.mark.asyncio
    async def test_unknown_types_are_reported(self):
        async def client_test():
            result = await self.client.get_equipment_for_container("f001")

            assert result.was_failure
            assert isinstance(result.thrown, UnsupportedOperationException)
            assert str(result.thrown) == "Identified object type 'other' is not supported by the network service"

        def responses(_):
            nio = Any()
            # noinspection PyUnresolvedReferences
            nio.Pack(Diagram().to_pb())
            yield GetIdentifiedObjectsResponse(identifiedObjects=[NetworkIdentifiedObject(other=nio)])

        await self.mock_server.validate(client_test, [StreamGrpc('getEquipmentForContainers', [responses])])

    @pytest.mark.asyncio
    async def test_timeout(self):
        pass
        # TODO: EWB-1249 this is dumb and doesn't actually test the client configured timeout
        # Ideally this should be changed so that this tests EVERY gRPC call passing in a timeout
        # and that the client times out the request.
        # It seems that the client never times out the request (???) and passes the timeout to the server. This means we'll
        # need to create a real server that times out or mock the behaviour (in which case what's the point?)
        # ns = create_loops_network()
        # client = NetworkConsumerClient(channel=self.channel, timeout=1)

        # async def client_test():
        #    res = await self.client.get_network_hierarchy()
        #    assert res.was_failure
        #    res.thrown.args[0]._code == StatusCode.DEADLINE_EXCEEDED

        # await self.mock_server.validate(client_test, [
        #    UnaryGrpc('getNetworkHierarchy', unary_from_fixed(None, _create_hierarchy_response_with_sleep(ns, 3))),
        # ])


def _assert_contains_mrids(service: BaseService, *mrids):
    for mrid in mrids:
        assert service.get(mrid)


def _response_of(io: IdentifiedObject, response_type):
    return response_type(identifiedObjects=[_to_network_identified_object(io)])


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
    elif isinstance(obj, LvFeeder):
        nio = NetworkIdentifiedObject(lvFeeder=obj.to_pb())
    else:
        raise Exception(f"Missing class in create response - you should implement it: {str(obj)}")
    return nio


def _create_container_equipment_responses(ns: NetworkService, mrids: Optional[Iterable[str]] = None) \
    -> Callable[[GetEquipmentForContainersRequest], Generator[GetEquipmentForContainersResponse, None, None]]:
    valid: Dict[str, EquipmentContainer] = {mrid: ns[mrid] for mrid in mrids} if mrids else ns

    def responses(request: GetEquipmentForContainersRequest):
        for mrid in request.mrids:
            ec = valid[mrid]
            if ec:
                for equip in ec.equipment:
                    yield _response_of(equip, GetEquipmentForContainersResponse)
            else:
                raise AssertionError(f"Requested unexpected container {mrid}.")

    return responses


def _create_restriction_equipment_responses(ns: NetworkService, mrids: Optional[Iterable[str]] = None) \
    -> Callable[[GetEquipmentForRestrictionRequest], Generator[GetEquipmentForRestrictionResponse, None, None]]:
    valid: Dict[str, OperationalRestriction] = {mrid: ns[mrid] for mrid in mrids} if mrids else ns

    def responses(request: GetEquipmentForRestrictionRequest) -> Generator[GetEquipmentForRestrictionResponse, None, None]:
        or1 = valid[request.mrid]
        if or1:
            for equip in or1.equipment:
                yield _response_of(equip, GetEquipmentForRestrictionResponse)
        else:
            raise AssertionError(f"Requested unexpected restriction {request.mrid}.")

    return responses


def _create_cn_responses(ns: NetworkService, mrids: Optional[Iterable[str]] = None) \
    -> Callable[[GetTerminalsForNodeRequest], Generator[GetTerminalsForNodeResponse, None, None]]:
    valid: Dict[str, ConnectivityNode] = {mrid: ns[mrid] for mrid in mrids} if mrids else ns

    def responses(request: GetTerminalsForNodeRequest) -> Generator[GetTerminalsForNodeResponse, None, None]:
        cn = valid[request.mrid]
        if cn:
            for terminal in cn.terminals:
                # noinspection PyUnresolvedReferences
                yield GetTerminalsForNodeResponse(terminal=terminal.to_pb())
        else:
            raise AssertionError(f"Requested unexpected cn {request.mrid}.")

    return responses


def _create_container_current_equipment_responses(ns: NetworkService, mrids: Optional[Iterable[str]] = None) \
    -> Callable[[GetCurrentEquipmentForFeederRequest], Generator[GetCurrentEquipmentForFeederResponse, None, None]]:
    valid: Dict[str, Feeder] = {mrid: ns[mrid] for mrid in mrids} if mrids else ns

    def responses(request: GetCurrentEquipmentForFeederRequest) -> Generator[GetCurrentEquipmentForFeederResponse, None, None]:
        fdr = valid[request.mrid]
        if fdr:
            for equip in fdr.current_equipment:
                yield _response_of(equip, GetCurrentEquipmentForFeederResponse)
        else:
            raise AssertionError(f"Requested unexpected feeder {request.mrid}.")

    return responses


# noinspection PyUnresolvedReferences
def _create_hierarchy_response_with_sleep(service: NetworkService, sleep_time: int) -> GetNetworkHierarchyResponse:
    sleep(sleep_time)
    return _create_hierarchy_response(service)


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


def _validate_hierarchy(hierarchy, service):
    assert hierarchy.geographical_regions.keys() == {it.mrid for it in service.objects(GeographicalRegion)}
    assert hierarchy.sub_geographical_regions.keys() == {it.mrid for it in service.objects(SubGeographicalRegion)}
    assert hierarchy.substations.keys() == {it.mrid for it in service.objects(Substation)}
    assert hierarchy.feeders.keys() == {it.mrid for it in service.objects(Feeder)}
    assert hierarchy.circuits.keys() == {it.mrid for it in service.objects(Circuit)}
    assert hierarchy.loops.keys() == {it.mrid for it in service.objects(Loop)}


def _create_object_responses(ns: NetworkService, mrids: Optional[Iterable[str]] = None) \
    -> Callable[[GetIdentifiedObjectsRequest], Generator[GetIdentifiedObjectsResponse, None, None]]:
    valid: Dict[str, IdentifiedObject] = {mrid: ns[mrid] for mrid in mrids} if mrids else ns

    def responses(request: GetIdentifiedObjectsRequest) -> Generator[GetIdentifiedObjectsResponse, None, None]:
        for mrid in request.mrids:
            obj = valid[mrid]
            if obj:
                yield _response_of(obj, GetIdentifiedObjectsResponse)
            else:
                raise AssertionError(f"Requested unexpected object {mrid}.")

    return responses


def _create_container_responses(
    ns: NetworkService,
    mrids: Optional[Iterable[str]] = None,
    expected_include_energizing_containers: Optional[int] = None,
    expected_include_energized_containers: Optional[int] = None
) -> Callable[[GetEquipmentForContainersRequest], Generator[GetEquipmentForContainersResponse, None, None]]:
    valid: Dict[str, EquipmentContainer] = {mrid: ns[mrid] for mrid in mrids} if mrids else ns

    def responses(request: GetEquipmentForContainersRequest) -> Generator[GetEquipmentForContainersResponse, None, None]:
        if expected_include_energizing_containers is not None:
            assert request.includeEnergizingContainers == expected_include_energizing_containers
        if expected_include_energized_containers is not None:
            assert request.includeEnergizedContainers == expected_include_energized_containers

        for mrid in request.mrids:
            container = valid[mrid]
            if container:
                for equipment in container.equipment:
                    yield _response_of(equipment, GetEquipmentForContainersResponse)
            else:
                raise AssertionError(f"Requested unexpected container {mrid}.")

    return responses
