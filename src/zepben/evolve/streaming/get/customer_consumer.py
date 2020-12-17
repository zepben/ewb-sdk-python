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
from typing import Optional, Iterable, AsyncGenerator, List, Callable

from zepben.evolve import CustomerService, IdentifiedObject
from zepben.evolve.streaming.get.consumer import CimConsumerClient, MultiObjectResult, extract_identified_object
from zepben.evolve.streaming.grpc.grpc import GrpcResult
from zepben.protobuf.cc.cc_pb2_grpc import CustomerConsumerStub
from zepben.protobuf.cc.cc_requests_pb2 import GetIdentifiedObjectsRequest

__all__ = ["CustomerConsumerClient", "SyncCustomerConsumerClient"]


class CustomerConsumerClient(CimConsumerClient):
    _stub: CustomerConsumerStub = None

    def __init__(self, channel=None, stub: CustomerConsumerStub = None, error_handlers: List[Callable[[Exception], bool]] = None):
        super().__init__(error_handlers=error_handlers)
        if channel is None and stub is None:
            raise ValueError("Must provide either a channel or a stub")
        if stub is not None:
            self._stub = stub
        else:
            self._stub = CustomerConsumerStub(channel)

    async def get_identified_object(self, service: CustomerService, mrid: str) -> GrpcResult[Optional[IdentifiedObject]]:
        """
        Retrieve the object with the given `mrid` and store the result in the `service`.

        Exceptions that occur during sending will be caught and passed to all error handlers that have been registered against this client.

        Returns a `GrpcResult` with a result of one of the following:
             - The object if found
             - None if an object could not be found or it was found but not added to `service` (see `zepben.evolve.common.base_service.BaseService.add`).
             - An `Exception` if an error occurred while retrieving or processing the object, in which case, `GrpcResult.was_successful` will return false.
        """
        async def y():
            async for io, _ in self._process_identified_objects(service, [mrid]):
                return io
            else:
                return None

        return await self.try_rpc(y)

    async def get_identified_objects(self, service: CustomerService, mrids: Iterable[str]) -> GrpcResult[MultiObjectResult]:
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

    async def _process_identified_objects(self, service: CustomerService, mrids: Iterable[str]) -> AsyncGenerator[IdentifiedObject, None]:
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
            io, mrid = extract_identified_object(service, og.identifiedObject)
            if io:
                yield io, mrid
            else:
                yield None, mrid
            for owned_obj in og.ownedIdentifiedObject:
                extracted, mrid = extract_identified_object(service, owned_obj)
                if extracted:
                    yield extracted, mrid
                else:
                    yield None, mrid


class SyncCustomerConsumerClient(CustomerConsumerClient):

    def get_identified_object(self, service: CustomerService, mrid: str) -> GrpcResult[Optional[IdentifiedObject]]:
        """
        Retrieve the object with the given `mrid` and store the result in the `service`.

        Exceptions that occur during sending will be caught and passed to all error handlers that have been registered against this client.

        Returns a `GrpcResult` with a result of one of the following:
             - The object if found
             - None if an object could not be found or it was found but not added to `service` (see `zepben.evolve.common.base_service.BaseService.add`).
             - An `Exception` if an error occurred while retrieving or processing the object, in which case, `GrpcResult.was_successful` will return false.
        """
        return get_event_loop().run_until_complete(super().get_identified_objects(service, mrid))

    def get_identified_objects(self, service: CustomerService, mrids: Iterable[str]) -> GrpcResult[MultiObjectResult]:
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
