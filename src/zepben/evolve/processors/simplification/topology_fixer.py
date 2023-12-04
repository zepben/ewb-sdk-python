#  Copyright 2023 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Set, List

from zepben.evolve.processors.simplification.reshape import Reshape

from zepben.evolve import NetworkService, ConnectivityNode, Terminal
from zepben.evolve.processors.simplification.reshaper import Reshaper


class TopologyFixer(Reshaper):

    def process(self, service: NetworkService, cumulativeReshapes: Reshape = None) -> Reshape:
        removedMRIDs: Set[str] = set()
        addedNodes: Set[ConnectivityNode] = set()

        class Counter:
            def __init__(self, start=0):
                self.count = start

            def next(self):
                old = self.count
                self.count += 1
                return old

        wholeNumbers = Counter(1)

        original_terminal_list = list(service.objects(Terminal))

        for terminal in original_terminal_list:
            if terminal.conducting_equipment is None:
                removedMRIDs.add(terminal.mrid)
                service.disconnect(terminal)
                service.remove(terminal)
            elif terminal.connectivity_node is None:
                node = ConnectivityNode(mrid=f'generated-hanging-cn{wholeNumbers.next()}')
                service.add(node)
                service.connect_by_mrid(terminal, node.mrid)
                addedNodes.add(node)

        original_connectivity_node_list: List[ConnectivityNode] = list(service.objects(ConnectivityNode))
        for cn in original_connectivity_node_list:
            if cn.num_terminals() == 0:
                removedMRIDs.add(cn.mrid)
                service.remove(cn)

        return Reshape({mrid: set() for mrid in removedMRIDs}, {node: set() for node in addedNodes})
