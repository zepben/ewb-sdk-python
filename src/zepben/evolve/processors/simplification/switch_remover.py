#  Copyright 2023 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from zepben.evolve import NetworkService, Switch, Junction, Terminal, normally_open
from zepben.evolve.processors.simplification.conducting_equipment_remover import removeEquipment
from zepben.evolve.processors.simplification.reshape import Reshape
from zepben.evolve.processors.simplification.reshaper import Reshaper

__all__ = ["SwitchRemover"]

NOOP = Reshape(dict(), dict())


class SwitchRemover(Reshaper):
    open_test = normally_open

    def __init__(self, open_test=normally_open):
        self.open_test = open_test

    def process(self, service: NetworkService, cumulativeReshapes: [Reshape] = NOOP) -> Reshape:
        originalToSimplified = dict()
        simplifiedToOriginal = dict()
        original_switches = list(service.objects(
            Switch))  # ...think this is safe since removeEquipment will only remove the switch/terminals/conductivity nodes, not other conducting equipment/ other switches
        for switch in original_switches:
            if not self.open_test(switch):
                newJuction = Junction()
                service.add(newJuction)
                for terminal in switch.terminals:
                    newTerminal = Terminal()
                    service.add(newTerminal)
                    newJuction.add_terminal(newTerminal)
                    if terminal.connectivity_node is not None:
                        service.connect_by_mrid(newTerminal, terminal.connectivity_node.mrid)
                        originalToSimplified[terminal.mrid] = {newTerminal}
                        simplifiedToOriginal[newTerminal] = {terminal.mrid}
                originalToSimplified[switch.mrid] = {newJuction}
                simplifiedToOriginal[newJuction] = {switch.mrid}
                removeEquipment(switch, service)
            else:
                for removedIO in removeEquipment(switch, service):
                    originalToSimplified[removedIO.mrid] = set()

        # TODO: cumulativeReshape?
        return Reshape(originalToSimplified, simplifiedToOriginal)
