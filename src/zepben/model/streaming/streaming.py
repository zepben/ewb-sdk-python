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
from zepben.model import Network, MetricsStore
from zepben.model.streaming.exceptions import StreamingException
from zepben.postbox.pb_pb2_grpc import NetworkDataStub
from dataclasses import dataclass


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
    :return: A :class:`zepben.model.network.Network` containing the streamed network.
    """
    network = Network(MetricsStore())
    stream_response = rpc(*args, **kwargs)
    for eq_msg in stream_response:
        field = getattr(eq_msg, eq_msg.WhichOneof('equipment'))
        try:
            network.add(field)
        except Exception as e:
            raise StreamingException((f"Failed to add [{field.mRID}|{field.name}] to network. Are you using a cimbend ",
                                      "version compatible with the server? Underlying error was: {e}"))
    return network


async def send_network(stub: NetworkDataStub, ec: Network, network_id: str = ""):
    for pb_type in ec.type_map.pb_to_cim.keys():
        rpc = getattr(stub, ec.type_map.grpc[pb_type])
        for io in ec.type_map.all[pb_type].fget(ec).values():
            rpc(io.to_pb())

