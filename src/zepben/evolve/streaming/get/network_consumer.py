#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations

from asyncio import get_event_loop
from typing import Iterable, Dict, Optional, AsyncGenerator, Union, List, Callable, Set

from dataclassy import dataclass

from zepben.evolve import NetworkService, Feeder, Conductor
from zepben.evolve.streaming.get.consumer import MultiObjectResult, extract_identified_object, CimConsumerClient
from zepben.evolve.streaming.get.hierarchy.data import NetworkHierarchyIdentifiedObject, NetworkHierarchyGeographicalRegion, NetworkHierarchySubGeographicalRegion, \
    NetworkHierarchySubstation, NetworkHierarchy, NetworkHierarchyFeeder
from zepben.evolve.streaming.grpc.grpc import GrpcResult
from zepben.protobuf.nc.nc_pb2_grpc import NetworkConsumerStub
import zepben.evolve.services.common.resolver as resolver
from zepben.protobuf.nc.nc_requests_pb2 import GetIdentifiedObjectsRequest, GetNetworkHierarchyRequest

__all__ = ["NetworkConsumerClient", "SyncNetworkConsumerClient"]


MAX_64_BIT_INTEGER = 9223372036854775807


@dataclass(slots=True)
class NetworkResult(object):
    network_service: Optional[NetworkService]
    failed: Set[str] = set()


def _lookup(mrids: Iterable[str], lookup: Dict[str, NetworkHierarchyIdentifiedObject]):
    return {mrid: lookup[mrid] for mrid in mrids if mrid is not None}


def _finalise_links(geographical_regions: Dict[str, NetworkHierarchyGeographicalRegion],
                    sub_geographical_regions: Dict[str, NetworkHierarchySubGeographicalRegion],
                    substations: Dict[str, NetworkHierarchySubstation]):
    for gr in geographical_regions.values():
        for sgr in gr.sub_geographical_regions.values():
            sgr.geographical_region = gr
    for sgr in sub_geographical_regions.values():
        for subs in sgr.substations.values():
            subs.sub_geographical_region = sgr
    for subs in substations.values():
        for feeder in subs.feeders.values():
            feeder.substation = subs


