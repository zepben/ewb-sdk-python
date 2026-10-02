#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["VariantConsumerClient", "SyncVariantConsumerClient"]

import datetime
from asyncio import get_event_loop
from typing import AsyncGenerator, Callable, Iterable, List, Optional, Tuple

from zepben.protobuf.metadata.metadata_requests_pb2 import GetMetadataRequest
from zepben.protobuf.metadata.metadata_responses_pb2 import GetMetadataResponse
from zepben.protobuf.vc.vc_pb2_grpc import VariantConsumerStub
from zepben.protobuf.vc.vc_requests_pb2 import GetChangeSetRequest, GetIdentifiedObjectsRequest, GetNetworkModelProjectsRequest

from zepben.ewb import datetime_to_timestamp
from zepben.ewb.model.cim.iec61970.base.core.identifiable import Identifiable
from zepben.ewb.services.variant.variant_service import VariantService
from zepben.ewb.services.variant.translator import variant_cim2proto  # noqa: F401  (applies the pb `mrid()` extensions)
from zepben.ewb.services.variant.translator.variant_proto2cim import add_from_pb
from zepben.ewb.streaming.get.consumer import CimConsumerClient, MultiObjectResult
from zepben.ewb.streaming.grpc.grpc import GrpcResult

# noinspection PyUnresolvedReferences
from zepben.ewb.services.variant.translator import variant_pb_extensions  # noqa: F401


