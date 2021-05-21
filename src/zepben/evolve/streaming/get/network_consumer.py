#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations

import warnings
from asyncio import get_event_loop
from itertools import chain
from typing import Iterable, Dict, Optional, AsyncGenerator, Union, List, Callable, Set, Tuple, Generic, TypeVar, Awaitable, Iterator

from dataclassy import dataclass
from zepben.protobuf.nc.nc_data_pb2 import NetworkIdentifiedObject
from zepben.protobuf.nc.nc_pb2_grpc import NetworkConsumerStub
from zepben.protobuf.nc.nc_requests_pb2 import GetIdentifiedObjectsRequest, GetNetworkHierarchyRequest, GetEquipmentForContainerRequest, \
    GetCurrentEquipmentForFeederRequest, GetEquipmentForRestrictionRequest, GetTerminalsForNodeRequest

from zepben.evolve import NetworkService, Feeder, IdentifiedObject, BaseService, UnsupportedOperationException, CableInfo, OverheadWireInfo, AssetOwner, \
    Organisation, Location, Meter, UsagePoint, OperationalRestriction, FaultIndicator, BaseVoltage, ConnectivityNode, GeographicalRegion, Site, \
    SubGeographicalRegion, Substation, Terminal, AcLineSegment, Breaker, Disconnector, EnergyConsumer, EnergyConsumerPhase, EnergySource, EnergySourcePhase, \
    Fuse, Jumper, Junction, LinearShuntCompensator, PerLengthSequenceImpedance, PowerTransformer, PowerTransformerEnd, RatioTapChanger, Recloser, Circuit, \
    Loop, Pole, Streetlight, Accumulator, Analog, Discrete, Control, RemoteControl, RemoteSource, PowerTransformerInfo, PowerElectronicsConnection, \
    PowerElectronicsConnectionPhase, BatteryUnit, PhotoVoltaicUnit, PowerElectronicsWindUnit, BusbarSection, LoadBreakSwitch, TransformerTankInfo, \
    TransformerEndInfo, TransformerStarImpedance, EquipmentContainer, NetworkHierarchy, MultiObjectResult, CimConsumerClient
from zepben.evolve.streaming.grpc.grpc import GrpcResult

__all__ = ["NetworkConsumerClient", "SyncNetworkConsumerClient"]

MAX_64_BIT_INTEGER = 9223372036854775807


@dataclass(slots=True)
class NetworkResult(object):
    network_service: Optional[NetworkService]
    failed: Set[str] = set()


