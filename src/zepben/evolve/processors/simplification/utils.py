#  Copyright 2023 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Optional, Collection, List, Set, Callable

from zepben.evolve import NetworkService, ConnectivityNode, IdentifiedObject, Terminal, Traversal, BasicTraversal, create_basic_depth_trace

class Counter:
    def __init__(self, start=0):
        self.count = start

    def next(self):
        old = self.count
        self.count += 1
        return old


class NameFactory():

    def __init__(self):
        self.counter = Counter()

    def get_name(self):
        return self.counter.next()


terminal_name_factory = NameFactory()
cn_name_factory = NameFactory()
ac_name_factory = NameFactory()

def collapseIntoConnectivityNode(service: NetworkService,
                                 outerTerminals: Collection[Terminal],
                                 innerObjects: Collection[IdentifiedObject],
                                 originalToSimplified,
                                 simplifiedToOriginal) -> Optional[ConnectivityNode]:
    if len(innerObjects) <= 1:
        return None

    collapsedNode = ConnectivityNode("cn-"+str(cn_name_factory.get_name()))
    service.add(collapsedNode)
    simplifiedObjects = {collapsedNode}

    for terminal in outerTerminals:
        service.disconnect(terminal)
        service.connect_by_mrid(terminal, collapsedNode.mrid)

    for io in innerObjects:
        service.remove(io)
        originalToSimplified[io.mrid] = simplifiedObjects

    simplifiedToOriginal[collapsedNode.mrid] = {io.mrid for io in innerObjects}
    return collapsedNode


def traceCollapsibleGroup(outerTerminals: List[Terminal],
                          innerObjects: Set[IdentifiedObject],
                          collapsible: Callable,
                          ) -> Traversal:
    def myTraversal(cn: ConnectivityNode, traversal: BasicTraversal):
        innerObjects.add(cn)

        for terminal in cn.terminals:
            ce = terminal.conducting_equipment
            if ce is None:
                innerObjects.add(terminal)
            else:
                if not collapsible(ce):
                    outerTerminals.append(terminal)
                else:
                    if ce not in innerObjects:
                        innerObjects.add(ce)
                        for t in ce.terminals:
                            innerObjects.add(t)
                            if t.connectivity_node is not None:
                                traversal.process_queue.put(t.connectivity_node)

    return create_basic_depth_trace(myTraversal)


async def collapseGroupStartingFromNode(service: NetworkService, node: ConnectivityNode, collapsible, originalToSimplified,
                                        simplifiedToOriginal) -> Optional[ConnectivityNode]:
    outerTerminals = list()
    innerObjects = set()
    await traceCollapsibleGroup(outerTerminals, innerObjects, collapsible).run(node)
    return collapseIntoConnectivityNode(service, outerTerminals, innerObjects, originalToSimplified, simplifiedToOriginal)
