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
from typing import Iterable, Dict, Optional, Set, Tuple

from dataclassy import dataclass

from zepben.evolve.streaming.exceptions import UnsupportedOperationException
from zepben.protobuf.nc.nc_data_pb2 import NetworkIdentifiedObject

from zepben.evolve.streaming.grpc.grpc import GrpcClient, GrpcResult

__all__ = ["CimConsumerClient", "MultiObjectResult", "extract_identified_object"]


@dataclass()
class MultiObjectResult(object):
    value: Dict[str, IdentifiedObject] = dict()
    failed: Set[str] = set()


class CimConsumerClient(GrpcClient):

    @abstractmethod
    async def get_identified_object(self, service: BaseService, mrid: str) -> GrpcResult:
        """
        Retrieve the object with the given `mrid` and store the result in the `service`.
                                                                                                                 
        Exceptions that occur during sending will be caught and passed to all error handlers that have been registered against this client.

        Returns a `GrpcResult` with a result of one of the following:
             - The object if found
             - null if an object could not be found or it was found but not added to `service` (see `zepben.evolve.common.base_service.BaseService.add`).
             - An `Exception` if an error occurred while retrieving or processing the object, in which case, `GrpcResult.was_successful` will return false.
        """
        raise NotImplementedError()

    @abstractmethod
    async def get_identified_objects(self, service: BaseService, mrids: Iterable[str]) -> GrpcResult:
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
        raise NotImplementedError()


def extract_identified_object(service: NetworkService, nio: NetworkIdentifiedObject) -> Tuple[Optional[IdentifiedObject], str]:
    """
    Add an equipment to the network.
    `stub` A network consumer stub.
    `network` The network to add the equipment to.
    `equipment_io` The equipment identified object returned by the server.
    Raises `UnsupportedOperationException` if `nio` was invalid/unset.
    """
    io_type = nio.WhichOneof("identifiedObject")
    if io_type:
        pbio = getattr(nio, io_type)
        return service.add_from_pb(pbio), pbio.mrid()
    else:
        raise UnsupportedOperationException(f"Received a NetworkIdentifiedObject where no field was set")
