#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from dataclasses import dataclass
from typing import Awaitable, Callable, List, TypeVar, Union, Optional, Iterable, Generator

# noinspection PyPackageRequirements
import grpc
import grpc_testing
# noinspection PyPackageRequirements
from google.protobuf.descriptor import ServiceDescriptor

from streaming.get.catching_thread import CatchingThread

GrpcRequest = TypeVar('GrpcRequest')
GrpcResponse = TypeVar('GrpcResponse')


@dataclass
class StreamGrpc:
    function: str
    processors: List[Callable[[GrpcRequest], Generator[GrpcResponse, None, None]]]
    """
    The processors to run in order for this function StreamGrpc.
    For example if you expect getIdentifiedObjects to be called twice in a row, you could provide two processors for getIdentifiedObjects here, rather
    than two separate StreamGrpcs
    """

    force_timeout: bool = False


@dataclass
class UnaryGrpc:
    function: str
    processor: Callable[[GrpcRequest], Generator[GrpcResponse, None, None]]
    force_timeout: bool = False


def stream_from_fixed(expected_requests: List[str], responses: Iterable[GrpcResponse]) -> List[Callable[[GrpcRequest], Generator[GrpcResponse, None, None]]]:
    def process(request: GrpcRequest) -> Generator[GrpcResponse, None, None]:
        for response in responses:
            yield response

        assert len(request.mrids) == len(expected_requests)
        assert set(request.mrids) == set(expected_requests)

    return [process]


def unary_from_fixed(expected_request: Optional[str], response: GrpcResponse):
    def process(request: GrpcRequest) -> Generator[GrpcResponse, None, None]:
        yield response

        if expected_request:
            assert request.mrid == expected_request

    return process


class MockServer:

    def __init__(self, channel: grpc_testing.Channel, grpc_service: ServiceDescriptor):
        self.channel: grpc_testing.Channel = channel
        self.grpc_service: ServiceDescriptor = grpc_service

    async def validate(self, client_test: Callable[[], Awaitable[None]], interactions: List[Union[StreamGrpc, UnaryGrpc]]):
        """
        Run a server that mocks RPC requests by invoking the provided `interactions` in order.

        :param client_test: The test code to call.
        :param interactions: An ordered list of interactions expected for this server.
        """
        server = CatchingThread(target=self._run_server_logic, args=[interactions])
        server.start()

        await client_test()
        server.join()

        if server.exception:
            raise server.exception

    def _run_server_logic(self, interactions: List[Union[StreamGrpc, UnaryGrpc]]):
        for i in interactions:
            if isinstance(i, StreamGrpc):
                self._run_stream_server_logic(i)
            elif isinstance(i, UnaryGrpc):
                self._run_unary_server_logic(i)
            else:
                raise NotImplementedError(f"No server logic has been configured for {type(i)}")

    def _run_stream_server_logic(self, interaction: StreamGrpc):
        for processor in interaction.processors:
            _, rpc = self.channel.take_stream_stream(self.grpc_service.methods_by_name[interaction.function])
            rpc.send_initial_metadata(())

            try:
                request = rpc.take_request()
                if interaction.force_timeout:
                    rpc.terminate(None, (), grpc.StatusCode.DEADLINE_EXCEEDED, '')
                    return

                for response in processor(request):
                    rpc.send_response(response)

                rpc.requests_closed()
            finally:
                rpc.terminate((), grpc.StatusCode.OK, '')

    def _run_unary_server_logic(self, interaction: UnaryGrpc):
        _, request, rpc = self.channel.take_unary_unary(self.grpc_service.methods_by_name[interaction.function])
        rpc.send_initial_metadata(())
        if interaction.force_timeout:
            rpc.terminate(None, (), grpc.StatusCode.DEADLINE_EXCEEDED, '')
            return

        try:
            for response in interaction.processor(request):
                rpc.terminate(response, (), grpc.StatusCode.OK, '')
        except Exception as e:
            rpc.terminate((), (), grpc.StatusCode.OK, '')
            raise e
