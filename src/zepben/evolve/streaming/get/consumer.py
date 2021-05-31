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

from abc import abstractmethod
from typing import Iterable, Dict, Set, TypeVar, Generic, Tuple, Optional, AsyncGenerator, Type, Generator

from dataclassy import dataclass

from zepben.evolve import BaseService, IdentifiedObject, UnsupportedOperationException
from zepben.evolve.streaming.grpc.grpc import GrpcClient, GrpcResult

__all__ = ["CimConsumerClient", "MultiObjectResult"]


@dataclass()
class MultiObjectResult(object):
    objects: Dict[str, IdentifiedObject] = dict()
    failed: Set[str] = set()


ServiceType = TypeVar('ServiceType', bound=BaseService)
PBIdentifiedObject = TypeVar('PBIdentifiedObject')
GrpcRequest = TypeVar('GrpcRequest')


class CimConsumerClient(GrpcClient, Generic[ServiceType]):
    """
    Base class that defines some helpful functions when producer clients are sending to the server.

    ## WARNING ##
        The :class:`MultiObjectResult` operations below are not atomic upon a :class:`BaseService`, and thus if processing fails partway through, any
        previously successful additions will have been processed by the service, and thus you may have an incomplete service. Also note that adding to the
        service may not occur for an object if another object with the same mRID is already present in service. `MultiObjectResult.failed` can be used to
        check for mRIDs that were not found or retrieved but not added to service (this should not be the case unless you are processing things concurrently).

    Parameters
        T: The base service to send objects from.
    """

    @property
    @abstractmethod
    def service(self) -> ServiceType:
        """
        The service to store all retrieved objects in.
        """
        raise NotImplementedError()

    async def get_identified_object(self, mrid: str) -> GrpcResult[IdentifiedObject]:
        """
        Retrieve the object with the given `mRID` and store the result in the `service`.

        Exceptions that occur during sending will be caught and passed to all error handlers that have been registered by `addErrorHandler`.

        Returns a :class:`GrpcResult` with a result of one of the following:
            - When `GrpcResult.wasSuccessful`, the item found, accessible via `GrpcResult.value`.
            - When `GrpcResult.wasFailure`, the error that occurred retrieving or processing the the object, accessible via `GrpcResult.thrown`. One of:
                - :class:`NoSuchElementException` if the object could not be found.
                - The gRPC error that occurred while retrieving the object
        """
        return await self._get_identified_object(mrid)

    async def get_identified_objects(self, mrids: Iterable[str]) -> GrpcResult[MultiObjectResult]:
        """
        Retrieve the objects with the given `mRIDs` and store the results in the `service`.

        Exceptions that occur during processing will be caught and passed to all error handlers that have been registered by `addErrorHandler`.

        @return A :class:`GrpcResult` with a result of one of the following:
            - When `GrpcResult.wasSuccessful`, a map containing the retrieved objects keyed by mRID, accessible via `GrpcResult.value`. If an item was not
              found, or couldn't be added to `service`, it will be excluded from the map and its mRID will be present in `MultiObjectResult.failed`
              (see `BaseService.add`).
            - When `GrpcResult.wasFailure`, the error that occurred retrieving or processing the object, accessible via `GrpcResult.thrown`.

        Note the :class:`CimConsumerClient` warning in this case.
        """
        return await self._get_identified_objects(mrids)

    async def _get_identified_object(self, mrid: str) -> GrpcResult[Optional[IdentifiedObject]]:
        async def rpc():
            async for io, _ in self._process_identified_objects([mrid]):
                return io
            else:
                raise ValueError(f"No object with mRID {mrid} could be found.")

        return await self.try_rpc(rpc)

    async def _get_identified_objects(self, mrids: Iterable[str]) -> GrpcResult[MultiObjectResult]:
        async def rpc():
            return await self._process_extract_results(mrids, self._process_identified_objects(set(mrids)))

        return await self.try_rpc(rpc)

    @abstractmethod
    async def _process_identified_objects(self, mrids: Iterable[str]) -> AsyncGenerator[Tuple[Optional[IdentifiedObject], str], None]:
        #
        # NOTE: this is a stupid test that is meant to fail to make sure we never yield, but we need to have the yield to make it return the generator.
        #
        if self is None:
            yield
        raise NotImplementedError()

    CIM_TYPE = TypeVar("CIM_TYPE", bound=IdentifiedObject)

    def _extract_identified_object(self,
                                   desc: str,
                                   pb_io: PBIdentifiedObject,
                                   pb_type_to_cim: Dict[str, Type[CIM_TYPE]],
                                   check_presence: bool = True) -> Tuple[Optional[IdentifiedObject], str]:
        """
        Add a :class:`CustomerIdentifiedObject` to the service. Will convert from protobuf to CIM type.

        Parameters
            - `pb_io` - The wrapped identified object returned by the server.
            - `pb_type_to_cim` - The mapping of wrapped identified object types to CIM objects.
            - `check_presence` - Whether to check if `cio` already exists in the service and skip if it does.

        Raises :class:`UnsupportedOperationException` if `pb_io` was invalid/unset.
        """
        io_type = pb_io.WhichOneof("identifiedObject")
        if io_type:
            cim_type = pb_type_to_cim.get(io_type, None)
            if cim_type is None:
                raise UnsupportedOperationException(f"Identified object type '{io_type}' is not supported by the {desc} service")

            pb = getattr(pb_io, io_type)
            if check_presence:
                cim = self.service.get(pb.mrid(), cim_type, default=None)
                if cim is not None:
                    return cim, cim.mrid

            # noinspection PyUnresolvedReferences
            return self.service.add_from_pb(pb), pb.mrid()
        else:
            raise UnsupportedOperationException(f"Received a {desc} identified object where no field was set")

    @staticmethod
    async def _process_extract_results(mrids: Iterable[str], extracted: AsyncGenerator[Tuple[Optional[IdentifiedObject], str], None]) -> MultiObjectResult:
        results = {}
        failed = set(mrids)

        async for result in extracted:
            if result[0] is not None:
                results[result[0].mrid] = result[0]
                failed.remove(result[0].mrid)

        return MultiObjectResult(results, failed)

    @staticmethod
    def _batch_send(request: GrpcRequest, mrids: Iterable[str]) -> Generator[GrpcRequest, None, None]:
        count = 0
        for mrid in mrids:
            count += 1
            if count % 1000 == 0:
                yield request
                del request.mrids[:]
            request.mrids.append(mrid)

        if request.mrids:
            yield request
