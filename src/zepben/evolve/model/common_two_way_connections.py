from typing import List, Dict

from zepben.evolve import UsagePoint, Equipment, Feeder, OperationalRestriction, EquipmentContainer, ConductingEquipment, Terminal, PowerElectronicsConnection, \
    PowerElectronicsUnit


def add_common_equipment_connections(eq: Equipment, usage_points: List[UsagePoint] = None, equipment_containers: List[EquipmentContainer] = None,
                                     operational_restrictions: List[OperationalRestriction] = None, current_feeders: List[Feeder] = None):
    if usage_points:
        for usage_point in usage_points:
            usage_point.add_equipment(eq)
    if equipment_containers:
        for ec in equipment_containers:
            ec.add_equipment(eq)
    if operational_restrictions:
        for opr in operational_restrictions:
            opr.add_equipment(eq)
    if current_feeders:
        for feeder in current_feeders:
            feeder.add_equipment(eq)


def add_conducting_equipment_connection(ce: ConductingEquipment, usage_points: List[UsagePoint] = None, equipment_containers: List[EquipmentContainer] = None,
                                        operational_restrictions: List[OperationalRestriction] = None, current_feeders: List[Feeder] = None,
                                        terminals: List[Terminal] = None):
    add_common_equipment_connections(ce, usage_points, equipment_containers, operational_restrictions, current_feeders)
    if terminals:
        for terminal in terminals:
            terminal.conducting_equipment = ce


def add_equipment_container_connection(ec, equipments: List[Equipment] = None):
    if equipments:
        for e in equipments:
            e.add_container(ec)


def add_power_electronics_connection_connection(peu: PowerElectronicsUnit, usage_points: List[UsagePoint] = None,
                                                equipment_containers: List[EquipmentContainer] = None,
                                                operational_restrictions: List[OperationalRestriction] = None, current_feeders: List[Feeder] = None,
                                                power_electronics_connection: PowerElectronicsConnection = None):
    add_common_equipment_connections(peu, usage_points, equipment_containers, operational_restrictions, current_feeders)
    if power_electronics_connection:
        power_electronics_connection.add_unit(peu)
