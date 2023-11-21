#  Copyright 2023 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from zepben.evolve import NetworkService, Switch, Junction, Terminal
from zepben.evolve.processors.simplification.ConductingEquipmentRemover import removeEquipment
from zepben.evolve.processors.simplification.Reshape import Reshape
from zepben.evolve.processors.simplification.Reshaper import Reshaper

__all__ = ["SwitchRemover"]

NOOP = Reshape(dict(), dict())


class SwitchRemover(Reshaper):

    def process(self, service: NetworkService, cumulativeReshapes: [Reshape] = NOOP) -> Reshape:
        originalToSimplified = dict()
        simplifiedToOriginal = dict()
        original_switches = list(service.objects(Switch)) #think this is safe since removeEquipment will only remove the switch/terminals/conductivity nodes, not other conducting equipment/ other switches
        for switch in original_switches:
            if not switch.is_open():
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
                    originalToSimplified[removedIO] = set()

        # TODO: cumulativeReshape?
        return Reshape(originalToSimplified, simplifiedToOriginal)
