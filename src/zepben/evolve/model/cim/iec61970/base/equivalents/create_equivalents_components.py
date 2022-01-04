#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List

from zepben.evolve import *
from zepben.evolve.model.common_two_way_connections import add_conducting_equipment_connection

__all__ = ["create_equivalent_branch"]


def create_equivalent_branch(mrid: str = None, name: str = '', description: str = "", names: List[Name] = None, location: Location = None,
                             asset_info: AssetInfo = None, in_service: bool = True, normally_in_service: bool = True, usage_points: List[UsagePoint] = None,
                             equipment_containers: List[EquipmentContainer] = None, operational_restrictions: List[OperationalRestriction] = None,
                             current_feeders: List[Feeder] = None, base_voltage: BaseVoltage = None, terminals: List[Terminal] = None,
                             negative_r12: float = None, negative_r21: float = None, negative_x12: float = None, negative_x21: float = None,
                             positive_r12: float = None, positive_r21: float = None, positive_x12: float = None, positive_x21: float = None,
                             r: float = None, r21: float = None, x: float = None, x21: float = None, zero_r12: float = None, zero_r21: float = None,
                             zero_x12: float = None, zero_x21: float = None) -> EquivalentBranch:
    """
    EquivalentBranch(EquivalentEquipment(ConductingEquipment(Equipment(PowerSystemResource(IdentifiedObject)))))
    IdentifiedObject: mrid, name, description, names
    PowerSystemResource: location, asset_info
    Equipment: in_service, normally_in_service, usage_points, equipment_containers, operational_restrictions, current_feeders
    ConductingEquipment: base_voltage, terminals
    EquivalentEquipment:
    EquivalentBranch: negative_r12, negative_r21, negative_x12, negative_x21, positive_r12, positive_r21, positive_x12, positive_x21, r, r21, x, x21, zero_r12,
                      zero_r21, zero_x12, zero_x21
    """
    eb = EquivalentBranch(**locals())
    add_conducting_equipment_connection(eb, usage_points, equipment_containers, operational_restrictions, current_feeders, terminals)
    return eb

