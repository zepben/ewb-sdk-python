#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import traceback
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
    Stream of requests and matching stream of responses.

    The processors to run in order for this function StreamGrpc. There should be an entry in this list for every request sent
    via the same stream, with the expected responses to that request.

    If you expect multiple requests to be made by subsequent calls to a new stream, they should be specified by two separate
    StreamGrpc instances, rather than providing two processors here.
    """

    force_timeout: bool = False


@dataclass
class UnaryGrpc:
    function: str
    processor: Callable[[GrpcRequest], Generator[GrpcResponse, None, None]]
    """
    Unary request and matching unary response.

    Will cause errors in the processing if the generator produces more than one response.
    """
    force_timeout: bool = False


@dataclass
class StreamUnaryGrpc:
    function: str
    request_validators: List[Callable[[GrpcRequest], None]]
    """
    Stream of requests.
    
    Requires one per request sent via the same stream. For multiple requests on different streams use multiple StreamUnaryGrpc instances.
    """
    response: GrpcResponse
    """
    Unary response to send after request stream is closed.
    """
    force_timeout: bool = False


@dataclass
class UnaryStreamGrpc:
    function: str
    processor: Callable[[GrpcRequest], Generator[GrpcResponse, None, None]]
    """
    Unary request and matching stream of responses.
    """
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

    async def validate(self, client_test: Callable[[], Awaitable[None]], interactions: List[Union[StreamGrpc, UnaryGrpc, StreamUnaryGrpc, UnaryStreamGrpc]]):
        """
        Run a server that mocks RPC requests by invoking the provided `interactions` in order.

        :param client_test: The test code to call.
        :param interactions: An ordered list of interactions expected for this server.
        """
        # Run the server logic in another thread.
        # noinspection PyTypeChecker
        server = CatchingThread(target=self._run_server_logic, args=[interactions])
        server.start()

        # Send the client requests. We need to wrap this in an exception logging block to get any errors from asserts in the
        # client test, as the pytest logging only give the outcome, not which line actually caused it.
        # noinspection PyBroadException
        try:
            await client_test()
        except Exception:
            print(traceback.format_exc())

        # Wait for the server to finish. If this times out your test, it indicates that not all expected requests were received, or the request stream
        # wasn't closed/completed.
        server.join()

        if server.exception:
            raise server.exception

    def _run_server_logic(self, interactions: List[Union[StreamGrpc, UnaryGrpc]]):
        for i in interactions:
            if isinstance(i, StreamGrpc):
                self._run_stream_server_logic(i)
            elif isinstance(i, UnaryGrpc):
                self._run_unary_server_logic(i)
            elif isinstance(i, StreamUnaryGrpc):
                self._run_stream_unary_server_logic(i)
            elif isinstance(i, UnaryStreamGrpc):
                self._run_unary_stream_server_logic(i)
            else:
                raise NotImplementedError(f"No server logic has been configured for {type(i)}")

    def _run_stream_server_logic(self, interaction: StreamGrpc):
        # Take the expected StreamStream message.
        _, rpc = self.channel.take_stream_stream(self.grpc_service.methods_by_name[interaction.function])
        rpc.send_initial_metadata(())

        try:
            for processor in interaction.processors:
                # Take a request from the stream.
                request = rpc.take_request()
                if interaction.force_timeout:
                    rpc.terminate((), grpc.StatusCode.DEADLINE_EXCEEDED, '')
                    return

                # Send each yielded item to the response stream.
                for response in processor(request):
                    rpc.send_response(response)

            # Ensure the requests stream is closed.
            rpc.requests_closed()
        finally:
            # Terminate the message regardless of exceptions or completion.
            rpc.terminate((), grpc.StatusCode.OK, '')

    def _run_unary_server_logic(self, interaction: UnaryGrpc):
        # Take the expected UnaryUnary message, which includes the request.
        _, request, rpc = self.channel.take_unary_unary(self.grpc_service.methods_by_name[interaction.function])
        rpc.send_initial_metadata(())

        if interaction.force_timeout:
            rpc.terminate(None, (), grpc.StatusCode.DEADLINE_EXCEEDED, '')
            return

        try:
            #
            # NOTE: Although this is looping, the processor should only yield a single entry (it is Unary after all). Yielding multiple items will
            #       cause multiple calls to `terminate` which will cause errors.
            #
            for response in interaction.processor(request):
                rpc.terminate(response, (), grpc.StatusCode.OK, '')
        except Exception as e:
            # If there were errors in the processor, send a blank response.
            rpc.terminate((), (), grpc.StatusCode.OK, '')
            raise e

    def _run_stream_unary_server_logic(self, interaction: StreamUnaryGrpc):
        _, rpc = self.channel.take_stream_unary(self.grpc_service.methods_by_name[interaction.function])
        rpc.send_initial_metadata(())

        try:
            for validator in interaction.request_validators:
                request = rpc.take_request()
                if interaction.force_timeout:
                    rpc.terminate(None, (), grpc.StatusCode.DEADLINE_EXCEEDED, '')
                    return

                validator(request)

            rpc.requests_closed()

            # NOTE: We don't want to move this to a finally block, otherwise it will send a second terminate if it times out above.
            rpc.terminate(interaction.response, (), grpc.StatusCode.OK, '')
        except Exception as e:
            rpc.terminate(interaction.response, (), grpc.StatusCode.OK, '')
            raise e

    def _run_unary_stream_server_logic(self, interaction: UnaryStreamGrpc):
        # Take the expected UnaryStream message, which includes the request.
        _, request, rpc = self.channel.take_unary_stream(self.grpc_service.methods_by_name[interaction.function])
        rpc.send_initial_metadata(())

        try:
            if interaction.force_timeout:
                rpc.terminate((), grpc.StatusCode.DEADLINE_EXCEEDED, '')
                return

            # Send each yielded item to the response stream.
            for response in interaction.processor(request):
                rpc.send_response(response)

            # Ensure the requests stream is closed.
            rpc.requests_closed()
        finally:
            # Terminate the message regardless of exceptions or completion.
            rpc.terminate((), grpc.StatusCode.OK, '')
