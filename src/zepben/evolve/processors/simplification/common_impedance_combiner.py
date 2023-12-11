#  Copyright 2023 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import List, Callable, Set

from dataclassy import dataclass

from zepben.evolve import NetworkService, Feeder, AcLineSegment, Terminal, ConnectivityNode, create_basic_depth_trace, BasicTraversal, \
    connected_terminals, PhaseCode, Location, CurrentPhases, NormalPhases
from zepben.evolve.processors.simplification.reshape import Reshape
from zepben.evolve.processors.simplification.reshaper import Reshaper
from zepben.evolve.services.network.tracing import tracing

__all__ = ["CommonImpedanceCombiner"]


@dataclass(slots=True)
class LineChain(object):
    lines: List[AcLineSegment]
    startTerminal: Terminal
    endTerminal: Terminal


class CommonImpedanceCombiner(Reshaper):
    in_service_test = lambda c: c.normally_in_service
    setPhases = tracing.set_phases()

    def __init__(self, in_service_test=lambda c: c.normally_in_service):
        self.in_service_test = in_service_test

    async def process(self, service: NetworkService, cumulativeReshapes: Reshape = None) -> Reshape:
        originalToSimplified = dict()
        simplifiedToOriginal = dict()

        importantNodes = set()
        for feeder in service.objects(Feeder):
            if feeder.normal_head_terminal is not None:
                if feeder.normal_head_terminal.mrid in cumulativeReshapes.originalToNew and cumulativeReshapes.originalToNew[feeder.normal_head_terminal.mrid] is not None:
                    tmp = list(cumulativeReshapes.originalToNew[feeder.normal_head_terminal.mrid])
                    if len(tmp) > 0:
                        if isinstance(tmp[0], ConnectivityNode):
                            importantNodes.add(tmp[0])
                        else:
                            importantNodes.add(feeder.normal_head_terminal.connectivity_node)
                    else:
                        importantNodes.add(feeder.normal_head_terminal.connectivity_node)
                else:
                    importantNodes.add(feeder.normal_head_terminal.connectivity_node)

        original_list = list(service.objects(AcLineSegment))

        for acls in filter(lambda ce: ce.mrid in service, original_list):
            chain = await commonImpedanceChain(acls, self.in_service_test, importantNodes)
            if len(chain.lines) > 1:
                chainRep = chain.lines[0]

                newStartTerminal = Terminal()
                newStartTerminal.phases = chain.startTerminal.phases
                newStartTerminal.current_feeder_direction = chain.startTerminal.current_feeder_direction
                newStartTerminal.normal_feeder_direction = chain.startTerminal.normal_feeder_direction
                service.add(newStartTerminal)

                newEndTerminal = Terminal()
                newEndTerminal.phases = chain.endTerminal.phases
                newEndTerminal.current_feeder_direction = chain.endTerminal.current_feeder_direction
                newEndTerminal.normal_feeder_direction = chain.endTerminal.normal_feeder_direction
                for SPK in PhaseCode.ABCN:
                    newEndTerminal.traced_phases.set_current(SPK, chain.endTerminal.traced_phases.current(SPK))
                    newEndTerminal.traced_phases.set_normal(SPK, chain.endTerminal.traced_phases.normal(SPK))

                service.add(newEndTerminal)

                sumAcls = AcLineSegment()
                sumLocations = Location()
                for line in chain.lines:
                    if line.location is not None:
                        for point in line.location.points:
                            sumLocations.add_point(point)
                service.add(sumLocations)
                sumAcls.location = sumLocations

                sumAcls.in_service = chainRep.in_service
                sumAcls.normally_in_service = chainRep.normally_in_service
                for container in chainRep.containers:
                    sumAcls.add_container(container)
                for container in chainRep.current_containers:
                    sumAcls.add_current_container(container)
                sumAcls.base_voltage = chainRep.base_voltage
                sumAcls.add_terminal(newStartTerminal)
                sumAcls.add_terminal(newEndTerminal)
                sumAcls.length = sum([line.length for line in chain.lines if line.length is not None], 0.0)
                sumAcls.asset_info = chainRep.asset_info
                sumAcls.per_length_sequence_impedance = chainRep.per_length_sequence_impedance

                service.add(sumAcls)

                if chain.startTerminal.connectivity_node is not None:
                    service.connect_by_mrid(newStartTerminal, chain.startTerminal.connectivity_node.mrid)

                if chain.endTerminal.connectivity_node is not None:
                    service.connect_by_mrid(newEndTerminal, chain.endTerminal.connectivity_node.mrid)

                self.setPhases.spread_phases(chain.startTerminal, newStartTerminal, NormalPhases)  # is that actually anything close to want I want?
                self.setPhases.spread_phases(chain.startTerminal, newStartTerminal, CurrentPhases)
                self.setPhases.spread_phases(chain.endTerminal, newStartTerminal, NormalPhases)
                self.setPhases.spread_phases(chain.endTerminal, newStartTerminal, CurrentPhases)

                service.disconnect(chain.startTerminal)
                service.disconnect(chain.endTerminal)

                mapsToLine = []

                for line in chain.lines:
                    for terminal in line.terminals:
                        if terminal.connectivity_node is not None:
                            mapsToLine.append(terminal.connectivity_node.mrid)
                            service.remove(terminal.connectivity_node)
                        mapsToLine.append(terminal.mrid)
                        service.remove(terminal)
                    mapsToLine.append(line.mrid)
                    service.remove(line)

                mapsToLine = set(mapsToLine) - {chain.startTerminal.mrid, chain.endTerminal.mrid}

                originalToSimplified[chain.startTerminal.mrid] = {newStartTerminal}
                originalToSimplified[chain.endTerminal.mrid] = {newEndTerminal}

                for mrid in mapsToLine:
                    originalToSimplified[mrid] = {sumAcls}

                simplifiedToOriginal[newStartTerminal] = {chain.startTerminal.mrid}
                simplifiedToOriginal[newEndTerminal] = {chain.endTerminal.mrid}
                simplifiedToOriginal[sumAcls] = mapsToLine

        return Reshape(originalToSimplified, simplifiedToOriginal)


