#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List

from zepben.evolve import *
from zepben.evolve.model.common_two_way_connections import add_equipment_container_connection


def create_circuit(mrid: str = None, name: str = '', description: str = "", names: List[Name] = None, location: Location = None, asset_info: AssetInfo = None, 
                   equipment: List[Equipment] = None, loop: Loop = None, end_terminals: List[Terminal] = None, end_substations: List[Substation] = None
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
    c = Circuit(**locals())
    add_equipment_container_connection(c, equipment)
    if loop:
        loop.add_circuit(c)
    if end_substations:
        for es in end_substations:
            es.add_circuit(c)
    return c


def create_loop(mrid: str = None, name: str = '', description: str = "", names: List[Name] = None, circuits: List[Circuit] = None,
                substations: List[Substation] = None, energizing_substations: List[Substation] = None) -> Loop:
    """
    Loop(IdentifiedObject)
    IdentifiedObject: mrid, name, description, names
    Loop: circuits, substations, energizing_substations
    """
    loop = Loop(**locals())
    if circuits:
        for c in circuits:
            c.loop = loop
    if substations:
        for s in substations:
            s.add_loop(loop)
    if energizing_substations:
        for es in energizing_substations:
            if substations and es not in substations:
                es.add_loop(loop)
    return loop
