#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar
from zepben.evolve import BusbarSection, Queue,  BasicTraversal, ConnectivityTracker, connected_terminals

if TYPE_CHECKING:
    from zepben.evolve import ConnectivityResult
    from zepben.evolve.types import OpenTest, QueueNext
    T = TypeVar("T")

__all__ = ["create_connectivity_traversal"]


def create_connectivity_traversal(open_test: OpenTest, queue: Queue[ConnectivityResult]):
    # noinspection PyArgumentList
    return BasicTraversal(
        queue_next=_queue_next_connectivity_result_with_open_test(open_test),
        process_queue=queue,
        tracker=ConnectivityTracker()
    )


def _queue_next_connectivity_result_with_open_test(open_test: OpenTest) -> QueueNext[ConnectivityResult]:
    def queue_next(cr: ConnectivityResult, traversal: BasicTraversal[ConnectivityResult]):
        if cr.to_equip is None or open_test(cr.to_equip, None):
            return

        if isinstance(cr.to_equip, BusbarSection):
            connectivity = (
                conn
                for term in cr.to_equip.terminals
                for conn in connected_terminals(term) if conn.to_terminal is not cr.from_terminal
            )
            for conn in connectivity:
                traversal.process_queue.put(conn)

        else:
            connectivity = [
                conn
                for term in cr.to_equip.terminals if term is not cr.to_terminal
                for conn in connected_terminals(term)
            ]

            busbars = filter(lambda cn: isinstance(cn.to_equip, BusbarSection), connectivity)
            has_busbar = False
            for busbar in busbars:
                traversal.process_queue.put(busbar)
                has_busbar = True

            if not has_busbar:
                for conn in connectivity:
                    traversal.process_queue.put(conn)

    return queue_next
