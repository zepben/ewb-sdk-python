#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["NetworkConsumerClient", "SyncNetworkConsumerClient"]

import warnings
from asyncio import get_event_loop
from itertools import chain
from typing import Iterable, Dict, Optional, AsyncGenerator, Union, List, Callable, Set, Tuple, Generic, TypeVar, Awaitable, cast

from zepben.protobuf.metadata.metadata_requests_pb2 import GetMetadataRequest
from zepben.protobuf.metadata.metadata_responses_pb2 import GetMetadataResponse
from zepben.protobuf.nc.nc_pb2_grpc import NetworkConsumerStub
from zepben.protobuf.nc.nc_requests_pb2 import GetIdentifiedObjectsRequest, GetNetworkHierarchyRequest, GetEquipmentForContainersRequest, \
    GetEquipmentForRestrictionRequest, GetTerminalsForNodeRequest, IncludedEnergizingContainers as PBIncludedEnergizingContainers, \
    IncludedEnergizedContainers as PBIncludedEnergizedContainers, NetworkState as PBNetworkState

from zepben.ewb import NetworkService, IdentifiedObject, Organisation, Location, OperationalRestriction, BaseVoltage, ConnectivityNode, Substation, Terminal, \
    AcLineSegment, Breaker, Disconnector, EnergyConsumer, \
    EnergySource, EnergySourcePhase, \
    Fuse, Jumper, PowerTransformer, Recloser, Circuit, \
    Loop, Pole, Streetlight, Control, RemoteControl, RemoteSource, PowerTransformerInfo, PowerElectronicsConnection, \
    BatteryUnit, PhotoVoltaicUnit, PowerElectronicsWindUnit, LoadBreakSwitch, TransformerTankInfo, \
    TransformerEndInfo, TransformerStarImpedance, EquipmentContainer, NetworkHierarchy, MultiObjectResult, CimConsumerClient, NoLoadTest, OpenCircuitTest, \
    ShortCircuitTest, EquivalentBranch, ShuntCompensatorInfo, LvFeeder, CurrentRelay, CurrentTransformer, RelayInfo, SwitchInfo, \
    CurrentTransformerInfo, EvChargingUnit, TapChangerControl, ServiceInfo, PotentialTransformer, DistanceRelay, VoltageRelay, ProtectionRelayScheme, \
    ProtectionRelaySystem, GroundDisconnector, Ground, SeriesCompensator, PotentialTransformerInfo, PanDemandResponseFunction, BatteryControl, \
    StaticVarCompensator, PerLengthPhaseImpedance, GroundingImpedance, PetersenCoil, ReactiveCapabilityCurve, SynchronousMachine, PowerSystemResource, Asset
from zepben.ewb.dataclassy import dataclass
from zepben.ewb.model.cim.extensions.iec61970.base.core.site import Site
from zepben.ewb.model.cim.iec61968.assetinfo.cable_info import CableInfo
from zepben.ewb.model.cim.iec61968.assetinfo.overhead_wire_info import OverheadWireInfo
from zepben.ewb.model.cim.iec61968.assets.asset_owner import AssetOwner
from zepben.ewb.model.cim.iec61968.metering.meter import Meter
from zepben.ewb.model.cim.iec61968.metering.usage_point import UsagePoint
from zepben.ewb.model.cim.iec61970.base.auxiliaryequipment.fault_indicator import FaultIndicator
from zepben.ewb.model.cim.iec61970.base.core.feeder import Feeder
from zepben.ewb.model.cim.iec61970.base.core.geographical_region import GeographicalRegion
from zepben.ewb.model.cim.iec61970.base.core.sub_geographical_region import SubGeographicalRegion
from zepben.ewb.model.cim.iec61970.base.meas.accumulator import Accumulator
from zepben.ewb.model.cim.iec61970.base.meas.analog import Analog
from zepben.ewb.model.cim.iec61970.base.meas.discrete import Discrete
from zepben.ewb.model.cim.iec61970.base.wires.busbar_section import BusbarSection
from zepben.ewb.model.cim.iec61970.base.wires.clamp import Clamp
from zepben.ewb.model.cim.iec61970.base.wires.cut import Cut
from zepben.ewb.model.cim.iec61970.base.wires.energy_consumer_phase import EnergyConsumerPhase
from zepben.ewb.model.cim.iec61970.base.wires.junction import Junction
from zepben.ewb.model.cim.iec61970.base.wires.linear_shunt_compensator import LinearShuntCompensator
from zepben.ewb.model.cim.iec61970.base.wires.per_length_sequence_impedance import PerLengthSequenceImpedance
from zepben.ewb.model.cim.iec61970.base.wires.power_electronics_connection_phase import PowerElectronicsConnectionPhase
from zepben.ewb.model.cim.iec61970.base.wires.power_transformer_end import PowerTransformerEnd
from zepben.ewb.model.cim.iec61970.base.wires.ratio_tap_changer import RatioTapChanger
# noinspection PyProtectedMember
from zepben.ewb.services.common.enum_mapper import EnumMapper
from zepben.ewb.services.network.network_state import NetworkState
from zepben.ewb.streaming.get.included_energized_containers import IncludedEnergizedContainers
from zepben.ewb.streaming.get.included_energizing_containers import IncludedEnergizingContainers
from zepben.ewb.streaming.grpc.grpc import GrpcResult

