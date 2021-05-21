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
from typing import Iterable, Dict, Set, TypeVar, Generic, Tuple, Optional, AsyncGenerator

from dataclassy import dataclass

from zepben.evolve import BaseService, IdentifiedObject
from zepben.evolve.streaming.grpc.grpc import GrpcClient, GrpcResult

__all__ = ["CimConsumerClient", "MultiObjectResult"]


@dataclass()
class MultiObjectResult(object):
    objects: Dict[str, IdentifiedObject] = dict()
    failed: Set[str] = set()


ServiceType = TypeVar('ServiceType', bound=BaseService)


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

    @abstractmethod
    async def get_identified_object(self, service: ServiceType, mrid: str) -> GrpcResult[IdentifiedObject]:
        """
        Retrieve the object with the given `mRID` and store the result in the `service`.

        Exceptions that occur during sending will be caught and passed to all error handlers that have been registered by `addErrorHandler`.

        Returns a :class:`GrpcResult` with a result of one of the following:
            - When `GrpcResult.wasSuccessful`, the item found, accessible via `GrpcResult.value`.
            - When `GrpcResult.wasFailure`, the error that occurred retrieving or processing the the object, accessible via `GrpcResult.thrown`. One of:
                - :class:`NoSuchElementException` if the object could not be found.
                - The gRPC error that occurred while retrieving the object
        """
        raise NotImplementedError()

    @abstractmethod
    async def get_identified_objects(self, service: ServiceType, mrids: Iterable[str]) -> GrpcResult[MultiObjectResult]:
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
        raise NotImplementedError()

    @staticmethod
    async def _process_extract_results(mrids: Iterable[str], extracted: AsyncGenerator[Tuple[Optional[IdentifiedObject], str], None]) -> MultiObjectResult:
        results = {}
        failed = set(mrids)

        async for result in extracted:
            if result[0] is not None:
                results[result[0].mrid] = result[0]
                failed.remove(result[0].mrid)

        return MultiObjectResult(results, failed)
