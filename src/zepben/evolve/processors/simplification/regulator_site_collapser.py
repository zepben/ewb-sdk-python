#  Copyright 2023 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import logging
from typing import List, Dict, Optional, Set, Callable

from dataclassy import dataclass

from zepben.evolve import normally_open, set_phases, NetworkService, Terminal, ConductingEquipment, PriorityQueue, PowerTransformer, TransformerFunctionKind, \
    connected_equipment, AcLineSegment, Switch, ConnectivityNode, phase_code_from_single_phases, IdentifiedObject, SinglePhaseKind, FeederDirection, PhaseCode, \
    normal_phases, current_phases, PowerTransformerEnd
from zepben.evolve.processors.simplification.conducting_equipment_remover import removeEquipment
from zepben.evolve.processors.simplification.reshape import Reshape
from zepben.evolve.processors.simplification.reshaper import Reshaper


class Regulator:
    siteId: str = None
    isDistributed: bool = None

    def __init__(self, siteId, isDistributed):
        self.siteId = siteId
        self.isDistributed = isDistributed


def isLong(acls: AcLineSegment) -> bool:
    return acls.length is not None and acls.length > 10.0


AcLineSegment.isLong = isLong


class RegulatorSiteCollapser(Reshaper):
    logger = logging.getLogger(__name__)
    openTest = normally_open
    feederDirectionProperty = None
    getFeederDirectionProperty: Callable = None
    setFeederDirectionProperty: Callable = None
    setPhases = set_phases()

    def __init__(self, logger=logging.getLogger(__name__), openTest=normally_open, feederDirectionProperty: str = "normal_feeder_direction"):
        self.logger = logger
        self.openTest = openTest
        self.feederDirectionProperty = getattr(Terminal, feederDirectionProperty)
        self.getFeederDirectionProperty = lambda t: self.feederDirectionProperty.__get__(t)
        self.setFeederDirectionProperty = lambda t, v: self.feederDirectionProperty.__set__(t, v)

    async def process(self, service: NetworkService, cumulativeReshapes: Reshape = None) -> Reshape:
        regulatorSites: Set[Regulator] = set()
        candidateTerminalsBySite: Dict[str, Set[Terminal]] = {}
        assetsBySite: Dict[str, List[ConductingEquipment]] = {}

        self.sortAssetsBySite(service, regulatorSites, candidateTerminalsBySite, assetsBySite)

        originalToSimplified: Dict[str, Set[IdentifiedObject]] = {}
        simplifiedToOriginal: Dict[IdentifiedObject, Set[str]] = {}

        for regulator in regulatorSites:
            candidateTerminals: Set[Terminal] = set()
            if regulator.siteId in candidateTerminalsBySite.keys():
                candidateTerminals = candidateTerminalsBySite[regulator.siteId]

            assetsBySiteGreaterThanOne = False
            if regulator.siteId in assetsBySite.keys():
                assetsBySiteGreaterThanOne = len(assetsBySite[regulator.siteId]) > 1

            if regulator.isDistributed or assetsBySiteGreaterThanOne:
                removedMRIDs, addedObjects = self.replaceRegulatorSite(service, assetsBySite, regulator, candidateTerminals)
                for mRIDS in removedMRIDs:
                    originalToSimplified[mRIDS] = addedObjects
                for io in addedObjects:
                    simplifiedToOriginal[io] = removedMRIDs

        return Reshape(originalToSimplified, simplifiedToOriginal)

    def replaceRegulatorSite(self,
                             service: NetworkService,
                             assetsBySite: Dict[str, List[ConductingEquipment]],
                             regulatorInfo: Regulator,
                             candidateTerminals: Set[Terminal]) -> (Set[str], Set[IdentifiedObject]):
        childAssets: Optional[List[ConductingEquipment]] = None
        if regulatorInfo.siteId in assetsBySite.keys():
            childAssets = assetsBySite[regulatorInfo.siteId]

        if childAssets is None:
            raise Exception(f'INTERNAL ERROR: Failed to remove regulator site for {regulatorInfo.siteId} as it is not found in the site list???? '
                            f'How the heck is that possible???')

        removedMRIDs: Set[str] = set()
        addedObjects: Set[IdentifiedObject] = set()

        regulator = self.disconnectAndRemove(service, childAssets, removedMRIDs)

        if regulator is not None:
            self.pruneCandidateTerminals(service, regulatorInfo.siteId, candidateTerminals)
            if regulatorInfo.isDistributed:
                addedObjects.add(self.createConnectingNode(service, regulator, candidateTerminals, removedMRIDs))
            else:
                for io in self.createRegulator(service, regulator, candidateTerminals):
                    addedObjects.add(io)
        else:
            self.logger.warning(f'Regulator {regulatorInfo.siteId} has been removed while attempting to collapse. '
                                f'Please contact your administrator to ensure the regulator tee off points belong to the regulator site.')

        return removedMRIDs, addedObjects

    def createRegulator(self,
                        service: NetworkService,
                        oldRegulator: PowerTransformer,
                        candidateTerminals: Set[Terminal]) -> Set[IdentifiedObject]:
        regulator = PowerTransformer(mrid=f'{oldRegulator.mrid}-collapsed')
        regulator.location = oldRegulator.location
        regulator.in_service = oldRegulator.in_service
        regulator.normally_in_service = oldRegulator.normally_in_service
        regulator.commissioned_date = oldRegulator.commissioned_date
        for container in oldRegulator.containers:
            regulator.add_container(container)
        for current_container in oldRegulator.current_containers:
            regulator.add_current_container(current_container)
        for usage_pair in oldRegulator.usage_points:
            regulator.add_usage_point(usage_pair)
        for operational_restrictions in oldRegulator.operational_restrictions:
            regulator.add_operational_restriction(operational_restrictions)
        regulator.base_voltage = oldRegulator.base_voltage
        regulator.vector_group = oldRegulator.vector_group
        regulator.transformer_utilisation = oldRegulator.transformer_utilisation
        regulator.construction_kind = oldRegulator.construction_kind
        regulator.function = oldRegulator.function

        if len(candidateTerminals) < 2:
            self.logger.error(f'Could not determine connection points for regulator {oldRegulator.mrid}. This regulator will not be created.')
            return set()

        service.add(regulator)

        firstTerminalFirst: Optional[bool] = None
        """
                if not any({self.feederDirectionProperty(t) in [FeederDirection.UPSTREAM, FeederDirection.DOWNSTREAM]
                    and any([self.feederDirectionProperty(ta) != self.feederDirectionProperty(t) for ta in t.other_terminals()])
                    for t in candidateTerminals}):
        """

        do_the_thing = True

        for t in candidateTerminals:
            if self.getFeederDirectionProperty(t) in [FeederDirection.UPSTREAM, FeederDirection.DOWNSTREAM]:
                if any({self.getFeederDirectionProperty(ta) != self.getFeederDirectionProperty(t) for ta in t.other_terminals()}):
                    do_the_thing = False

        if do_the_thing:
            candidateTerminalsList: List[Terminal] = list(candidateTerminals)
            for i, terminal in enumerate(candidateTerminalsList):
                connectedAssets: List[ConductingEquipment] = [rs.to_equip for rs in connected_equipment(terminal.conducting_equipment)]

                for asset in connectedAssets:
                    if any({self.getFeederDirectionProperty(t) != self.getFeederDirectionProperty(next(asset.terminals)) for t in asset.terminals}):
                        if isinstance(asset, AcLineSegment):
                            """
                            possibleOutConnection: bool = False
                            for ca in connectedAssets:
                                for t in ca.terminals:
                                    if self.feederDirectionProperty(t) == FeederDirection.BOTH:
                                        possibleOutConnection = True
                                        break
                                if possibleOutConnection:
                                    break
                            """
                            firstTerminalFirst = self.determineDirectionFromConductor(asset,
                                                                                      terminal.conducting_equipment,
                                                                                      i,
                                                                                      any({self.getFeederDirectionProperty(t) == FeederDirection.BOTH for t in
                                                                                           [ca.terminals for ca in connectedAssets]}))
                        else:
                            connectedAssets2 = [rs.to_equip for rs in connected_equipment(asset)]
                            possibleOutConnection: bool = any({self.getFeederDirectionProperty(t) == FeederDirection.BOTH for t in
                                                               [ca.terminals for ca in connectedAssets2]})

                            for ca in filter(lambda ce: isinstance(ce, AcLineSegment), connectedAssets2):
                                if any({self.getFeederDirectionProperty(t) != self.getFeederDirectionProperty(next(ca.terminals)) for t in ca.terminals}):
                                    firstTerminalFirst = self.determineDirectionFromConductor(ca, asset, i, possibleOutConnection)
                                    if (i == 0) == firstTerminalFirst:
                                        break
                if firstTerminalFirst is not None:
                    break

            if firstTerminalFirst is None:
                self.logger.warning(
                    f'Could not definitively determine primary terminal of regulator {regulator.mrid}. Regulator direction may or may not be inverted.')
                for candidateTerminal in candidateTerminals:
                    self.addTerminalConnectionForRegulator(service, regulator, candidateTerminal)
            elif firstTerminalFirst:
                for i in range(len(candidateTerminals)):
                    self.addTerminalConnectionForRegulator(service, regulator, candidateTerminalsList[i])
            else:
                for i in reversed(range(len(candidateTerminals))):
                    self.addTerminalConnectionForRegulator(service, regulator, candidateTerminalsList[i])

        else:
            for t in candidateTerminals:
                if (self.getFeederDirectionProperty(t) == FeederDirection.DOWNSTREAM and
                    any({self.getFeederDirectionProperty(ta) != FeederDirection.DOWNSTREAM for ta in t.other_terminals()})):
                    self.addTerminalConnectionForRegulator(service, regulator, t)
            for t in candidateTerminals:
                if (self.getFeederDirectionProperty(t) == FeederDirection.DOWNSTREAM and
                    all({self.getFeederDirectionProperty(ta) == FeederDirection.DOWNSTREAM for ta in t.other_terminals()})):
                    self.addTerminalConnectionForRegulator(service, regulator, t)
            for t in candidateTerminals:
                if self.getFeederDirectionProperty(t) == FeederDirection.BOTH or self.getFeederDirectionProperty(t) == FeederDirection.NONE:
                    self.addTerminalConnectionForRegulator(service, regulator, t)
            for t in candidateTerminals:
                if (self.getFeederDirectionProperty(t) == FeederDirection.UPSTREAM and
                    all({self.getFeederDirectionProperty(ta) == FeederDirection.UPSTREAM for ta in t.other_terminals()})):
                    self.addTerminalConnectionForRegulator(service, regulator, t)
            for t in candidateTerminals:
                if (self.getFeederDirectionProperty(t) == FeederDirection.UPSTREAM and
                    any({self.getFeederDirectionProperty(ta) != FeederDirection.UPSTREAM for ta in t.other_terminals()})):
                    self.addTerminalConnectionForRegulator(service, regulator, t)

        if regulator.get_terminal_by_sn(1).phases != regulator.get_terminal_by_sn(1).phases:  # appears to be a bug
            self.logger.warning(f'Regulator {regulator.mrid} has different phasing at its primary and secondary.')
            toReturn = set(regulator.terminals)  # should make the return type frozenSet {} + {}
            toReturn.add(regulator)
            return toReturn

        regulatorPhase = oldRegulator.get_terminal_by_sn(1).phases
        regulatorPhaseWhen = regulator.get_terminal_by_sn(1).phases

        if regulatorPhaseWhen in [PhaseCode.A, PhaseCode.B, PhaseCode.C]:
            self.logger.warning(f'Regulator {regulator.mrid} is a SWER regulator. This is not supported at present.')
        elif regulatorPhaseWhen == PhaseCode.AB:
            regulatorPhase = PhaseCode.A
        elif regulatorPhaseWhen == PhaseCode.BC:
            regulatorPhase = PhaseCode.B
        elif regulatorPhaseWhen == PhaseCode.AC:
            regulatorPhase = PhaseCode.C

        for terminal in regulator.terminals:
            terminal.phases = regulatorPhase
            self.createEnd(service, regulator, terminal, oldRegulator)
        toReturn = set(regulator.terminals)
        toReturn.add(regulator)
        return toReturn

    def createEnd(self,
                  service: NetworkService,
                  regulator: PowerTransformer,
                  regTerminal: Terminal,
                  oldRegulator: PowerTransformer):
        end: PowerTransformerEnd = PowerTransformerEnd(mrid=f'{regulator.mrid}-e{regTerminal.sequence_number}')
        end.power_transformer = regulator
        end.terminal = regTerminal

        regulator.add_end(end)
        service.add(end)

        tapChanger = None  # appears to be unused
        ratio_tap_changers = [end.ratio_tap_changer for end in oldRegulator.ends if end.ratio_tap_changer is not None]
        if len(ratio_tap_changers) > 0:
            tapChanger = ratio_tap_changers[0]

        try:
            oldEnd = oldRegulator.get_end_by_num(regTerminal.sequence_number)
            end.grounded = oldEnd.grounded
            end.r_ground = oldEnd.r_ground
            end.x_ground = oldEnd.x_ground
            end.base_voltage = oldEnd.base_voltage
            end.ratio_tap_changer = oldEnd.ratio_tap_changer
            if oldEnd.ratio_tap_changer is not None:
                oldEnd.ratio_tap_changer.transformer_end = end
            end.star_impedance = oldEnd.star_impedance
            end.b = oldEnd.b
            end.b0 = oldEnd.b0
            end.connection_kind = oldEnd.connection_kind
            end.g = oldEnd.g
            end.g0 = oldEnd.g0
            end.phase_angle_clock = oldEnd.phase_angle_clock
            end.r = oldEnd.r
            end.r0 = oldEnd.r0
            end.rated_u = oldEnd
            end.x = oldEnd.x
            end.x0 = oldEnd.x0
            for rating in oldEnd.s_ratings:
                end.add_transformer_end_rated_s(rating)



        except IndexError:
            pass

    def createTerminalOnRegulator(self, service: NetworkService, regulator: PowerTransformer, phaseCode: PhaseCode) -> Terminal:
        newTerminal = Terminal(mrid=f'{regulator.mrid}-t{regulator.num_terminals() + 1}', phases=phaseCode)
        regulator.add_terminal(newTerminal)
        service.add(newTerminal)
        return newTerminal

    def addTerminalConnectionForRegulator(self,
                                          service: NetworkService,
                                          regulator: PowerTransformer,
                                          candidateTerminal: Terminal):
        terminal: Terminal = self.createTerminalOnRegulator(service, regulator, candidateTerminal.phases)
        assignThisToFeederDirectionProperty = ~self.getFeederDirectionProperty(candidateTerminal)  # change from callable to property?
        self.setFeederDirectionProperty(terminal, assignThisToFeederDirectionProperty)
        service.connect_terminals(candidateTerminal, terminal)
        self.setPhases.spread_phases(candidateTerminal, terminal, normal_phases)
        self.setPhases.spread_phases(candidateTerminal, terminal, current_phases)

    def determineDirectionFromConductor(self,
                                        conductor: AcLineSegment,
                                        startPointAsset: ConductingEquipment,
                                        terminalNumber: int,
                                        possibleOutConnection: bool
                                        ) -> bool:
        firstTerminalFirst: Optional[bool] = None

        for terminal1 in conductor.terminals:
            if terminal1.connectivity_node is not None:
                if any({t.conducting_equipment == startPointAsset for t in terminal1.connectivity_node.terminals}):
                    if self.getFeederDirectionProperty(terminal1) == FeederDirection.DOWNSTREAM:
                        firstTerminalFirst = terminalNumber == 0
                    elif self.getFeederDirectionProperty(terminal1) == FeederDirection.UPSTREAM and not possibleOutConnection:
                        firstTerminalFirst = terminalNumber == 1
                    break
        return firstTerminalFirst

    def createConnectingNode(self,
                             service: NetworkService,
                             removedRegulator: PowerTransformer,
                             candidateTerminals: Set[Terminal],
                             removedMRIDs: Set[str]) -> ConnectivityNode:
        connectingNode = ConnectivityNode(mrid=f'{removedRegulator.mrid}-collapsed-node')
        service.add(connectingNode)
        for terminal in candidateTerminals:
            if terminal.connectivity_node is not None and terminal.connectivity_node.num_terminals() == 1:
                removedMRIDs.add(terminal.connectivity_node.mrid)
            service.disconnect(terminal)
            service.connect_by_mrid(terminal, connectingNode.mrid)

        return connectingNode

    def pruneCandidateTerminals(self, service: NetworkService, siteId: str, terminals: Set[Terminal]):
        if len(terminals) == 2:
            return
        if len(terminals) < 2:
            self.logger.warning(f'Regulator {siteId} does not have enough candidate terminals and will not be collapsed.')

        terminalsByOtherEnd: Dict[ConductingEquipment, List[Terminal]] = {}
        terminalsCopy: List[Terminal] = list(terminals)

        for terminal in terminalsCopy:
            otherEnd: List[ConductingEquipment] = self.connectedToOtherEnd(terminal)
            if len(otherEnd) == 0:
                if terminal.conducting_equipment is not None:
                    service.remove(terminal.conducting_equipment)
                    terminals.remove(terminal)
                else:
                    for other in otherEnd:
                        if other not in terminalsByOtherEnd.keys():
                            terminalsByOtherEnd[other] = []
                        terminalsByOtherEnd[other].append(terminal)

        for asset, otherEndTerminals in terminalsByOtherEnd.items():
            if len(otherEndTerminals) > 1:
                for terminal in asset.terminals:
                    self.removeAssetChain(service, terminal, terminals)

                    service.disconnect(terminal)
                    service.remove(terminal)
                service.remove(asset)

        if len(terminals) > 2:
            self.logger.warning(f'Regulator {siteId} has too many viable terminals and will not be collapsed correctly. '
                                f'Please contact your administrator to ensure the regulator tee off points belong to the regulator site.')
        elif len(terminals) < 2:
            self.logger.warning(f'Regulator {siteId} does not have enough viable terminals and will not be collapsed correctly. '
                                f'Please contact your administrator to ensure the regulator tee off points belong to the regulator site.')

    def removeAssetChain(self, service: NetworkService, terminal: Terminal, terminals: Set[Terminal]):
        connectedTerminals: List[Terminal] = list(terminal.connected_terminals())
        if len(connectedTerminals) > 1:
            return

        service.disconnect(terminal)
        if terminal.conducting_equipment is not None:
            service.remove(terminal.conducting_equipment)
        terminals.remove(terminal)

        if len(connectedTerminals) > 0:
            connectedTerminal = connectedTerminals[0]
            service.disconnect(connectedTerminal)
            other = next(connectedTerminal.other_terminals(), None)
            if other is not None:
                self.removeAssetChain(service, other, terminals)

    def connectedToOtherEnd(self, terminal: Terminal) -> List[ConductingEquipment]:
        toReturn: List[ConductingEquipment] = []

        other = next(terminal.other_terminals(), None)
        if other is not None:
            for connected in other.connected_terminals():
                if connected.conducting_equipment is not None:
                    toReturn.append(connected.conducting_equipment)

        return toReturn

    def disconnectAndRemove(self,
                            service: NetworkService,
                            childAssets: List[ConductingEquipment],
                            removedMRIDs: Set[str]) -> Optional[PowerTransformer]:
        regulator: Optional[PowerTransformer] = None
        regulatorPhases: Set[SinglePhaseKind] = set()
        regulatorCount = 0

        for asset in childAssets:
            for removed in removeEquipment(asset, service):
                removedMRIDs.add(removed.mrid)
            if isinstance(asset, PowerTransformer) and asset.function == TransformerFunctionKind.voltageRegulator:
                regulatorCount += 1
                for phase in next(asset.terminals).phases.single_phases:
                    regulatorPhases.add(phase)
                if regulator is None or len(regulator.name) > len(asset.name):
                    regulator = asset

        if regulator is not None:
            for terminal in regulator.terminals:
                terminal.phases = phase_code_from_single_phases(regulatorPhases)

        return regulator

    def sortAssetsBySite(self,
                         service: NetworkService,
                         regulatorSites: Set[Regulator],
                         candidateTerminalsBySite: Dict[str, Set[Terminal]],
                         assetsBySite: Dict[str, List[ConductingEquipment]]):
        regulatorSites.clear()
        candidateTerminalsBySite.clear()
        assetsBySite.clear()

        orphanedRegulators = RegulatorQueue()

        for transformer in service.objects(PowerTransformer):
            if transformer.function == TransformerFunctionKind.voltageRegulator:
                orphanedRegulators.put_regulator(transformer)
                regulatorSites.add(Regulator(transformer.mrid, False))
                if "" not in assetsBySite.keys():
                    assetsBySite[""] = []
                else:
                    if transformer in assetsBySite[""]:
                        assetsBySite[""].remove(transformer)
                assetsBySite[transformer.mrid] = [transformer]

        while orphanedRegulators.isNotEmpty():
            regulator = orphanedRegulators.get_regulator()
            assetsToProcess = set()
            candidateTerminals = set()

            for t in regulator.terminals:
                if len(list(t.connected_terminals())) == 0:
                    candidateTerminals.add(t)

            self.findCandidateTerminals(regulator.mrid, regulator, assetsToProcess, candidateTerminals, regulatorSites, assetsBySite)

            additionalRegulators: List[ConductingEquipment] = []
            removeAdditionalRegulators = True

            while len(assetsToProcess) > 0:
                asset = assetsToProcess.pop()
                if asset in orphanedRegulators.get_list():
                    additionalRegulators.append(asset)
                if asset not in assetsBySite[regulator.mrid] and not isinstance(asset, AcLineSegment) or not asset.isLong():
                    assetsBySite[regulator.mrid].append(asset)
                self.findCandidateTerminals(regulator.mrid, asset, assetsToProcess, candidateTerminals, regulatorSites, assetsBySite)

            if (len(candidateTerminals) > 2 and not self.pruneCandidateTerminalsGIS(regulator.mrid, candidateTerminals, assetsBySite)) or \
                len(candidateTerminals) < 2:
                regulatorSites &= {rs for rs in regulatorSites if rs.siteId != regulator.mrid}
                removeAdditionalRegulators = False
                self.logger.warning(f'Unable to collapse site for regulator {regulator.mrid}. Regulator site will be as per original EWB data.')

            for additionalRegulator in additionalRegulators:
                if removeAdditionalRegulators:
                    additionalPhases = additionalRegulator.get_terminal_by_sn(1).phases
                    for t in regulator.terminals:
                        t.phases = phase_code_from_single_phases(t.phases.single_phases + additionalPhases.single_phases)
                regulatorSites &= {rs for rs in regulatorSites if rs.siteId != additionalRegulator.mrid}
                orphanedRegulators.remove_regulator(additionalRegulator)
            candidateTerminalsBySite[regulator.mrid] = candidateTerminals

    def pruneCandidateTerminalsGIS(self, regulatorId: str, terminals: Set[Terminal], assetsBySite: Dict[str, List[ConductingEquipment]]) -> bool:
        if len(terminals) == 2:
            return True
        if len(terminals) > 3:
            self.logger.warning(f'Regulator {regulatorId} has too many viable terminals and will not be collapsed correctly. '
                                f'Please contact your administrator to ensure the incoming and outgoing lines at the regulator site are correct.')
            return False

        connectivityNodes: List[ConnectivityNode] = [terminal.connectivity_node for terminal in terminals]

        if len(connectivityNodes) != len(terminals):
            self.logger.warning(f'Could not find connectivity node for all externally connecting terminals for regulator {regulatorId}. '
                                f'Please contact your administrator to ensure the incoming and outgoing lines at the regulator site are correct.')

        repeatedIndex = -1
        newCandidate: Optional[Terminal] = None

        for i in range(1, len(terminals)):
            if connectivityNodes[i] == connectivityNodes[i - 1]:
                tmp = next((t for t in connectivityNodes[i].terminals if t not in terminals), None)
                if tmp is not None:
                    newCandidate = next(tmp.other_terminals())
                    repeatedIndex = i
                    break
                else:
                    self.logger.warning(f'Could not prune extra connections for regulator {regulatorId}. '
                                        f'Please contact your administrator to ensure the incoming and outgoing lines at the regulator site are correct.')
                    return False

        if repeatedIndex == -1:
            self.logger.warning(f'Could not prune extra connections for regulator {regulatorId}. '
                                f'Please contact your administrator to ensure the incoming and outgoing lines at the regulator site are correct.')
            return False

        duplicateTerminals = {t for t in terminals if t in connectivityNodes[repeatedIndex].terminals}
        terminals -= duplicateTerminals

        try:
            if newCandidate.conducting_equipment in assetsBySite[regulatorId]:
                assetsBySite[regulatorId].remove(newCandidate.conducting_equipment)
        except KeyError:
            pass

        return True

    def findCandidateTerminals(self,
                               regulatorId: str,
                               asset: ConductingEquipment,
                               assetsToProcess: Set[ConductingEquipment],
                               candidateTerminals: Set[Terminal],
                               regulatorSites: Set[Regulator],
                               assetsBySite: Dict[str, List[ConductingEquipment]]):
        assetToAdd: List[ConductingEquipment] = []
        newCandidateTerminals: Set[Terminal] = set()

        for cr in connected_equipment(asset):
            ca = cr.to_equip
            if isinstance(ca, AcLineSegment) and ca.isLong():
                for terminal in ca.terminals:
                    if terminal.connectivity_node is not None:
                        if any(t.conducting_equipment == asset for t in terminal.connectivity_node.terminals):
                            if terminal not in candidateTerminals and terminal not in newCandidateTerminals:
                                if not isinstance(asset, Switch) or not self.openTest(asset):  # is not a switch or is closed switch
                                    if len(newCandidateTerminals) > 0 and regulatorId != asset.mrid:
                                        try:
                                            assetsBySite[regulatorId].remove(asset)
                                        except KeyError:
                                            pass
                                        except ValueError:
                                            pass
                                        candidateTerminals.add(next(t for t in asset.terminals if t not in terminal.connected_terminals()))
                                        return
                                    newCandidateTerminals.add(terminal)
                        rs = next((r for r in regulatorSites if r.siteId == regulatorId), None)
                        if rs is not None:
                            if not rs.isDistributed:
                                for farTerminal in terminal.connectivity_node.terminals:
                                    if farTerminal.conducting_equipment != asset:
                                        for regulator1 in regulatorSites:
                                            if regulator1.siteId != regulatorId:
                                                if farTerminal.conducting_equipment in assetsBySite[regulator1.siteId]:
                                                    rs.isDistributed = True
            else:
                try:
                    if (ca not in assetsBySite[regulatorId] and
                        ca not in assetsToProcess and
                        (not isinstance(asset, Switch) or not self.openTest(asset))):
                        assetToAdd.append(ca)
                except KeyError:
                    pass
        assetsToProcess |= set(assetToAdd)
        candidateTerminals |= newCandidateTerminals