class NetworkConsumerClient(CimConsumerClient[NetworkService]):
    """
    Consumer client for a :class:`NetworkService`.

    ## WARNING ##
        The :class:`MultiObjectResult` operations below are not atomic upon a :class:`NetworkService`, and thus if processing fails partway through, any
        previously successful additions will have been processed by the service, and thus you may have an incomplete service. Also note that adding to the
        service may not occur for an object if another object with the same mRID is already present in service. `MultiObjectResult.failed` can be used to
        check for mRIDs that were not found or retrieved but not added to service (this should not be the case unless you are processing things concurrently).
    """

    _stub: NetworkConsumerStub = None

    def __init__(self, channel=None, stub: NetworkConsumerStub = None, error_handlers: List[Callable[[Exception], bool]] = None):
        """
        :param channel: a gRPC channel used to create a stub if no stub is provided.
        :param stub: the gRPC stub to use for this consumer client.
        :param error_handlers: a collection of handlers to be processed for any errors that occur.
        """
        super().__init__(error_handlers=error_handlers)
        if channel is None and stub is None:
            raise ValueError("Must provide either a channel or a stub")
        if stub is not None:
            self._stub = stub
        else:
            self._stub = NetworkConsumerStub(channel)

    async def get_identified_object(self, service: NetworkService, mrid: str) -> GrpcResult[IdentifiedObject]:
        """
        Retrieve the object with the given `mRID` and store the result in the `service`.

        Exceptions that occur during sending will be caught and passed to all error handlers that have been registered.

        Parameters
            - `service` - The :class:`NetworkService` to store fetched objects in.
            - `mRID` - The mRID to retrieve.

        Returns a :class:`GrpcResult` with a result of one of the following:
            - When `GrpcResult.wasSuccessful`, the item found, accessible via `GrpcResult.value`.
            - When `GrpcResult.wasFailure`, the error that occurred retrieving or processing the the object, accessible via `GrpcResult.thrown`. One of:
                - :class:`NoSuchElementException` if the object could not be found.
                - The gRPC error that occurred while retrieving the object
        """
        return await self._get_identified_object(service, mrid)

    async def get_identified_objects(self, service: NetworkService, mrids: Iterable[str]) -> GrpcResult[MultiObjectResult]:
        """
        Retrieve the objects with the given [mRIDs] and store the results in the [service].

        Exceptions that occur during processing will be caught and passed to all error handlers that have been registered.

        Parameters
            - `service` - The :class:`NetworkService` to store fetched objects in.
            - `mRIDs` - The mRIDs to retrieve.

        Returns a :class:`GrpcResult` with a result of one of the following:
            - When `GrpcResult.wasSuccessful`, a map containing the retrieved objects keyed by mRID, accessible via `GrpcResult.value`. If an item was not
              found, or couldn't be added to `service`, it will be excluded from the map and its mRID will be present in `MultiObjectResult.failed` (see
              `BaseService.add`).
            - When `GrpcResult.wasFailure`, the error that occurred retrieving or processing the the object, accessible via `GrpcResult.thrown`.

        Note the :class:`NetworkConsumerClient` warning in this case.
        """
        return await self._get_identified_objects(service, mrids)

    async def get_equipment_for_container(self, service: NetworkService, container: Union[str, EquipmentContainer]) -> GrpcResult[MultiObjectResult]:
        """
        Retrieve the :class:`Equipment` for the :class:`EquipmentContainer` represented by `container`
       
        Exceptions that occur during retrieval will be caught and passed to all error handlers that have been registered against this client.
       
        Parameters
            - `service` - The :class:`NetworkService` to store fetched objects in.
            - `container` - The :class:`EquipmentContainer` (or its mRID) to fetch equipment for.
       
        Returns a :class:`GrpcResult` with a result of one of the following:
            - When `GrpcResult.wasSuccessful`, a map containing the retrieved objects keyed by mRID, accessible via `GrpcResult.value`. If an item was not
              found, or couldn't be added to `service`, it will be excluded from the map and its mRID will be present in `MultiObjectResult.failed` (see
              `BaseService.add`).
            - When `GrpcResult.wasFailure`, the error that occurred retrieving or processing the the object, accessible via `GrpcResult.thrown`.
        
        Note the :class:`NetworkConsumerClient` warning in this case.
        """
        return await self._handle_multi_object_rpc(lambda: self._process_equipment_for_container(service, container))

    async def get_current_equipment_for_feeder(self, service: NetworkService, feeder: [str, Feeder]) -> GrpcResult[MultiObjectResult]:
        """
        Retrieve the current :class:`Equipment` for the :class:`Feeder` represented by `feeder`
       
        Exceptions that occur during retrieval will be caught and passed to all error handlers that have been registered against this client.
       
        Parameters
            - `service` - The :class:`NetworkService` to store fetched objects in.
            - `feeder` - The :class:`Feeder` (or its mRID) to fetch the current equipment for.
       
        Returns a :class:`GrpcResult` with a result of one of the following:
            - When `GrpcResult.wasSuccessful`, a map containing the retrieved objects keyed by mRID, accessible via `GrpcResult.value`. If an item was not
              found, or couldn't be added to `service`, it will be excluded from the map and its mRID will be present in `MultiObjectResult.failed` (see
              `BaseService.add`).
            - When `GrpcResult.wasFailure`, the error that occurred retrieving or processing the the object, accessible via `GrpcResult.thrown`.
        
        Note the :class:`NetworkConsumerClient` warning in this case.
        """
        return await self._handle_multi_object_rpc(lambda: self._process_current_equipment_for_feeder(service, feeder))

    async def get_equipment_for_restriction(self, service: NetworkService, restriction: [str, OperationalRestriction]) -> GrpcResult[MultiObjectResult]:
        """
        Retrieve the :class:`Equipment` for the :class:`OperationalRestriction` represented by `restriction`

        Exceptions that occur during retrieval will be caught and passed to all error handlers that have been registered against this client.

        Parameters
            - `service` - The :class:`NetworkService` to store fetched objects in.
            - `restriction` - The :class:`OperationalRestriction` (or its mRID) to fetch equipment for.

        Returns a :class:`GrpcResult` with a result of one of the following:
            - When `GrpcResult.wasSuccessful`, a map containing the retrieved objects keyed by mRID, accessible via `GrpcResult.value`. If an item was not
              found, or couldn't be added to `service`, it will be excluded from the map and its mRID will be present in `MultiObjectResult.failed` (see
              `BaseService.add`).
            - When `GrpcResult.wasFailure`, the error that occurred retrieving or processing the the object, accessible via `GrpcResult.thrown`.

        Note the :class:`NetworkConsumerClient` warning in this case.
        """
        return await self._handle_multi_object_rpc(lambda: self._process_equipment_for_restriction(service, restriction))

    async def get_terminals_for_connectivity_node(self, service: NetworkService, node: [str, ConnectivityNode]) -> GrpcResult[MultiObjectResult]:
        """
        Retrieve the :class:`Terminal`s for the :class:`ConnectivityNode` represented by `node`

        Exceptions that occur during retrieval will be caught and passed to all error handlers that have been registered against this client.

        Parameters
            - `service` - The :class:`NetworkService` to store fetched objects in.
            - `node` - The :class:`ConnectivityNode` (or its mRID) to fetch terminals for.

        Returns a :class:`GrpcResult` with a result of one of the following:
            - When `GrpcResult.wasSuccessful`, a map containing the retrieved objects keyed by mRID, accessible via `GrpcResult.value`. If an item was not
              found, or couldn't be added to `service`, it will be excluded from the map and its mRID will be present in `MultiObjectResult.failed` (see
              `BaseService.add`).
            - When `GrpcResult.wasFailure`, the error that occurred retrieving or processing the the object, accessible via `GrpcResult.thrown`.

        Note the :class:`NetworkConsumerClient` warning in this case.
        """
        return await self._handle_multi_object_rpc(lambda: self._process_terminals_for_connectivity_node(service, node))

    async def get_network_hierarchy(self, service: NetworkService) -> GrpcResult[NetworkHierarchy]:
        """
        Retrieve the network hierarchy

        Parameters
            - `service` - The :class:`NetworkService` to store fetched objects in.

        Returns a simplified version of the network hierarchy that can be used to make further in-depth requests.
        """
        return await self._get_network_hierarchy(service)

    async def get_feeder(self, service: NetworkService, mrid: str) -> GrpcResult[MultiObjectResult]:
        """
        Retrieve the feeder network for the specified `mrid` and store the results in the `service`.

        This is a convenience method that will fetch the feeder object and all of the equipment referenced by the feeder (normal state), along with
        all references. This should entail a complete connectivity model for the feeder, however not the connectivity between multiple feeders.

        Parameters
            - `service` - The :class:`NetworkService` to store fetched objects in.
            - `mrid` - The mRID of the :class:`Feeder` to fetch equipment for.

        Returns a :class:`GrpcResult` of a :class:`MultiObjectResult`. If successful, containing a map keyed by mRID of all the objects retrieved. If an item
        couldn't be added to `service`, its mRID will be present in `MultiObjectResult.failed`.

        In addition to normal gRPC errors, you may also receive an unsuccessful :class:`GrpcResult` with the following errors:
         * - :class:`ValueError` if the requested object was not found or was not a :class:`Feeder`.
        """
        warnings.warn('`get_feeder` is deprecated, prefer the more generic `get_equipment_container`', DeprecationWarning)
        return await self._get_equipment_container(service, mrid, Feeder)

    async def get_equipment_container(self, service: NetworkService, mrid: str, expected_class: type = EquipmentContainer) -> GrpcResult[MultiObjectResult]:
        """
        /***
         * Retrieve the equipment container network for the specified `mrid` and store the results in the `service`.
         *
         * This is a convenience method that will fetch the container object and all of the equipment contained, along with all subsequent
         * references. This should entail a complete connectivity model for the container, however not the connectivity between multiple containers.
         *
        Parameters
            - `service` - The :class:`NetworkService` to store fetched objects in.
            - `mrid` - The mRID of the :class:`EquipmentContainer` to fetch.
         * @param expected_class The expected type of the fetched container.
         *
         * Returns a :class:`GrpcResult` of a :class:`MultiObjectResult`. If successful, containing a map keyed by mRID of all the objects retrieved. If an
           item couldn't be added to `service`, its mRID will be present in `MultiObjectResult.failed`.
         *
         * In addition to normal gRPC errors, you may also receive an unsuccessful :class:`GrpcResult` with the following errors:
         * - :class:`ValueError` if the requested object was not found or was of the wrong type.
         */
        """
        return await self._get_equipment_container(service, mrid, expected_class)

    async def get_equipment_for_loop(self, service: NetworkService, loop: Union[str, Loop]) -> GrpcResult[MultiObjectResult]:
        """
        Retrieve the :class:`Equipment` for the :class:`Loop` represented by `mRID`

        Exceptions that occur during retrieval will be caught and passed to all error handlers that have been registered against this client.

        Parameters
            - `service` - The :class:`NetworkService` to store fetched objects in.
            - `restriction` - The :class:`Loop` (or its mRID) to fetch equipment for.

        Returns a :class:`GrpcResult` with a result of one of the following:
            - When `GrpcResult.wasSuccessful`, a map containing the retrieved objects keyed by mRID, accessible via `GrpcResult.value`. If an item was not
              found, or couldn't be added to `service`, it will be excluded from the map and its mRID will be present in `MultiObjectResult.failed` (see
              `BaseService.add`).
            - When `GrpcResult.wasFailure`, the error that occurred retrieving or processing the the object, accessible via `GrpcResult.thrown`.

        Note the :class:`NetworkConsumerClient` warning in this case.
        """
        return await self._get_equipment_for_loop(service, loop)

    async def get_all_loops(self, service: NetworkService) -> GrpcResult[MultiObjectResult]:
        """
        Retrieve the :class:`Equipment` for all :class:`Loop` instances in `service`.

        Exceptions that occur during retrieval will be caught and passed to all error handlers that have been registered against this client.

        Parameters
            - `service` - The :class:`NetworkService` to store fetched objects in.

        Returns a :class:`GrpcResult` with a result of one of the following:
            - When `GrpcResult.wasSuccessful`, a map containing the retrieved objects keyed by mRID, accessible via `GrpcResult.value`. If an item was not
              found, or couldn't be added to `service`, it will be excluded from the map and its mRID will be present in `MultiObjectResult.failed` (see
              `BaseService.add`).
            - When `GrpcResult.wasFailure`, the error that occurred retrieving or processing the the object, accessible via `GrpcResult.thrown`.

        Note the :class:`NetworkConsumerClient` warning in this case.
        """
        return await self._get_all_loops(service)

    async def retrieve_network(self) -> GrpcResult[NetworkResult]:
        """
        Retrieve the entire network.
        Returns a GrpcResult containing the complete `zepben.evolve.network.network.NetworkService` from the server.
        """
        return await self._retrieve_network()

    async def _get_identified_object(self, service: NetworkService, mrid: str) -> GrpcResult[Optional[IdentifiedObject]]:
        async def rpc():
            async for io, _ in self._process_identified_objects(service, [mrid]):
                return io
            else:
                raise ValueError(f"No object with mRID {mrid} could be found.")

        return await self.try_rpc(rpc)

    async def _get_identified_objects(self, service: NetworkService, mrids: Iterable[str]) -> GrpcResult[MultiObjectResult]:
        return await self.try_rpc(lambda: self._process_extract_results(mrids, self._process_identified_objects(service, set(mrids))))

    async def _get_network_hierarchy(self, service: NetworkService) -> GrpcResult[NetworkHierarchy]:
        return await self.try_rpc(lambda: self._handle_network_hierarchy(service))

    async def _get_equipment_container(self, service: NetworkService, mrid: str, expected_class: type = EquipmentContainer) -> GrpcResult[MultiObjectResult]:
        async def get_additional(it: EquipmentContainer, mor: MultiObjectResult) -> Optional[GrpcResult[MultiObjectResult]]:
            result = await self.get_equipment_for_container(service, it)

            if result.was_failure:
                return GrpcResult(result.thrown, result.was_error_handled)

            mor.objects.update(result.value.objects)
            return None

        return await self._get_with_references(service, mrid, expected_class, get_additional)

    async def _get_equipment_for_loop(self, service: NetworkService, loop: Union[str, Loop]) -> GrpcResult[MultiObjectResult]:
        mrid = loop.mrid if isinstance(loop, Loop) else loop

        async def get_additional(it: Loop, mor: MultiObjectResult) -> Optional[GrpcResult[MultiObjectResult]]:
            error = await self._resolve_references(service, mor)

            if error:
                return error

            containers: Iterator[EquipmentContainer] = chain(it.circuits, it.substations, it.energizing_substations)
            for container in containers:
                result = await self.get_equipment_for_container(service, container.mrid)
                if result.was_failure:
                    return GrpcResult(result.thrown, result.was_error_handled)

                mor.objects.update(result.value.objects)

            return None

        return await self._get_with_references(service, mrid, Loop, get_additional)

    async def _get_all_loops(self, service: NetworkService) -> GrpcResult[MultiObjectResult]:
        response = await self.get_network_hierarchy(service)
        if response.was_failure:
            return GrpcResult(response.thrown, response.was_error_handled)

        hierarchy = response.value

        mor = MultiObjectResult()
        mor.objects.update(hierarchy.geographical_regions)
        mor.objects.update(hierarchy.sub_geographical_regions)
        mor.objects.update(hierarchy.substations)
        mor.objects.update(hierarchy.feeders)
        mor.objects.update(hierarchy.circuits)
        mor.objects.update(hierarchy.loops)

        containers: Set[EquipmentContainer] = set()
        for loop in hierarchy.loops.values():
            containers.update(chain(loop.circuits, loop.substations, loop.energizing_substations))

        for container in containers:
            result = await self.get_equipment_for_container(service, container.mrid)
            if result.was_failure:
                return GrpcResult(result.thrown, result.was_error_handled)

            mor.objects.update(result.value.objects)

        error = await self._resolve_references(service, mor)
        if error:
            return error

        return GrpcResult(mor)

    async def _retrieve_network(self) -> GrpcResult[NetworkResult]:
        service = NetworkService()
        result = (await self._get_network_hierarchy(service)).throw_on_error()

        hierarchy: NetworkHierarchy = result.result
        failed = set()
        for mrid in chain(hierarchy.substations, hierarchy.feeders, hierarchy.circuits):
            result = await self._get_equipment_container(service, mrid, Feeder)
            if result.was_successful:
                failed.update(result.result.failed)

        return GrpcResult(NetworkResult(service, failed))

    async def _process_equipment_for_container(self, service: NetworkService, it: Union[str, EquipmentContainer]) -> AsyncGenerator[IdentifiedObject, None]:
        mrid = it.mrid if isinstance(it, EquipmentContainer) else it
        responses = self._stub.getEquipmentForContainer(GetEquipmentForContainerRequest(mrid=mrid))
        for response in responses:
            yield _extract_identified_object(service, response.identifiedObject)

    async def _process_current_equipment_for_feeder(self, service: NetworkService, it: Union[str, Feeder]) -> AsyncGenerator[IdentifiedObject, None]:
        mrid = it.mrid if isinstance(it, Feeder) else it
        responses = self._stub.getCurrentEquipmentForFeeder(GetCurrentEquipmentForFeederRequest(mrid=mrid))
        for response in responses:
            yield _extract_identified_object(service, response.identifiedObject)

    async def _process_equipment_for_restriction(self,
                                                 service: NetworkService,
                                                 it: Union[str, OperationalRestriction]) -> AsyncGenerator[IdentifiedObject, None]:
        mrid = it.mrid if isinstance(it, OperationalRestriction) else it
        responses = self._stub.getEquipmentForRestriction(GetEquipmentForRestrictionRequest(mrid=mrid))
        for response in responses:
            yield _extract_identified_object(service, response.identifiedObject)

    async def _process_terminals_for_connectivity_node(self,
                                                       service: NetworkService,
                                                       it: Union[str, ConnectivityNode]) -> AsyncGenerator[IdentifiedObject, None]:
        mrid = it.mrid if isinstance(it, ConnectivityNode) else it
        responses = self._stub.getTerminalsForNode(GetTerminalsForNodeRequest(mrid=mrid))
        for response in responses:
            # noinspection PyUnresolvedReferences
            yield service.get(response.terminal.mrid(), Terminal, default=None) or service.add_from_pb(response.terminal), response.terminal.mrid()

    async def _process_identified_objects(self, service: NetworkService, mrids: Iterable[str]) -> AsyncGenerator[Tuple[Optional[IdentifiedObject], str], None]:
        if not mrids:
            return

        to_fetch = set()
        existing = set()
        for mrid in mrids:
            try:
                io = service.get(mrid)
                existing.add((io, io.mrid))
            except KeyError:
                to_fetch.add(mrid)

        if to_fetch:
            responses = self._stub.getIdentifiedObjects(GetIdentifiedObjectsRequest(mrids=to_fetch))
            for response in responses:
                yield _extract_identified_object(service, response.identifiedObject, check_presence=False)  # Already checked presence above

        for io in existing:
            yield io

    async def _handle_network_hierarchy(self, service: NetworkService):
        response = self._stub.getNetworkHierarchy(GetNetworkHierarchyRequest())

        return NetworkHierarchy(
            _to_map(service, response.geographicalRegions, GeographicalRegion),
            _to_map(service, response.subGeographicalRegions, SubGeographicalRegion),
            _to_map(service, response.substations, Substation),
            _to_map(service, response.feeders, Feeder),
            _to_map(service, response.circuits, Circuit),
            _to_map(service, response.loops, Loop)
        )

    async def _handle_multi_object_rpc(self, processor: Callable[[], AsyncGenerator[IdentifiedObject, None]]) -> GrpcResult[MultiObjectResult]:
        result = MultiObjectResult()

        async def rpc():
            async for io, _mrid in processor():
                if io:
                    result.objects[io.mrid] = io
                else:
                    result.failed.add(_mrid)
            return result

        return await self.try_rpc(rpc)

    T = TypeVar('T', bound=IdentifiedObject)

    async def _get_with_references(self,
                                   service: NetworkService,
                                   mrid: str,
                                   expected_class: type(Generic[T]),
                                   get_additional: Callable[[Generic[T], MultiObjectResult], Awaitable[Optional[GrpcResult[MultiObjectResult]]]]
                                   ) -> GrpcResult[MultiObjectResult]:
        response = await self.get_identified_object(service, mrid)
        if response.was_failure:
            return GrpcResult(response.thrown, response.was_error_handled)

        io = response.value

        if not isinstance(io, expected_class):
            e = ValueError(f"Requested mrid {mrid} was not a {expected_class.__name__}, was {type(io).__name__}")
            return GrpcResult(e, self.try_handle_error(e))

        mor = MultiObjectResult()
        mor.objects[io.mrid] = io

        error = await get_additional(io, mor)
        if error:
            return error

        error = await self._resolve_references(service, mor)
        if error:
            return error

        return GrpcResult(mor)

    async def _resolve_references(self, service: NetworkService, mor: MultiObjectResult) -> Optional[GrpcResult[MultiObjectResult]]:
        res = mor
        keep_processing = True
        while keep_processing:
            to_resolve = set()
            for obj in res.objects:
                for ref in service.get_unresolved_references_from(obj):
                    to_resolve.add(ref.to_mrid)

            response = await self.get_identified_objects(service, to_resolve)
            if response.was_failure:
                return GrpcResult(response.thrown, response.was_error_handled)

            res = response.value

            mor.objects.update(res.objects)
            keep_processing = bool(res.objects)

        return None


