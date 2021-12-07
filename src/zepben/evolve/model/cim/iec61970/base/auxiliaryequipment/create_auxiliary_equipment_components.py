#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List

from zepben.evolve import *


def create_fault_indicator(mrid: str = None, name: str = '', description: str = "", names: List[Name] = None, location: Location = None,
                           asset_info: AssetInfo = None, in_service: bool = True, normally_in_service: bool = True, usage_points: List[UsagePoint] = None,
                           equipment_containers: List[EquipmentContainer] = None, operational_restrictions: List[OperationalRestriction] = None,
                           current_feeders: List[Feeder] = None, terminal: Terminal = None) -> FaultIndicator:
    """
    FaultIndicator(AuxiliaryEquipment(Equipment(PowerSystemResource(IdentifiedObject))))
    IdentifiedObject: mrid, name, description, names
    PowerSystemResource: location, asset_info
    Equipment: in_service, normally_in_service, usage_points, equipment_containers, operational_restrictions, current_feeders
    AuxiliaryEquipment: terminal
    FaultIndicator:
    """
    args = locals()
    return FaultIndicator(**args)