class VariantConsumerClient(CimConsumerClient[VariantService, VariantConsumerStub]):
    """
    Consumer client for a :class:`VariantService`.

    ## WARNING ##
        The :class:`MultiObjectResult` operations below are not atomic upon a :class:`VariantService`, and thus if processing fails partway through, any
        previously successful additions will have been processed by the service, and thus you may have an incomplete service. Also note that adding to the
        service may not occur for an object if another object with the same mRID is already present in service. `MultiObjectResult.failed` can be used to
        check for mRIDs that were not found or retrieved but not added to service (this should not be the case unless you are processing things concurrently).
    """

    __service: VariantService

    @property
    def service(self) -> VariantService:
        return self.__service

    def __init__(self, channel=None, stub: VariantConsumerStub = None, variant_service: Optional[VariantService] = None,
                 error_handlers: List[Callable[[Exception], bool]] = None, timeout: int = 60):
        """
        :param channel: a gRPC channel used to create a stub if no stub is provided.
        :param stub: the gRPC stub to use for this consumer client.
        :param variant_service: the :class:`VariantService` to store retrieved objects in.
        :param error_handlers: a collection of handlers to be processed for any errors that occur.
        """
        if stub is not None:
            super().__init__(error_handlers=error_handlers, timeout=timeout, stub=stub)
        elif channel is not None:
            super().__init__(error_handlers=error_handlers, timeout=timeout, stub=VariantConsumerStub(channel))
        else:
            raise ValueError("Must provide either a channel or a stub")

        self.__service = variant_service or VariantService()

    async def get_change_set(self, mrid: str, base_model_version: Optional[datetime.date] = None) -> GrpcResult[MultiObjectResult]:
        """
        Retrieve a :class:`ChangeSet` and all its associations from the server. See :meth:`get_change_sets` documentation.
        """
        return await self.get_change_sets([mrid], base_model_version)

    async def get_change_sets(self, mrids: Iterable[str], base_model_version: Optional[datetime.date] = None) -> GrpcResult[MultiObjectResult]:
        """
        Retrieve a :class:`ChangeSet` and all its associations from the server. This does not receive the contents of the ChangeSet, only the metadata.
        To retrieve the contents you should use :meth:`ChangeSetConsumerClient.get_change_set`, which will call this function for you.

        :param mrids: The mRIDs of the :class:`ChangeSet`s to retrieve.
        :param base_model_version: The base model version to retrieve the change set against.
        :return: A :class:`GrpcResult` of a :class:`MultiObjectResult`. If successful, containing a map keyed by mRID of all the objects retrieved. If an
            item was not found, or couldn't be added to `service`, it will be excluded from the map and its mRID will be present in `MultiObjectResult.failed`
        """
        async def rpc() -> MultiObjectResult:
            mor = MultiObjectResult()
            for mrid in mrids:
                request = GetChangeSetRequest(changeSetMRID=mrid)
                if base_model_version is not None:
                    # noinspection PyTypeChecker
                    request.modelVersion = datetime_to_timestamp(datetime.datetime.combine(base_model_version, datetime.time.min))
                responses = self._stub.getChangeSet(request, timeout=self.timeout)
                async for response in responses:
                    result = add_from_pb(response.identifiableObject, self.service)
                    if result.identifiable is not None:
                        mor.objects[result.mrid] = result.identifiable
                    else:
                        mor.failed.add(result.mrid)

            resolved = await self._resolve_references(mor)
            if resolved is not None:
                return resolved
            return mor

        return await self.try_rpc(rpc)

    async def get_network_model_projects(self) -> GrpcResult[MultiObjectResult]:
        """
        Retrieve all :class:`NetworkModelProject`s from the server.
        """
        async def rpc() -> MultiObjectResult:
            return await self._process_extract_results(None, self._process_network_model_projects(None))

        return await self.try_rpc(rpc)

    async def get_network_model_project(self, mrid: str) -> GrpcResult[Identifiable]:
        """
        Retrieve the :class:`NetworkModelProject` with the given `mrid` from the server.
        """
        async def rpc() -> Identifiable:
            async for identifiable, _ in self._process_network_model_projects([mrid]):
                if identifiable is not None:
                    return identifiable
            raise ValueError(f"No object with mRID {mrid} could be found.")

        return await self.try_rpc(rpc)

    async def _process_network_model_projects(self, mrids: Optional[Iterable[str]] = None) -> AsyncGenerator[Tuple[Identifiable | None, str], None]:
        request = GetNetworkModelProjectsRequest()
        if mrids is None:
            responses = self._stub.getNetworkModelProjects(iter([request]), timeout=self.timeout)
        else:
            responses = self._stub.getNetworkModelProjects(self._batch_send(request, mrids), timeout=self.timeout)
        async for response in responses:
            for pb_nmp in response.networkModelProjects:
                cim = self.service.get(pb_nmp.mrid(), default=None) or self.service.add_from_pb(pb_nmp)
                yield (cim, pb_nmp.mrid()) if cim is not None else (None, pb_nmp.mrid())

    async def _run_get_metadata(self, request: GetMetadataRequest) -> GetMetadataResponse:
        return await self._stub.getMetadata(request, timeout=self.timeout)

    async def _process_identifiables(self, mrids: Iterable[str]) -> AsyncGenerator[Tuple[Identifiable | None, str], None]:
        if not mrids:
            return
        responses = self._stub.getIdentifiedObjects(self._batch_send(GetIdentifiedObjectsRequest(), mrids), timeout=self.timeout)
        async for response in responses:
            for io in response.identifiableObjects:
                result = add_from_pb(io, self.service)
                yield (result.identifiable, result.mrid)

    async def _resolve_references(self, mor: MultiObjectResult) -> Optional[GrpcResult[MultiObjectResult]]:
        res = mor
        while True:
            to_resolve = {
                ref.to_mrid
                for mrid in res.objects
                for ref in self.service.get_unresolved_references_from(mrid)
            }
            if not to_resolve:
                return None
            res = (await self.get_identifiables(to_resolve)).on_error(
                lambda thrown, was_handled: GrpcResult(thrown, was_handled)
            ).value
            mor.objects.update(res.objects)


class SyncVariantConsumerClient(VariantConsumerClient):
    """Synchronised wrapper for :class:`VariantConsumerClient`"""

    def get_change_set(self, mrid: str, base_model_version: Optional[datetime.date] = None) -> GrpcResult[MultiObjectResult]:
        return get_event_loop().run_until_complete(super().get_change_set(mrid, base_model_version))

    def get_change_sets(self, mrids: Iterable[str], base_model_version: Optional[datetime.date] = None) -> GrpcResult[MultiObjectResult]:
        return get_event_loop().run_until_complete(super().get_change_sets(mrids, base_model_version))

    def get_network_model_projects(self) -> GrpcResult[MultiObjectResult]:
        return get_event_loop().run_until_complete(super().get_network_model_projects())

    def get_network_model_project(self, mrid: str) -> GrpcResult[Identifiable]:
        return get_event_loop().run_until_complete(super().get_network_model_project(mrid))