MAX_64_BIT_INTEGER = 9223372036854775807


@dataclass(slots=True)
class NetworkResult(object):
    network_service: Optional[NetworkService]
    failed: Set[str] = set()


_map_include_energizing_containers = EnumMapper(IncludedEnergizingContainers, PBIncludedEnergizingContainers)
_map_include_energized_containers = EnumMapper(IncludedEnergizedContainers, PBIncludedEnergizedContainers)
_map_network_state = EnumMapper(NetworkState, PBNetworkState)


class NetworkConsumerClient(CimConsumerClient[NetworkService]):
    """
    Consumer client for a :class:`NetworkService`.

    ## WARNING ##
        The :class:`MultiObjectResult` operations below are not atomic upon a :class:`NetworkService`, and thus if processing fails partway through, any
        previously successful additions will have been processed by the service, and thus you may have an incomplete service. Also note that adding to the
        service may not occur for an object if another object with the same mRID is already present in service. `MultiObjectResult.failed` can be used to
        check for mRIDs that were not found or retrieved but not added to service (this should not be the case unless you are processing things concurrently).
    """

    CIM_IO = TypeVar('CIM_IO', bound=IdentifiedObject)
    PB_IO = TypeVar('PB_IO')

    __service: NetworkService
    __network_hierarchy: Optional[NetworkHierarchy]

    @property
    def service(self) -> NetworkService:
        return self.__service

    _stub: NetworkConsumerStub = None

    def __init__(self, channel=None, stub: NetworkConsumerStub = None, error_handlers: List[Callable[[Exception], bool]] = None, timeout: int = 60):
        """
        :param channel: a gRPC channel used to create a stub if no stub is provided.
        :param stub: the gRPC stub to use for this consumer client.
        :param error_handlers: a collection of handlers to be processed for any errors that occur.
        """
        super().__init__(error_handlers=error_handlers, timeout=timeout)
        if channel is None and stub is None:
            raise ValueError("Must provide either a channel or a stub")
        if stub is not None:
            self._stub = stub
        else:
            self._stub = NetworkConsumerStub(channel)

        self.__service = NetworkService()
        self.__network_hierarchy = None

    async def get_equipment_for_container(
        self,
        container: Union[str, EquipmentContainer],
        include_energizing_containers: IncludedEnergizingContainers = IncludedEnergizingContainers.NONE,
        include_energized_containers: IncludedEnergizedContainers = IncludedEnergizedContainers.NONE,
        network_state: NetworkState = NetworkState.NORMAL
    ) -> GrpcResult[MultiObjectResult]:
        """
        Retrieve the :class:`Equipment` for the :class:`EquipmentContainer` represented by `container`

        Exceptions that occur during retrieval will be caught and passed to all error handlers that have been registered against this client.

        Parameters
            - `container` - The :class:`EquipmentContainer` (or its mRID) to fetch equipment for.
            - `include_energizing_containers` - The level of energizing containers to include equipment from.
            - `include_energized_containers` - The level of energized containers to include equipment from.
            - `network_state` - The network state of the equipment.

        Returns a :class:`GrpcResult` with a result of one of the following:
            - When `GrpcResult.wasSuccessful`, a map containing the retrieved objects keyed by mRID, accessible via `GrpcResult.value`. If an item was not
              found, or couldn't be added to `service`, it will be excluded from the map and its mRID will be present in `MultiObjectResult.failed` (see
              `BaseService.add`).
            - When `GrpcResult.wasFailure`, the error that occurred retrieving or processing the object, accessible via `GrpcResult.thrown`.

        Note the :class:`NetworkConsumerClient` warning in this case.
        """
        return await self._get_equipment_for_container(container, include_energizing_containers, include_energized_containers, network_state)

    async def get_equipment_for_containers(
        self,
        containers: Iterable[str],
        include_energizing_containers: IncludedEnergizingContainers = IncludedEnergizingContainers.NONE,
        include_energized_containers: IncludedEnergizedContainers = IncludedEnergizedContainers.NONE,
        network_state: NetworkState = NetworkState.NORMAL
    ):
        """
        Retrieve the :class:`Equipment` for the :class:`EquipmentContainer`'s represented in `containers`

        Exceptions that occur during retrieval will be caught and passed to all error handlers that have been registered against this client.

        Parameters
            - `containers` - The mRIDs of :class:`EquipmentContainer`'s to fetch equipment for.
            - `include_energizing_containers` - The level of energizing containers to include equipment from.
            - `include_energized_containers` - The level of energized containers to include equipment from.
            - `network_state` - The network state of the equipment.

        Returns a :class:`GrpcResult` with a result of one of the following:
            - When `GrpcResult.wasSuccessful`, a map containing the retrieved objects keyed by mRID, accessible via `GrpcResult.value`. If an item was not
              found, or couldn't be added to `service`, it will be excluded from the map and its mRID will be present in `MultiObjectResult.failed` (see
              `BaseService.add`).
            - When `GrpcResult.wasFailure`, the error that occurred retrieving or processing the object, accessible via `GrpcResult.thrown`.

        Note the :class:`NetworkConsumerClient` warning in this case.
        """
        return await self._get_equipment_for_containers(containers, include_energizing_containers, include_energized_containers, network_state)

    async def get_equipment_for_restriction(self, restriction: [str, OperationalRestriction]) -> GrpcResult[MultiObjectResult]:
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
            - When `GrpcResult.wasFailure`, the error that occurred retrieving or processing the object, accessible via `GrpcResult.thrown`.

        Note the :class:`NetworkConsumerClient` warning in this case.
        """
        return await self._get_equipment_for_restriction(restriction)

    async def get_terminals_for_connectivity_node(self, node: [str, ConnectivityNode]) -> GrpcResult[MultiObjectResult]:
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
            - When `GrpcResult.wasFailure`, the error that occurred retrieving or processing the object, accessible via `GrpcResult.thrown`.

        Note the :class:`NetworkConsumerClient` warning in this case.
        """
        return await self._get_terminals_for_connectivity_node(node)

    async def get_network_hierarchy(self) -> GrpcResult[NetworkHierarchy]:
        """
        Retrieve the network hierarchy

        Parameters
            - `service` - The :class:`NetworkService` to store fetched objects in.

        Returns a simplified version of the network hierarchy that can be used to make further in-depth requests.
        """
        return await self._get_network_hierarchy()

    async def _run_get_metadata(self, request: GetMetadataRequest) -> GetMetadataResponse:
        return await self._stub.getMetadata(request, timeout=self.timeout)

    async def get_equipment_container(
        self,
        mrid: str,
        expected_class: type = EquipmentContainer,
        include_energizing_containers: IncludedEnergizingContainers = IncludedEnergizingContainers.NONE,
        include_energized_containers: IncludedEnergizedContainers = IncludedEnergizedContainers.NONE,
        network_state: NetworkState = NetworkState.NORMAL
    ) -> GrpcResult[MultiObjectResult]:
        """
        Retrieve the equipment container network for the specified `mrid` and store the results in the `service`.

        This is a convenience method that will fetch the container object and all of the equipment contained, along with all subsequent
        references. This should entail a complete connectivity model for the container, however not the connectivity between multiple containers.

        Parameters
            - `mrid` - The mRID of the :class:`EquipmentContainer` to fetch.
            - `expected_class` - The expected type of the fetched container.
            - `include_energizing_containers` - The level of energizing containers to include equipment from.
            - `include_energized_containers` - The level of energized containers to include equipment from.
            - `network_state` - The network state of the equipment.

        Returns a :class:`GrpcResult` of a :class:`MultiObjectResult`. If successful, containing a map keyed by mRID of all the objects retrieved. If an
        item couldn't be added to `service`, its mRID will be present in `MultiObjectResult.failed`.

        In addition to normal gRPC errors, you may also receive an unsuccessful :class:`GrpcResult` with the following errors:
            - :class:`ValueError` if the requested object was not found or was of the wrong type.

        """
        return await self._get_equipment_container(mrid, expected_class, include_energizing_containers, include_energized_containers, network_state)

    async def get_equipment_for_loop(self, loop: Union[str, Loop], network_state: NetworkState = NetworkState.NORMAL) -> GrpcResult[
        MultiObjectResult]:
        """
        Retrieve the :class:`Equipment` for the :class:`Loop` represented by `mRID`

        Exceptions that occur during retrieval will be caught and passed to all error handlers that have been registered against this client.

        Parameters
            - `service` - The :class:`NetworkService` to store fetched objects in.
            - `restriction` - The :class:`Loop` (or its mRID) to fetch equipment for.
            - `network_state` - The network state of the equipment.

        Returns a :class:`GrpcResult` with a result of one of the following:
            - When `GrpcResult.wasSuccessful`, a map containing the retrieved objects keyed by mRID, accessible via `GrpcResult.value`. If an item was not
              found, or couldn't be added to `service`, it will be excluded from the map and its mRID will be present in `MultiObjectResult.failed` (see
              `BaseService.add`).
            - When `GrpcResult.wasFailure`, the error that occurred retrieving or processing the object, accessible via `GrpcResult.thrown`.

        Note the :class:`NetworkConsumerClient` warning in this case.
        """
        return await self._get_equipment_for_loop(loop, network_state)

    async def get_all_loops(self, network_state: NetworkState = NetworkState.NORMAL) -> GrpcResult[MultiObjectResult]:
        """
        Retrieve the :class:`Equipment` for all :class:`Loop` instances in `service`.

        Exceptions that occur during retrieval will be caught and passed to all error handlers that have been registered against this client.

        Parameters
            - `service` - The :class:`NetworkService` to store fetched objects in.
            - `network_state` - The network state of the equipment.

        Returns a :class:`GrpcResult` with a result of one of the following:
            - When `GrpcResult.wasSuccessful`, a map containing the retrieved objects keyed by mRID, accessible via `GrpcResult.value`. If an item was not
              found, or couldn't be added to `service`, it will be excluded from the map and its mRID will be present in `MultiObjectResult.failed` (see
              `BaseService.add`).
            - When `GrpcResult.wasFailure`, the error that occurred retrieving or processing the object, accessible via `GrpcResult.thrown`.

        Note the :class:`NetworkConsumerClient` warning in this case.
        """
        return await self._get_all_loops(network_state)

    async def retrieve_network(self) -> GrpcResult[NetworkResult]:
        """
        Retrieve the entire network.
        Returns a GrpcResult containing the complete `NetworkService` from the server.
        """
        return await self._retrieve_network()

    async def _get_equipment_for_container(
        self,
        container: Union[str, EquipmentContainer],
        include_energizing_containers: IncludedEnergizingContainers = IncludedEnergizingContainers.NONE,
        include_energized_containers: IncludedEnergizedContainers = IncludedEnergizedContainers.NONE,
        network_state: NetworkState = NetworkState.NORMAL
    ) -> GrpcResult[MultiObjectResult]:
        return await self._handle_multi_object_rpc(
            lambda: self._process_equipment_for_container(container, include_energizing_containers, include_energized_containers, network_state)
        )

    async def _get_equipment_for_containers(
        self,
        containers: Iterable[str],
        include_energizing_containers: IncludedEnergizingContainers = IncludedEnergizingContainers.NONE,
        include_energized_containers: IncludedEnergizedContainers = IncludedEnergizedContainers.NONE,
        network_state: NetworkState = NetworkState.NORMAL
    ) -> GrpcResult[MultiObjectResult]:
        return await self._handle_multi_object_rpc(
            lambda: self._process_equipment_for_containers(containers, include_energizing_containers, include_energized_containers, network_state)
        )

    async def _get_equipment_for_restriction(self, restriction: [str, OperationalRestriction]) -> GrpcResult[MultiObjectResult]:
        return await self._handle_multi_object_rpc(lambda: self._process_equipment_for_restriction(restriction))

    async def _get_terminals_for_connectivity_node(self, node: [str, ConnectivityNode]) -> GrpcResult[MultiObjectResult]:
        return await self._handle_multi_object_rpc(lambda: self._process_terminals_for_connectivity_node(node))

    async def _get_network_hierarchy(self) -> GrpcResult[NetworkHierarchy]:
        if self.__network_hierarchy:
            # noinspection PyArgumentList
            return GrpcResult(self.__network_hierarchy)
        return await self.try_rpc(lambda: self._handle_network_hierarchy())

    async def _get_equipment_container(
        self,
        mrid: str,
        expected_class: type = EquipmentContainer,
        include_energizing_containers: IncludedEnergizingContainers = IncludedEnergizingContainers.NONE,
        include_energized_containers: IncludedEnergizedContainers = IncludedEnergizedContainers.NONE,
        network_state: NetworkState = NetworkState.NORMAL
    ) -> GrpcResult[MultiObjectResult]:
        async def get_additional(it: EquipmentContainer, mor: MultiObjectResult) -> Optional[GrpcResult[MultiObjectResult]]:
            result = await self._get_equipment_for_container(it, include_energizing_containers, include_energized_containers, network_state)

            if result.was_failure:
                # noinspection PyArgumentList
                return GrpcResult(result.thrown, result.was_error_handled)

            mor.objects.update(result.value.objects)
            return None

        return await self._get_with_references(mrid, expected_class, get_additional)

    async def _get_equipment_for_loop(self, loop: Union[str, Loop], network_state: NetworkState = NetworkState.NORMAL) -> GrpcResult[
        MultiObjectResult]:
        mrid = loop.mrid if isinstance(loop, Loop) else loop

        async def get_additional(it: Loop, mor: MultiObjectResult) -> Optional[GrpcResult[MultiObjectResult]]:
            mor.objects.update({cir.mrid: cir for cir in it.circuits})
            mor.objects.update({sub.mrid: sub for sub in it.substations})
            mor.objects.update({sub.mrid: sub for sub in it.energizing_substations})

            # `chain` infers the type as Circuit instead of EquipmentContainer, so provide a wrapper that forces the correct type.
            def chain_typed(*iterables: Iterable[EquipmentContainer]): return chain(*iterables)

            containers: Set[str] = {ec.mrid for ec in chain_typed(it.circuits, it.substations, it.energizing_substations)}
            result = await self._get_equipment_for_containers(containers, network_state=network_state)
            if result.was_failure:
                # noinspection PyArgumentList
                return GrpcResult(result.thrown, result.was_error_handled)

            mor.objects.update(result.value.objects)

            return None

        return await self._get_with_references(mrid, Loop, get_additional)

    async def _get_all_loops(self, network_state: NetworkState = NetworkState.NORMAL) -> GrpcResult[MultiObjectResult]:
        response = await self._get_network_hierarchy()
        if response.was_failure:
            # noinspection PyArgumentList
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
            containers.update(chain(cast(Iterable[EquipmentContainer], loop.circuits), loop.substations, loop.energizing_substations))

        result = await self._get_equipment_for_containers(map(lambda it: it.mrid, containers), network_state=network_state)
        if result.was_failure:
            # noinspection PyArgumentList
            return GrpcResult(result.thrown, result.was_error_handled)

        mor.objects.update(result.value.objects)

        error = await self._resolve_references(mor)
        if error:
            return error

        # noinspection PyArgumentList
        return GrpcResult(mor)

    async def _retrieve_network(self) -> GrpcResult[NetworkResult]:
        result = (await self._get_network_hierarchy()).throw_on_error()

        hierarchy: NetworkHierarchy = result.result
        failed = set()
        for mrid in chain(hierarchy.substations, hierarchy.feeders, hierarchy.circuits):
            result = await self._get_equipment_container(mrid)
            if result.was_successful:
                failed.update(result.result.failed)

        # noinspection PyArgumentList
        return GrpcResult(NetworkResult(self.service, failed))

    async def _process_equipment_for_container(
        self, it: Union[str, EquipmentContainer],
        include_energizing_containers: IncludedEnergizingContainers,
        include_energized_containers: IncludedEnergizedContainers,
        network_state: NetworkState = NetworkState.NORMAL
    ) -> AsyncGenerator[IdentifiedObject, None]:
        async for response in self._process_equipment_for_containers(
            [it.mrid if isinstance(it, EquipmentContainer) else it],
            include_energizing_containers,
            include_energized_containers,
            network_state
        ):
            yield response

    async def _process_equipment_for_containers(
        self,
        mrids: Iterable[str],
        include_energizing_containers: IncludedEnergizingContainers,
        include_energized_containers: IncludedEnergizedContainers,
        network_state: NetworkState = NetworkState.NORMAL
    ) -> AsyncGenerator[IdentifiedObject, None]:
        request = GetEquipmentForContainersRequest()
        request.includeEnergizingContainers = _map_include_energizing_containers.to_pb(include_energizing_containers)
        request.includeEnergizedContainers = _map_include_energized_containers.to_pb(include_energized_containers)
        request.networkState = _map_network_state.to_pb(network_state)
        responses = self._stub.getEquipmentForContainers(self._batch_send(request, mrids), timeout=self.timeout)
        async for response in responses:
            for nio in response.identifiedObjects:
                yield self._extract_identified_object("network", nio, _nio_type_to_cim)

    async def _process_equipment_for_restriction(self,
                                                 it: Union[str, OperationalRestriction]) -> AsyncGenerator[IdentifiedObject, None]:
        mrid = it.mrid if isinstance(it, OperationalRestriction) else it
        responses = self._stub.getEquipmentForRestriction(GetEquipmentForRestrictionRequest(mrid=mrid), timeout=self.timeout)
        async for response in responses:
            for nio in response.identifiedObjects:
                yield self._extract_identified_object("network", nio, _nio_type_to_cim)

    async def _process_terminals_for_connectivity_node(self,
                                                       it: Union[str, ConnectivityNode]) -> AsyncGenerator[IdentifiedObject, None]:
        mrid = it.mrid if isinstance(it, ConnectivityNode) else it
        responses = self._stub.getTerminalsForNode(GetTerminalsForNodeRequest(mrid=mrid), timeout=self.timeout)
        async for response in responses:
            # noinspection PyUnresolvedReferences
            yield self.service.get(response.terminal.mrid(), Terminal, default=None) or self.service.add_from_pb(response.terminal), response.terminal.mrid()

    async def _process_identified_objects(self, mrids: Iterable[str]) -> AsyncGenerator[Tuple[Optional[IdentifiedObject], str], None]:
        if not mrids:
            return

        responses = self._stub.getIdentifiedObjects(self._batch_send(GetIdentifiedObjectsRequest(), mrids), timeout=self.timeout)
        async for response in responses:
            for nio in response.identifiedObjects:
                yield self._extract_identified_object("network", nio, _nio_type_to_cim)

    async def _handle_network_hierarchy(self):
        response = await self._stub.getNetworkHierarchy(GetNetworkHierarchyRequest(), timeout=self.timeout)

        # noinspection PyArgumentList
        self.__network_hierarchy = NetworkHierarchy(
            self._to_map(response.geographicalRegions, GeographicalRegion),
            self._to_map(response.subGeographicalRegions, SubGeographicalRegion),
            self._to_map(response.substations, Substation),
            self._to_map(response.feeders, Feeder),
            self._to_map(response.circuits, Circuit),
            self._to_map(response.loops, Loop)
        )

        return self.__network_hierarchy

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

    async def _get_with_references(self,
                                   mrid: str,
                                   expected_class: type(Generic[CIM_IO]),
                                   get_additional: Callable[[Generic[CIM_IO], MultiObjectResult], Awaitable[Optional[GrpcResult[MultiObjectResult]]]]
                                   ) -> GrpcResult[MultiObjectResult]:
        if not self.__network_hierarchy:
            response = await self._get_network_hierarchy()
            if response.was_failure:
                # noinspection PyArgumentList
                return GrpcResult(response.thrown, response.was_error_handled)

        io = self.service.get(mrid, default=None)
        if not io:
            response = await self._get_identified_object(mrid)
            if response.was_failure:
                # noinspection PyArgumentList
                return GrpcResult(response.thrown, response.was_error_handled)

            io = response.value

        if not isinstance(io, expected_class):
            e = ValueError(f"Requested mrid {mrid} was not a {expected_class.__name__}, was {type(io).__name__}")
            # noinspection PyArgumentList
            return GrpcResult(e, self.try_handle_error(e))

        mor = MultiObjectResult()
        mor.objects[io.mrid] = io

        error = await get_additional(io, mor)
        if error:
            return error

        error = await self._resolve_references(mor)
        if error:
            return error

        # noinspection PyArgumentList
        return GrpcResult(mor)

    async def _resolve_references(self, mor: MultiObjectResult) -> Optional[GrpcResult[MultiObjectResult]]:
        res = mor
        keep_processing = True
        subsequent = False
        while keep_processing:
            to_resolve = set()
            for obj in res.objects:
                for ref in self.service.get_unresolved_references_from(obj):
                    # Skip any reference trying to resolve from an EquipmentContainer on subsequent passes - e.g a PowerTransformer trying to pull in its LvFeeder.
                    # EquipmentContainers should be retrieved explicitly or via a hierarchy call.
                    if subsequent and EquipmentContainer in ref.resolver.from_class.__bases__:
                        continue
                    # Skip any reference trying to resolve from an asset back to a PSR (e.g. Pole back to ConductingEquipment) on subsequent passes.
                    # Subsequent here is not currently necessary, but makes sure that if any future caller of this function starts by resolving
                    # from an Asset first, it will pull in the PSR.
                    if subsequent and Asset == ref.resolver.from_class and PowerSystemResource == ref.resolver.to_class:
                        continue
                    to_resolve.add(ref.to_mrid)

            response = await self._get_identified_objects(to_resolve)
            if response.was_failure:
                # noinspection PyArgumentList
                return GrpcResult(response.thrown, response.was_error_handled)

            res = response.value

            mor.objects.update(res.objects)
            mor.failed.update(res.failed)
            keep_processing = bool(res.objects)
            subsequent = True

        return None

    def _to_map(self, objects: Iterable[Generic[PB_IO]], class_: type(Generic[CIM_IO])) -> Dict[str, CIM_IO]:
        result = {}

        for pb in objects:
            # noinspection PyUnresolvedReferences
            cim = self.service.get(pb.mrid(), class_, None) or self.service.add_from_pb(pb)
            result[cim.mrid] = cim

        return result


