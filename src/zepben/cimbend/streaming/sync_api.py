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
        :param mrid: ID of the network to retrieve (not supported yet) TODO
        :return: An :class:`zepben.cimbend.network.Network` populated with the network.
        """
        ec = get_event_loop().run_until_complete(super().get_whole_network(self.network_stub.getWholeNetwork, Identity(mRID=mrid)))
        return ec

    def send_services(self, services: Union[BaseService, List[BaseService]]):
        """
        Send a feeder to the connected server. A feeder must start with a feeder circuit :class:`zepben.cimbend.switch.Breaker`.

        :param services: The services to send. Must extend :class:`zepben.cimbend.BaseService`
        :return: A :class:`zepben.cimbend.streaming.streaming.FeederStreamResult
        :raises: A derivative of :class:`zepben.cimbend.exceptions.MissingReferenceException` if a incorrect reference
                 between types is made.
        """
        return get_event_loop().run_until_complete(super().send(services=services))



