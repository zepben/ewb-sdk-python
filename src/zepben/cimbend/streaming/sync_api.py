


#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from typing import Union, List

from zepben.cimbend.common import BaseService
from zepben.cimbend.streaming.api import WorkbenchConnection
from asyncio import get_event_loop
__all__ = ["SyncWorkbenchConnection"]


class SyncWorkbenchConnection(WorkbenchConnection):
    def __init__(self, channel):
        super().__init__(channel)

    def get_whole_network(self, mrid=''):
        """
        Retrieve an entire network from the connection.
        `mrid` ID of the network to retrieve (not supported yet) TODO
        Returns An `zepben.cimbend.network.Network` populated with the network.
        """
        ec = get_event_loop().run_until_complete(super().get_whole_network(self.network_stub.getWholeNetwork, Identity(mRID=mrid)))
        return ec

    def send_services(self, services: Union[BaseService, List[BaseService]]):
        """
        Send a feeder to the connected server. A feeder must start with a feeder circuit `zepben.cimbend.switch.Breaker`.

        `services` The services to send. Must extend `zepben.cimbend.BaseService`
        Returns A `zepben.cimbend.streaming.streaming.FeederStreamResult`
        Raises A derivative of `zepben.cimbend.exceptions.MissingReferenceException` if a incorrect reference
                 between types is made.
        """
        return get_event_loop().run_until_complete(super().send(services=services))



