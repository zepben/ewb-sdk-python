#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations

from abc import abstractmethod
from typing import Iterable, Callable, AsyncGenerator, Dict, List, Optional

from zepben.protobuf.nc.nc_data_pb2 import NetworkIdentifiedObject

from zepben.cimbend import Feeder
from zepben.cimbend.streaming.data import NetworkHierarchyFeeder, NetworkHierarchySubstation, NetworkHierarchySubGeographicalRegion, \
    NetworkHierarchyGeographicalRegion, NetworkHierarchyIdentifiedObject, NetworkHierarchy
from zepben.cimbend.streaming.grpc import GrpcClient, GrpcResult
from zepben.protobuf.nc.nc_pb2_grpc import NetworkConsumerStub
from zepben.protobuf.nc.nc_requests_pb2 import GetNetworkHierarchyRequest, GetIdentifiedObjectsRequest
import zepben.cimbend.common.resolver as resolver

__all__ = ["CimConsumerClient", "NetworkConsumerClient"]


class CimConsumerClient(GrpcClient):

    @abstractmethod
    async def get_identified_object(self, service: BaseService, mrid: str) -> GrpcResult:
        """
        Retrieve the object with the given `mrid` and store the result in the `service`.
                                                                                                                 
        Exceptions that occur during sending will be caught and passed to all error handlers that have been registered against this client.
        If none of the registered error handlers return true to indicate the error has been handled, the exception will be rethrown.

        Returns the item if found as a `GrpcResult`, otherwise None.
        """
        raise NotImplementedError()

    @abstractmethod
    async def get_identified_objects(self, service: BaseService, mrids: Iterable[str]) -> GrpcResult:
        """
        Retrieve the objects with the given `mrids` and store the results in the `service`.

        Exceptions that occur during sending will be caught and passed to all error handlers that have been registered against this client.
        If none of the registered error handlers return true to indicate the error has been handled, the exception will be rethrown.

        Returns a map of the retrieved items keyed by their `mrid` as a `GrpcResult`. If an item is not found it will be excluded from the map.
        """
        raise NotImplementedError()


