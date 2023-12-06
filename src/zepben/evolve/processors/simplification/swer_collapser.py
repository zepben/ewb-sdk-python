#  Copyright 2023 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Dict, Optional

from services.network import tracing
from zepben.evolve.types import PhaseSelector

from zepben.evolve.processors.simplification.reshape import Reshape

from zepben.evolve import NetworkService, BaseVoltage, PowerTransformer, TransformerFunctionKind, PowerTransformerEnd, PhaseCode, FeederDirection, LvFeeder, \
    ConductingEquipment, EnergyConsumer, RegulatingCondEq, ConnectivityNode, set_phases, CurrentPhases, NormalPhases
from zepben.evolve.processors.simplification.reshaper import Reshaper
from zepben.evolve.processors.simplification.utils import collapseGroupStartingFromNode

__all__ = ['SwerCollapser']

class SwerCollapser(Reshaper):
    baseLV: int = 250
    setPhases = set_phases()

    def __init__(self, baseLV: int = 250):
        self.baseLV = baseLV

    async def process(self, service: NetworkService, cumulativeReshapes: Reshape = None) -> Reshape:
        originalToSimplified = dict()
        simplifiedToOriginal = dict()

        def create_base_voltage() -> BaseVoltage:
            bv = BaseVoltage(mrid=f'bv-{self.baseLV}V')
            bv.nominal_voltage = self.baseLV
            service.add(bv)
            return bv

        lvBaseVoltage = next((bv for bv in service.objects(BaseVoltage) if bv.nominal_voltage == self.baseLV), create_base_voltage())

        original_list = list(service.objects(PowerTransformer))
        for pt in original_list:
            if isSwerIsolator(pt):
                await self.processIsolationTransformer(pt, service, originalToSimplified, simplifiedToOriginal, lvBaseVoltage)

        return Reshape(originalToSimplified, simplifiedToOriginal)

    async def processIsolationTransformer(self,
                                          isoTx: PowerTransformer,
                                          service: NetworkService,
                                          originalToSimplified: Dict,
                                          simplifiedToOriginal: Dict,
                                          lvBaseVoltage: BaseVoltage):
        for pte in isoTx.ends:
            if isSwer(pte):
                if pte.terminal is not None:  # if is None continue
                    lvfeeder = LvFeeder(mrid=f'{pte.terminal.mrid}-lvf')
                    lvfeeder.normal_head_terminal = pte.terminal
                    lvfeeder.add_equipment(isoTx)
                    lvfeeder.add_current_equipment(isoTx)
                    for feeder in isoTx.normal_feeders:
                        lvfeeder.add_normal_energizing_feeder(feeder)

                    isoTx.add_container(lvfeeder)
                    isoTx.add_current_container(lvfeeder)
                    for feeder in isoTx.normal_feeders:
                        feeder.add_normal_energized_lv_feeder(lvfeeder)

                    service.add(lvfeeder)

                    if pte.terminal.connectivity_node is not None:
                        NetworkService.collapseGroupStartingFromNode = collapseGroupStartingFromNode
                        collapsed_node: Optional[ConnectivityNode] = await service.collapseGroupStartingFromNode(
                            pte.terminal.connectivity_node,
                            isCollapsibleSwerEquipment,
                            originalToSimplified,
                            simplifiedToOriginal
                        )

                        if collapsed_node is not None:
                            for outerTerminal in collapsed_node.terminals:
                                if outerTerminal is not pte.terminal:
                                    outerTerminal.phases = pte.terminal.phases
                                    self.setPhases.spread_phases(pte.terminal, outerTerminal, CurrentPhases)
                                    self.setPhases.spread_phases(pte.terminal, outerTerminal, NormalPhases)

                                if outerTerminal.conducting_equipment is not None:  # if None no action required
                                    if issubclass(outerTerminal.conducting_equipment.__class__, PowerTransformer):
                                        pt_end = outerTerminal.conducting_equipment.get_end_by_terminal(outerTerminal)  # exception unhandled
                                        pt_end.base_voltage = lvBaseVoltage
                                        pt_end.rated_u = lvBaseVoltage.nominal_voltage

                                    else:
                                        outerTerminal.conducting_equipment.base_voltage = lvBaseVoltage
                                        for container in outerTerminal.conducting_equipment.containers:
                                            container.remove_equipment(outerTerminal.conducting_equipment)
                                            container.remove_current_equipment(outerTerminal.conducting_equipment)

                                        outerTerminal.conducting_equipment.clear_containers()
                                        outerTerminal.conducting_equipment.clear_current_containers()

                    for cn in pte.terminal.connected_terminals():
                        if cn.conducting_equipment is not None:
                            lvfeeder.add_equipment(cn.conducting_equipment)
                            lvfeeder.add_current_equipment(cn.conducting_equipment)
                            cn.conducting_equipment.add_container(lvfeeder)
                            cn.conducting_equipment.add_current_container(lvfeeder)


def isSwerIsolator(power_transformer: PowerTransformer) -> bool:
    return power_transformer.function is TransformerFunctionKind.isolationTransformer and any((isSwer(x) for x in power_transformer.ends))


def isSwer(pte: PowerTransformerEnd) -> bool:
    pte_voltage = 0
    if pte.base_voltage is not None:
        pte_voltage = pte.base_voltage.nominal_voltage
    elif pte.rated_u is not None:
        pte_voltage = pte.rated_u

    if pte.terminal is not None:
        if pte.terminal.phases in [PhaseCode.A, PhaseCode.B, PhaseCode.C]:
            if pte_voltage > 1000:
                if pte.terminal.normal_feeder_direction in FeederDirection.DOWNSTREAM:
                    return True
    return False


def isCollapsibleSwerEquipment(ce: ConductingEquipment) -> bool:
    if issubclass(ce.__class__, (EnergyConsumer, RegulatingCondEq)):
        return False
    if issubclass(ce.__class__, PowerTransformer):
        return ce.function != TransformerFunctionKind.isolationTransformer
    return True