class NetworkConsumerClient(CimConsumerClient):
    _stub: NetworkConsumerStub = None

    def __init__(self, channel=None, stub: NetworkConsumerStub = None, error_handlers: List[Callable[[Exception], bool]] = None):
        super().__init__(error_handlers=error_handlers)
        if channel is None and stub is None:
            raise ValueError("Must provide either a channel or a stub")
        if stub is not None:
            self._stub = stub
        else:
            self._stub = NetworkConsumerStub(channel)

    async def get_identified_object(self, service: NetworkService, mrid: str) -> GrpcResult[Optional[IdentifiedObject]]:
        """
        Retrieve the object with the given `mrid` and store the result in the `service`.

        Exceptions that occur during sending will be caught and passed to all error handlers that have been registered against this client.

        Returns a `GrpcResult` with a result of one of the following:
             - The object if found
             - None if an object could not be found or it was found but not added to `service` (see `zepben.evolve.common.base_service.BaseService.add`).
             - An `Exception` if an error occurred while retrieving or processing the object, in which case, `GrpcResult.was_successful` will return false.
        """
        return await self._get_identified_object(service, mrid)

    async def get_identified_objects(self, service: NetworkService, mrids: Iterable[str]) -> GrpcResult[MultiObjectResult]:
        """
        Retrieve the objects with the given `mrids` and store the results in the `service`.

        Exceptions that occur during sending will be caught and passed to all error handlers that have been registered against this client.

        WARNING: This operation is not atomic upon `service`, and thus if processing fails partway through `mrids`, any previously successful mRID will have been
        added to the service, and thus you may have an incomplete `BaseService`. Also note that adding to the `service` may not occur for an object if another
        object with the same mRID is already present in `service`. `MultiObjectResult.failed` can be used to check for mRIDs that were retrieved but not
        added to `service`.

        Returns a `GrpcResult` with a result of one of the following:
        - A `MultiObjectResult` containing a map of the retrieved objects keyed by mRID. If an item is not found it will be excluded from the map.
          If an item couldn't be added to `service` its mRID will be present in `MultiObjectResult.failed` (see `zepben.evolve.common.base_service.BaseService.add`).
        - An `Exception` if an error occurred while retrieving or processing the objects, in which case, `GrpcResult.was_successful` will return false.
          Note the warning above in this case.
        """
        return await self._get_identified_objects(service, mrids)

    async def get_network_hierarchy(self) -> GrpcResult[NetworkHierarchy]:
        """
        Retrieve the network hierarchy

        Returns a simplified version of the network hierarchy that can be used to make further in-depth requests.
        """
        return await self._get_network_hierarchy()

    async def get_feeder(self, service: NetworkService, mrid: str) -> GrpcResult[MultiObjectResult]:
        """
        Retrieve the feeder network for the specified `mrid` and store the results in the `service`.

        This is a convenience method that will fetch the feeder object, all of the equipment referenced by the feeder (normal state),
        the terminals of all elements, the connectivity between terminals, the locations of all elements, the ends of all transformers
        and the wire info for all conductors.

        Returns a GrpcResult of a `MultiObjectResult`, containing a map keyed by mRID of all the objects retrieved as part of retrieving the `Feeder` and the
        'Feeder' itself. If an item couldn't be added to `service`, its mRID will be present in `MultiObjectResult.failed`.
        """
        return await self._get_feeder(service, mrid)

    async def retrieve_network(self) -> GrpcResult[Union[NetworkResult, Exception]]:
        """
        Retrieve the entire network.
        Returns a GrpcResult containing the complete `zepben.evolve.network.network.NetworkService` from the server.
        """
        return await self._retrieve_network()

    async def _get_identified_object(self, service: NetworkService, mrid: str) -> GrpcResult[Optional[IdentifiedObject]]:
        async def y():
            async for io, _ in self._process_identified_objects(service, [mrid]):
                return io
            else:
                return None

        return await self.try_rpc(y)

    async def _get_identified_objects(self, service: NetworkService, mrids: Iterable[str]) -> GrpcResult[MultiObjectResult]:
        async def y():
            results = dict()
            failed = set()
            async for io, mrid in self._process_identified_objects(service, mrids):
                if io:
                    results[io.mrid] = io
                else:
                    failed.add(mrid)
            return MultiObjectResult(results, failed)

        return await self.try_rpc(y)

    async def _get_network_hierarchy(self) -> GrpcResult[NetworkHierarchy]:
        return await self.try_rpc(self._handle_network_hierarchy)

    async def _get_feeder(self, service: NetworkService, mrid: str) -> GrpcResult[MultiObjectResult]:
        feeder_response = await self._get_identified_object(service, mrid)
        if feeder_response.was_failure:
            return feeder_response
        feeder: Feeder = feeder_response.result

        if not feeder:
            return GrpcResult(result=None)

        equipment_objects = await self._get_identified_objects(service, service.get_unresolved_reference_mrids(resolver.ec_equipment(feeder)))
        if equipment_objects.was_failure:
            return equipment_objects

        resolvers = list()
        resolvers.append(resolver.normal_energizing_substation(feeder))
        for equip in feeder.equipment:
            try:
                for terminal in equip.terminals:
                    resolvers.append(resolver.connectivity_node(terminal))
                if isinstance(equip, Conductor):
                    resolvers.append(resolver.per_length_sequence_impedance(equip))
                    resolvers.append(resolver.asset_info(equip))
            except AttributeError:
                pass  # Not ConductingEquipment.
            resolvers.append(resolver.psr_location(equip))

        mrids = service.get_unresolved_reference_mrids(resolvers)
        objects = await self._get_identified_objects(service, mrids)
        if objects.was_failure:
            return objects
        objects.result.value.update(equipment_objects.result.value)  # Combine with previous results
        objects.result.value[feeder.mrid] = feeder  # Add feeder to result
        return GrpcResult(result=MultiObjectResult(objects.result.value, objects.result.failed.union(equipment_objects.result.failed)))

    async def _retrieve_network(self) -> GrpcResult[Union[NetworkResult, Exception]]:
        service = NetworkService()
        result = await self._get_network_hierarchy()
        if result.was_failure:
            return result

        hierarchy: NetworkHierarchy = result.result
        for mrid in hierarchy.geographical_regions.keys():
            gr_result = await self._get_identified_object(service, mrid)
            if gr_result.was_failure:
                return gr_result

        for mrid in hierarchy.sub_geographical_regions.keys():
            sgr_result = await self._get_identified_object(service, mrid)
            if sgr_result.was_failure:
                return sgr_result

        for mrid in hierarchy.substations.keys():
            substation_result = await self._get_identified_object(service, mrid)
            if substation_result.was_failure:
                return substation_result

        for mrid in hierarchy.feeders.keys():
            feeder_result = await self._get_identified_object(service, mrid)
            if feeder_result.was_failure:
                return feeder_result

        failed = set()
        while service.has_unresolved_references():
            # we only want to break out if we've been trying to resolve the same set of references as we did in the last iteration.
            # so if we didn't resolve anything in the last iteration (i.e, the number of unresolved refs didn't change) we keep a
            # record of those mRIDs and break out of the loop if they don't change after another fetch.

            failed = set()
            for mrid in service.unresolved_mrids():
                result = (await self._get_identified_object(service, mrid)).throw_on_error()
                if result.was_failure or result.result is None:
                    failed.add(mrid)

            if failed:
                if failed == set(service.unresolved_mrids()):
                    return GrpcResult(NetworkResult(service, failed))

        return GrpcResult(NetworkResult(service, failed))

    async def _process_unresolved(self, service):
        for mrid in service.unresolved_mrids():
            await self._get_identified_object(service, mrid)

    async def _process_identified_objects(self, service: NetworkService, mrids: Iterable[str]) -> AsyncGenerator[IdentifiedObject, None]:
        to_fetch = set()
        existing = set()
        for mrid in mrids:
            try:
                fetched = service.get(mrid)
                existing.add((fetched, fetched.mrid))
            except KeyError:
                to_fetch.add(mrid)

        responses = self._stub.getIdentifiedObjects(GetIdentifiedObjectsRequest(mrids=to_fetch))
        for response in responses:
            og = response.objectGroup
            yield extract_identified_object(service, og.identifiedObject)
            for owned_obj in og.ownedIdentifiedObject:
                yield extract_identified_object(service, owned_obj)

    async def _handle_network_hierarchy(self):
        response = self._stub.getNetworkHierarchy(GetNetworkHierarchyRequest())
        feeders = {f.mRID: NetworkHierarchyFeeder(f.mRID, f.name) for f in response.feeders}
        substations = {s.mRID: NetworkHierarchySubstation(s.mRID, s.name, _lookup(s.feederMrids, feeders)) for s in response.substations}
        sub_geographical_regions = {s.mRID: NetworkHierarchySubGeographicalRegion(s.mRID, s.name, _lookup(s.substationMrids, substations)) for s in
                                    response.subGeographicalRegions}
        geographical_regions = {g.mRID: NetworkHierarchyGeographicalRegion(g.mRID, g.name, _lookup(g.subGeographicalRegionMrids, sub_geographical_regions)) for
                                g in response.geographicalRegions}

        _finalise_links(geographical_regions, sub_geographical_regions, substations)
        return NetworkHierarchy(geographical_regions, sub_geographical_regions, substations, feeders)


