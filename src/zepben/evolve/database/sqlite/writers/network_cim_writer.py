from dataclassy import dataclass

from zepben.evolve import CableInfo, TableCableInfo, PreparedStatement, WireInfo, TableWireInfo, AssetInfo, TableOverheadWireInfo, OverheadWireInfo, \
    PowerTransformerInfo, TablePowerTransformerInfo, TableAcDcTerminals, AcDcTerminal, BaseVoltage, TableBaseVoltages, TableConductingEquipment, \
    ConductingEquipment, TableEquipment, Equipment, Feeder, TableEquipmentUsagePoints, ConnectivityNode, TableConnectivityNodes, \
    TableConnectivityNodeContainers, ConnectivityNodeContainer, TablePowerSystemResources, PowerSystemResource, TableEquipmentContainers, EquipmentContainer, \
    TableFeeders, GeographicalRegion, TableGeographicalRegions, Site, TableSites, TableSubGeographicalRegions, SubGeographicalRegion, TableSubstations, \
    Substation, Terminal, TableTerminals, TableAssetInfo, TablePowerElectronicsUnit, PowerElectronicsUnit, BatteryUnit, TableBatteryUnit, \
    PhotoVoltaicUnit, TablePhotoVoltaicUnit, PowerElectronicsWindUnit, TablePowerElectronicsWindUnit, AcLineSegment, TableAcLineSegments, TableConductors, \
    Conductor, Breaker, TableBreakers, LoadBreakSwitch, TableLoadBreakSwitches, BusbarSection, \
    TableBusbarSections, TableConnectors, Connector, Disconnector, TableDisconnectors, TableEnergyConnections, EnergyConnection, TableEnergyConsumers, \
    EnergyConsumer, EnergyConsumerPhase, TableEnergyConsumerPhases, EnergySource, TableEnergySources, TableEnergySourcePhases, EnergySourcePhase, Fuse, \
    TableFuses, Jumper, TableJumpers, Junction, TableJunctions, TableLines, Line, LinearShuntCompensator, TableLinearShuntCompensators, \
    TablePerLengthSequenceImpedances, TablePerLengthLineParameters, \
    PerLengthLineParameter, PerLengthSequenceImpedance, TableRegulatingCondEq, RegulatingCondEq, TableShuntCompensators, ShuntCompensator, \
    TableProtectedSwitches, ProtectedSwitch, TableSwitches, Switch, PowerElectronicsConnection, TablePowerElectronicsConnection, \
    PowerElectronicsConnectionPhase, TablePowerElectronicsConnectionPhases, PowerTransformer, TablePowerTransformers, PowerTransformerEnd, \
    TablePowerTransformerEnds, TableTransformerEnds, TransformerEnd, TransformerStarImpedance, TableTransformerStarImpedance, TableTapChangers, TapChanger, \
    RatioTapChanger, TableRatioTapChangers, TableCircuits, Circuit, Loop, TableLoops, LoopSubstationRelationship, UsagePoint, EndDevice, \
    TableUsagePointsEndDevices, AssetOrganisationRole, Asset, TableAssetOrganisationRolesAssets, TableEquipmentEquipmentContainers, TableCircuitsSubstations, \
    TableCircuitsTerminals, TableLoopsSubstations
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

    # ** ** ** ** ** ** IEC61970 WIRES ** ** ** ** ** ** #

    def save_power_electronics_unit(self,
                                    table: TablePowerElectronicsUnit,
                                    insert: PreparedStatement,
                                    power_electronics_unit: PowerElectronicsUnit,
                                    description: str
                                    ) -> bool:
        insert.add_value(table.power_electronics_connection_mrid.query_index,
                         power_electronics_unit.power_electronics_connection.mrid)
        insert.add_value(table.max_p.query_index, power_electronics_unit.max_p)
        insert.add_value(table.min_p.query_index, power_electronics_unit.min_p)
        return self.save_equipment(table, insert, power_electronics_unit, description)

    def save(self, battery_unit: BatteryUnit) -> bool:
        table = self.database_tables.get_table(TableBatteryUnit)
        insert = self.database_tables.get_insert(TableBatteryUnit)
        insert.add_value(table.battery_state.query_index, battery_unit.battery_state.name)
        insert.add_value(table.rated_e.query_index, battery_unit.rated_e)
        insert.add_value(table.stored_e.query_index, battery_unit.stored_e)
        return self.save_power_electronics_unit(table, insert, battery_unit, "battery unit")

    def save(self, photovoltaic_unit: PhotoVoltaicUnit) -> bool:
        table = self.database_tables.get_table(TablePhotoVoltaicUnit)
        insert = self.database_tables.get_insert(TablePhotoVoltaicUnit)
        return self.save_power_electronics_unit(table, insert, photovoltaic_unit, "photo voltaic unit")

    def save(self, power_electronics_wind_unit: PowerElectronicsWindUnit) -> bool:
        table = self.database_tables.get_table(TablePowerElectronicsWindUnit)
        insert = self.database_tables.get_insert(TablePowerElectronicsWindUnit)
        return self.save_power_electronics_unit(table, insert, power_electronics_wind_unit, "power electronics wind unit")

    def save(self, ac_line_segment: AcLineSegment) -> bool:
        table = self.database_tables.get_table(TableAcLineSegments)
        insert = self.database_tables.get_insert(TableAcLineSegments)
        insert.add_value(table.per_length_sequence_impedance_mrid.query_index,
                         ac_line_segment.per_length_sequence_impedance.mrid)
        return self._save_conductor(table, insert, ac_line_segment, "AC line segment")

    def save(self, breaker: Breaker) -> bool:
        table = self.database_tables.get_table(TableBreakers)
        insert = self.database_tables.get_insert(TableBreakers)
        return self._save_protected_switch(table, insert, breaker, "breaker")

    def save(self, loadBreakSwitch: LoadBreakSwitch) -> bool:
        table = self.database_tables.get_table(TableLoadBreakSwitches)
        insert = self.database_tables.get_insert(TableLoadBreakSwitches)
        return self._save_protected_switch(table, insert, loadBreakSwitch, "load break switch")

    def save(self, busbarSection: BusbarSection) -> bool:
        table = self.database_tables.get_table(TableBusbarSections)
        insert = self.database_tables.get_insert(TableBusbarSections)
        return self._save(table, insert, busbarSection, "busbar section")

    def _save_conductor(self, table: TableConductors,
                        insert: PreparedStatement,
                        conductor: Conductor,
                        description: str) -> bool:
        insert.add_value(table.length.query_index, conductor.length)
        insert.add_value(table.wire_info_mrid.query_index, conductor.asset_info.mrid)
        return self._save_conducting_equipment(table, insert, conductor, description)

    def _save_connector(self, table: TableConnectors,
                        insert: PreparedStatement, connector: Connector, description: str) -> bool: \
        return self._save_conducting_equipment(table, insert, connector, description)

    def save(self, disconnector: Disconnector) -> bool:
        table = self.database_tables.get_table(TableDisconnectors)
        insert = self.database_tables.get_insert(TableDisconnectors)
        return self._save_switch(table, insert, disconnector, "disconnector")

    def _save_energy_connection(self, table: TableEnergyConnections, insert: PreparedStatement,
                                energyConnection: EnergyConnection, description: str) -> bool:
        return self._save_conducting_equipment(table, insert, energyConnection, description)

    def save(self, energyConsumer: EnergyConsumer) -> bool:
        table = self.database_tables.get_table(TableEnergyConsumers)
        insert = self.database_tables.get_insert(TableEnergyConsumers)
        insert.add_value(table.customer_count.query_index, energyConsumer.customer_count)
        insert.add_value(table.grounded.query_index, energyConsumer.grounded)
        insert.add_value(table.p.query_index, energyConsumer.p)
        insert.add_value(table.q.query_index, energyConsumer.q)
        insert.add_value(table.p_fixed.query_index, energyConsumer.p_fixed)
        insert.add_value(table.q_fixed.query_index, energyConsumer.q_fixed)
        insert.add_value(table.phase_connection.query_index, energyConsumer.phase_connection.name)
        return self._save_energy_connection(table, insert, energyConsumer, "energy consumer")

    def save(self, energy_consumer_phase: EnergyConsumerPhase) -> bool:
        table = self.database_tables.get_table(TableEnergyConsumerPhases)
        insert = self.database_tables.get_insert(TableEnergyConsumerPhases)
        insert.add_value(table.energy_consumer_mrid.query_index, energy_consumer_phase.energy_consumer.mrid)
        insert.add_value(table.phase.query_index, energy_consumer_phase.phase.name)
        insert.add_value(table.p.query_index, energy_consumer_phase.p)
        insert.add_value(table.q.query_index, energy_consumer_phase.q)
        insert.add_value(table.p_fixed.query_index, energy_consumer_phase.p_fixed)
        insert.add_value(table.q_fixed.query_index, energy_consumer_phase.q_fixed)
        return self._save_power_system_resource(table, insert, energy_consumer_phase, "energy consumer phase")

    def save(self, energy_source: EnergySource) -> bool:
        table = self.database_tables.get_table(TableEnergySources)
        insert = self.database_tables.get_insert(TableEnergySources)
        insert.add_value(table.active_power.query_index, energy_source.active_power)
        insert.add_value(table.reactive_power.query_index, energy_source.reactive_power)
        insert.add_value(table.voltage_angle.query_index, energy_source.voltage_angle)
        insert.add_value(table.voltage_magnitude.query_index, energy_source.voltage_magnitude)
        insert.add_value(table.p_max.query_index, energy_source.p_max)
        insert.add_value(table.p_min.query_index, energy_source.p_min)
        insert.add_value(table.r.query_index, energy_source.r)
        insert.add_value(table.r0.query_index, energy_source.r0)
        insert.add_value(table.rn.query_index, energy_source.rn)
        insert.add_value(table.x.query_index, energy_source.x)
        insert.add_value(table.x0.query_index, energy_source.x0)
        insert.add_value(table.xn.query_index, energy_source.xn)
        return self._save_energy_connection(table, insert, energy_source, "energy source")

    def save(self, energy_source_phase: EnergySourcePhase) -> bool:
        table = self.database_tables.get_table(TableEnergySourcePhases)
        insert = self.database_tables.get_insert(TableEnergySourcePhases)
        insert.add_value(table.energy_source_mrid.query_index, energy_source_phase.energy_source.mrid)
        insert.add_value(table.phase.query_index, energy_source_phase.phase.name)
        return self._save_power_system_resource(table, insert, energy_source_phase, "energy source phase")

    def save(self, fuse: Fuse) -> bool:
        table = self.database_tables.get_table(TableFuses)
        insert = self.database_tables.get_insert(TableFuses)
        return self._save_switch(table, insert, fuse, "fuse")

    def save(self, jumper: Jumper) -> bool:
        table = self.database_tables.get_table(TableJumpers)
        insert = self.database_tables.get_insert(TableJumpers)
        return self._save_switch(table, insert, jumper, "jumper")

    def save(self, junction: Junction) -> bool:
        table = self.database_tables.get_table(TableJunctions)
        insert = self.database_tables.get_insert(TableJunctions)
        return self._save_connector(table, insert, junction, "junction")

    def _save_line(self, table: TableLines, insert: PreparedStatement, line: Line, description: str) -> bool:
        return self._save_equipment_container(table, insert, line, description)

    def save(self, linear_shunt_compensator: LinearShuntCompensator) -> bool:
        table = self.database_tables.get_table(TableLinearShuntCompensators)
        insert = self.database_tables.get_insert(TableLinearShuntCompensators)
        insert.add_value(table.b0_per_section.query_index, linear_shunt_compensator.b0_per_section)
        insert.add_value(table.b_per_section.query_index, linear_shunt_compensator.b_per_section)
        insert.add_value(table.g0_per_section.query_index, linear_shunt_compensator.g0_per_section)
        insert.add_value(table.g_per_section.query_index, linear_shunt_compensator.g_per_section)
        return self._save_shunt_compensator(table, insert, linear_shunt_compensator, "linear shunt compensator")

    # todo: Add _save_per_length_impedance with  TablePerLengthImpedances input
    # def _save_per_length_impedance(self, table: TablePerLengthImpedances,
    #                               insert: PreparedStatement,
    #                               per_length_sequence_impedance: PerLengthImpedance, description: str) -> bool:
    #    return self._save_per_length_line_parameter(table, insert, per_length_sequence_impedance, description)

    def _save_per_length_line_parameter(self, table: TablePerLengthLineParameters,
                                        insert: PreparedStatement,
                                        perLengthLineParameter: PerLengthLineParameter,
                                        description: str) -> bool:
        return self._save_identified_object(table, insert, perLengthLineParameter, description)

    def save(self, perLengthSequenceImpedance: PerLengthSequenceImpedance) -> bool:
        table = self.database_tables.get_table(TablePerLengthSequenceImpedances)
        insert = self.database_tables.get_insert(TablePerLengthSequenceImpedances)
        insert.add_value(table.r.query_index, perLengthSequenceImpedance.r)
        insert.add_value(table.x.query_index, perLengthSequenceImpedance.x)
        insert.add_value(table.r0.query_index, perLengthSequenceImpedance.r0)
        insert.add_value(table.x0.query_index, perLengthSequenceImpedance.x0)
        insert.add_value(table.bch.query_index, perLengthSequenceImpedance.bch)
        insert.add_value(table.gch.query_index, perLengthSequenceImpedance.gch)
        insert.add_value(table.b0ch.query_index, perLengthSequenceImpedance.b0ch)
        insert.add_value(table.g0ch.query_index, perLengthSequenceImpedance.g0ch)
        return self._save_per_length_impedance(table, insert, perLengthSequenceImpedance, "per length sequence impedance")

    def save(self, power_electronics_connection: PowerElectronicsConnection) -> bool:
        table = self.database_tables.get_table(TablePowerElectronicsConnection)
        insert = self.database_tables.get_insert(TablePowerElectronicsConnection)
        insert.add_value(table.max_i_fault.query_index, power_electronics_connection.max_i_fault)
        insert.add_value(table.max_q.query_index, power_electronics_connection.max_q)
        insert.add_value(table.min_q.query_index, power_electronics_connection.min_q)
        insert.add_value(table.p.query_index, power_electronics_connection.p)
        insert.add_value(table.q.query_index, power_electronics_connection.q)
        insert.add_value(table.rated_s.query_index, power_electronics_connection.rated_s)
        insert.add_value(table.rated_u.query_index, power_electronics_connection.rated_u)
        return self._save_regulating_cond_eq(table, insert, power_electronics_connection, "power electronics connection")

    def save(self, power_electronics_connection_phase: PowerElectronicsConnectionPhase) -> bool:
        table = self.database_tables.get_table(TablePowerElectronicsConnectionPhases)
        insert = self.database_tables.get_insert(TablePowerElectronicsConnectionPhases)
        insert.add_value(table.power_electronics_connection_mrid.query_index,
                         power_electronics_connection_phase.power_electronics_connection.mrid)
        insert.add_value(table.p.query_index, power_electronics_connection_phase.p)
        insert.add_value(table.phase.query_index, power_electronics_connection_phase.phase.name)
        insert.add_value(table.q.query_index, power_electronics_connection_phase.q)
        return self._save_power_system_resource(table, insert, power_electronics_connection_phase,
                                                "power electronics connection phase")

    def save(self, power_transformer: PowerTransformer) -> bool:
        table = self.database_tables.get_table(TablePowerTransformers)
        insert = self.database_tables.get_insert(TablePowerTransformers)
        insert.add_value(table.vector_group.query_index, power_transformer.vector_group.name)
        insert.add_value(table.transformer_utilisation.query_index, power_transformer.transformer_utilisation)
        insert.add_value(table.power_transformer_info_mrid.query_index, power_transformer.asset_info.mrid)
        return self._save_conducting_equipment(table, insert, power_transformer, "power transformer")

    def save(self, power_transformer_end: PowerTransformerEnd) -> bool:
        table = self.database_tables.get_table(TablePowerTransformerEnds)
        insert = self.daabase_tables.get_insert(TablePowerTransformerEnds)
        insert.add_value(table.power_transformer_mrid.query_index, power_transformer_end.power_transformer.mrid)
        insert.add_value(table.connection_kind.query_index, power_transformer_end.connection_kind.name)
        insert.add_value(table.phase_angle_clock.query_index, power_transformer_end.phase_angle_clock)
        insert.add_value(table.b.query_index, power_transformer_end.b)
        insert.add_value(table.b0.query_index, power_transformer_end.b0)
        insert.add_value(table.g.query_index, power_transformer_end.g)
        insert.add_value(table.g0.query_index, power_transformer_end.g0)
        insert.add_value(table.r.query_index, power_transformer_end.r)
        insert.add_value(table.r0.query_index, power_transformer_end.r0)
        insert.add_value(table.rated_s.query_index, power_transformer_end.rated_s)
        insert.add_value(table.rated_u.query_index, power_transformer_end.rated_u)
        insert.add_value(table.x.query_index, power_transformer_end.x)
        insert.add_value(table.x0.query_index, power_transformer_end.x0)
        return self.saveTransformerEnd(table, insert, power_transformer_end, "power transformer end")

    def _save_protected_switch(self, table: TableProtectedSwitches,
                               insert: PreparedStatement,
                               protected_switch: ProtectedSwitch,
                               description: str) -> bool:
        return self._save_switch(table, insert, protected_switch, description)

    def save(self, ratio_tap_changer: RatioTapChanger) -> bool:
        table = self.database_tables.get_table(TableRatioTapChangers)
        insert = self.database_tables.get_insert(TableRatioTapChangers)
        insert.add_value(table.transformer_end_mrid.query_index, ratio_tap_changer.transformer_end.mrid)
        insert.add_value(table.step_voltage_increment.query_index, ratio_tap_changer.step_voltage_increment)
        return self._save_tap_changer(table, insert, ratio_tap_changer, "ratio tap changer")

    def _save_regulating_cond_eq(self, table: TableRegulatingCondEq, insert: PreparedStatement,
                                 regulating_cond_eq: RegulatingCondEq, description: str) -> bool:
        insert.add_value(table.control_enabled.query_index, regulating_cond_eq.control_enabled)
        return self._save_energy_connection(table, insert, regulating_cond_eq, description)

    def _save_shunt_compensator(self, table: TableShuntCompensators, insert: PreparedStatement,
                                shuntCompensator: ShuntCompensator, description: str) -> bool:
        insert.add_value(table.grounded.query_index, shuntCompensator.grounded)
        insert.add_value(table.nom_u.query_index, shuntCompensator.nom_u)
        insert.add_value(table.phase_connection.query_index, shuntCompensator.phase_connection.name)
        insert.add_value(table.sections.query_index, shuntCompensator.sections)
        return self._save_regulating_cond_eq(table, insert, shuntCompensator, description)

    def _save_switch(self, table: TableSwitches,
                     insert: PreparedStatement, switch: Switch, description: str) -> bool:
        insert.add_value(table.normal_open.query_index, switch.is_normally_open())
        insert.add_value(table.open.query_index, switch.is_open())
        return self._save_conducting_equipment(table, insert, switch, description)

    def _save_tap_changer(self, table: TableTapChangers, insert: PreparedStatement,
                          tap_changer: TapChanger, description: str) -> bool:
        insert.add_value(table.control_enabled.query_index, tap_changer.control_enabled)
        insert.add_value(table.high_step.query_index, tap_changer.high_step)
        insert.add_value(table.low_step.query_index, tap_changer.low_step)
        insert.add_value(table.neutral_u.query_index, tap_changer.neutral_step)
        insert.add_value(table.neutral_u.query_index, tap_changer.neutral_u)
        insert.add_value(table.normal_step.query_index, tap_changer.normal_step)
        insert.add_value(table.step.query_index, tap_changer.step)
        return self._save_power_system_resource(table, insert, tap_changer, description)

    def _save_transformer_end(self,
                              table: TableTransformerEnds,
                              insert: PreparedStatement,
                              transformer_end: TransformerEnd,
                              description: str) -> bool:
        insert.add_value(table.end_number.query_index, transformer_end.end_number)
        insert.add_value(table.terminal_mrid.query_index, transformer_end.terminal.mrid)
        insert.add_value(table.base_voltage_mrid.query_index, transformer_end.base_voltage.mrid)
        insert.add_value(table.grounded.query_index, transformer_end.grounded)
        insert.add_value(table.r_ground.query_index, transformer_end.r_ground)
        insert.add_value(table.x_ground.query_index, transformer_end.x_ground)
        insert.add_value(table.star_impedance_mrid.query_index, transformer_end.star_impedance.mrid)
        return self.save_identified_object(table, insert, transformer_end, description)

    def save(self, transformer_star_impedance: TransformerStarImpedance) -> bool:
        table = self.database_tables.get_table(TableTransformerStarImpedance)
        insert = self.database_tables.get_insert(TableTransformerStarImpedance)
        insert.add_value(table.r.query_index, transformer_star_impedance.r)
        insert.add_value(table.r0.query_index, transformer_star_impedance.r0)
        insert.add_value(table.x.query_index, transformer_star_impedance.x)
        insert.add_value(table.x0.query_index, transformer_star_impedance.x0)
        insert.add_value(table.transformer_end_info_mrid.query_index, transformer_star_impedance.transformer_end_info.mrid)
        return self.save_identified_object(table, insert, transformer_star_impedance, "transformer star impedance")

    # ** ** ** ** ** ** IEC61970 InfIEC61970 ** ** ** ** ** ** #

    def save(self, circuit: Circuit) -> bool:
        table = self.database_tables.get_table(TableCircuits)
        insert = self.database_tables.get_insert(TableCircuits)
        insert.add_value(table.loop_mrid.query_index, circuit.loop.mrid)
        status = True
        for sub in circuit.end_substations:
            status = status and self._save_circuit_to_substation_association(circuit, sub)
        for t in circuit.end_terminals:
            status = status and self._save_circuit_to_terminal_association(circuit, t)
        return status and self._save_line(table, insert, circuit, "circuit")

    def save(self, loop: Loop) -> bool:
        table = self.database_tables.get_table(TableLoops)
        insert = self.database_tables.get_insert(TableLoops)
        status = True
        for sub in loop.energizing_substations:
            status = status and self._save_loop_to_substation_association(loop, sub,
                                                                          LoopSubstationRelationship.SUBSTATION_ENERGIZES_LOOP)
        for sub in loop.substations:
            status = status and self._save_loop_to_substation_association(loop, sub,
                                                                          LoopSubstationRelationship.LOOP_ENERGIZES_SUBSTATION)
        return status and self.save_identified_object(table, insert, loop, "loop")

    # todo: add  /************ IEC61970 MEAS ************/

    # todo: add /************ IEC61970 SCADA ************/

    # ** ** ** ** ** ** ASSOCIATIONS ** ** ** ** ** **  #
    def _save_asset_organisation_role_to_asset_association(self, asset_organisation_role: AssetOrganisationRole, asset: Asset) -> bool:
        table = self.database_tables.get_table(TableAssetOrganisationRolesAssets)
        insert = self.database_tables.get_insert(TableAssetOrganisationRolesAssets)
        insert.add_value(table.asset_organisation_role_mrid.query_index, asset_organisation_role.mrid)
        insert.add_value(table.asset_mrid.query_index, asset.mrid)
        return self.try_execute_single_update(insert, f"{asset_organisation_role.mrid}-to-{asset.mrid}",
                                              "asset organisation role to asset association")

    def _save_usage_point_to_end_device_association(self, usage_point: UsagePoint, end_device: EndDevice) -> bool:
        table = self.database_tables.get_table(TableUsagePointsEndDevices)
        insert = self.database_tables.get_insert(TableUsagePointsEndDevices)
        insert.add_value(table.usage_point_mrid.query_index, usage_point.mrid)
        insert.add_value(table.end_device_mrid.query_index, end_device.mrid)
        return self.try_execute_single_update(insert,
                                              f"{usage_point.mrid}-to-{end_device.mrid}",
                                              "usage point to end device association")

    def _save_equipment_to_usage_point_association(self, equipment: Equipment, usage_point: UsagePoint) -> bool:
        table = self.database_tables.get_table(TableEquipmentUsagePoints)
        insert = self.database_tables.get_insert(TableEquipmentUsagePoints)
        insert.add_value(table.equipment_mrid.query_index, equipment.mrid)
        insert.add_value(table.usage_point_mrid.query_index, usage_point.mrid)
        return self.try_execute_single_update(insert,
                                              f"{equipment.mrid}-to-{usage_point.mrid}",
                                              "Equipment to UsagePoint association ")

    def _save_equipment_to_equipment_container_association(self, equipment: Equipment, equipmentContainer: EquipmentContainer) -> bool:
        table = self.database_tables.get_table(TableEquipmentEquipmentContainers)
        insert = self.database_tables.get_insert(TableEquipmentEquipmentContainers)
        insert.add_value(table.equipment_mrid.query_index, equipment.mrid)
        insert.add_value(table.equipment_container_mrid.query_index, equipmentContainer.mrid)
        return self.try_execute_single_update(insert,
                                              f"{equipment.mrid}-to-{equipmentContainer.mrid}",
                                              "equipment to equipment container association")

    def _save_circuit_to_substation_association(self, circuit: Circuit, substation: Substation) -> bool:
        table = self.database_tables.get_table(TableCircuitsSubstations)
        insert = self.database_tables.get_insert(TableCircuitsSubstations)
        insert.add_value(table.circuit_mrid.query_index, circuit.mrid)
        insert.add_value(table.substation_mrid.query_index, substation.mrid)
        return self.try_execute_single_update(
            insert, f"{circuit.mrid}-to-{substation.mrid}",
            "circuit to substation association")

    def _save_circuit_to_terminal_association(self, circuit: Circuit, terminal: Terminal) -> bool:
        table = self.database_tables.get_table(TableCircuitsTerminals)
        insert = self.database_tables.get_insert(TableCircuitsTerminals)
        insert.add_value(table.circuit_mrid.query_index, circuit.mrid)
        insert.add_value(table.terminal_mrid.query_index, terminal.mrid)
        return self.try_execute_single_update(insert, f"{circuit.mrid}-to-{terminal.mrid}", "circuit to terminal association")

    def _save_loop_to_substation_association(self, loop: Loop, substation: Substation, relationship: LoopSubstationRelationship) -> bool:
        table = self.database_tables.get_table(TableLoopsSubstations)
        insert = self.database_tables.get_insert(TableLoopsSubstations)
        insert.add_value(table.loop_mrid.query_index, loop.mrid)
        insert.add_value(table.substation_mrid.query_index, substation.mrid)
        insert.add_value(table.relationship.query_index, relationship.name)
        return self.try_execute_single_update(insert,
                                              f"{loop.mrid}-to-{substation.mrid}",
                                              f"loop to substation association")