class SyncNetworkConsumerClient(NetworkConsumerClient):
    """Synchronised wrapper for :class:`NetworkConsumerClient`"""

    def get_identified_object(self, service: NetworkService, mrid: str) -> GrpcResult[IdentifiedObject]:
        return get_event_loop().run_until_complete(super().get_identified_objects(service, mrid))

    def get_identified_objects(self, service: NetworkService, mrids: Iterable[str]) -> GrpcResult[MultiObjectResult]:
        return get_event_loop().run_until_complete(super().get_identified_objects(service, mrids))

    def get_equipment_for_container(self, service: NetworkService, mrid: str) -> GrpcResult[MultiObjectResult]:
        return get_event_loop().run_until_complete(super().get_equipment_for_container(service, mrid))

    def get_current_equipment_for_feeder(self, service: NetworkService, mrid: str) -> GrpcResult[MultiObjectResult]:
        return get_event_loop().run_until_complete(super().get_current_equipment_for_feeder(service, mrid))

    def get_equipment_for_restriction(self, service: NetworkService, mrid: str) -> GrpcResult[MultiObjectResult]:
        return get_event_loop().run_until_complete(super().get_equipment_for_restriction(service, mrid))

    def get_terminals_for_connectivity_node(self, service: NetworkService, mrid: str) -> GrpcResult[MultiObjectResult]:
        return get_event_loop().run_until_complete(super().get_terminals_for_connectivity_node(service, mrid))

    def get_network_hierarchy(self, service: NetworkService):
        return get_event_loop().run_until_complete(super().get_network_hierarchy(service))

    def get_feeder(self, service: NetworkService, mrid: str) -> GrpcResult[MultiObjectResult]:
        warnings.warn('`get_feeder` is deprecated, prefer the more generic `get_equipment_container`', DeprecationWarning)
        return get_event_loop().run_until_complete(super().get_equipment_container(service, mrid, Feeder))

    def get_equipment_container(self, service: NetworkService, mrid: str, expected_class: type = EquipmentContainer) -> GrpcResult[MultiObjectResult]:
        return get_event_loop().run_until_complete(super().get_equipment_container(service, mrid, expected_class))

    def get_equipment_for_loop(self, service: NetworkService, loop: Union[str, Loop]) -> GrpcResult[MultiObjectResult]:
        return get_event_loop().run_until_complete(super().get_equipment_for_loop(self, service, loop))

    def get_all_loops(self, service: NetworkService) -> GrpcResult[MultiObjectResult]:
        return get_event_loop().run_until_complete(super().get_all_loops(self, service))

    def retrieve_network(self) -> GrpcResult[Union[NetworkResult, Exception]]:
        return get_event_loop().run_until_complete(super().retrieve_network())


