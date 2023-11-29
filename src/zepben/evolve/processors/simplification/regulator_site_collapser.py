#  Copyright 2023 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import logging
from typing import List, Dict, Optional, Set

from dataclassy import dataclass

from zepben.evolve import normally_open, set_phases, NetworkService, Terminal, ConductingEquipment, PriorityQueue, PowerTransformer, TransformerFunctionKind, \
    connected_equipment, AcLineSegment, Switch, ConnectivityNode
from zepben.evolve.processors.simplification.reshape import Reshape
from zepben.evolve.processors.simplification.reshaper import Reshaper


@dataclass(slots=True)
class Regulator:
    siteId: str
    isDistributed: bool


def isLong(acls: AcLineSegment) -> bool:
    return acls.length is not None and acls.length > 10.0


AcLineSegment.isLong = isLong


class RegulatorSiteCollapser(Reshaper):
    logger = logging.getLogger(__name__)
    openTest = normally_open
    feederDirectionProperty = lambda t: t.normal_feeder_direction

    setPhases = set_phases()

    def __init__(self, logger=None, openTest=normally_open, feederDirectionProperty=lambda t: t.normal_feeder_direction):
        self.logger = logger
        self.openTest = openTest
        self.feederDirectionProperty = feederDirectionProperty

    def process(self, service: NetworkService, cumulativeReshapes: Reshape = None) -> Reshape:
        regulatorSites = set()
        candidateTerminalsBySite = {}
        assetsBySite = {}
        self.sortAssetsBySite(service, regulatorSites, candidateTerminalsBySite, assetsBySite)

    def sortAssetsBySite(self,
                         service: NetworkService,
                         regulatorSites: Set,
                         candidateTerminalsBySite: Dict[str, List[Terminal]],
                         assetsBySite: Dict[str, List[ConductingEquipment]]):
        regulatorSites.clear()
        candidateTerminalsBySite.clear()
        assetsBySite.clear()

        # no tapChangerControl on any end | mrid

        x = PowerTransformer()

        list(x.ends)[0].ratio_tap_changer.tap_changer_control

        orphanedRegulators = RegulatorQueue()

        for transformer in service.objects(PowerTransformer):
            if transformer.function == TransformerFunctionKind.voltageRegulator:
                orphanedRegulators.put_regulator(transformer)
                regulatorSites.add(Regulator(transformer.mrid, False))
                assetsBySite[""] = []  # I don't understand yet
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
                if asset in orphanedRegulators:
                    additionalRegulators.append(asset)
                if asset not in assetsBySite[regulator.mrid] and not isinstance(asset, AcLineSegment) or not asset.isLong():
                    assetsBySite[regulator.mrid].append(asset)
                self.findCandidateTerminals(regulator.mrid, asset, assetsToProcess, candidateTerminals, regulatorSites, assetsBySite)

            if (len(candidateTerminals) > 2 and not pruneCandidateTerminalsGIS(regulator.mrid, candidateTerminals, assetsBySite)) or len(
                candidateTerminals) > 2:
                pass

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
            if connectivityNodes[i] == connectivityNodes[i-1]:
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
                            if ca in assetsBySite[regulatorId] and ca not in assetsToProcess and (not isinstance(asset, Switch) or not self.openTest(asset)):
                                assetToAdd.append(ca)
                        except KeyError:
                            pass
        assetsToProcess += assetToAdd
        candidateTerminals += newCandidateTerminals


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

    def put_regulator(self, regulator):
        self.queue.put(WrappedRegulator(regulator))

    def get_regulator(self) -> PowerTransformer:
        return self.queue.get().regulator

    def isNotEmpty(self):
        return not self.queue.empty()
