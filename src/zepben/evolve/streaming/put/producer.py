#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from abc import abstractmethod
from asyncio import get_event_loop
from typing import TypeVar, Union, List, Dict, Type, Callable

from grpc import Channel
from zepben.protobuf.mp.mp_pb2_grpc import MeasurementProducerStub
from zepben.protobuf.mp.mp_requests_pb2 import CreateAnalogValuesRequest, CreateDiscreteValuesRequest, CreateAccumulatorValuesRequest

from zepben.evolve import NetworkService, BaseService, DiagramService, CustomerService, MeasurementService, MeasurementValue, AnalogValue, AccumulatorValue, \
    DiscreteValue
from zepben.evolve.services.network.translator.network_cim2proto import CimTranslationException
from zepben.evolve.streaming.exceptions import UnsupportedOperationException
from zepben.evolve.streaming.grpc.grpc import GrpcClient, GrpcResult
from zepben.evolve.streaming.put.network_rpc import network_rpc_map, diagram_rpc_map, customer_rpc_map, measurement_rpc_map
from zepben.protobuf.cp.cp_pb2_grpc import CustomerProducerStub
from zepben.protobuf.cp.cp_requests_pb2 import CreateCustomerServiceRequest, CompleteCustomerServiceRequest
from zepben.protobuf.dp.dp_pb2_grpc import DiagramProducerStub
from zepben.protobuf.dp.dp_requests_pb2 import CompleteDiagramServiceRequest, CreateDiagramServiceRequest
from zepben.protobuf.np.np_pb2_grpc import NetworkProducerStub
from zepben.protobuf.np.np_requests_pb2 import CreateNetworkRequest, CompleteNetworkRequest

__all__ = ["CimProducerClient", "CustomerProducerClient", "NetworkProducerClient", "DiagramProducerClient", "MeasurementProducerClient", "ProducerClient",
           "SyncProducerClient", "SyncCustomerProducerClient", "SyncNetworkProducerClient", "SyncDiagramProducerClient", "SyncMeasurementProducerClient"]

T = TypeVar("T", bound=BaseService)


async def _send(stub, service, rpc_map):
    if not service:
        return

    for obj in service.objects():
        try:
            pb = obj.to_pb()
        except Exception as e:
            raise CimTranslationException(f"Failed to translate {obj} to protobuf.") from e

        try:
            rpc = getattr(stub, rpc_map[type(pb)][0])
        except AttributeError as e:
            raise UnsupportedOperationException(f"RPC {rpc_map[type(pb)][0]} could not be found in {stub.__class__.__name__}") from e

        attrname = f"{obj.__class__.__name__[:1].lower()}{obj.__class__.__name__[1:]}"
        try:
            req = rpc_map[type(pb)][1]()
            getattr(req, attrname).CopyFrom(pb)
        except AttributeError as e:
            raise AttributeError(f"Protobuf attribute {attrname} could not be found - is evolve-grpc in sync?") from e

        try:
            rpc(req)
        except Exception as e:
            raise Exception(f"Failed to call {rpc_map[type(pb)][0]} with {str(obj)}.") from e


class CimProducerClient(GrpcClient):
    """Base class that defines some helpful functions when producer clients are sending to the server."""


    @abstractmethod
    def send(self, service: T = None):
        """
        Sends objects within the given `service` to the producer server.
                                                                                                                 
        Exceptions that occur during sending will be caught and passed to all error handlers that have been registered. If none of the registered error handlers
        return true to indicate the error has been handled, the exception will be rethrown.
        """
        raise NotImplementedError()


class NetworkProducerClient(CimProducerClient):
    _stub: NetworkProducerStub = None

    def __init__(self, channel=None, stub: NetworkProducerStub = None, error_handlers: List[Callable[[Exception], bool]] = None):
        super().__init__(error_handlers=error_handlers)
        if stub is not None:
            self._stub = stub
        elif channel is not None:
            self._stub = NetworkProducerStub(channel)
        else:
            raise ValueError("Must provide either a channel or a stub")

    async def send(self, service: NetworkService = None):
        """
        Sends objects within the given `service` to the producer server.

        Exceptions that occur during sending will be caught and passed to all error handlers that have been registered. If none of the registered error handlers
        return true to indicate the error has been handled, the exception will be rethrown.
        """
        await self.try_rpc(lambda: self._stub.CreateNetwork(CreateNetworkRequest()))

        await _send(self._stub, service, network_rpc_map)

        await self.try_rpc(lambda: self._stub.CompleteNetwork(CompleteNetworkRequest()))


class DiagramProducerClient(CimProducerClient):
    _stub: DiagramProducerStub = None

    def __init__(self, channel=None, stub: DiagramProducerStub = None, error_handlers: List[Callable[[Exception], bool]] = None):
        super().__init__(error_handlers=error_handlers)
        if stub is not None:
            self._stub = stub
        elif channel is not None:
            self._stub = DiagramProducerStub(channel)
        else:
            raise ValueError("Must provide either a channel or a stub")

    async def send(self, service: DiagramService = None):
        """
        Sends objects within the given `service` to the producer server.

        Exceptions that occur during sending will be caught and passed to all error handlers that have been registered. If none of the registered error handlers
        return true to indicate the error has been handled, the exception will be rethrown.
        """
        await self.try_rpc(lambda: self._stub.CreateDiagramService(CreateDiagramServiceRequest()))

        await _send(self._stub, service, diagram_rpc_map)

        await self.try_rpc(lambda: self._stub.CompleteDiagramService(CompleteDiagramServiceRequest()))