class WrappedRegulator:
    regulator = None

    def __init__(self, regulator):
        self.regulator = regulator

    def __lt__(self, other):
        if self.has_tap_changers(self.regulator) == self.has_tap_changers(other.regulator):
            return self.regulator.mrid < other.regulator.mrid
        return self.has_tap_changers(self.regulator) > self.has_tap_changers(other.regulator)

    def has_tap_changers(self, regulator: PowerTransformer) -> bool:
        has_tap_changer = False
        for end in regulator.ends:
            if end.ratio_tap_changer is not None and end.ratio_tap_changer.tap_changer_control is not None:
                has_tap_changer = True
        return has_tap_changer


class RegulatorQueue:
    queue = PriorityQueue()

    def get_list(self) -> List[PowerTransformer]:
        return [r.regulator for r in list(self.queue.queue)]

    def put_regulator(self, regulator: PowerTransformer):
        self.queue.put(WrappedRegulator(regulator))

    def get_regulator(self) -> PowerTransformer:
        return self.queue.get().regulator

    def isNotEmpty(self):
        return not self.queue.empty()

    def remove_regulator(self, regulator: PowerTransformer):
        theAbsoluteWorst = PriorityQueue()
        while self.isNotEmpty():
            tmp = self.get_regulator()
            if tmp is not regulator:
                theAbsoluteWorst.put(WrappedRegulator(tmp))
        self.queue = theAbsoluteWorst