class SyncNetworkConsumerClient(NetworkConsumerClient):

    def get_identified_object(self, service: NetworkService, mrid: str) -> GrpcResult[Optional[IdentifiedObject]]:
        """
        Retrieve the object with the given `mrid` and store the result in the `service`.

        Exceptions that occur during sending will be caught and passed to all error handlers that have been registered against this client.

        Returns a `GrpcResult` with a result of one of the following:
             - The object if found
             - None if an object could not be found or it was found but not added to `service` (see `zepben.evolve.common.base_service.BaseService.add`).
             - An `Exception` if an error occurred while retrieving or processing the object, in which case, `GrpcResult.was_successful` will return false.
        """
        return get_event_loop().run_until_complete(super().get_identified_objects(service, mrid))

    def get_identified_objects(self, service: NetworkService, mrids: Iterable[str]) -> GrpcResult[MultiObjectResult]:
        """
        Retrieve the objects with the given `mrids` and store the results in the `service`.

        Exceptions that occur during sending will be caught and passed to all error handlers that have been registered against this client.

        WARNING: This operation is not atomic upon `service`, and thus if processing fails partway through `mrids`, any previously successful mRID will have been
        added to the service, and thus you may have an incomplete `BaseService`. Also note that adding to the `service` may not occur for an object if another
        object with the same mRID is already present in `service`. `MultiObjectResult.failed` can be used to check for mRIDs that were retrieved but not
        added to `service`.

        Returns a `GrpcResult` with a result of one of the following:
        - A `MultiObjectResult` containing a map of the retrieved objects keyed by mRID. If an item is not found it will be excluded from the map.
          If an item couldn't be added to `service` its mRID will be present in `MultiObjectResult.failed` (see `zepben.evolve.common.base_service.BaseService.add`).
        - An `Exception` if an error occurred while retrieving or processing the objects, in which case, `GrpcResult.was_successful` will return false.
          Note the warning above in this case.
        """
        return get_event_loop().run_until_complete(super().get_identified_objects(service, mrids))

    def get_network_hierarchy(self):
        """
        Retrieve the network hierarchy
        Returns a simplified version of the network hierarchy that can be used to make further in-depth requests.
        """
        return get_event_loop().run_until_complete(super().get_network_hierarchy())

    def get_feeder(self, service: NetworkService, mrid: str) -> GrpcResult[MultiObjectResult]:
        """
        Retrieve the feeder network for the specified `mrid` and store the results in the `service`.

        This is a convenience method that will fetch the feeder object, all of the equipment referenced by the feeder (normal state),
        the terminals of all elements, the connectivity between terminals, the locations of all elements, the ends of all transformers
        and the wire info for all conductors.

        Returns a GrpcResult of a `MultiObjectResult`, containing a map keyed by mRID of all the objects retrieved as part of retrieving the `Feeder` and the
        'Feeder' itself. If an item couldn't be added to `service`, its mRID will be present in `MultiObjectResult.failed`.
        """
        return get_event_loop().run_until_complete(super().get_feeder(service, mrid))

    def retrieve_network(self) -> GrpcResult[Union[NetworkResult, Exception]]:
        return get_event_loop().run_until_complete(super().retrieve_network())