class SyncNetworkConsumerClient(NetworkConsumerClient):
    """Synchronised wrapper for :class:`NetworkConsumerClient`"""

    def get_identified_object(self, mrid: str) -> GrpcResult[IdentifiedObject]:
        return get_event_loop().run_until_complete(super().get_identified_object(mrid))

    def get_identified_objects(self, mrids: Iterable[str]) -> GrpcResult[MultiObjectResult]:
        return get_event_loop().run_until_complete(super().get_identified_objects(mrids))

    def get_equipment_for_container(
        self,
        container: Union[str, EquipmentContainer],
        include_energizing_containers: IncludedEnergizingContainers = IncludedEnergizingContainers.NONE,
        include_energized_containers: IncludedEnergizedContainers = IncludedEnergizedContainers.NONE,
        network_state: NetworkState = NetworkState.NORMAL
    ) -> GrpcResult[MultiObjectResult]:
        return get_event_loop().run_until_complete(
            super().get_equipment_for_container(container, include_energizing_containers, include_energized_containers, network_state)
        )

    def get_equipment_for_containers(
        self,
        containers: Iterable[str],
        include_energizing_containers: IncludedEnergizingContainers = IncludedEnergizingContainers.NONE,
        include_energized_containers: IncludedEnergizedContainers = IncludedEnergizedContainers.NONE,
        network_state: NetworkState = NetworkState.NORMAL
    ) -> GrpcResult[MultiObjectResult]:
        return get_event_loop().run_until_complete(
            super().get_equipment_for_containers(containers, include_energizing_containers, include_energized_containers, network_state)
        )

    def get_equipment_for_restriction(self, mrid: str) -> GrpcResult[MultiObjectResult]:
        return get_event_loop().run_until_complete(super().get_equipment_for_restriction(mrid))

    def get_terminals_for_connectivity_node(self, mrid: str) -> GrpcResult[MultiObjectResult]:
        return get_event_loop().run_until_complete(super().get_terminals_for_connectivity_node(mrid))

    def get_network_hierarchy(self):
        return get_event_loop().run_until_complete(super().get_network_hierarchy())

    def get_feeder(self, mrid: str) -> GrpcResult[MultiObjectResult]:
        warnings.warn('`get_feeder` is deprecated, prefer the more generic `get_equipment_container`', DeprecationWarning)
        return get_event_loop().run_until_complete(super().get_equipment_container(mrid, Feeder))

    def get_equipment_container(
        self,
        mrid: str,
        expected_class: type = EquipmentContainer,
        include_energizing_containers: IncludedEnergizingContainers = IncludedEnergizingContainers.NONE,
        include_energized_containers: IncludedEnergizedContainers = IncludedEnergizedContainers.NONE,
        network_state: NetworkState = NetworkState.NORMAL
    ) -> GrpcResult[MultiObjectResult]:
        return get_event_loop().run_until_complete(
            super().get_equipment_container(mrid, expected_class, include_energizing_containers, include_energized_containers, network_state)
        )

    def get_equipment_for_loop(self, loop: Union[str, Loop], network_state: NetworkState = NetworkState.NORMAL) -> GrpcResult[MultiObjectResult]:
        # noinspection PyArgumentList
        return get_event_loop().run_until_complete(super().get_equipment_for_loop(self, loop, network_state))

    def get_all_loops(self, network_state: NetworkState = NetworkState.NORMAL) -> GrpcResult[MultiObjectResult]:
        # noinspection PyArgumentList
        return get_event_loop().run_until_complete(super().get_all_loops(self, network_state))

    def retrieve_network(self) -> GrpcResult[Union[NetworkResult, Exception]]:
        return get_event_loop().run_until_complete(super().retrieve_network())

    def get_metadata(self) -> GrpcResult[ServiceInfo]:
        return get_event_loop().run_until_complete(super().get_metadata())


