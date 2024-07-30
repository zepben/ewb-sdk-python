#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from asyncio import get_event_loop
from typing import Optional, Iterable, AsyncGenerator, List, Callable, Tuple

from zepben.evolve import CustomerService, IdentifiedObject, Organisation, Customer, CustomerAgreement, PricingStructure, Tariff, ServiceInfo
from zepben.evolve.streaming.get.consumer import CimConsumerClient, MultiObjectResult
from zepben.evolve.streaming.grpc.grpc import GrpcResult
from zepben.protobuf.cc.cc_pb2_grpc import CustomerConsumerStub
from zepben.protobuf.cc.cc_requests_pb2 import GetIdentifiedObjectsRequest, GetCustomersForContainerRequest
from zepben.protobuf.metadata.metadata_requests_pb2 import GetMetadataRequest
from zepben.protobuf.metadata.metadata_responses_pb2 import GetMetadataResponse

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

    __service: CustomerService

    @property
    def service(self) -> CustomerService:
        return self.__service

    _stub: CustomerConsumerStub = None

    def __init__(self, channel=None, stub: CustomerConsumerStub = None, error_handlers: List[Callable[[Exception], bool]] = None, timeout: int = 60):
        super().__init__(error_handlers=error_handlers, timeout=timeout)
        if channel is None and stub is None:
            raise ValueError("Must provide either a channel or a stub")
        if stub is not None:
            self._stub = stub
        else:
            self._stub = CustomerConsumerStub(channel)

        self.__service = CustomerService()

    async def get_customers_for_container(self, mrid: str) -> GrpcResult[MultiObjectResult]:
        return await self._get_customers_for_containers({mrid})

    async def get_customers_for_containers(self, mrids: Iterable[str]) -> GrpcResult[MultiObjectResult]:
        return await self._get_customers_for_containers(mrids)

    async def _run_get_metadata(self, request: GetMetadataRequest) -> GetMetadataResponse:
        return await self._stub.getMetadata(request, timeout=self.timeout)

    async def _get_customers_for_containers(self, mrids: Iterable[str]) -> GrpcResult[MultiObjectResult]:
        async def rpc():
            return await self._process_extract_results(None, self._process_customers_for_containers(mrids))

        return await self.try_rpc(rpc)

    async def _process_customers_for_containers(self, mrids: Iterable[str]) -> AsyncGenerator[Tuple[Optional[IdentifiedObject], str], None]:
        if not mrids:
            return

        responses = self._stub.getCustomersForContainer(self._batch_send(GetCustomersForContainerRequest(), mrids), timeout=self.timeout)
        async for response in responses:
            for cio in response.identifiedObjects:
                yield self._extract_identified_object("customer", cio, _cio_type_to_cim)

    async def _process_identified_objects(self, mrids: Iterable[str]) -> AsyncGenerator[Tuple[Optional[IdentifiedObject], str], None]:
        if not mrids:
            return

        responses = self._stub.getIdentifiedObjects(self._batch_send(GetIdentifiedObjectsRequest(), mrids), timeout=self.timeout)
        async for response in responses:
            for cio in response.identifiedObjects:
                yield self._extract_identified_object("customer", cio, _cio_type_to_cim)


class SyncCustomerConsumerClient(CustomerConsumerClient):

    def get_identified_object(self, mrid: str) -> GrpcResult[Optional[IdentifiedObject]]:
        return get_event_loop().run_until_complete(super()._get_identified_objects(mrid))

    def get_identified_objects(self, mrids: Iterable[str]) -> GrpcResult[MultiObjectResult]:
        return get_event_loop().run_until_complete(super()._get_identified_objects(mrids))

    def get_customers_for_container(self, mrid: str) -> GrpcResult[MultiObjectResult]:
        return get_event_loop().run_until_complete(super()._get_customers_for_containers({mrid}))

    def get_customers_for_containers(self, mrids: Iterable[str]) -> GrpcResult[MultiObjectResult]:
        return get_event_loop().run_until_complete(super()._get_customers_for_containers(mrids))

    def get_metadata(self) -> GrpcResult[ServiceInfo]:
        return get_event_loop().run_until_complete(super().get_metadata())


_cio_type_to_cim = {
    "organisation": Organisation,
    "customer": Customer,
    "customerAgreement": CustomerAgreement,
    "pricingStructure": PricingStructure,
    "tariff": Tariff
}
