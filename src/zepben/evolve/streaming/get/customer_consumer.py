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

from zepben.protobuf.cc.cc_data_pb2 import CustomerIdentifiedObject

from zepben.evolve import CustomerService, IdentifiedObject, UnsupportedOperationException, Organisation, Customer, CustomerAgreement, PricingStructure, Tariff
from zepben.evolve.streaming.get.consumer import CimConsumerClient, MultiObjectResult
from zepben.evolve.streaming.grpc.grpc import GrpcResult
from zepben.protobuf.cc.cc_pb2_grpc import CustomerConsumerStub
from zepben.protobuf.cc.cc_requests_pb2 import GetIdentifiedObjectsRequest

__all__ = ["CustomerConsumerClient", "SyncCustomerConsumerClient"]


class CustomerConsumerClient(CimConsumerClient[CustomerService]):
    """
    Consumer client for a :class:`CustomerService`.

    ## WARNING ##
        The :class:`MultiObjectResult` operations below are not atomic upon a :class:`CustomerService`, and thus if processing fails partway through, any
        previously successful additions will have been processed by the service, and thus you may have an incomplete service. Also note that adding to the
        service may not occur for an object if another object with the same mRID is already present in service. `MultiObjectResult.failed` can be used to
        check for mRIDs that were not found or retrieved but not added to service (this should not be the case unless you are processing things concurrently).
    """

    _stub: CustomerConsumerStub = None

    def __init__(self, channel=None, stub: CustomerConsumerStub = None, error_handlers: List[Callable[[Exception], bool]] = None):
        super().__init__(error_handlers=error_handlers)
        if channel is None and stub is None:
            raise ValueError("Must provide either a channel or a stub")
        if stub is not None:
            self._stub = stub
        else:
            self._stub = CustomerConsumerStub(channel)

    async def get_identified_object(self, service: CustomerService, mrid: str) -> GrpcResult[IdentifiedObject]:
        """
        Retrieve the object with the given `mRID` and store the result in the `service`.

        Exceptions that occur during sending will be caught and passed to all error handlers that have been registered.

        Parameters
            - `service` - The :class:`CustomerService` to store fetched objects in.
            - `mRID` - The mRID to retrieve.

        Returns a :class:`GrpcResult` with a result of one of the following:
            - When `GrpcResult.wasSuccessful`, the item found, accessible via `GrpcResult.value`.
            - When `GrpcResult.wasFailure`, the error that occurred retrieving or processing the the object, accessible via `GrpcResult.thrown`. One of:
                - :class:`NoSuchElementException` if the object could not be found.
                - The gRPC error that occurred while retrieving the object
        """
        return await self._get_identified_object(service, mrid)

    async def get_identified_objects(self, service: CustomerService, mrids: Iterable[str]) -> GrpcResult[MultiObjectResult]:
        """
        Retrieve the objects with the given [mRIDs] and store the results in the [service].

        Exceptions that occur during processing will be caught and passed to all error handlers that have been registered.

        Parameters
            - `service` - The :class:`CustomerService` to store fetched objects in.
            - `mRIDs` - The mRIDs to retrieve.

        Returns a :class:`GrpcResult` with a result of one of the following:
            - When `GrpcResult.wasSuccessful`, a map containing the retrieved objects keyed by mRID, accessible via `GrpcResult.value`. If an item was not
              found, or couldn't be added to `service`, it will be excluded from the map and its mRID will be present in `MultiObjectResult.failed` (see
              `BaseService.add`).
            - When `GrpcResult.wasFailure`, the error that occurred retrieving or processing the the object, accessible via `GrpcResult.thrown`.

        Note the :class:`CustomerConsumerClient` warning in this case.
        """
        return await self._get_identified_objects(service, mrids)

    async def _get_identified_object(self, service: CustomerService, mrid: str) -> GrpcResult[Optional[IdentifiedObject]]:
        async def rpc():
            async for io, _ in self._process_identified_objects(service, [mrid]):
                return io
            else:
                raise ValueError(f"No object with mRID {mrid} could be found.")

        return await self.try_rpc(rpc)

    async def _get_identified_objects(self, service: CustomerService, mrids: Iterable[str]) -> GrpcResult[MultiObjectResult]:
        return await self.try_rpc(lambda: self._process_extract_results(mrids, self._process_identified_objects(service, set(mrids))))

    async def _process_identified_objects(self, service: CustomerService, mrids: Iterable[str]) -> AsyncGenerator[Tuple[Optional[IdentifiedObject], str], None]:
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


class SyncCustomerConsumerClient(CustomerConsumerClient):

    def get_identified_object(self, service: CustomerService, mrid: str) -> GrpcResult[Optional[IdentifiedObject]]:
        return get_event_loop().run_until_complete(super().get_identified_objects(service, mrid))

    def get_identified_objects(self, service: CustomerService, mrids: Iterable[str]) -> GrpcResult[MultiObjectResult]:
        return get_event_loop().run_until_complete(super().get_identified_objects(service, mrids))


def _extract_identified_object(service: CustomerService, cio: CustomerIdentifiedObject, check_presence: bool = True) -> Tuple[Optional[IdentifiedObject], str]:
    """
    Add a :class:`CustomerIdentifiedObject` to the service. Will convert from protobuf to CIM type.

    Parameters
        - `service` - The :class:`CustomerService` to add the identified object to.
        - `cio` - The :class:`CustomerIdentifiedObject` returned by the server.
        - `check_presence` - Whether to check if `cio` already exists in the service and skip if it does.

    Raises :class:`UnsupportedOperationException` if `cio` was invalid/unset.
    """
    io_type = cio.WhichOneof("identifiedObject")
    if io_type:
        cim_type = _cio_type_to_cim.get(io_type, None)
        if cim_type is None:
            raise UnsupportedOperationException(f"Identified object type '{io_type}' is not supported by the customer service")

        pb = getattr(cio, io_type)
        if check_presence:
            cim = service.get(pb.mrid(), cim_type, default=None)
            if cim is not None:
                return cim, cim.mrid

        # noinspection PyUnresolvedReferences
        return service.add_from_pb(pb), pb.mrid()
    else:
        raise UnsupportedOperationException(f"Received a CustomerIdentifiedObject where no field was set")


_cio_type_to_cim = {
    "organisation": Organisation,
    "customer": Customer,
    "customerAgreement": CustomerAgreement,
    "pricingStructure": PricingStructure,
    "tariff": Tariff
}
