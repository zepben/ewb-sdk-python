#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from _weakref import ReferenceType
from typing import List

from zepben.evolve import *


def create_base_voltage(mrid: str = None, name: str = '', description: str = "", names: List[Name] = None, nominal_voltage: int = 0) -> BaseVoltage:
    """
    BaseVoltage(IdentifiedObject)
    IdentifiedObject: mrid, name, description, names
    BaseVoltage: nominal_voltage
    """
    args = locals()
    return BaseVoltage(**args)


def create_connectivity_node(mrid: str = None, name: str = '', description: str = "", names: List[Name] = None, terminals: List[Terminal] = None
                             ) -> ConnectivityNode:
    """
    ConnectivityNode(IdentifiedObject)
    IdentifiedObject: mrid, name, description, names
    ConnectivityNode: terminals
    """
    args = locals()
    return ConnectivityNode(**args)


def create_feeder(mrid: str = None, name: str = '', description: str = "", names: List[Name] = None, location: Location = None,
                  asset_info: AssetInfo = None, equipment: Dict[str, Equipment] = None, normal_head_terminal: Terminal = None,
                  normal_energizing_substation: Substation = None, current_equipment: Dict[str, Equipment] = None) -> Feeder:
    """
    Feeder(EquipmentContainer(ConnectivityNodeContainer(PowerSystemResource(IdentifiedObject))))
    IdentifiedObject: mrid, name, description, names
    PowerSystemResource: location, asset_info
    ConnectivityNodeContainer:
    EquipmentContainer: equipment
    Feeder: normal_head_terminal, normal_energizing_substation, current_equipment
    """
    args = locals()
    return Feeder(**args)


def create_geographical_region(mrid: str = None, name: str = '', description: str = "", names: List[Name] = None,
                               sub_geographical_regions: List[SubGeographicalRegion] = None) -> GeographicalRegion:
    """
    GeographicalRegion(IdentifiedObject)
    IdentifiedObject: mrid, name, description, names
    GeographicalRegion: sub_geographical_regions
    """
    args = locals()
    return GeographicalRegion(**args)


def create_name(name: str, type: NameType, identified_object: IdentifiedObject = None) -> Name:
    """
    Name()
    Name: name, type, identified_object
    """
    args = locals()
    # noinspection PyArgumentList
    return Name(**args)


def create_name_type(name: str, description: str = "", names_index: Dict[str, Name] = None, names_multi_index: Dict[str, List[Name]] = None) -> NameType:
    """
    NameType()
    NameType: name, description, names_index, names_multi_index
    """
    args = locals()
    # noinspection PyArgumentList
    return NameType(**args)


def create_site(mrid: str = None, name: str = '', description: str = "", names: List[Name] = None, location: Location = None,
                asset_info: AssetInfo = None, equipment: Dict[str, Equipment] = None) -> Site:
    """
    Site(EquipmentContainer(ConnectivityNodeContainer(PowerSystemResource(IdentifiedObject))))
    IdentifiedObject: mrid, name, description, names
    PowerSystemResource: location, asset_info
    ConnectivityNodeContainer:
    EquipmentContainer: equipment
    Site:
    """
    args = locals()
    return Site(**args)


def create_sub_geographical_region(mrid: str = None, name: str = '', description: str = "", names: List[Name] = None,
                                   geographical_region: GeographicalRegion = None, substations: List[Substation] = None) -> SubGeographicalRegion:
    """
    SubGeographicalRegion(IdentifiedObject)
    IdentifiedObject: mrid, name, description, names
    SubGeographicalRegion: geographical_region, substations
    """
    args = locals()
    return SubGeographicalRegion(**args)


def create_substation(mrid: str = None, name: str = '', description: str = "", names: List[Name] = None, location: Location = None,
                      asset_info: AssetInfo = None, equipment: Dict[str, Equipment] = None, sub_geographical_region: SubGeographicalRegion = None,
                      normal_energized_feeders: List[Feeder] = None, loops: List[Loop] = None, energized_loops: List[Loop] = None,
                      circuits: List[Circuit] = None) -> Substation:
    """
    Substation(EquipmentContainer(ConnectivityNodeContainer(PowerSystemResource(IdentifiedObject))))
    IdentifiedObject: mrid, name, description, names
    PowerSystemResource: location, asset_info
    ConnectivityNodeContainer:
    EquipmentContainer: equipment
    Substation: sub_geographical_region, normal_energized_feeders, loops, energized_loops, circuits
    """
    args = locals()
    return Substation(**args)


def create_terminal(mrid: str = None, name: str = '', description: str = "", names: List[Name] = None, conducting_equipment: ConductingEquipment = None,
                    phases: PhaseCode = PhaseCode.ABC, sequence_number: int = 0, traced_phases: TracedPhases = TracedPhases(), cn: ReferenceType = None
                    ) -> Terminal:
    """
    Terminal(AcDcTerminal(IdentifiedObject))
    IdentifiedObject: mrid, name, description, names
    AcDcTerminal:
    Terminal: conducting_equipment, phases, sequence_number, traced_phases, cn
    """
    args = locals()
    return Terminal(**args)
