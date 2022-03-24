#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations

import itertools
from typing import TYPE_CHECKING, TypeVar

from zepben.evolve.services.network.network_service import connected_terminals
if TYPE_CHECKING:
    from zepben.evolve import ConnectivityResult, BusbarSection, Traversal
    from zepben.evolve.types import OpenTest, QueueNext
    T = TypeVar("T")

__all__ = ["queue_next_connectivity_result_with_open_test"]


# TODO rename this to something sane
def queue_next_connectivity_result_with_open_test(open_test: OpenTest) -> QueueNext[ConnectivityResult]:
    def queue_next(cr: ConnectivityResult, traversal: Traversal[ConnectivityResult]):
        if cr.to_equip is None or open_test(cr.to_equip, None):
            return

        if isinstance(cr.to_equip, BusbarSection):
            connectivity = itertools.chain(*(connected_terminals(term) for term in cr.to_equip.terminals))
            for conn in connectivity:
                if conn.to_terminal != cr.from_terminal:
                    traversal.process_queue.put(conn)

        else:
            connectivity = itertools.chain(*(connected_terminals(term) for term in filter(lambda t: t != cr.to_terminal, cr.to_equip.terminals)))

            busbars = filter(lambda cn: isinstance(cn.to_equip, BusbarSection), connectivity)
            has_busbar = False
            for busbar in busbars:
                traversal.process_queue.put(busbar)
                has_busbar = True

            if not has_busbar:
                for conn in connectivity:
                    traversal.process_queue.put(conn)

    return queue_next