_nio_type_to_cim = {
    ##################################
    # Extensions IEC61968 Asset Info #
    ##################################

    "relayInfo": RelayInfo,

    ################################
    # Extensions IEC61968 Metering #
    ################################

    "panDemandResponseFunction": PanDemandResponseFunction,

    #################################
    # Extensions IEC61970 Base Core #
    #################################

    "site": Site,

    ###################################
    # Extensions IEC61970 Base Feeder #
    ###################################

    "loop": Loop,
    "lvFeeder": LvFeeder,

    ##################################################
    # Extensions IEC61970 Base Generation Production #
    ##################################################

    "evChargingUnit": EvChargingUnit,

    #######################################
    # Extensions IEC61970 Base Protection #
    #######################################

    "distanceRelay": DistanceRelay,
    "protectionRelayScheme": ProtectionRelayScheme,
    "protectionRelaySystem": ProtectionRelaySystem,
    "voltageRelay": VoltageRelay,

    ##################################
    # Extensions IEC61970 Base Wires #
    ##################################

    "batteryControl": BatteryControl,

    #######################
    # IEC61968 Asset Info #
    #######################

    "cableInfo": CableInfo,
    "noLoadTest": NoLoadTest,
    "openCircuitTest": OpenCircuitTest,
    "overheadWireInfo": OverheadWireInfo,
    "powerTransformerInfo": PowerTransformerInfo,
    "shortCircuitTest": ShortCircuitTest,
    "shuntCompensatorInfo": ShuntCompensatorInfo,
    "switchInfo": SwitchInfo,
    "transformerEndInfo": TransformerEndInfo,
    "transformerTankInfo": TransformerTankInfo,

    ###################
    # IEC61968 Assets #
    ###################

    "assetOwner": AssetOwner,

    ###################
    # IEC61968 Common #
    ###################

    "organisation": Organisation,
    "location": Location,
    "streetlight": Streetlight,

    #####################################
    # IEC61968 InfIEC61968 InfAssetInfo #
    #####################################

    "currentTransformerInfo": CurrentTransformerInfo,
    "potentialTransformerInfo": PotentialTransformerInfo,

    ##################################
    # IEC61968 InfIEC61968 InfAssets #
    ##################################

    "pole": Pole,

    #####################
    # IEC61968 Metering #
    #####################

    "meter": Meter,
    "usagePoint": UsagePoint,

    #######################
    # IEC61968 Operations #
    #######################

    "operationalRestriction": OperationalRestriction,

    #####################################
    # IEC61970 Base Auxiliary Equipment #
    #####################################

    "currentTransformer": CurrentTransformer,
    "faultIndicator": FaultIndicator,
    "potentialTransformer": PotentialTransformer,

    ######################
    # IEC61970 Base Core #
    ######################

    "baseVoltage": BaseVoltage,
    "connectivityNode": ConnectivityNode,
    "feeder": Feeder,
    "geographicalRegion": GeographicalRegion,
    "subGeographicalRegion": SubGeographicalRegion,
    "substation": Substation,
    "terminal": Terminal,

    #############################
    # IEC61970 Base Equivalents #
    #############################

    "equivalentBranch": EquivalentBranch,

    #######################################
    # IEC61970 Base Generation Production #
    #######################################

    "batteryUnit": BatteryUnit,
    "photoVoltaicUnit": PhotoVoltaicUnit,
    "powerElectronicsWindUnit": PowerElectronicsWindUnit,

    ######################
    # IEC61970 Base Meas #
    ######################

    "accumulator": Accumulator,
    "analog": Analog,
    "control": Control,
    "discrete": Discrete,

    ############################
    # IEC61970 Base Protection #
    ############################

    "currentRelay": CurrentRelay,

    #######################
    # IEC61970 Base Scada #
    #######################

    "remoteControl": RemoteControl,
    "remoteSource": RemoteSource,

    #######################
    # IEC61970 Base Wires #
    #######################

    "acLineSegment": AcLineSegment,
    "breaker": Breaker,
    "busbarSection": BusbarSection,
    "clamp": Clamp,
    "cut": Cut,
    "disconnector": Disconnector,
    "energyConsumer": EnergyConsumer,
    "energyConsumerPhase": EnergyConsumerPhase,
    "energySource": EnergySource,
    "energySourcePhase": EnergySourcePhase,
    "fuse": Fuse,
    "ground": Ground,
    "groundDisconnector": GroundDisconnector,
    "groundingImpedance": GroundingImpedance,
    "jumper": Jumper,
    "junction": Junction,
    "linearShuntCompensator": LinearShuntCompensator,
    "loadBreakSwitch": LoadBreakSwitch,
    "perLengthPhaseImpedance": PerLengthPhaseImpedance,
    "perLengthSequenceImpedance": PerLengthSequenceImpedance,
    "petersenCoil": PetersenCoil,
    "powerElectronicsConnection": PowerElectronicsConnection,
    "powerElectronicsConnectionPhase": PowerElectronicsConnectionPhase,
    "powerTransformer": PowerTransformer,
    "powerTransformerEnd": PowerTransformerEnd,
    "ratioTapChanger": RatioTapChanger,
    "reactiveCapabilityCurve": ReactiveCapabilityCurve,
    "recloser": Recloser,
    "seriesCompensator": SeriesCompensator,
    "staticVarCompensator": StaticVarCompensator,
    "synchronousMachine": SynchronousMachine,
    "tapChangerControl": TapChangerControl,
    "transformerStarImpedance": TransformerStarImpedance,

    ###############################
    # IEC61970 InfIEC61970 Feeder #
    ###############################

    "circuit": Circuit,
}