class CustomerProducerClient(CimProducerClient):
    _stub: CustomerProducerStub = None

    def __init__(self, channel=None, stub: CustomerProducerStub = None, error_handlers: List[Callable[[Exception], bool]] = None):
        super().__init__(error_handlers=error_handlers)
        if stub is not None:
            self._stub = stub
        elif channel is not None:
            self._stub = CustomerProducerStub(channel)
        else:
            raise ValueError("Must provide either a channel or a stub")

    async def send(self, service: CustomerService = None):
        """
        Sends objects within the given `service` to the producer server.

        Exceptions that occur during sending will be caught and passed to all error handlers that have been registered. If none of the registered error handlers
        return true to indicate the error has been handled, the exception will be rethrown.
        """
        await self.try_rpc(lambda: self._stub.CreateCustomerService(CreateCustomerServiceRequest()))

        await _send(self._stub, service, customer_rpc_map)

        await self.try_rpc(lambda: self._stub.CompleteCustomerService(CompleteCustomerServiceRequest()))


class MeasurementProducerClient(CimProducerClient):
    _stub: MeasurementProducerStub = None

    def __init__(self, channel=None, stub: MeasurementProducerStub = None, error_handlers: List[Callable[[Exception], bool]] = None):
        super().__init__(error_handlers=error_handlers)
        if stub is not None:
            self._stub = stub
        elif channel is not None:
            self._stub = MeasurementProducerStub(channel)
        else:
            raise ValueError("Must provide either a channel or a stub")

    async def send(self, service: MeasurementService = None):
        """
        Sends objects within the given `service` to the producer server.

        Exceptions that occur during sending will be caught and passed to all error handlers that have been registered. If none of the registered error handlers
        return true to indicate the error has been handled, the exception will be rethrown.
        """
        await _send(self._stub, service, measurement_rpc_map)

    async def send_analogs(self, analogs: List[AnalogValue]):
        request = CreateAnalogValuesRequest(analogValues=[av.to_pb() for av in analogs])
        self._stub.CreateAnalogValues(request)

    async def send_accumulators(self, accumulators: List[AccumulatorValue]):
        request = CreateAccumulatorValuesRequest(analogValues=[av.to_pb() for av in accumulators])
        self._stub.CreateAccumulatorValues(request)

    async def send_discretes(self, discretes: List[DiscreteValue]):
        request = CreateDiscreteValuesRequest(analogValues=[dv.to_pb() for dv in discretes])
        self._stub.CreateDiscreteValues(request)


class ProducerClient(CimProducerClient):
    _channel: Channel = None
    _clients: Dict[Type[BaseService], CimProducerClient] = None

    def __init__(self, channel: Channel = None, clients: Dict[Type[BaseService], CimProducerClient] = None, error_handlers: List[Callable[[Exception], bool]] = None):
        super().__init__(error_handlers=error_handlers)

        if clients is not None:
            self._clients = clients.copy()
        elif channel is not None:
            self._channel = channel
            self._clients = {
                NetworkService: NetworkProducerClient(self._channel),
                DiagramService: DiagramProducerClient(self._channel),
                CustomerService: CustomerProducerClient(self._channel)
            }
        else:
            raise ValueError("You must provide either a channel or clients")

    async def send(self, services: Union[List[BaseService], BaseService] = None):
        """
        Send each service in `services` to the server.

        Exceptions that occur during sending will be caught and passed to all error handlers that have been registered. If none of the registered error handlers
        return true to indicate the error has been handled, the exception will be rethrown.
        """
        if not services:
            return GrpcResult(UnsupportedOperationException("No services were provided"))

        sent = []
        for service in services:
            client = self._clients[type(service)]
            await client.send(service)
            sent.append(type(service))

        for s in self._clients.keys():
            if s not in sent:
                client = self._clients[s]
                await client.send()


class SyncProducerClient(ProducerClient):

    def send(self, services: Union[List[BaseService], BaseService] = None):
        return get_event_loop().run_until_complete(super().send(services))


class SyncCustomerProducerClient(CustomerProducerClient):

    def send(self, service: CustomerService = None):
        return get_event_loop().run_until_complete(super().send(service))


class SyncNetworkProducerClient(NetworkProducerClient):

    def send(self, service: NetworkService = None):
        return get_event_loop().run_until_complete(super().send(service))


class SyncDiagramProducerClient(DiagramProducerClient):

    def send(self, service: DiagramService = None):
        return get_event_loop().run_until_complete(super().send(service))


class SyncMeasurementProducerClient(MeasurementProducerClient):

    def send(self, service: MeasurementService = None):
        return get_event_loop().run_until_complete(super().send(service))

    async def send_analogs(self, analogs: List[AnalogValue]):
        return get_event_loop().run_until_complete(super().send_analogs(analogs))

    async def send_accumulators(self, accumulators: List[AccumulatorValue]):
        return get_event_loop().run_until_complete(super().send_accumulators(accumulators))

    async def send_discretes(self, discretes: List[DiscreteValue]):
        return get_event_loop().run_until_complete(super().send_discretes(discretes))
