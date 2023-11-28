#  Copyright 2023 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Optional, List, Callable, Set, Iterable, Collection

from zepben.evolve.processors.simplification.reshape import Reshape

from zepben.evolve import NetworkService, ConnectivityNode, ConductingEquipment, EnergySource, EnergyConsumer, PowerTransformer, Switch, RegulatingCondEq, \
    AcLineSegment, connected_equipment, ShuntCompensator
from zepben.evolve.processors.simplification.reshaper import Reshaper
from zepben.evolve.processors.simplification.utils import collapseGroupStartingFromNode


class NegligibleImpedanceCollapser(Reshaper):
    minLineResistance0hms: float
    minLineReactance0hms: float

    def __init__(self, minLineResistance0hms: float = 0.001, minLineReactance0hms: float = 0.001):
        self.minLineResistance0hms = minLineResistance0hms
        self.minLineReactance0hms = minLineReactance0hms

    async def process(self, service: [NetworkService], cumulativeReshapes: [Reshape] = None) -> Reshape:
        originalToSimplified = dict()
        simplifiedToOriginal = dict()

        original_list = list(service.objects(ConnectivityNode))
        NetworkService.collapseGroupStartingFromNode = collapseGroupStartingFromNode
        for node in filter(lambda ce: ce.mrid in service, original_list):  # ...does this actually work...
            await service.collapseGroupStartingFromNode(node, self.canCollapse, originalToSimplified, simplifiedToOriginal)
        return Reshape(originalToSimplified, simplifiedToOriginal)

    def canCollapse(self, equipment: ConductingEquipment) -> bool:
        if issubclass(equipment.__class__, (EnergySource, EnergyConsumer, PowerTransformer, Switch, RegulatingCondEq)):
            return False
        elif issubclass(equipment.__class__, AcLineSegment):
            return self.hasNegligibleImpedance(equipment) and not self.connectedToShuntCompensator(equipment)
        else:
            return True

    def hasNegligibleImpedance(self, acls: AcLineSegment) -> bool:
        length = 0.0 if acls.length is None else acls.length

        r = 0.0
        x = 0.0
        if acls.per_length_sequence_impedance is not None:
            if acls.per_length_sequence_impedance.r is not None:
                r = acls.per_length_sequence_impedance.r
            if acls.per_length_sequence_impedance.x is not None:
                x = acls.per_length_sequence_impedance.x

        return length * r < self.minLineResistance0hms or length * x < self.minLineReactance0hms

    def connectedToShuntCompensator(self, equipment: ConductingEquipment) -> bool:
        for connected in connected_equipment(equipment):
            if issubclass(connected.to_equip.__class__, ShuntCompensator):
                return True
        return False
