

#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from typing import List, Union

from zepben.cimbend.common import BaseService
from zepben.cimbend.network import NetworkService
from zepben.cimbend.customer import CustomerService
from zepben.cimbend.diagram import DiagramService
from zepben.protobuf.np.np_pb2_grpc import NetworkProducerStub
from zepben.protobuf.cp.cp_pb2_grpc import CustomerProducerStub
from zepben.protobuf.dp.dp_pb2_grpc import DiagramProducerStub
from zepben.cimbend.streaming.streaming import retrieve_network, send_network, send_customer, send_diagram, \
    create_network, complete_network, create_diagram, complete_diagram, create_customer, complete_customer, \
    CimTranslationException

__all__ = ["WorkbenchConnection"]

NetworkProducerStub.send = send_network
NetworkProducerStub.create = create_network
NetworkProducerStub.complete = complete_network
DiagramProducerStub.send = send_diagram
DiagramProducerStub.create = create_diagram
DiagramProducerStub.complete = complete_diagram
CustomerProducerStub.send = send_customer
CustomerProducerStub.create = create_customer
CustomerProducerStub.complete = complete_customer


class WorkbenchConnection(object):

    def __init__(self, channel):
        self.channel = channel
        self._stubs = {
            NetworkService: NetworkProducerStub(channel),
            DiagramService: DiagramProducerStub(channel),
            CustomerService: CustomerProducerStub(channel)
        }

    # async def get_whole_network(self, mrid=""):
    #     """
    #     Retrieve an entire network from the connection.
    #     `mrid` ID of the network to retrieve (not supported yet) TODO
    #     Returns An `zepben.cimbend.network.Network` populated with the network.
    #     """
    #     ec = await retrieve_network(self.network_stub.getWholeNetwork, Identity(mRID=mrid))
    #     return ec
    async def _send_service(self, service: BaseService):
        stub = self._stubs[type(service)]
        await stub.create()
        await stub.send(service)
        await stub.complete()

    async def send(self, services: Union[List[BaseService], BaseService]):
        sent = []
        try:
            for service in services:
                await self._send_service(service)
                sent.append(type(service))
        except AttributeError:
            await self._send_service(services)
            sent.append(type(services))

        for s in self._stubs.keys():
            if s not in sent:
                stub = self._stubs[s]
                await stub.create()
                await stub.complete()

    # async def send_feeder(self, ns: NetworkService):
    #     """
    #     Send a feeder to the connected server. A feeder must start with a feeder circuit `zepben.cimbend.switch.Breaker`.
    #
    #     `ns` The Network containing all equipment in the feeder.
    #     Returns A `zepben.cimbend.streaming.streaming.FeederStreamResult`
    #     Raises A derivative of `zepben.cimbend.exceptions.MissingReferenceException` if a incorrect reference
    #              between types is made.
    #     """
    #     # res = await send_network(self.network_stub, ns)
    #     return res

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.channel.close()
