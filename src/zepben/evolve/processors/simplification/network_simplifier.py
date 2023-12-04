#  Copyright 2023 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from abc import abstractmethod
from enum import Enum
from typing import Optional

from zepben.evolve.processors.simplification.reshape import Reshape

from zepben.evolve.processors.simplification.common_impedance_combiner import CommonImpedanceCombiner
from zepben.evolve.processors.simplification.equipment_container_fixer import EquipmentContainerFixer
from zepben.evolve.processors.simplification.feeder_head_terminal_resolver import FeederHeadTerminalResolver

from zepben.evolve.processors.simplification.swer_collapser import SwerCollapser

from zepben.evolve.processors.simplification.negligible_impedance_collapser import NegligibleImpedanceCollapser

from zepben.evolve.processors.simplification.switch_remover import SwitchRemover

from zepben.evolve import NetworkService, normally_open, currently_open
from zepben.evolve.processors.simplification.out_of_service_remover import OutOfServiceRemover
from zepben.evolve.processors.simplification.regulator_site_collapser import RegulatorSiteCollapser
from zepben.evolve.processors.simplification.topology_fixer import TopologyFixer


class ProcessorsController:

    @abstractmethod
    def process(self, service: NetworkService):
        raise NotImplementedError


class NetworkState(Enum):
    Normal = 0
    Current = 1


class NetworkSimplifier(ProcessorsController):

    def __init__(self,
                 regulatorSiteCollapser: Optional[RegulatorSiteCollapser] = RegulatorSiteCollapser(),
                 outOfServiceRemover: OutOfServiceRemover = OutOfServiceRemover(),
                 switchRemover: Optional[SwitchRemover] = SwitchRemover(),
                 negligibleImpedanceCollapser: NegligibleImpedanceCollapser = NegligibleImpedanceCollapser(),
                 swerCollapser: Optional[SwerCollapser] = SwerCollapser(),
                 commonImpedanceCombiner: CommonImpedanceCombiner = CommonImpedanceCombiner(),
                 topologyFixer: TopologyFixer = TopologyFixer(),
                 equipmentContainerFixer: EquipmentContainerFixer = EquipmentContainerFixer(),
                 feederHeadTerminalResolver: FeederHeadTerminalResolver = FeederHeadTerminalResolver()
                 ):
        self._regulatorSiteCollapser = regulatorSiteCollapser
        self._outOfServiceRemover = outOfServiceRemover
        self._switchRemover = switchRemover
        self._negligibleImpedanceCollapser = negligibleImpedanceCollapser
        self._swerCollapser = swerCollapser
        self._commonImpedanceCombiner = commonImpedanceCombiner
        self._topologyFixer = topologyFixer
        self._equipmentContainerFixer = equipmentContainerFixer
        self._feederHeadTerminalResolver = feederHeadTerminalResolver

    async def process(self, service: NetworkService):
        cumulativeReshape = Reshape({}, {})

        reshapers = {rs for rs in {
            self._regulatorSiteCollapser,
            self._outOfServiceRemover,
            self._switchRemover,
            self._negligibleImpedanceCollapser,
            self._swerCollapser,
            self._commonImpedanceCombiner,
            self._topologyFixer
        } if rs is not None}

        reshapePostProcessors = { rpp for rpp in {
            self._equipmentContainerFixer,
            self._feederHeadTerminalResolver
        } if rpp is not None}

        for reshaper in reshapers:
            cumulativeReshape += await reshaper.process(service, cumulativeReshape)

        for reshapePostProcessor in reshapePostProcessors:
            await reshapePostProcessor.process(service, cumulativeReshape)

        return cumulativeReshape
def temp_constructor_builder_thing(
    networkState: NetworkState = NetworkState.Normal,
    keepSplitRegulators: bool = False,
    keepSwitches: bool = False,
    minLineResistance0hms: float = 0.001,
    minLineReactance0hms: float = 0.001,
    collapsedSwerVoltage: Optional[int] = None) -> NetworkSimplifier:
    return NetworkSimplifier(
        RegulatorSiteCollapser(
            openTest=currently_open if networkState == NetworkState.Current else normally_open,
            feederDirectionProperty="current_feeder_direction" if networkState == NetworkState.Current else "normal_feeder_direction"
        ) if not keepSplitRegulators else None,
        OutOfServiceRemover(lambda ce: ce.in_service if networkState == NetworkState.Current else lambda ce: ce.normally_in_service),
        SwitchRemover(currently_open if networkState == NetworkState.Current else normally_open) if keepSwitches else None,
        NegligibleImpedanceCollapser(minLineResistance0hms, minLineReactance0hms),
        SwerCollapser(collapsedSwerVoltage) if collapsedSwerVoltage is not None else None,
        CommonImpedanceCombiner(lambda ce: ce.in_service if networkState == NetworkState.Current else lambda ce: ce.normally_in_service),
        TopologyFixer(),
        EquipmentContainerFixer(),
        FeederHeadTerminalResolver(
            feederDirectionPropertyName="current_feeder_direction" if networkState == NetworkState.Current else "normal_feeder_direction")
    )
