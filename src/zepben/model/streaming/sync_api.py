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
from zepben.model.streaming.api import WorkbenchConnection
from asyncio import get_event_loop
__all__ = ["SyncWorkbenchConnection"]


class SyncWorkbenchConnection(WorkbenchConnection):
    def __init__(self, channel):
        super().__init__(channel)

    def get_whole_network(self, mrid=''):
        """
        Retrieve an entire network from the connection.
        :param mrid: ID of the network to retrieve (not supported yet) TODO
        :return: An :class:`zepben.model.network.EquipmentContainer` populated with the network.
        """
        ec = get_event_loop().run_until_complete(super().get_whole_network(self.network.getWholeNetwork, Identity(mRID=mrid)))
        return ec

    def send_feeder(self, ec: EquipmentContainer):
        """
        Send a feeder to the connected server. A feeder must start with a feeder circuit :class:`zepben.model.switch.Breaker`.

        :param ec: The EquipmentContainer containing all equipment in the feeder.
        :return: A :class:`zepben.model.streaming.streaming.FeederStreamResult
        :raises: A derivative of :class:`zepben.model.exceptions.MissingReferenceException` if a incorrect reference
                 between types is made.
        """
        return get_event_loop().run_until_complete(super().send_feeder(ec=ec))



