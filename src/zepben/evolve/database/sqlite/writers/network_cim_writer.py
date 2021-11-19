from dataclassy import dataclass

from zepben.evolve import CableInfo, TableCableInfo, PreparedStatement, WireInfo, TableWireInfo, AssetInfo, TableOverheadWireInfo, OverheadWireInfo, \
    PowerTransformerInfo, TablePowerTransformerInfo, TableAcDcTerminals, AcDcTerminal, BaseVoltage, TableBaseVoltages, TableConductingEquipment, \
    ConductingEquipment, TableEquipment, Equipment, Feeder, TableEquipmentUsagePoints, ConnectivityNode, TableConnectivityNodes, \
    TableConnectivityNodeContainers, ConnectivityNodeContainer, TablePowerSystemResources, PowerSystemResource, TableEquipmentContainers, EquipmentContainer, \
    TableFeeders, GeographicalRegion, TableGeographicalRegions, Site, TableSites, TableSubGeographicalRegions, SubGeographicalRegion, TableSubstations, \
    Substation, Terminal, TableTerminals, UsagePoint, TableAssetInfo
from zepben.evolve.database.sqlite.writers.base_cim_writer import BaseCIMWriter


@dataclass
class NetworkCIMWriter(BaseCIMWriter):
    # ** ** ** ** ** ** IEC61968 ASSET INFO ** ** ** ** ** ** #
    def save(self, cable_info: CableInfo) -> bool:
        table = self.database_tables.get_table(TableCableInfo)
        insert = self.database_tables.get_insert(TableCableInfo)

        return self._save_wire_info(table, insert, cable_info, "cable info")

    # todo: def save(self, short_circuit_test: ShortCircuitTest):
    # todo: def save(self, no_load_test: NoLoadTest):
    # todo: def save(self, open_circuit_test: OpenCircuitTest):
    # todo: def save(ShuntCompensatorInfo)

    def save(self, overhead_wire_info: OverheadWireInfo) -> bool:
        table = self.database_tables.get_table(TableOverheadWireInfo)
        insert = self.database_tables.get_insert(TableOverheadWireInfo)

        return self._save_wire_info(table, insert, overhead_wire_info, "overhead wire info")

    def save(self, power_transformer_info: PowerTransformerInfo) -> bool:
        table = self.database_tables.get_table(TablePowerTransformerInfo)
        insert = self.database_tables.get_insert(TablePowerTransformerInfo)

        return self._save_asset_info(table, insert, power_transformer_info, "power transformer info")

    # todo: save (self, transformer_end_info: TransformerEndInfo) when TransformerEndInfo is merged.
    # def save(self, transformer_end_info: TransformerEndInfo) -> bool:
    #     table = self.database_tables.get_table(TableTransformerEndInfo)
    #     insert = self.database_tables.get_insert(TableTransformerEndInfo)
    #
    #     insert.add_value(table.connection_kind.query_index, transformer_end_info.connection_kind.name)
    #     insert.add_value(table.emergency_s.query_index, transformer_end_info.emergency_s)
    #     insert.add_value(table.end_number.query_index, transformer_end_info.end_number)
    #     insert.add_value(table.insulation_u.query_index, transformer_end_info.insulation_u)
    #     insert.add_value(table.phase_angle_clock.query_index, transformer_end_info.phase_angle_clock)
    #     insert.add_value(table.r.query_index, transformer_end_info.r)
    #     return self._save_asset_info(table, insert, transformer_end_info, "transformer end info")

    def _save_wire_info(self, table: TableWireInfo, insert: PreparedStatement, wire_info: WireInfo, description: str) -> bool:
        insert.add_value(table.rated_current.query_index, wire_info.rated_current)
        insert.add_value(table.material.query_index, wire_info.material.name)
        return True

    def _save_asset_info(self, table: TableAssetInfo, insert: PreparedStatement, asset_info: AssetInfo, description: str) -> bool:
        return self.save_identified_object(table, insert, asset_info, description)

    # ** ** ** ** ** ** IEC61968 ASSETS ** ** ** ** ** ** #
    # TODO: Writer for IEC61968 Assets

    # ** ** ** ** ** ** IEC61968 COMMON ** ** ** ** ** ** #
    # TODO: Writer for IEC61968 COMMON

    # ** ** ** ** ** ** IEC61968 METERING ** ** ** ** ** ** #
    # TODO: Writer for IEC61968 METERING

    # ** ** ** ** ** ** IEC61968 OPERATIONS ** ** ** ** ** ** #
    # TODO: Writer for IEC61968 OPERATIONS

    # ** ** ** ** ** ** IEC61968 AUXILIARY EQUIPMENT ** ** ** #
    # TODO: Writer for IEC61968 AUXILIARY EQUIPMENT

    # ** ** ** ** ** ** IEC61968 AUXILIARY EQUIPMENT ** ** ** #
    # TODO: Writer for IEC61968 AUXILIARY EQUIPMENT

    # ** ** ** ** ** ** IEC61970 CORE ** ** ** #
    def _save_ac_dc_terminal(self, table: TableAcDcTerminals, insert: PreparedStatement,
                             ac_dc_terminal: AcDcTerminal, description: str) -> bool:
        return self.save_identified_object(table, insert, ac_dc_terminal, description)

    def save(self, base_voltage: BaseVoltage) -> bool:
        table = self.database_tables.get_table(TableBaseVoltages)
        insert = self.database_tables.get_insert(TableBaseVoltages)

        insert.add_value(table.nominal_voltage.query_index, base_voltage.nominal_voltage)

        return self.save_identified_object(table, insert, base_voltage, "base voltage")

    def _save_conducting_equipment(self, table: TableConductingEquipment, insert: PreparedStatement,
                                   conducting_equipment: ConductingEquipment, description: str) -> bool:
        insert.add_value(table.base_voltage_mrid.query_index, conducting_equipment.base_voltage.mrid)
        return self.save_equipment(table, insert, conducting_equipment, description)

    def save(self, connectivity_node: ConnectivityNode) -> bool:
        table = self.database_tables.get_table(TableConnectivityNodes)
        insert = self.database_tables.get_insert(TableConnectivityNodes)
        return self.save_identified_object(table, insert, connectivity_node, "connectivity node")

    def _save_connectivity_node_container(self,
                                          table: TableConnectivityNodeContainers,
                                          insert: PreparedStatement,
                                          connectivity_node_container: ConnectivityNodeContainer,
                                          description: str) -> bool:
        return self._save_power_system_resource(table, insert, connectivity_node_container, description)

    def save_equipment(self,
                       table: TableEquipment,
                       insert: PreparedStatement,
                       equipment: Equipment,
                       description: str) -> bool:
        insert.add_value(table.normally_in_service.query_index, equipment.normally_in_service)
        insert.add_value(table.in_service.query_index, equipment.in_service)
        status = True
        for e in equipment.containers:
            if not isinstance(e, Feeder):
                status = status and self.save_association(equipment, e)
        return status and self._save_power_system_resource(table, insert, equipment, description)

    def _save_equipment_container(self, table: TableEquipmentContainers,
                                  insert: PreparedStatement,
                                  equipment_container: EquipmentContainer,
                                  description: str) -> bool:
        return self._save_connectivity_node_container(table, insert, equipment_container, description)

    def save(self, feeder: Feeder):
        table = self.database_tables.get_table(TableFeeders)
        insert = self.database_tables.get_insert(TableFeeders)
        insert.add_value(table.normal_head_terminal_mrid.query_index, feeder.normal_head_terminal.mrid)
        insert.add_value(table.normal_energizing_substation_mrid.query_index, feeder.normal_energizing_substation.mrid)
        return self._save_equipment_container(table, insert, feeder, "feeder")

    def save(self, geographical_region: GeographicalRegion) -> bool:
        table = self.database_tables.get_table(TableGeographicalRegions)
        insert = self.database_tables.get_insert(TableGeographicalRegions)
        return self.save_identified_object(table, insert, geographical_region, "geographical region")

    def _save_power_system_resource(self,
                                    table: TablePowerSystemResources,
                                    insert: PreparedStatement,
                                    power_system_resource: PowerSystemResource,
                                    description: str) -> bool:
        insert.add_value(table.location_mrid.query_index, power_system_resource.location.mrid)
        # todo: insert.add_value(table.num_controls.query_index, power_system_resource.num_controls)
        return self.save_identified_object(table, insert, power_system_resource, description)

    def save(self, site: Site) -> bool:
        table = self.database_tables.get_table(TableSites)
        insert = self.database_tables.get_insert(TableSites)
        return self._save_equipment_container(table, insert, site, "site")

    def save(self, sub_geographical_region: SubGeographicalRegion) -> bool:
        table = self.database_tables.get_table(TableSubGeographicalRegions)
        insert = self.database_tables.get_insert(TableSubGeographicalRegions)
        insert.add_value(table.geographical_region_mrid.query_index, sub_geographical_region.geographical_region.mrid)
        return self.save_identified_object(table, insert, sub_geographical_region, "sub-geographical region")

    def save(self, substation: Substation) -> bool:
        table = self.database_tables.get_table(TableSubstations)
        insert = self.database_tables.get_insert(TableSubstations)
        insert.add_value(table.sub_geographical_region_mrid.query_index, substation.sub_geographical_region.mrid)
        return self.save_identified_object(table, insert, substation, "substation")

    def save(self, terminal: Terminal) -> bool:
        table = self.database_tables.get_table(TableTerminals)
        insert = self.database_tables.get_insert(TableTerminals)
        insert.add_value(table.connectivity_node_mrid.query_index, terminal.conducting_equipment.mrid)
        insert.add_value(table.sequence_number.query_index, terminal.sequence_number)
        insert.add_value(table.connectivity_node_mrid.query_index, terminal.connectivity_node())
        insert.add_value(table.phases.query_index, terminal.phases.name)
        return self._save_ac_dc_terminal(table, insert, terminal, "terminal")

    # todo: Other classes IEC61970 WIRES

    # ** ** ** ** ** ** ASSOCIATIONS ** ** ** ** ** **  #
    # todo: saveAssociation(assetOrganisationRole: AssetOrganisationRole, asset: Asset)
    # todo: saveAssociation(usagePoint: UsagePoint, endDevice: EndDevice)

    def save_association(self, equipment: Equipment, usage_point: UsagePoint) -> bool:
        table = self.database_tables.get_table(TableEquipmentUsagePoints)
        insert = self.database_tables.get_insert(TableEquipmentUsagePoints)
        insert.add_value(table.equipment_mrid.query_index, equipment.mrid)
        insert.add_value(table.usage_point_mrid.query_index, usage_point.mrid)
        return self.try_execute_single_update(insert,
                                              f"{equipment.mrid}-to-{usage_point.mrid}",
                                              "Equipment to UsagePoint association ")

    # todo: add other saveAssociations
