"""
Copyright 2019 Zeppelin Bend Pty Ltd
This file is part of cimbend.

cimbend is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

cimbend is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with cimbend.  If not, see <https://www.gnu.org/licenses/>.
"""
from zepben.cimbend import NetworkService, MetricsStore, CustomerService, DiagramService, ConnectivityNode, Terminal, \
    PowerTransformerEnd
from zepben.cimbend.streaming.exceptions import StreamingException
from zepben.protobuf.cp.cp_pb2_grpc import CustomerProducerStub
from zepben.protobuf.cp.cp_requests_pb2 import CreateCustomerServiceRequest, CompleteCustomerServiceRequest
from zepben.protobuf.dp.dp_pb2_grpc import DiagramProducerStub
from zepben.protobuf.dp.dp_requests_pb2 import CreateDiagramServiceRequest, CompleteDiagramServiceRequest
from zepben.protobuf.np.np_pb2_grpc import NetworkProducerStub
from zepben.protobuf.np.np_requests_pb2 import CreateNetworkRequest, CompleteNetworkRequest
from zepben.cimbend.streaming.network_rpc import rpc_map
from zepben.cimbend.network.translator.network_cim2proto import *

from dataclasses import dataclass

__all__ = ["retrieve_network", "send_network", "send_customer", "send_diagram", "FeederStreamResult", "FeederSummary"]


# TODO: Fill in all fields
@dataclass
class FeederSummary:
    acls_count: int
    node_count: int


@dataclass
class FeederStreamResult:
    success: bool
    summary: FeederSummary


async def retrieve_network(rpc, *args, **kwargs):
    """
    Given an RPC call that returns a stream of Equipment, this will stream the equipment into a new Network
    and return that container.

    :param rpc: The RPC call to be executed.
    :param *args: args to be passed to the RPC call
    :param **kwargs: kwargs to be passed to the RPC call
    :return: A :class:`zepben.cimbend.network.Network` containing the streamed network.
    """
    network = NetworkService(metrics_store=MetricsStore())
    stream_response = rpc(*args, **kwargs)
    for eq_msg in stream_response:
        field = getattr(eq_msg, eq_msg.WhichOneof('equipment'))
        try:
            network.add(field)
        except Exception as e:
            raise StreamingException((f"Failed to add [{field.mRID}|{field.name}] to network. Are you using a cimbend ",
                                      "version compatible with the server? Underlying error was: {e}"))
    return network


async def create_network(stub: NetworkProducerStub):
    stub.CreateNetwork(CreateNetworkRequest())


async def complete_network(stub: NetworkProducerStub):
    stub.CompleteNetwork(CompleteNetworkRequest())


class NoSuchRPCException(Exception):
    pass


class ProtoAttributeError(Exception):
    pass


async def send_network(stub: NetworkProducerStub, network_service: NetworkService):
    """
    Send a feeder to the connected server.
    Note that ConnectivityNodes are never sent with this method, a Terminal is sent containeing the ConnectivityNode mRID
    which is the only necessary information to rebuild ConnectivityNodes.
    :param ns: The Network containing all equipment in the feeder.
    :return: A :class:`zepben.cimbend.streaming.streaming.FeederStreamResult
    """
    # Terminals and PTE's are handled specifically below
    for obj in network_service.objects(exc_types=[ConnectivityNode, Terminal, PowerTransformerEnd]):
        try:
            pb = obj.to_pb()
        except Exception as e:
            raise CimTranslationException(f"Failed to translate {obj} to protobuf.") from e

        try:
            rpc = getattr(stub, rpc_map[type(pb)][0])
        except AttributeError as e:
            raise NoSuchRPCException(f"RPC {rpc_map[type(pb)][0]} could not be found in {stub.__class__.__name__}") from e

        try:
            attrname = f"{obj.__class__.__name__[:1].lower()}{obj.__class__.__name__[1:]}"
            req = rpc_map[type(pb)][1]()
            # Terminals are always sent with ConductingEquipment, so if we have a "terminals" field, add them here.
            if hasattr(req, "terminals"):
                for _, terminal in obj.terminals:
                    req.terminals.append(terminal.to_pb())
            if hasattr(req, "ends"):
                for _, end in obj.ends:
                    req.ends.append(end.to_pb())
            getattr(req, attrname).CopyFrom(pb)
        except AttributeError as e:
            raise ProtoAttributeError() from e

        rpc(req)


async def create_diagram(stub: DiagramProducerStub):
    stub.CreateDiagramService(CreateDiagramServiceRequest())


async def complete_diagram(stub: DiagramProducerStub):
    stub.CompleteDiagramService(CompleteDiagramServiceRequest())


async def send_diagram(stub: DiagramProducerStub, diagram_service: DiagramService):
    pass


async def create_customer(stub: CustomerProducerStub):
    stub.CreateCustomerService(CreateCustomerServiceRequest())


async def complete_customer(stub: CustomerProducerStub):
    stub.CompleteCustomerService(CompleteCustomerServiceRequest())


async def send_customer(stub: CustomerProducerStub, customer_service: CustomerService):
    pass



