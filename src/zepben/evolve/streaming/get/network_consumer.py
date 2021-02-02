#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations

from asyncio import get_event_loop
from typing import Iterable, Dict, Optional, AsyncGenerator, Union, List, Callable, Set, Generator

from dataclassy import dataclass

from zepben.evolve import NetworkService, Feeder, ConnectivityNode, Terminal, Equipment, EquipmentContainer, Substation, IdentifiedObject
from zepben.evolve.services.common.reference_resolvers import Relationship
from zepben.evolve.streaming.get.consumer import MultiObjectResult, extract_identified_object, CimConsumerClient
from zepben.evolve.streaming.get.hierarchy.data import NetworkHierarchyIdentifiedObject, NetworkHierarchyGeographicalRegion, \
    NetworkHierarchySubGeographicalRegion, NetworkHierarchySubstation, NetworkHierarchy, NetworkHierarchyFeeder
from zepben.evolve.streaming.grpc.grpc import GrpcResult
from zepben.protobuf.nc.nc_pb2_grpc import NetworkConsumerStub
import zepben.evolve.services.common.resolver as resolver
from zepben.protobuf.nc.nc_requests_pb2 import GetIdentifiedObjectsRequest, GetNetworkHierarchyRequest, GetEquipmentForContainerRequest

__all__ = ["NetworkConsumerClient", "SyncNetworkConsumerClient"]