def _extract_identified_object(service: NetworkService, nio: NetworkIdentifiedObject) -> Optional[IdentifiedObject]:
    """
    Add an equipment to the network.
    `stub` A network consumer stub.
    `network` The network to add the equipment to.
    `equipment_io` The equipment identified object returned by the server.
    """
    io_type = nio.WhichOneof("identifiedObject")
    if io_type:
        pbio = getattr(nio, io_type)
        return service.add_from_pb(pbio)
    return None


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

    def __init__(self, channel=None, stub: NetworkConsumerStub = None):
        if channel is None and stub is None:
            raise ValueError("Must provide either a channel or a stub")
        if stub is not None:
            self._stub = stub
        else:
            self._stub = NetworkConsumerStub(channel)

    async def get_identified_object(self, service: NetworkService, mrid: str) -> GrpcResult:
        """
        Retrieve the object with the given `mrid` and store the result in the `service`.

        Exceptions that occur during sending will be caught and passed to all error handlers that have been registered against this client.
        If none of the registered error handlers return true to indicate the error has been handled, the exception will be rethrown.

        Returns the item if found as a `GrpcResult`, otherwise None.
        """
        return await self.try_rpc(lambda: next(self._process_identified_objects(service, GetIdentifiedObjectsRequest(mrids=[mrid])), None))

    async def get_identified_objects(self, service: NetworkService, mrids: Iterable[str]) -> GrpcResult[Dict[str, IdentifiedObject]]:
        """
        Retrieve the objects with the given `mrids` and store the results in the `service`.

        Exceptions that occur during sending will be caught and passed to all error handlers that have been registered against this client.
        If none of the registered error handlers return true to indicate the error has been handled, the exception will be rethrown.

        Returns a map of the retrieved items keyed by their `mrid` as a `GrpcResult`. If an item is not found it will be excluded from the map.
        """
        async def y():
            z = dict()
            failed = set(mrids)
            async for x in self._process_identified_objects(service, mrids):
                if x is not None:
                    z[x.mrid] = x
                    failed.remove(x.mrid)
            for mrid in failed:
                if mrid:
                    z[mrid] = None
                else:
                    z[mrid] = None
            return z
        return await self.try_rpc(y)

    async def get_network_hierarchy(self) -> GrpcResult[NetworkHierarchy]:
        """
        Retrieve the network hierarchy

        Returns a simplified version of the network hierarchy that can be used to make further in-depth requests.
        """
        return await self.try_rpc(self._handle_network_hierarchy)

    async def get_feeder(self, service: NetworkService, mrid: str) -> GrpcResult[Feeder]:
        """
        Retrieve the feeder network for the specified `mrid` and store the results in the `service`.
                                                                                                                              
        This is a convenience method that will fetch the feeder object, all of the equipment referenced by the feeder (normal state),
        the terminals of all elements, the connectivity between terminals, the locations of all elements, the ends of all transformers
        and the wire info for all conductors.

        Returns a GrpcResult containing either the `zepben.cimbend.cim.iec61970.base.core.equipment_container.Feeder`, or None if it was not found.
        """
        feeder_response = await self.get_identified_object(service, mrid)
        feeder = feeder_response.throw_on_error().result

        if not feeder:
            return GrpcResult(None)

        await self.get_identified_objects(service, service.get_unresolved_reference_mrids(resolver.ec_equipment(feeder))).throw_on_error()
        mrids = service.get_unresolved_reference_mrids(resolver.normal_energizing_substation(feeder))
        for equip in feeder.equipment:
            try:
                for terminal in equip.terminals:
                    mrids.update(service.get_unresolved_reference_mrids(resolver.connectivity_node(terminal)))
            except AttributeError:
                pass  # No terminals.

            mrids.update(service.get_unresolved_reference_mrids(resolver.per_length_sequence_impedance(equip)))
            mrids.update(service.get_unresolved_reference_mrids(resolver.asset_info(equip)))
            mrids.update(service.get_unresolved_reference_mrids(resolver.location(equip)))

        await self.get_identified_objects(service, mrids).throw_on_error()
        return GrpcResult(feeder)

    async def _process_identified_objects(self, service: NetworkService, mrids: Iterable[str]) -> AsyncGenerator[IdentifiedObject, None]:
        responses = self._stub.getIdentifiedObjects(GetIdentifiedObjectsRequest(mrids=mrids))
        for response in responses:
            og = response.objectGroup
            io = _extract_identified_object(service, og.identifiedObject)
            if io:
                yield io
            for owned_obj in og.ownedIdentifiedObject:
                extracted = _extract_identified_object(service, owned_obj)
                if extracted:
                    yield extracted

    async def _handle_network_hierarchy(self):
        response = self._stub.getIdentifiedObjects(GetNetworkHierarchyRequest())
        feeders = {f.mrid: NetworkHierarchyFeeder(f.mrid, f.name) for f in response.feeders}
        substations = {s.mrid: NetworkHierarchySubstation(s.mrid, s.name, _lookup(s.feederMRIDs, feeders)) for s in response.substations}
        sub_geographical_regions = {s.mrid: NetworkHierarchySubGeographicalRegion(s.mrid, s.name, _lookup(s.substationMRIDs, substations)) for s in
                                    response.subGeographicalRegions}
        geographical_regions = {g.mrid: NetworkHierarchyGeographicalRegion(g.mrid, g.name, _lookup(g.subGeographicalRegionMRIDs, sub_geographical_regions)) for
                                g in response.geographicalRegions}

        _finalise_links(geographical_regions, sub_geographical_regions, substations)
        return NetworkHierarchy(geographical_regions, sub_geographical_regions, substations, feeders)
