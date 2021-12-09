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
    return BaseVoltage(**locals())


def create_connectivity_node(mrid: str = None, name: str = '', description: str = "", names: List[Name] = None, terminals: List[Terminal] = None
                             ) -> ConnectivityNode:
    """
    ConnectivityNode(IdentifiedObject)
    IdentifiedObject: mrid, name, description, names
    ConnectivityNode: terminals
    """
    return ConnectivityNode(**locals())


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
    return Feeder(**locals())


def create_geographical_region(mrid: str = None, name: str = '', description: str = "", names: List[Name] = None,
                               sub_geographical_regions: List[SubGeographicalRegion] = None) -> GeographicalRegion:
    """
    GeographicalRegion(IdentifiedObject)
    IdentifiedObject: mrid, name, description, names
    GeographicalRegion: sub_geographical_regions
    """
    return GeographicalRegion(**locals())


def create_name(name: str, type: NameType, identified_object: IdentifiedObject = None) -> Name:
    """
    Name()
    Name: name, type, identified_object
    """
    # noinspection PyArgumentList
    return Name(**locals())


def create_name_type(name: str, description: str = "", _names_index: Dict[str, Name] = dict(), _names_multi_index: Dict[str, List[Name]] = dict()) -> NameType:
    """
    NameType()
    NameType: name, description, _names_index, _names_multi_index
    """
    # noinspection PyArgumentList
    return NameType(**locals())


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
    return Site(**locals())


def create_sub_geographical_region(mrid: str = None, name: str = '', description: str = "", names: List[Name] = None,
                                   geographical_region: GeographicalRegion = None, substations: List[Substation] = None) -> SubGeographicalRegion:
    """
    SubGeographicalRegion(IdentifiedObject)
    IdentifiedObject: mrid, name, description, names
    SubGeographicalRegion: geographical_region, substations
    """
    return SubGeographicalRegion(**locals())


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
    return Substation(**locals())


def create_terminal(mrid: str = None, name: str = '', description: str = "", names: List[Name] = None, conducting_equipment: ConductingEquipment = None,
                    phases: PhaseCode = PhaseCode.ABC, sequence_number: int = 0, normal_feeder_direction: FeederDirection = FeederDirection.NONE,
                    current_feeder_direction: FeederDirection = FeederDirection.NONE, traced_phases: TracedPhases = TracedPhases(), cn: ReferenceType = None,
                    connectivity_node: ConnectivityNode = None) -> Terminal:
    """
    Terminal(AcDcTerminal(IdentifiedObject))
    IdentifiedObject: mrid, name, description, names
    AcDcTerminal:
    Terminal: conducting_equipment, phases, sequence_number, traced_phases, cn, connectivity_node
    """
    return Terminal(**locals())