T = TypeVar('T')
U = TypeVar('U', bound=IdentifiedObject)


def _to_map(service: NetworkService, objects: Iterable[Generic[T]], class_: type(Generic[U])) -> Dict[str, U]:
    result = {}

    for pb in objects:
        # noinspection PyUnresolvedReferences
        cim = service.get(pb.mrid(), class_, None) or service.add_from_pb(pb)
        result[cim.mrid] = cim

    return result


def _extract_identified_object(service: BaseService, nio: NetworkIdentifiedObject, check_presence: bool = True) -> Tuple[Optional[IdentifiedObject], str]:
    """
    Add a :class:`NetworkIdentifiedObject` to the service. Will convert from protobuf to CIM type.

    Parameters
        - `service` - The :class:`NetworkService` to add the identified object to.
        - `nio` - The :class:`NetworkIdentifiedObject` returned by the server.
        - `check_presence` - Whether to check if `nio` already exists in the service and skip if it does.

    Raises :class:`UnsupportedOperationException` if `nio` was invalid/unset.
    """
    io_type = nio.WhichOneof("identifiedObject")
    if io_type:
        cim_type = _nio_type_to_cim.get(io_type, None)
        if cim_type is None:
            raise UnsupportedOperationException(f"Identified object type '{io_type}' is not supported by the network service")

        pb = getattr(nio, io_type)
        if check_presence:
            cim = service.get(pb.mrid(), cim_type, default=None)
            if cim is not None:
                return cim, cim.mrid

        # noinspection PyUnresolvedReferences
        return service.add_from_pb(pb), pb.mrid()
    else:
        raise UnsupportedOperationException(f"Received a NetworkIdentifiedObject where no field was set")


