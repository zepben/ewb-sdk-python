#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List

from zepben.evolve import *


def create_circuit(mrid: str = None, name: str = '', description: str = "", names: List[Name] = None, location: Location = None, asset_info: AssetInfo = None, 
                   equipment: Dict[str, Equipment] = None, loop: Loop = None, end_terminals: List[Terminal] = None, end_substations: List[Substation] = None
                   ) -> Circuit:
    """
    Circuit(Line(EquipmentContainer(ConnectivityNodeContainer(PowerSystemResource(IdentifiedObject)))))
    IdentifiedObject: mrid, name, description, names
    PowerSystemResource: location, asset_info
    ConnectivityNodeContainer:
    EquipmentContainer: equipment
    Line:
    Circuit: loop, end_terminals, end_substations
    """
    args = locals()
    return Circuit(**args)


def create_loop(mrid: str = None, name: str = '', description: str = "", names: List[Name] = None, circuits: List[Circuit] = None,
                substations: List[Substation] = None, energizing_substations: List[Substation] = None) -> Loop:
    """
    Loop(IdentifiedObject)
    IdentifiedObject: mrid, name, description, names
    Loop: circuits, substations, energizing_substations
    """
    args = locals()
    return Loop(**args)