async def commonImpedanceChain(acls: AcLineSegment, inServiceTest: Callable[[AcLineSegment], bool], nodesToKeep: Set[ConnectivityNode]) -> LineChain:
    backwardTerminals = []
    forwardTerminals = []

    def traceTerminalsToList(acc: List[Terminal]):
        def queue_next(t: Terminal, traversal: BasicTraversal[Terminal]):
            for to_terminal in [term.to_terminal for term in connected_terminals(t)]:
                if to_terminal.phases == t.phases:
                    if isinstance(to_terminal.conducting_equipment, AcLineSegment):
                        if to_terminal.conducting_equipment.per_length_sequence_impedance == acls.per_length_sequence_impedance:
                            if to_terminal.conducting_equipment.asset_info == acls.asset_info:
                                if inServiceTest(to_terminal.conducting_equipment) == inServiceTest(acls):
                                    for term in to_terminal.other_terminals():
                                        traversal.process_queue.put(term)

        async def stop_cond_one(t: Terminal) -> bool:
            return len(connected_terminals(t)) > 1

        async def stop_cond_two(t: Terminal) -> bool:
            return t.connectivity_node in nodesToKeep

        async def step_action_one(t: Terminal, is_stopping: bool):
            acc.append(t)

        trace = (create_basic_depth_trace(queue_next)
                 .add_stop_condition(stop_cond_one)
                 .add_stop_condition(stop_cond_two)
                 .add_step_action(step_action_one))
        return trace

    await traceTerminalsToList(backwardTerminals).run(acls.get_terminal_by_sn(1))
    await traceTerminalsToList(forwardTerminals).run(acls.get_terminal_by_sn(2))

    backwardLines = [term.conducting_equipment for term in backwardTerminals if isinstance(term.conducting_equipment, AcLineSegment)]
    forwardLines = [term.conducting_equipment for term in forwardTerminals if isinstance(term.conducting_equipment, AcLineSegment)]
    backwardLines.reverse()
    return LineChain(lines=backwardLines + forwardLines[1:], startTerminal=backwardTerminals[-1], endTerminal=forwardTerminals[-1])
