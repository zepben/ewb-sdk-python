#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ["DiagramConsumerClient", "SyncDiagramConsumerClient"]

from asyncio import get_event_loop
from dataclasses import dataclass
from typing import Optional, Iterable, AsyncGenerator, List, Callable, Tuple, Union

from zepben.ewb.dataslot import custom_len, MRIDListRouter, MRIDDictRouter, boilermaker, TypeRestrictedDescriptor, WeakrefDescriptor, dataslot, BackedDescriptor, ListAccessor, ValidatedDescriptor, MRIDListAccessor, custom_get, custom_remove, override_boilerplate, ListActions, MRIDDictAccessor, BackingValue, custom_clear, custom_get_by_mrid, custom_add, NoResetDescriptor, ListRouter, validate
from typing_extensions import deprecated
from zepben.protobuf.dc.dc_pb2_grpc import DiagramConsumerStub
from zepben.protobuf.dc.dc_requests_pb2 import GetIdentifiedObjectsRequest, GetDiagramObjectsRequest
from zepben.protobuf.metadata.metadata_requests_pb2 import GetMetadataRequest
from zepben.protobuf.metadata.metadata_responses_pb2 import GetMetadataResponse

from zepben.ewb import DiagramService, IdentifiedObject, ServiceInfo
from zepben.ewb.model.cim.iec61970.base.diagramlayout.diagram import Diagram
from zepben.ewb.model.cim.iec61970.base.diagramlayout.diagram_object import DiagramObject
from zepben.ewb.streaming.get.consumer import CimConsumerClient, MultiObjectResult
from zepben.ewb.streaming.grpc.grpc import GrpcResult

@dataclass
class DiagramConsumerClient(CimConsumerClient[DiagramService]):
    """
    Consumer client for a :class:`DiagramService`.

    ## WARNING ##
        The :class:`MultiObjectResult` operations below are not atomic upon a :class:`DiagramService`, and thus if processing fails partway through, any
        previously successful additions will have been processed by the service, and thus you may have an incomplete service. Also note that adding to the
        service may not occur for an object if another object with the same mRID is already present in service. `MultiObjectResult.failed` can be used to
        check for mRIDs that were not found or retrieved but not added to service (this should not be the case unless you are processing things concurrently).
    """

    __service: DiagramService = None

    @property
    def service(self) -> DiagramService:
        return self.__service

    _stub: DiagramConsumerStub = None

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

    async def _process_diagram_objects(self, mrids: Iterable[str]) -> AsyncGenerator[Tuple[IdentifiedObject | None, str], None]:
        if not mrids:
            return

        responses = self._stub.getDiagramObjects(self._batch_send(GetDiagramObjectsRequest(), mrids), timeout=self.timeout)
        async for response in responses:
            for dio in response.identifiedObjects:
                yield self._extract_identified_object("diagram", dio, _dio_type_to_cim)

    async def _process_identified_objects(self, mrids: Iterable[str]) -> AsyncGenerator[Tuple[IdentifiedObject | None, str], None]:
        if not mrids:
            return

        responses = self._stub.getIdentifiedObjects(self._batch_send(GetIdentifiedObjectsRequest(), mrids), timeout=self.timeout)
        async for response in responses:
            for dio in response.identifiedObjects:
                yield self._extract_identified_object("diagram", dio, _dio_type_to_cim)


@dataclass
class SyncDiagramConsumerClient(DiagramConsumerClient):

    def get_identified_object(self, mrid: str) -> GrpcResult[IdentifiedObject | None]:
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