MAX_64_BIT_INTEGER = 9223372036854775807
_EXCLUDED_GET_FEEDER = {
    Relationship(ConnectivityNode, Terminal),
    Relationship(Feeder, Equipment),
    Relationship(Equipment, Feeder),
    Relationship(EquipmentContainer, Equipment),
    Relationship(Equipment, EquipmentContainer),
    Relationship(Substation, Equipment),
    Relationship(Equipment, Substation),
}


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

    async def get_equipment_for_container(self, service: NetworkService, mrid: str) -> GrpcResult[MultiObjectResult]:
        """
        Retrieve the `Equipment` for the `EquipmentContainer` represented by `mrid`
        Exceptions that occur during retrieval will be caught and passed to all error handlers that have been registered against this client.

        `mrid` The mRID of the `EquipmentContainer` to fetch equipment for.
        Returns a `GrpcResult` with a result of one of the following:
        - A `MultiObjectResult` containing a map of the retrieved objects keyed by mRID. If an item is not found it will be excluded from the map.
          If an item couldn't be added to `service` its mRID will be present in `MultiObjectResult.failed` (see `zepben.evolve.common.base_service.BaseService.add`).
        - An `Exception` if an error occurred while retrieving or processing the objects, in which case, `GrpcResult.was_successful` will return false.
        """
        return await self._get_equipment_for_container(service, mrid)

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

    async def _get_identified_objects(self, service: NetworkService, mrids: Iterable[str], result: MultiObjectResult = None) -> GrpcResult[MultiObjectResult]:
        """
        `service` The service to add any results to.
        `mrids` The mRIDs to fetch from the server.
        `result` an existing `MultiObjectResult` to populate. A new result will be created if not provided.
        Returns a GrpcResult with a MultiObjectResult containing everything that was added to `service`.
        """
        if result is None:
            result = MultiObjectResult()

        async def y():
            async for io, mrid in self._process_identified_objects(service, mrids):
                if io:
                    result.value[io.mrid] = io
                else:
                    result.failed.add(mrid)
            return result

        return await self.try_rpc(y)

    async def _get_equipment_for_container(self, service: NetworkService, mrid: str, result: MultiObjectResult = None) -> GrpcResult[MultiObjectResult]:
        """
        `service` The service to add any results to.
        `mrid` The mRID of the `EquipmentContainer` to fetch `Equipment` for from the server.
        `result` an existing `MultiObjectResult` to populate. A new result will be created if not provided.
        Returns a GrpcResult with a MultiObjectResult containing everything that was added to `service`.
        """
        if result is None:
            result = MultiObjectResult()

        async def y():
            async for io, _mrid in self._process_equipment_container(service, mrid):
                if io:
                    result.value[io.mrid] = io
                else:
                    result.failed.add(_mrid)
            return result

        return await self.try_rpc(y)

    async def _get_network_hierarchy(self) -> GrpcResult[NetworkHierarchy]:
        return await self.try_rpc(self._handle_network_hierarchy)

    async def _get_feeder(self, service: NetworkService, mrid: str) -> GrpcResult[MultiObjectResult]:
        feeder_response = (await self._get_identified_object(service, mrid)).throw_on_error()
        feeder: Feeder = feeder_response.result

        if not feeder:
            return GrpcResult(result=None)

        if not isinstance(feeder, Feeder):
            return GrpcResult(result=ValueError(f"Requested mrid {mrid} was not a Feeder, was {type(feeder)}"))

        mor = MultiObjectResult()
        res = (await self._get_equipment_for_container(service, feeder.mrid)).throw_on_error()
        mor.value.update(res.result.value)
        # We need to resolve all the unresolved references for each piece of equipment, but then we need to
        # also do the same for the resolutions, and so on so forth until the entire tree of references originating from the Feeder has been resolved,
        # however we don't know how long this tree is until we've resolved everything. So we start by resolving all the equipment, then we iteratively
        # descend the tree by checking for unresolved references for the objects we just resolved in the previous iteration.
        to_resolve = self._get_unresolved_mrids(service, res.result.value.keys(), _EXCLUDED_GET_FEEDER)
        while True:
            res = await self._get_objects(service, to_resolve)
            if not res.value:
                break
            mor.value.update(res.value)
            to_resolve = self._get_unresolved_mrids(service, res.value.keys(), _EXCLUDED_GET_FEEDER)

        # Get the rest of the unresolved references for the feeder (e.g substation)
        await self._get_objects(service, service.get_unresolved_reference_mrids_from(feeder.mrid), mor)
        mor.value[feeder.mrid] = feeder

        return GrpcResult(result=mor)

    async def _get_objects(self, service: NetworkService, mrids: Iterable[str], result: MultiObjectResult = None) -> MultiObjectResult:
        if not mrids:
            return MultiObjectResult() if result is None else result
        objects = (await self._get_identified_objects(service, mrids, result)).throw_on_error()
        return objects.result

    def _get_unresolved_mrids(self, service: NetworkService, mrids: Iterable[str], excluded: Set[Relationship] = None) -> Generator[str, None, None]:
        seen = set()
        for m in mrids:
            for i in service.get_unresolved_reference_mrids_from(m, excluded):
                if i in seen:
                    continue
                yield i
                seen.add(i)

    async def _retrieve_network(self) -> GrpcResult[Union[NetworkResult, Exception]]:
        service = NetworkService()
        result = (await self._get_network_hierarchy()).throw_on_error()

        hierarchy: NetworkHierarchy = result.result
        mor = MultiObjectResult()
        for mrid in hierarchy.geographical_regions.keys():
            gr_result = (await self._get_identified_object(service, mrid)).throw_on_error()
            if gr_result.result is None:
                mor.failed.add(mrid)

        for mrid in hierarchy.sub_geographical_regions.keys():
            sgr_result = (await self._get_identified_object(service, mrid)).throw_on_error()
            if sgr_result.result is None:
                mor.failed.add(mrid)

        for mrid in hierarchy.substations.keys():
            substation_result = (await self._get_identified_object(service, mrid)).throw_on_error()
            if substation_result.result is None:
                mor.failed.add(mrid)

        for mrid in hierarchy.feeders.keys():
            feeder_result = (await self._get_feeder(service, mrid)).throw_on_error()
            mor.failed.update(feeder_result.result.failed)

        # Possible that some previously failed resolutions were successful some other way, so check all the failures against the service
        for f in mor.failed:
            try:
                service.get(f)
                mor.failed.remove(f)
            except:
                pass

        return GrpcResult(NetworkResult(service, mor.failed))

    async def _process_unresolved(self, service):
        for mrid in service.unresolved_mrids():
            await self._get_identified_object(service, mrid)

    async def _process_equipment_container(self, service: NetworkService, mrid: str) -> AsyncGenerator[IdentifiedObject, None]:
        responses = self._stub.getEquipmentForContainer(GetEquipmentForContainerRequest(mrid=mrid))
        for response in responses:
            yield extract_identified_object(service, response.identifiedObject)

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
