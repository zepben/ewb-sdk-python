#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations

from asyncio import get_event_loop
from typing import Optional, Iterable, AsyncGenerator, List, Callable, Tuple, Union

from zepben.evolve import DiagramService, IdentifiedObject, Diagram, DiagramObject, ServiceInfo
from zepben.evolve.streaming.get.consumer import CimConsumerClient, MultiObjectResult
from zepben.evolve.streaming.grpc.grpc import GrpcResult
from zepben.protobuf.dc.dc_pb2_grpc import DiagramConsumerStub
from zepben.protobuf.dc.dc_requests_pb2 import GetIdentifiedObjectsRequest, GetDiagramObjectsRequest
from zepben.protobuf.metadata.metadata_requests_pb2 import GetMetadataRequest
from zepben.protobuf.metadata.metadata_responses_pb2 import GetMetadataResponse

__all__ = ["DiagramConsumerClient", "SyncDiagramConsumerClient"]


class DiagramConsumerClient(CimConsumerClient[DiagramService]):
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

    _stub: DiagramConsumerStub = None

    def __init__(self, channel=None, stub: DiagramConsumerStub = None, error_handlers: List[Callable[[Exception], bool]] = None, timeout: int = 60):
        super().__init__(error_handlers=error_handlers, timeout=timeout)
        if channel is None and stub is None:
            raise ValueError("Must provide either a channel or a stub")
        if stub is not None:
            self._stub = stub
        else:
            self._stub = DiagramConsumerStub(channel)

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

    async def _process_diagram_objects(self, mrids: Iterable[str]) -> AsyncGenerator[Tuple[Optional[IdentifiedObject], str], None]:
        if not mrids:
            return

        responses = self._stub.getDiagramObjects(self._batch_send(GetDiagramObjectsRequest(), mrids), timeout=self.timeout)
        async for response in responses:
            for dio in response.identifiedObjects:
                yield self._extract_identified_object("diagram", dio, _dio_type_to_cim)

    async def _process_identified_objects(self, mrids: Iterable[str]) -> AsyncGenerator[Tuple[Optional[IdentifiedObject], str], None]:
        if not mrids:
            return

        responses = self._stub.getIdentifiedObjects(self._batch_send(GetIdentifiedObjectsRequest(), mrids), timeout=self.timeout)
        async for response in responses:
            for dio in response.identifiedObjects:
                yield self._extract_identified_object("diagram", dio, _dio_type_to_cim)


class SyncDiagramConsumerClient(DiagramConsumerClient):

    def get_identified_object(self, mrid: str) -> GrpcResult[Optional[IdentifiedObject]]:
        return get_event_loop().run_until_complete(super()._get_identified_objects(mrid))

    def get_identified_objects(self, mrids: Iterable[str]) -> GrpcResult[MultiObjectResult]:
        return get_event_loop().run_until_complete(super()._get_identified_objects(mrids))

    def get_diagram_objects(self, mrid: Union[str, Iterable[str]]) -> GrpcResult[MultiObjectResult]:
        return get_event_loop().run_until_complete(super()._get_diagram_objects(mrid))

    def get_metadata(self) -> GrpcResult[ServiceInfo]:
        return get_event_loop().run_until_complete(super().get_metadata())


_dio_type_to_cim = {
    "diagram": Diagram,
    "diagramObject": DiagramObject
}
