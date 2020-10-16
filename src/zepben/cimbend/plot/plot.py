


#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from collections import namedtuple
from zepben.cimbend.tracing import Traversal, queue_next_equipment, SearchType

__all__ = ["extract_latlongs"]

LatLong = namedtuple('LatLong', 'lat long')


async def extract_latlongs(network):
    """
    Performs a trace that extracts latitudes and longitudes from
    all equipment in the network.
    `network` The network to trace. Will trace the entire network from the primary sources.
    Returns Tuple of a list of latitudes and a list of longitudes,
    """
    latlongs = []

    async def save_points(equip, stopping):
        for point in equip.position_points:
            latlongs.append(LatLong(lat=point.latitude, long=point.longitude))

    start_item = network.get_primary_sources()[0]
    trace = Traversal(queue_next=queue_next_equipment, start_item=start_item, search_type=SearchType.DEPTH, step_actions=[save_points])
    await trace.trace()
    return latlongs


