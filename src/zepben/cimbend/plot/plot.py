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


from collections import namedtuple
from zepben.cimbend.tracing import Traversal, queue_next_equipment, SearchType

__all__ = ["extract_latlongs"]

LatLong = namedtuple('LatLong', 'lat long')


async def extract_latlongs(network):
    """
    Performs a trace that extracts latitudes and longitudes from
    all equipment in the network.
    :param network: The network to trace. Will trace the entire network from the primary sources.
    :return: Tuple of a list of latitudes and a list of longitudes,
    """
    latlongs = []

    async def save_points(equip, stopping):
        for point in equip.position_points:
            latlongs.append(LatLong(lat=point.latitude, long=point.longitude))

    start_item = network.get_primary_sources()[0]
    trace = Traversal(queue_next=queue_next_equipment, start_item=start_item, search_type=SearchType.DEPTH, step_actions=[save_points])
    await trace.trace()
    return latlongs


