#  Copyright 2023 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import List

from zepben.evolve import ConductingEquipment, NetworkService, IdentifiedObject

# TODO: docs
"""
Removes conducting equipment along with its terminals. Also removes any connectivity nodes left without terminals.
return List of removed objects.
"""


def removeEquipment(ce: ConductingEquipment, service: NetworkService) -> List[IdentifiedObject]:
    removedObjects: List[IdentifiedObject] = []

    for terminal in ce.terminals:
        if terminal.connectivity_node is not None:
            node = terminal.connectivity_node
            service.disconnect(terminal)
            if node.num_terminals() == 0:
                removedObjects.append(node)
        service.remove(terminal)
        removedObjects.append(terminal)

    service.remove(ce)
    removedObjects.append(ce)
    return removedObjects
