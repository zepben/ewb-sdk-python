#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations

from asyncio import get_event_loop
from typing import Optional, Iterable, AsyncGenerator, List, Callable, Tuple

from zepben.protobuf.dc.dc_data_pb2 import DiagramIdentifiedObject
from zepben.protobuf.dc.dc_pb2_grpc import DiagramConsumerStub
from zepben.protobuf.dc.dc_requests_pb2 import GetIdentifiedObjectsRequest

from zepben.evolve import DiagramService, IdentifiedObject, UnsupportedOperationException, Diagram, DiagramObject
from zepben.evolve.streaming.get.consumer import CimConsumerClient, MultiObjectResult
from zepben.evolve.streaming.grpc.grpc import GrpcResult

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

    _stub: DiagramConsumerStub = None

    def __init__(self, channel=None, stub: DiagramConsumerStub = None, error_handlers: List[Callable[[Exception], bool]] = None):
        super().__init__(error_handlers=error_handlers)
        if channel is None and stub is None:
            raise ValueError("Must provide either a channel or a stub")
        if stub is not None:
            self._stub = stub
        else:
            self._stub = DiagramConsumerStub(channel)

    async def get_identified_object(self, service: DiagramService, mrid: str) -> GrpcResult[IdentifiedObject]:
        """
        Retrieve the object with the given `mRID` and store the result in the `service`.

        Exceptions that occur during sending will be caught and passed to all error handlers that have been registered.

        Parameters
            - `service` - The :class:`DiagramService` to store fetched objects in.
            - `mRID` - The mRID to retrieve.

        Returns a :class:`GrpcResult` with a result of one of the following:
            - When `GrpcResult.wasSuccessful`, the item found, accessible via `GrpcResult.value`.
            - When `GrpcResult.wasFailure`, the error that occurred retrieving or processing the the object, accessible via `GrpcResult.thrown`. One of:
                - :class:`NoSuchElementException` if the object could not be found.
                - The gRPC error that occurred while retrieving the object
        """
        return await self._get_identified_object(service, mrid)

    async def get_identified_objects(self, service: DiagramService, mrids: Iterable[str]) -> GrpcResult[MultiObjectResult]:
        """
        Retrieve the objects with the given [mRIDs] and store the results in the [service].

        Exceptions that occur during processing will be caught and passed to all error handlers that have been registered.

        Parameters
            - `service` - The :class:`DiagramService` to store fetched objects in.
            - `mRIDs` - The mRIDs to retrieve.

        Returns a :class:`GrpcResult` with a result of one of the following:
            - When `GrpcResult.wasSuccessful`, a map containing the retrieved objects keyed by mRID, accessible via `GrpcResult.value`. If an item was not
              found, or couldn't be added to `service`, it will be excluded from the map and its mRID will be present in `MultiObjectResult.failed` (see
              `BaseService.add`).
            - When `GrpcResult.wasFailure`, the error that occurred retrieving or processing the the object, accessible via `GrpcResult.thrown`.

        Note the :class:`DiagramConsumerClient` warning in this case.
        """
        return await self._get_identified_objects(service, mrids)

    async def _get_identified_object(self, service: DiagramService, mrid: str) -> GrpcResult[Optional[IdentifiedObject]]:
        async def rpc():
            async for io, _ in self._process_identified_objects(service, [mrid]):
                return io
            else:
                raise ValueError(f"No object with mRID {mrid} could be found.")

        return await self.try_rpc(rpc)

    async def _get_identified_objects(self, service: DiagramService, mrids: Iterable[str]) -> GrpcResult[MultiObjectResult]:
        return await self.try_rpc(lambda: self._process_extract_results(mrids, self._process_identified_objects(service, set(mrids))))

    async def _process_identified_objects(self, service: DiagramService, mrids: Iterable[str]) -> AsyncGenerator[Tuple[Optional[IdentifiedObject], str], None]:
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


class SyncDiagramConsumerClient(DiagramConsumerClient):

    def get_identified_object(self, service: DiagramService, mrid: str) -> GrpcResult[Optional[IdentifiedObject]]:
        return get_event_loop().run_until_complete(super().get_identified_objects(service, mrid))

    def get_identified_objects(self, service: DiagramService, mrids: Iterable[str]) -> GrpcResult[MultiObjectResult]:
        return get_event_loop().run_until_complete(super().get_identified_objects(service, mrids))


def _extract_identified_object(service: DiagramService, dio: DiagramIdentifiedObject, check_presence: bool = True) -> Tuple[Optional[IdentifiedObject], str]:
    """
    Add a :class:`DiagramIdentifiedObject` to the service. Will convert from protobuf to CIM type.

    Parameters
        - `service` - The :class:`DiagramService` to add the identified object to.
        - `dio` - The :class:`DiagramIdentifiedObject` returned by the server.
        - `check_presence` - Whether to check if `dio` already exists in the service and skip if it does.

    Raises :class:`UnsupportedOperationException` if `dio` was invalid/unset.
    """
    io_type = dio.WhichOneof("identifiedObject")
    if io_type:
        cim_type = _dio_type_to_cim.get(io_type, None)
        if cim_type is None:
            raise UnsupportedOperationException(f"Identified object type '{io_type}' is not supported by the diagram service")

        pb = getattr(dio, io_type)
        if check_presence:
            cim = service.get(pb.mrid(), cim_type, default=None)
            if cim is not None:
                return cim, cim.mrid

        # noinspection PyUnresolvedReferences
        return service.add_from_pb(pb), pb.mrid()
    else:
        raise UnsupportedOperationException(f"Received a DiagramIdentifiedObject where no field was set")


_dio_type_to_cim = {
    "diagram": Diagram,
    "diagramObject": DiagramObject
}