_nio_type_to_cim = {
    "cableInfo": CableInfo,
    "overheadWireInfo": OverheadWireInfo,
    "assetOwner": AssetOwner,
    "organisation": Organisation,
    "location": Location,
    "meter": Meter,
    "usagePoint": UsagePoint,
    "operationalRestriction": OperationalRestriction,
    "faultIndicator": FaultIndicator,
    "baseVoltage": BaseVoltage,
    "connectivityNode": ConnectivityNode,
    "feeder": Feeder,
    "geographicalRegion": GeographicalRegion,
    "site": Site,
    "subGeographicalRegion": SubGeographicalRegion,
    "substation": Substation,
    "terminal": Terminal,
    "acLineSegment": AcLineSegment,
    "breaker": Breaker,
    "disconnector": Disconnector,
    "energyConsumer": EnergyConsumer,
    "energyConsumerPhase": EnergyConsumerPhase,
    "energySource": EnergySource,
    "energySourcePhase": EnergySourcePhase,
    "fuse": Fuse,
    "jumper": Jumper,
    "junction": Junction,
    "linearShuntCompensator": LinearShuntCompensator,
    "perLengthSequenceImpedance": PerLengthSequenceImpedance,
    "powerTransformer": PowerTransformer,
    "powerTransformerEnd": PowerTransformerEnd,
    "ratioTapChanger": RatioTapChanger,
    "recloser": Recloser,
    "circuit": Circuit,
    "loop": Loop,
    "pole": Pole,
    "streetlight": Streetlight,
    "accumulator": Accumulator,
    "analog": Analog,
    "discrete": Discrete,
    "control": Control,
    "remoteControl": RemoteControl,
    "remoteSource": RemoteSource,
    "powerTransformerInfo": PowerTransformerInfo,
    "powerElectronicsConnection": PowerElectronicsConnection,
    "powerElectronicsConnectionPhase": PowerElectronicsConnectionPhase,
    "batteryUnit": BatteryUnit,
    "photoVoltaicUnit": PhotoVoltaicUnit,
    "powerElectronicsWindUnit": PowerElectronicsWindUnit,
    "busbarSection": BusbarSection,
    "loadBreakSwitch": LoadBreakSwitch,
    "transformerTankInfo": TransformerTankInfo,
    "transformerEndInfo": TransformerEndInfo,
    "transformerStarImpedance": TransformerStarImpedance
}
