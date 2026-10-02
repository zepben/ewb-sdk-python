#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["DiagramConsumerClient", "SyncDiagramConsumerClient"]

from asyncio import get_event_loop
from datetime import date, datetime, time
from typing import Iterable, AsyncGenerator, List, Callable, Tuple, Union, Optional

from zepben.protobuf.dc.dc_pb2_grpc import DiagramConsumerStub
from zepben.protobuf.dc.dc_requests_pb2 import GetIdentifiablesRequest, GetDiagramObjectsRequest, GetChangeSetObjectsRequest
from zepben.protobuf.metadata.metadata_requests_pb2 import GetMetadataRequest
from zepben.protobuf.metadata.metadata_responses_pb2 import GetMetadataResponse
from zepben.protobuf.vc.vc_data_pb2 import VariantContents as PBVariantContents

from zepben.ewb import DiagramService, ServiceInfo, datetime_to_timestamp
from zepben.ewb.database.paths.database_type import VariantContents
from zepben.ewb.model.cim.iec61970.base.core.identifiable import Identifiable
from zepben.ewb.model.cim.iec61970.base.diagramlayout.diagram import Diagram
from zepben.ewb.model.cim.iec61970.base.diagramlayout.diagram_object import DiagramObject
from zepben.ewb.services.common.enum_mapper import EnumMapper
from zepben.ewb.streaming.get.consumer import CimConsumerClient, MultiObjectResult
from zepben.ewb.streaming.grpc.grpc import GrpcResult

_map_variant_contents = EnumMapper(VariantContents, PBVariantContents)


class DiagramConsumerClient(CimConsumerClient[DiagramService, DiagramConsumerStub]):
    """
    Consumer client for a :class:`DiagramService`.

    ## WARNING ##
        The :class:`MultiObjectResult` operations below are not atomic upon a :class:`DiagramService`, and thus if processing fails partway through, any
        previously successful additions will have been processed by the service, and thus you may have an incomplete service. Also note that adding to the
        service may not occur for an object if another object with the same mRID is already present in service. `MultiObjectResult.failed` can be used to
        check for mRIDs that were not found or retrieved but not added to service (this should not be the case unless you are processing things concurrently).
    """

    __service: DiagramService

    @property
    def service(self) -> DiagramService:
        return self.__service

    def __init__(self, channel=None, stub: DiagramConsumerStub = None, error_handlers: List[Callable[[Exception], bool]] = None, timeout: int = 60):
        if stub is not None:
            super().__init__(error_handlers=error_handlers, timeout=timeout, stub=stub)
        elif channel is not None:
            super().__init__(error_handlers=error_handlers, timeout=timeout, stub=DiagramConsumerStub(channel))
        else:
            raise ValueError("Must provide either a channel or a stub")

        self.__service = DiagramService()

    async def get_diagram_objects(self, mrids: Union[str, Iterable[str]]) -> GrpcResult[MultiObjectResult]:
        return await self._get_diagram_objects(mrids)

    async def _run_get_metadata(self, request: GetMetadataRequest) -> GetMetadataResponse:
        return await self._stub.getMetadata(request, timeout=self.timeout)

    async def _get_diagram_objects(self, mrids: Union[str, Iterable[str]]) -> GrpcResult[MultiObjectResult]:
        async def rpc():
            if isinstance(mrids, str):
                return await self._process_extract_results(None, self._process_diagram_objects({mrids}))
            else:
                return await self._process_extract_results(None, self._process_diagram_objects(mrids))

        return await self.try_rpc(rpc)

    async def _process_diagram_objects(self, mrids: Iterable[str]) -> AsyncGenerator[Tuple[Identifiable | None, str], None]:
        if not mrids:
            return

        responses = self._stub.getDiagramObjects(self._batch_send(GetDiagramObjectsRequest(), mrids), timeout=self.timeout)
        async for response in responses:
            for dio in response.identifiables:
                yield self._extract_identifiable("diagram", dio, _dio_type_to_cim)

    async def _process_identifiables(self, mrids: Iterable[str]) -> AsyncGenerator[Tuple[Identifiable | None, str], None]:
        if not mrids:
            return

        responses = self._stub.getIdentifiables(self._batch_send(GetIdentifiablesRequest(), mrids), timeout=self.timeout)
        async for response in responses:
            for dio in response.identifiables:
                yield self._extract_identifiable("diagram", dio, _dio_type_to_cim)

    async def get_change_set_objects(self, mrid: str, variant_contents: VariantContents,
                                     base_model_version: Optional[date] = None) -> GrpcResult[DiagramService]:
        """
        Retrieve the diagram contents of a :class:`ChangeSet` from the server.
        This will return a new :class:`DiagramService` with just the diagram related contents of the :class:`ChangeSet`.
        Note this function does not populate `service` as merging a :class:`ChangeSet` with a :class:`DiagramService` should use `ChangeSetServices`.

        :param mrid: The mRID of the :class:`ChangeSet` to retrieve contents for.
        :param variant_contents: The contents to retrieve from the server.
        :param base_model_version: The base model version to retrieve the change set contents against.
        :return: A :class:`GrpcResult` of a :class:`DiagramService`.
        """
        async def rpc() -> DiagramService:
            diagram_service = DiagramService()
            request = GetChangeSetObjectsRequest(changeSetMRID=mrid, variantContents=_map_variant_contents.to_pb(variant_contents))
            if base_model_version is not None:
                request.modelVersion = datetime_to_timestamp(datetime.combine(base_model_version, time.min))
            responses = self._stub.getChangeSetObjects(request, timeout=self.timeout)
            async for response in responses:
                diagram_service.add_from_pb(response.identifiableObject)
            return diagram_service

        return await self.try_rpc(rpc)


class SyncDiagramConsumerClient(DiagramConsumerClient):

    def get_identifiable(self, mrid: str) -> GrpcResult[Identifiable | None]:
        return get_event_loop().run_until_complete(super()._get_identifiable(mrid))

    def get_identifiables(self, mrids: Iterable[str]) -> GrpcResult[MultiObjectResult]:
        return get_event_loop().run_until_complete(super()._get_identifiables(mrids))

    def get_diagram_objects(self, mrid: Union[str, Iterable[str]]) -> GrpcResult[MultiObjectResult]:
        return get_event_loop().run_until_complete(super()._get_diagram_objects(mrid))

    def get_metadata(self) -> GrpcResult[ServiceInfo]:
        return get_event_loop().run_until_complete(super().get_metadata())


_dio_type_to_cim = {
    "diagram": Diagram,
    "diagramObject": DiagramObject
}
