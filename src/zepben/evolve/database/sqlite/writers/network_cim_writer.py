#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve import CableInfo, TableCableInfo, PreparedStatement, WireInfo, TableWireInfo, AssetInfo, TableOverheadWireInfo, OverheadWireInfo, \
    PowerTransformerInfo, TablePowerTransformerInfo, TableAcDcTerminals, AcDcTerminal, BaseVoltage, TableBaseVoltages, TableConductingEquipment, \
    ConductingEquipment, TableEquipment, Equipment, Feeder, TableEquipmentUsagePoints, ConnectivityNode, TableConnectivityNodes, \
    TableConnectivityNodeContainers, ConnectivityNodeContainer, TablePowerSystemResources, PowerSystemResource, TableEquipmentContainers, EquipmentContainer, \
    TableFeeders, GeographicalRegion, TableGeographicalRegions, Site, TableSites, TableSubGeographicalRegions, SubGeographicalRegion, TableSubstations, \
    Substation, Terminal, TableTerminals, TableAssets, TableAssetInfo, TableAssetContainers, TablePowerElectronicsUnit, PowerElectronicsUnit, BatteryUnit, \
    TableBatteryUnit, PhotoVoltaicUnit, TablePhotoVoltaicUnit, PowerElectronicsWindUnit, TablePowerElectronicsWindUnit, AcLineSegment, TableAcLineSegments, \
    TableConductors, Conductor, Breaker, TableBreakers, LoadBreakSwitch, TableLoadBreakSwitches, BusbarSection, \
    TableBusbarSections, TableConnectors, Connector, Disconnector, TableDisconnectors, TableEnergyConnections, EnergyConnection, TableEnergyConsumers, \
    EnergyConsumer, EnergyConsumerPhase, TableEnergyConsumerPhases, EnergySource, TableEnergySources, TableEnergySourcePhases, EnergySourcePhase, Fuse, \
    TableFuses, Jumper, TableJumpers, Junction, TableJunctions, TableLines, Line, LinearShuntCompensator, TableLinearShuntCompensators, \
    TablePerLengthSequenceImpedances, TablePerLengthLineParameters, TableCircuitsSubstations, \
    PerLengthLineParameter, PerLengthSequenceImpedance, TableRegulatingCondEq, RegulatingCondEq, TableShuntCompensators, ShuntCompensator, \
    TableProtectedSwitches, ProtectedSwitch, TableSwitches, Switch, PowerElectronicsConnection, TablePowerElectronicsConnection, \
    PowerElectronicsConnectionPhase, TablePowerElectronicsConnectionPhases, PowerTransformer, TablePowerTransformers, PowerTransformerEnd, \
    TablePowerTransformerEnds, TableTransformerEnds, TransformerEnd, TransformerStarImpedance, TableTransformerStarImpedance, TableTapChangers, TapChanger, \
    RatioTapChanger, TableRatioTapChangers, TableCircuits, Circuit, Loop, TableLoops, LoopSubstationRelationship, UsagePoint, EndDevice, \
    TableUsagePointsEndDevices, AssetOrganisationRole, Asset, AssetContainer, TableAssetOrganisationRolesAssets, TableEquipmentEquipmentContainers, \
    TableCircuitsTerminals, TableLoopsSubstations, TransformerEndInfo, TableTransformerEndInfo, TransformerTankInfo, TableTransformerTankInfo, NoLoadTest, \
    TableNoLoadTests, TableTransformerTest, TransformerTest, ShortCircuitTest, TableShortCircuitTests, OpenCircuitTest, TableOpenCircuitTests, \
    PerLengthImpedance, TablePerLengthImpedances, TableAssetOrganisationRoles, AssetOwner, TableAssetOwners, TableStructures, Structure, Pole, TablePoles, \
    Streetlight, TableStreetlights, Location, TableLocations, TableLocationStreetAddressField, StreetAddress, TableLocationStreetAddresses, PositionPoint, \
    TablePositionPoints, TableStreetAddresses, TableTownDetails, TownDetail, StreetDetail, TableEndDevices, Meter, TableMeters, TableUsagePoints, \
    OperationalRestriction, TableOperationalRestrictions, TableFaultIndicators, TableAuxiliaryEquipment, AuxiliaryEquipment, FaultIndicator, \
    TableMeasurements, Measurement, Analog, TableAnalogs, Accumulator, TableAccumulators, Discrete, TableDiscretes, Control, TableControls, TableIoPoints, \
    IoPoint, TableRemotePoints, RemotePoint, RemoteControl, TableRemoteControls, RemoteSource, TableRemoteSources, ShuntCompensatorInfo, \
    CurrentTransformer, TableSensors, Sensor, TableCurrentTransformers, PotentialTransformer, TablePotentialTransformers, CurrentTransformerInfo, \
    TableCurrentTransformerInfo, PotentialTransformerInfo, TablePotentialTransformerInfo, TableShuntCompensatorInfo, EquivalentBranch, EquivalentEquipment, \
    Recloser, TableReclosers, TableEquipmentOperationalRestrictions, TableLvFeeders, LvFeeder, TableSwitchInfo, SwitchInfo, TableRelayInfo, \
    RelayInfo, CurrentRelay, TableProtectionRelayFunctions, TableCurrentRelays, TableProtectionRelayFunctionsProtectedSwitches, \
    TableRecloseDelays, EvChargingUnit, TableEvChargingUnits, TableRegulatingControls, RegulatingControl, TapChangerControl, TableTapChangerControls, \
    TablePowerTransformerEndRatings, TableGrounds, TableGroundDisconnectors, SeriesCompensator, TableSeriesCompensators, \
    ProtectionRelayFunction, RelaySetting, TableProtectionRelayFunctionThresholds, TableProtectionRelayFunctionTimeLimits, TableVoltageRelays, \
    TableDistanceRelays, TableProtectionRelaySchemes, TableProtectionRelaySystems, TableProtectionRelayFunctionsSensors, \
    TableProtectionRelaySchemesProtectionRelayFunctions, DistanceRelay, ProtectionRelayScheme, ProtectionRelaySystem, VoltageRelay, Ground, GroundDisconnector

from zepben.evolve.database.sqlite.tables.iec61970.base.equivalent_tables import TableEquivalentBranches, TableEquivalentEquipment
from zepben.evolve.database.sqlite.writers.base_cim_writer import BaseCIMWriter

__all__ = ["NetworkCIMWriter"]


class NetworkCIMWriter(BaseCIMWriter):

    # ************ IEC61968 ASSET INFO ************

    def save_cable_info(self, cable_info: CableInfo) -> bool:
        table = self.database_tables.get_table(TableCableInfo)
        insert = self.database_tables.get_insert(TableCableInfo)

        return self._save_wire_info(table, insert, cable_info, "cable info")

    def save_no_load_test(self, no_load_test: NoLoadTest) -> bool:
        table = self.database_tables.get_table(TableNoLoadTests)
        insert = self.database_tables.get_insert(TableNoLoadTests)

        insert.add_value(table.energised_end_voltage.query_index, no_load_test.energised_end_voltage)
        insert.add_value(table.exciting_current.query_index, no_load_test.exciting_current)
        insert.add_value(table.exciting_current_zero.query_index, no_load_test.exciting_current_zero)
        insert.add_value(table.loss.query_index, no_load_test.loss)
        insert.add_value(table.loss_zero.query_index, no_load_test.loss_zero)

        return self._save_transformer_test(table, insert, no_load_test, "no load test")

    def _save_transformer_test(self, table: TableTransformerTest, insert: PreparedStatement, transformer_test: TransformerTest, description: str) -> bool:
        insert.add_value(table.base_power.query_index, transformer_test.base_power)
        insert.add_value(table.temperature.query_index, transformer_test.temperature)

        return self._save_identified_object(table, insert, transformer_test, description)

    def save_short_circuit_test(self, short_circuit_test: ShortCircuitTest) -> bool:
        table = self.database_tables.get_table(TableShortCircuitTests)
        insert = self.database_tables.get_insert(TableShortCircuitTests)

        insert.add_value(table.current.query_index, short_circuit_test.current)
        insert.add_value(table.energised_end_step.query_index, short_circuit_test.energised_end_step)
        insert.add_value(table.grounded_end_step.query_index, short_circuit_test.grounded_end_step)
        insert.add_value(table.leakage_impedance.query_index, short_circuit_test.leakage_impedance)
        insert.add_value(table.leakage_impedance_zero.query_index, short_circuit_test.leakage_impedance_zero)
        insert.add_value(table.loss.query_index, short_circuit_test.loss)
        insert.add_value(table.loss_zero.query_index, short_circuit_test.loss_zero)
        insert.add_value(table.power.query_index, short_circuit_test.power)
        insert.add_value(table.voltage.query_index, short_circuit_test.voltage)
        insert.add_value(table.voltage_ohmic_part.query_index, short_circuit_test.voltage_ohmic_part)

        return self._save_transformer_test(table, insert, short_circuit_test, "short circuit test")

    def save_shunt_compensator_info(self, shunt_compensator_info: ShuntCompensatorInfo) -> bool:
        table = self.database_tables.get_table(TableShuntCompensatorInfo)
        insert = self.database_tables.get_insert(TableShuntCompensatorInfo)

        insert.add_value(table.max_power_loss.query_index, shunt_compensator_info.max_power_loss)
        insert.add_value(table.rated_current.query_index, shunt_compensator_info.rated_current)
        insert.add_value(table.rated_reactive_power.query_index, shunt_compensator_info.rated_reactive_power)
        insert.add_value(table.rated_voltage.query_index, shunt_compensator_info.rated_voltage)

        return self._save_asset_info(table, insert, shunt_compensator_info, "shunt compensator info")

    def save_switch_info(self, switch_info: SwitchInfo) -> bool:
        table = self.database_tables.get_table(TableSwitchInfo)
        insert = self.database_tables.get_insert(TableSwitchInfo)

        insert.add_value(table.rated_interrupting_time.query_index, switch_info.rated_interrupting_time)

        return self._save_asset_info(table, insert, switch_info, "switch info")

    def save_open_circuit_test(self, open_circuit_test: OpenCircuitTest) -> bool:
        table = self.database_tables.get_table(TableOpenCircuitTests)
        insert = self.database_tables.get_insert(TableOpenCircuitTests)

        insert.add_value(table.energised_end_step.query_index, open_circuit_test.energised_end_step)
        insert.add_value(table.energised_end_voltage.query_index, open_circuit_test.energised_end_voltage)
        insert.add_value(table.open_end_step.query_index, open_circuit_test.open_end_step)
        insert.add_value(table.open_end_voltage.query_index, open_circuit_test.open_end_voltage)
        insert.add_value(table.phase_shift.query_index, open_circuit_test.phase_shift)

        return self._save_transformer_test(table, insert, open_circuit_test, "open circuit test")

    def save_overhead_wire_info(self, overhead_wire_info: OverheadWireInfo) -> bool:
        table = self.database_tables.get_table(TableOverheadWireInfo)
        insert = self.database_tables.get_insert(TableOverheadWireInfo)

        return self._save_wire_info(table, insert, overhead_wire_info, "overhead wire info")

    def save_power_transformer_info(self, power_transformer_info: PowerTransformerInfo) -> bool:
        table = self.database_tables.get_table(TablePowerTransformerInfo)
        insert = self.database_tables.get_insert(TablePowerTransformerInfo)

        return self._save_asset_info(table, insert, power_transformer_info, "power transformer info")

    def save_transformer_end_info(self, transformer_end_info: TransformerEndInfo) -> bool:
        table = self.database_tables.get_table(TableTransformerEndInfo)
        insert = self.database_tables.get_insert(TableTransformerEndInfo)

        insert.add_value(table.connection_kind.query_index, transformer_end_info.connection_kind.short_name)
        insert.add_value(table.emergency_s.query_index, transformer_end_info.emergency_s)
        insert.add_value(table.end_number.query_index, transformer_end_info.end_number)
        insert.add_value(table.insulation_u.query_index, transformer_end_info.insulation_u)
        insert.add_value(table.phase_angle_clock.query_index, transformer_end_info.phase_angle_clock)
        insert.add_value(table.r.query_index, transformer_end_info.r)
        insert.add_value(table.rated_s.query_index, transformer_end_info.rated_s)
        insert.add_value(table.rated_u.query_index, transformer_end_info.rated_u)
        insert.add_value(table.short_term_s.query_index, transformer_end_info.short_term_s)
        insert.add_value(table.transformer_tank_info_mrid.query_index, self._mrid_or_none(transformer_end_info.transformer_tank_info))
        insert.add_value(table.energised_end_no_load_tests.query_index, self._mrid_or_none(transformer_end_info.energised_end_no_load_tests))
        insert.add_value(table.energised_end_short_circuit_tests.query_index, self._mrid_or_none(transformer_end_info.energised_end_short_circuit_tests))
        insert.add_value(table.grounded_end_short_circuit_tests.query_index, self._mrid_or_none(transformer_end_info.grounded_end_short_circuit_tests))
        insert.add_value(table.open_end_open_circuit_tests.query_index, self._mrid_or_none(transformer_end_info.open_end_open_circuit_tests))
        insert.add_value(table.energised_end_open_circuit_tests.query_index, self._mrid_or_none(transformer_end_info.energised_end_open_circuit_tests))

        return self._save_asset_info(table, insert, transformer_end_info, "transformer end info")

    def save_transformer_tank_info(self, transformer_tank_info: TransformerTankInfo) -> bool:
        table = self.database_tables.get_table(TableTransformerTankInfo)
        insert = self.database_tables.get_insert(TableTransformerTankInfo)

        insert.add_value(table.power_transformer_info_mrid.query_index, self._mrid_or_none(transformer_tank_info.power_transformer_info))

        return self._save_asset_info(table, insert, transformer_tank_info, "transformer tank info")

    def _save_wire_info(self, table: TableWireInfo, insert: PreparedStatement, wire_info: WireInfo, description: str) -> bool:
        insert.add_value(table.rated_current.query_index, wire_info.rated_current)
        insert.add_value(table.material.query_index, wire_info.material.name)

        return self._save_asset_info(table, insert, wire_info, description)

    def _save_asset_info(self, table: TableAssetInfo, insert: PreparedStatement, asset_info: AssetInfo, description: str) -> bool:
        return self._save_identified_object(table, insert, asset_info, description)

    # ************ IEC61968 ASSETS ************

    def _save_asset(self, table: TableAssets, insert: PreparedStatement, asset: Asset, description: str) -> bool:
        status = True
        insert.add_value(table.location_mrid.query_index, self._mrid_or_none(asset.location))
        for e in asset.organisation_roles:
            status = status and self._save_asset_organisation_role_to_asset_association(e, asset)

        return status and self._save_identified_object(table, insert, asset, description)

    def _save_asset_container(self, table: TableAssetContainers, insert: PreparedStatement, asset_container: AssetContainer, description: str) -> bool:
        return self._save_asset(table, insert, asset_container, description)

    def _save_asset_organisation_role(self,
                                      table: TableAssetOrganisationRoles,
                                      insert: PreparedStatement,
                                      asset_organisation_role: AssetOrganisationRole,
                                      description: str
                                      ) -> bool:
        return self._save_organisation_role(table, insert, asset_organisation_role, description)

    def save_asset_owner(self, asset_owner: AssetOwner) -> bool:
        table = self.database_tables.get_table(TableAssetOwners)
        insert = self.database_tables.get_insert(TableAssetOwners)

        return self._save_asset_organisation_role(table, insert, asset_owner, "asset owner")

    def _save_structure(self, table: TableStructures, insert: PreparedStatement, structure: Structure, description: str) -> bool:
        return self._save_asset_container(table, insert, structure, description)

    def save_pole(self, pole: Pole) -> bool:
        table = self.database_tables.get_table(TablePoles)
        insert = self.database_tables.get_insert(TablePoles)

        insert.add_value(table.classification.query_index, pole.classification)

        return self._save_structure(table, insert, pole, "pole")

    def save_streetlight(self, streetlight: Streetlight) -> bool:
        table = self.database_tables.get_table(TableStreetlights)
        insert = self.database_tables.get_insert(TableStreetlights)

        insert.add_value(table.pole_mrid.query_index, self._mrid_or_none(streetlight.pole))
        insert.add_value(table.light_rating.query_index, streetlight.light_rating)
        insert.add_value(table.lamp_kind.query_index, streetlight.lamp_kind.name)

        return self._save_asset(table, insert, streetlight, "streetlight")

    # ************ IEC61968 COMMON ************

    @staticmethod
    def insert_street_detail(table: TableStreetAddresses, insert: PreparedStatement, street_detail: StreetDetail):
        insert.add_value(table.building_name.query_index, street_detail.building_name if street_detail else None)
        insert.add_value(table.floor_identification.query_index, street_detail.floor_identification if street_detail else None)
        insert.add_value(table.street_name.query_index, street_detail.name if street_detail else None)
        insert.add_value(table.number.query_index, street_detail.number if street_detail else None)
        insert.add_value(table.suite_number.query_index, street_detail.suite_number if street_detail else None)
        insert.add_value(table.type.query_index, street_detail.type if street_detail else None)
        insert.add_value(table.display_address.query_index, street_detail.display_address if street_detail else None)

    @staticmethod
    def insert_town_detail(table: TableTownDetails, insert: PreparedStatement, town_detail: TownDetail):
        insert.add_value(table.town_name.query_index, town_detail.name if town_detail else None)
        insert.add_value(table.state_or_province.query_index, town_detail.state_or_province if town_detail else None)

    def save_location(self, location: Location) -> bool:
        table = self.database_tables.get_table(TableLocations)
        insert = self.database_tables.get_insert(TableLocations)

        status = self.save_location_street_address(location, TableLocationStreetAddressField.mainAddress, location.main_address, "location main address")
        for sequence_number, point in enumerate(location.points):
            status = status and self.save_position_point(location, sequence_number, point)

        return status and self._save_identified_object(table, insert, location, "location")

    def save_location_street_address(self, location: Location, field: TableLocationStreetAddressField, street_address: StreetAddress, description: str) -> bool:
        if street_address is None:
            return True

        table = self.database_tables.get_table(TableLocationStreetAddresses)
        insert = self.database_tables.get_insert(TableLocationStreetAddresses)

        insert.add_value(table.location_mrid.query_index, location.mrid)
        insert.add_value(table.address_field.query_index, field.name)

        return self._save_street_address(table, insert, street_address, "{}-{}".format(location.mrid, field), description)

    def save_position_point(self, location: Location, sequence_number: int, position_point: PositionPoint) -> bool:
        table = self.database_tables.get_table(TablePositionPoints)
        insert = self.database_tables.get_insert(TablePositionPoints)

        insert.add_value(table.location_mrid.query_index, location.mrid)
        insert.add_value(table.sequence_number.query_index, sequence_number)
        insert.add_value(table.x_position.query_index, position_point.x_position)
        insert.add_value(table.y_position.query_index, position_point.y_position)

        return self._try_execute_single_update(insert, "{}-point{}".format(location.mrid, sequence_number), "position point")

    def _save_street_address(self, table: TableStreetAddresses, insert: PreparedStatement, street_address: StreetAddress, street_id: str,
                             description: str) -> bool:
        insert.add_value(table.postal_code.query_index, street_address.postal_code)
        insert.add_value(table.po_box.query_index, street_address.po_box)

        self.insert_street_detail(table, insert, street_address.street_detail)
        self.insert_town_detail(table, insert, street_address.town_detail)

        return self._try_execute_single_update(insert, street_id, description)

    # ************ IEC61968 infIEC61968 InfAssetInfo ************

    def save_relay_info(self, relay_info: RelayInfo) -> bool:
        table = self.database_tables.get_table(TableRelayInfo)
        insert = self.database_tables.get_insert(TableRelayInfo)

        delay_table = self.database_tables.get_table(TableRecloseDelays)
        if relay_info.reclose_delays:
            for idx, delay in enumerate(relay_info.reclose_delays):
                delay_insert = self.database_tables.get_insert(TableRecloseDelays)
                delay_insert.add_value(delay_table.relay_info_mrid.query_index, relay_info.mrid)
                delay_insert.add_value(delay_table.sequence_number.query_index, idx)
                delay_insert.add_value(delay_table.reclose_delay.query_index, delay)
                self._try_execute_single_update(delay_insert, f"{relay_info.mrid}-rd-{idx}", "reclose delay")

        insert.add_value(table.curve_setting.query_index, relay_info.curve_setting)
        insert.add_value(table.reclose_fast.query_index, relay_info.reclose_fast)

        return self._save_asset_info(table, insert, relay_info, "relay info")

    # ************ IEC61968 infIEC61968 InfAssetInfo ************

    def save_current_transformer_info(self, current_transformer_info: CurrentTransformerInfo):
        table = self.database_tables.get_table(TableCurrentTransformerInfo)
        insert = self.database_tables.get_insert(TableCurrentTransformerInfo)

        insert.add_value(table.accuracy_class.query_index, current_transformer_info.accuracy_class)
        insert.add_value(table.accuracy_limit.query_index, current_transformer_info.accuracy_limit)
        insert.add_value(table.core_count.query_index, current_transformer_info.core_count)
        insert.add_value(table.ct_class.query_index, current_transformer_info.ct_class)
        insert.add_value(table.knee_point_voltage.query_index, current_transformer_info.knee_point_voltage)
        insert.add_ratio(table.max_ratio_numerator.query_index, table.max_ratio_denominator.query_index, current_transformer_info.max_ratio)
        insert.add_ratio(table.nominal_ratio_numerator.query_index, table.nominal_ratio_denominator.query_index, current_transformer_info.nominal_ratio)
        insert.add_value(table.primary_ratio.query_index, current_transformer_info.primary_ratio)
        insert.add_value(table.rated_current.query_index, current_transformer_info.rated_current)
        insert.add_value(table.secondary_fls_rating.query_index, current_transformer_info.secondary_fls_rating)
        insert.add_value(table.secondary_ratio.query_index, current_transformer_info.secondary_ratio)
        insert.add_value(table.usage.query_index, current_transformer_info.usage)

        return self._save_asset_info(table, insert, current_transformer_info, "current transformer info")

    def save_potential_transformer_info(self, potential_transformer_info: PotentialTransformerInfo):
        table = self.database_tables.get_table(TablePotentialTransformerInfo)
        insert = self.database_tables.get_insert(TablePotentialTransformerInfo)

        insert.add_value(table.accuracy_class.query_index, potential_transformer_info.accuracy_class)
        insert.add_ratio(table.nominal_ratio_numerator.query_index, table.nominal_ratio_denominator.query_index, potential_transformer_info.nominal_ratio)
        insert.add_value(table.primary_ratio.query_index, potential_transformer_info.primary_ratio)
        insert.add_value(table.pt_class.query_index, potential_transformer_info.pt_class)
        insert.add_value(table.rated_voltage.query_index, potential_transformer_info.rated_voltage)
        insert.add_value(table.secondary_ratio.query_index, potential_transformer_info.secondary_ratio)

        return self._save_asset_info(table, insert, potential_transformer_info, "potential transformer info")

    # ************ IEC61968 METERING ************

    def _save_end_device(self, table: TableEndDevices, insert: PreparedStatement, end_device: EndDevice, description: str) -> bool:
        insert.add_value(table.customer_mrid.query_index, end_device.customer_mrid)
        insert.add_value(table.service_location_mrid.query_index, self._mrid_or_none(end_device.service_location))

        status = True
        for e in end_device.usage_points:
            status = status and self._save_usage_point_to_end_device_association(e, end_device)

        return status and self._save_asset_container(table, insert, end_device, description)

    def save_meter(self, meter: Meter) -> bool:
        table = self.database_tables.get_table(TableMeters)
        insert = self.database_tables.get_insert(TableMeters)

        return self._save_end_device(table, insert, meter, "meter")

    def save_usage_point(self, usage_point: UsagePoint) -> bool:
        table = self.database_tables.get_table(TableUsagePoints)
        insert = self.database_tables.get_insert(TableUsagePoints)

        insert.add_value(table.location_mrid.query_index, self._mrid_or_none(usage_point.usage_point_location))
        insert.add_value(table.is_virtual.query_index, int(usage_point.is_virtual))
        insert.add_value(table.connection_category.query_index, usage_point.connection_category)
        insert.add_value(table.rated_power.query_index, usage_point.rated_power)
        insert.add_value(table.approved_inverter_capacity.query_index, usage_point.approved_inverter_capacity)

        status = True
        for e in usage_point.equipment:
            status = status and self._save_equipment_to_usage_point_association(e, usage_point)

        return status and self._save_identified_object(table, insert, usage_point, "usage point")

    # ************ IEC61968 OPERATIONS ************

    def save_operational_restriction(self, operational_restriction: OperationalRestriction) -> bool:
        table = self.database_tables.get_table(TableOperationalRestrictions)
        insert = self.database_tables.get_insert(TableOperationalRestrictions)

        status = True
        for e in operational_restriction.equipment:
            status = status and self._save_equipment_to_operational_restriction_association(e, operational_restriction)

        return status and self._save_document(table, insert, operational_restriction, "operational restriction")

    # ************ IEC61970 AUXILIARY EQUIPMENT ************

    def save_auxiliary_equipment(self, table: TableAuxiliaryEquipment, insert: PreparedStatement, auxiliary_equipment: AuxiliaryEquipment,
                                 description: str) -> bool:
        insert.add_value(table.terminal_mrid.query_index, self._mrid_or_none(auxiliary_equipment.terminal))

        return self._save_equipment(table, insert, auxiliary_equipment, description)

    def save_current_transformer(self, current_transformer: CurrentTransformer) -> bool:
        table = self.database_tables.get_table(TableCurrentTransformers)
        insert = self.database_tables.get_insert(TableCurrentTransformers)

        insert.add_value(table.current_transformer_info_mrid.query_index, self._mrid_or_none(current_transformer.current_transformer_info))
        insert.add_value(table.core_burden.query_index, current_transformer.core_burden)

        return self.save_sensor(table, insert, current_transformer, "current transformer")

    def save_fault_indicator(self, fault_indicator: FaultIndicator) -> bool:
        table = self.database_tables.get_table(TableFaultIndicators)
        insert = self.database_tables.get_insert(TableFaultIndicators)

        return self.save_auxiliary_equipment(table, insert, fault_indicator, "fault indicator")

    def save_potential_transformer(self, potential_transformer: PotentialTransformer) -> bool:
        table = self.database_tables.get_table(TablePotentialTransformers)
        insert = self.database_tables.get_insert(TablePotentialTransformers)

        insert.add_value(table.potential_transformer_info_mrid.query_index, self._mrid_or_none(potential_transformer.potential_transformer_info))
        insert.add_value(table.type.query_index, potential_transformer.type.short_name)

        return self.save_sensor(table, insert, potential_transformer, "potential transformer")

    def save_sensor(self, table: TableSensors, insert: PreparedStatement, sensor: Sensor, description: str) -> bool:
        return self.save_auxiliary_equipment(table, insert, sensor, description)

    # ************ IEC6190 BASE CORE ************

    def _save_ac_dc_terminal(self, table: TableAcDcTerminals, insert: PreparedStatement,
                             ac_dc_terminal: AcDcTerminal, description: str) -> bool:
        return self._save_identified_object(table, insert, ac_dc_terminal, description)

    def save_base_voltage(self, base_voltage: BaseVoltage) -> bool:
        table = self.database_tables.get_table(TableBaseVoltages)
        insert = self.database_tables.get_insert(TableBaseVoltages)

        insert.add_value(table.nominal_voltage.query_index, base_voltage.nominal_voltage)

        return self._save_identified_object(table, insert, base_voltage, "base voltage")

    def _save_conducting_equipment(self, table: TableConductingEquipment, insert: PreparedStatement, conducting_equipment: ConductingEquipment,
                                   description: str) -> bool:
        insert.add_value(table.base_voltage_mrid.query_index, self._mrid_or_none(conducting_equipment.base_voltage))

        return self._save_equipment(table, insert, conducting_equipment, description)

    def save_connectivity_node(self, connectivity_node: ConnectivityNode) -> bool:
        table = self.database_tables.get_table(TableConnectivityNodes)
        insert = self.database_tables.get_insert(TableConnectivityNodes)

        return self._save_identified_object(table, insert, connectivity_node, "connectivity node")

    def _save_connectivity_node_container(self, table: TableConnectivityNodeContainers, insert: PreparedStatement,
                                          connectivity_node_container: ConnectivityNodeContainer, description: str) -> bool:
        return self._save_power_system_resource(table, insert, connectivity_node_container, description)

    def _save_equipment(self, table: TableEquipment, insert: PreparedStatement, equipment: Equipment, description: str) -> bool:
        insert.add_value(table.normally_in_service.query_index, int(equipment.normally_in_service))
        insert.add_value(table.in_service.query_index, int(equipment.in_service))
        insert.add_value(table.commissioned_date.query_index, f"{equipment.commissioned_date.isoformat()}Z" if equipment.commissioned_date else None)
        status = True
        for e in equipment.containers:
            if not isinstance(e, Feeder):
                status = status and self._save_equipment_to_equipment_container_association(equipment, e)

        return status and self._save_power_system_resource(table, insert, equipment, description)

    def _save_equipment_container(self, table: TableEquipmentContainers,
                                  insert: PreparedStatement,
                                  equipment_container: EquipmentContainer,
                                  description: str) -> bool:
        return self._save_connectivity_node_container(table, insert, equipment_container, description)

    def save_feeder(self, feeder: Feeder):
        table = self.database_tables.get_table(TableFeeders)
        insert = self.database_tables.get_insert(TableFeeders)

        insert.add_value(table.normal_head_terminal_mrid.query_index, self._mrid_or_none(feeder.normal_head_terminal))
        insert.add_value(table.normal_energizing_substation_mrid.query_index, self._mrid_or_none(feeder.normal_energizing_substation))

        return self._save_equipment_container(table, insert, feeder, "feeder")

    def save_geographical_region(self, geographical_region: GeographicalRegion) -> bool:
        table = self.database_tables.get_table(TableGeographicalRegions)
        insert = self.database_tables.get_insert(TableGeographicalRegions)

        return self._save_identified_object(table, insert, geographical_region, "geographical region")

    def _save_power_system_resource(self,
                                    table: TablePowerSystemResources,
                                    insert: PreparedStatement,
                                    power_system_resource: PowerSystemResource,
                                    description: str) -> bool:
        insert.add_value(table.location_mrid.query_index, self._mrid_or_none(power_system_resource.location))
        insert.add_value(table.num_controls.query_index, 0)  # Currently unused

        return self._save_identified_object(table, insert, power_system_resource, description)

    def save_site(self, site: Site) -> bool:
        table = self.database_tables.get_table(TableSites)
        insert = self.database_tables.get_insert(TableSites)

        return self._save_equipment_container(table, insert, site, "site")

    def save_sub_geographical_region(self, sub_geographical_region: SubGeographicalRegion) -> bool:
        table = self.database_tables.get_table(TableSubGeographicalRegions)
        insert = self.database_tables.get_insert(TableSubGeographicalRegions)

        insert.add_value(table.geographical_region_mrid.query_index, self._mrid_or_none(sub_geographical_region.geographical_region))

        return self._save_identified_object(table, insert, sub_geographical_region, "sub-geographical region")

    def save_substation(self, substation: Substation) -> bool:
        table = self.database_tables.get_table(TableSubstations)
        insert = self.database_tables.get_insert(TableSubstations)

        insert.add_value(table.sub_geographical_region_mrid.query_index, self._mrid_or_none(substation.sub_geographical_region))

        return self._save_equipment_container(table, insert, substation, "substation")

    def save_terminal(self, terminal: Terminal) -> bool:
        table = self.database_tables.get_table(TableTerminals)
        insert = self.database_tables.get_insert(TableTerminals)

        insert.add_value(table.conducting_equipment_mrid.query_index, self._mrid_or_none(terminal.conducting_equipment))
        insert.add_value(table.sequence_number.query_index, terminal.sequence_number)
        insert.add_value(table.connectivity_node_mrid.query_index, self._mrid_or_none(terminal.connectivity_node))
        insert.add_value(table.phases.query_index, terminal.phases.short_name)

        return self._save_ac_dc_terminal(table, insert, terminal, "terminal")

    # ************ IEC61970 BASE EQUIVALENTS ************

    def save_equivalent_branch(self, equivalent_branch: EquivalentBranch) -> bool:
        table = self.database_tables.get_table(TableEquivalentBranches)
        insert = self.database_tables.get_insert(TableEquivalentBranches)

        insert.add_value(table.negative_r12.query_index, equivalent_branch.negative_r12)
        insert.add_value(table.negative_r21.query_index, equivalent_branch.negative_r21)
        insert.add_value(table.negative_x12.query_index, equivalent_branch.negative_x12)
        insert.add_value(table.negative_x21.query_index, equivalent_branch.negative_x21)
        insert.add_value(table.positive_r12.query_index, equivalent_branch.positive_r12)
        insert.add_value(table.positive_r21.query_index, equivalent_branch.positive_r21)
        insert.add_value(table.positive_x12.query_index, equivalent_branch.positive_x12)
        insert.add_value(table.positive_x21.query_index, equivalent_branch.positive_x21)
        insert.add_value(table.r.query_index, equivalent_branch.r)
        insert.add_value(table.r21.query_index, equivalent_branch.r21)
        insert.add_value(table.x.query_index, equivalent_branch.x)
        insert.add_value(table.x21.query_index, equivalent_branch.x21)
        insert.add_value(table.zero_r12.query_index, equivalent_branch.zero_r12)
        insert.add_value(table.zero_r21.query_index, equivalent_branch.zero_r21)
        insert.add_value(table.zero_x12.query_index, equivalent_branch.zero_x12)
        insert.add_value(table.zero_x21.query_index, equivalent_branch.zero_x21)

        return self._save_equivalent_equipment(table, insert, equivalent_branch, "equivalent branch")

    def _save_equivalent_equipment(self, table: TableEquivalentEquipment, insert: PreparedStatement, equivalent_equipment: EquivalentEquipment,
                                   description: str) -> bool:
        return self._save_conducting_equipment(table, insert, equivalent_equipment, description)

    # ************ IEC61970 Base Protection ************

    def save_current_relay(self, current_relay: CurrentRelay) -> bool:
        table = self.database_tables.get_table(TableCurrentRelays)
        insert = self.database_tables.get_insert(TableCurrentRelays)

        insert.add_value(table.current_limit_1.query_index, current_relay.current_limit_1)
        insert.add_value(table.inverse_time_flag.query_index, current_relay.inverse_time_flag)
        insert.add_value(table.time_delay_1.query_index, current_relay.time_delay_1)

        return self._save_protection_relay_function(table, insert, current_relay, "current relay")

    def save_distance_relay(self, distance_relay: DistanceRelay) -> bool:
        table = self.database_tables.get_table(TableDistanceRelays)
        insert = self.database_tables.get_insert(TableDistanceRelays)

        insert.add_value(table.backward_blind.query_index, distance_relay.backward_blind)
        insert.add_value(table.backward_reach.query_index, distance_relay.backward_reach)
        insert.add_value(table.backward_reactance.query_index, distance_relay.backward_reactance)
        insert.add_value(table.forward_blind.query_index, distance_relay.forward_blind)
        insert.add_value(table.forward_reach.query_index, distance_relay.forward_reach)
        insert.add_value(table.forward_reactance.query_index, distance_relay.forward_reactance)
        insert.add_value(table.operation_phase_angle1.query_index, distance_relay.operation_phase_angle1)
        insert.add_value(table.operation_phase_angle2.query_index, distance_relay.operation_phase_angle2)
        insert.add_value(table.operation_phase_angle3.query_index, distance_relay.operation_phase_angle3)

        return self._save_protection_relay_function(table, insert, distance_relay, "distance relay")

    def _save_protection_relay_function(self, table: TableProtectionRelayFunctions, insert: PreparedStatement,
                                        protection_relay_function: ProtectionRelayFunction,
                                        description: str) -> bool:
        insert.add_value(table.model.query_index, protection_relay_function.model)
        insert.add_value(table.reclosing.query_index, protection_relay_function.reclosing)
        insert.add_value(table.relay_delay_time.query_index, protection_relay_function.relay_delay_time)
        insert.add_value(table.protection_kind.query_index, protection_relay_function.protection_kind.short_name)
        insert.add_value(table.directable.query_index, protection_relay_function.directable)
        insert.add_value(table.power_direction.query_index, protection_relay_function.power_direction.short_name)
        insert.add_value(table.relay_info_mrid.query_index, self._mrid_or_none(protection_relay_function.asset_info))

        status = True
        for protected_switch in protection_relay_function.protected_switches:
            status = status and self._save_protection_relay_function_protected_switch(protection_relay_function, protected_switch)
        for sensor in protection_relay_function.sensors:
            status = status and self._save_protection_relay_function_sensor(protection_relay_function, sensor)
        for sequence_number, threshold in enumerate(protection_relay_function.thresholds):
            status = status and self.save_protection_relay_threshold(protection_relay_function, sequence_number, threshold)
        for sequence_number, time_limit in enumerate(protection_relay_function.time_limits):
            status = status and self.save_protection_relay_time_limit(protection_relay_function, sequence_number, time_limit)

        return status and self._save_power_system_resource(table, insert, protection_relay_function, description)

    def save_protection_relay_threshold(self, protection_relay_function: ProtectionRelayFunction, sequence_number: int, threshold: RelaySetting) -> bool:
        table = self.database_tables.get_table(TableProtectionRelayFunctionThresholds)
        insert = self.database_tables.get_insert(TableProtectionRelayFunctionThresholds)

        insert.add_value(table.protection_relay_function_mrid.query_index, protection_relay_function.mrid)
        insert.add_value(table.sequence_number.query_index, sequence_number)
        insert.add_value(table.unit_symbol.query_index, threshold.unit_symbol.short_name)
        insert.add_value(table.value.query_index, threshold.value)
        insert.add_value(table.name_.query_index, threshold.name)

        return self._try_execute_single_update(insert, f"{protection_relay_function.mrid}-threshold{sequence_number}", "protection relay function threshold")

    def save_protection_relay_time_limit(self, protection_relay_function: ProtectionRelayFunction, sequence_number: int, time_limit: float) -> bool:
        table = self.database_tables.get_table(TableProtectionRelayFunctionTimeLimits)
        insert = self.database_tables.get_insert(TableProtectionRelayFunctionTimeLimits)

        insert.add_value(table.protection_relay_function_mrid.query_index, protection_relay_function.mrid)
        insert.add_value(table.sequence_number.query_index, sequence_number)
        insert.add_value(table.time_limit.query_index, time_limit)

        return self._try_execute_single_update(insert, f"{protection_relay_function.mrid}-time_limit{sequence_number}", "protection relay function time limit")

    def save_protection_relay_scheme(self, protection_relay_scheme: ProtectionRelayScheme) -> bool:
        table = self.database_tables.get_table(TableProtectionRelaySchemes)
        insert = self.database_tables.get_insert(TableProtectionRelaySchemes)

        insert.add_value(table.system_mrid.query_index, self._mrid_or_none(protection_relay_scheme.system))

        status = True
        for function in protection_relay_scheme.functions:
            status = status and self._save_protection_relay_scheme_protection_relay_function(protection_relay_scheme, function)
        return status and self._save_identified_object(table, insert, protection_relay_scheme,  "protection relay scheme")

    def save_protection_relay_system(self, protection_relay_system: ProtectionRelaySystem) -> bool:
        table = self.database_tables.get_table(TableProtectionRelaySystems)
        insert = self.database_tables.get_insert(TableProtectionRelaySystems)

        insert.add_value(table.protection_kind.query_index, protection_relay_system.protection_kind.short_name)

        return self._save_equipment(table, insert, protection_relay_system, "protection relay system")

    def save_voltage_relay(self, voltage_relay: VoltageRelay) -> bool:
        table = self.database_tables.get_table(TableVoltageRelays)
        insert = self.database_tables.get_insert(TableVoltageRelays)

        return self._save_protection_relay_function(table, insert, voltage_relay, "voltage relay")

    # ************ IEC61970 BASE WIRES ************

    def _save_power_electronics_unit(self, table: TablePowerElectronicsUnit, insert: PreparedStatement, power_electronics_unit: PowerElectronicsUnit,
                                     description: str) -> bool:
        insert.add_value(table.power_electronics_connection_mrid.query_index, self._mrid_or_none(power_electronics_unit.power_electronics_connection))
        insert.add_value(table.max_p.query_index, power_electronics_unit.max_p)
        insert.add_value(table.min_p.query_index, power_electronics_unit.min_p)

        return self._save_equipment(table, insert, power_electronics_unit, description)

    def save_battery_unit(self, battery_unit: BatteryUnit) -> bool:
        table = self.database_tables.get_table(TableBatteryUnit)
        insert = self.database_tables.get_insert(TableBatteryUnit)

        insert.add_value(table.battery_state.query_index, battery_unit.battery_state.short_name)
        insert.add_value(table.rated_e.query_index, battery_unit.rated_e)
        insert.add_value(table.stored_e.query_index, battery_unit.stored_e)

        return self._save_power_electronics_unit(table, insert, battery_unit, "battery unit")

    def save_photovoltaic_unit(self, photovoltaic_unit: PhotoVoltaicUnit) -> bool:
        table = self.database_tables.get_table(TablePhotoVoltaicUnit)
        insert = self.database_tables.get_insert(TablePhotoVoltaicUnit)

        return self._save_power_electronics_unit(table, insert, photovoltaic_unit, "photo voltaic unit")

    def save_power_electronics_wind_unit(self, power_electronics_wind_unit: PowerElectronicsWindUnit) -> bool:
        table = self.database_tables.get_table(TablePowerElectronicsWindUnit)
        insert = self.database_tables.get_insert(TablePowerElectronicsWindUnit)

        return self._save_power_electronics_unit(table, insert, power_electronics_wind_unit, "power electronics wind unit")

    def save_ac_line_segment(self, ac_line_segment: AcLineSegment) -> bool:
        table = self.database_tables.get_table(TableAcLineSegments)
        insert = self.database_tables.get_insert(TableAcLineSegments)

        insert.add_value(table.per_length_sequence_impedance_mrid.query_index, self._mrid_or_none(ac_line_segment.per_length_sequence_impedance))

        return self._save_conductor(table, insert, ac_line_segment, "AC line segment")

    def save_breaker(self, breaker: Breaker) -> bool:
        table = self.database_tables.get_table(TableBreakers)
        insert = self.database_tables.get_insert(TableBreakers)

        insert.add_value(table.in_transit_time.query_index, breaker.in_transit_time)

        return self._save_protected_switch(table, insert, breaker, "breaker")

    def save_load_break_switch(self, load_break_switch: LoadBreakSwitch) -> bool:
        table = self.database_tables.get_table(TableLoadBreakSwitches)
        insert = self.database_tables.get_insert(TableLoadBreakSwitches)

        return self._save_protected_switch(table, insert, load_break_switch, "load break switch")

    def save_bus_bar_section(self, bus_bar_section: BusbarSection) -> bool:
        table = self.database_tables.get_table(TableBusbarSections)
        insert = self.database_tables.get_insert(TableBusbarSections)

        return self._save_connector(table, insert, bus_bar_section, "busbar section")

    def _save_conductor(self, table: TableConductors,
                        insert: PreparedStatement,
                        conductor: Conductor,
                        description: str) -> bool:
        insert.add_value(table.length.query_index, conductor.length)
        insert.add_value(table.wire_info_mrid.query_index, self._mrid_or_none(conductor.wire_info))

        return self._save_conducting_equipment(table, insert, conductor, description)

    def _save_connector(self, table: TableConnectors,
                        insert: PreparedStatement, connector: Connector, description: str) -> bool: \
        return self._save_conducting_equipment(table, insert, connector, description)

    def save_disconnector(self, disconnector: Disconnector) -> bool:
        table = self.database_tables.get_table(TableDisconnectors)
        insert = self.database_tables.get_insert(TableDisconnectors)

        return self._save_switch(table, insert, disconnector, "disconnector")

    def _save_energy_connection(self, table: TableEnergyConnections, insert: PreparedStatement, energy_connection: EnergyConnection, description: str) -> bool:
        return self._save_conducting_equipment(table, insert, energy_connection, description)

    def save_energy_consumer(self, energy_consumer: EnergyConsumer) -> bool:
        table = self.database_tables.get_table(TableEnergyConsumers)
        insert = self.database_tables.get_insert(TableEnergyConsumers)

        insert.add_value(table.customer_count.query_index, energy_consumer.customer_count)
        insert.add_value(table.grounded.query_index, energy_consumer.grounded)
        insert.add_value(table.p.query_index, energy_consumer.p)
        insert.add_value(table.q.query_index, energy_consumer.q)
        insert.add_value(table.p_fixed.query_index, energy_consumer.p_fixed)
        insert.add_value(table.q_fixed.query_index, energy_consumer.q_fixed)
        insert.add_value(table.phase_connection.query_index, energy_consumer.phase_connection.short_name)

        return self._save_energy_connection(table, insert, energy_consumer, "energy consumer")

    def save_energy_consumer_phase(self, energy_consumer_phase: EnergyConsumerPhase) -> bool:
        table = self.database_tables.get_table(TableEnergyConsumerPhases)
        insert = self.database_tables.get_insert(TableEnergyConsumerPhases)

        insert.add_value(table.energy_consumer_mrid.query_index, self._mrid_or_none(energy_consumer_phase.energy_consumer))
        insert.add_value(table.phase.query_index, energy_consumer_phase.phase.short_name)
        insert.add_value(table.p.query_index, energy_consumer_phase.p)
        insert.add_value(table.q.query_index, energy_consumer_phase.q)
        insert.add_value(table.p_fixed.query_index, energy_consumer_phase.p_fixed)
        insert.add_value(table.q_fixed.query_index, energy_consumer_phase.q_fixed)

        return self._save_power_system_resource(table, insert, energy_consumer_phase, "energy consumer phase")

    def save_energy_source(self, energy_source: EnergySource) -> bool:
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
        insert.add_value(table.is_external_grid.query_index, energy_source.is_external_grid)
        insert.add_value(table.r_min.query_index, energy_source.r_min)
        insert.add_value(table.rn_min.query_index, energy_source.rn_min)
        insert.add_value(table.r0_min.query_index, energy_source.r0_min)
        insert.add_value(table.x_min.query_index, energy_source.x_min)
        insert.add_value(table.xn_min.query_index, energy_source.xn_min)
        insert.add_value(table.x0_min.query_index, energy_source.x0_min)
        insert.add_value(table.r_max.query_index, energy_source.r_max)
        insert.add_value(table.rn_max.query_index, energy_source.rn_max)
        insert.add_value(table.r0_max.query_index, energy_source.r0_max)
        insert.add_value(table.x_max.query_index, energy_source.x_max)
        insert.add_value(table.xn_max.query_index, energy_source.xn_max)
        insert.add_value(table.x0_max.query_index, energy_source.x0_max)

        return self._save_energy_connection(table, insert, energy_source, "energy source")

    def save_energy_source_phase(self, energy_source_phase: EnergySourcePhase) -> bool:
        table = self.database_tables.get_table(TableEnergySourcePhases)
        insert = self.database_tables.get_insert(TableEnergySourcePhases)

        insert.add_value(table.energy_source_mrid.query_index, self._mrid_or_none(energy_source_phase.energy_source))
        insert.add_value(table.phase.query_index, energy_source_phase.phase.short_name)

        return self._save_power_system_resource(table, insert, energy_source_phase, "energy source phase")

    def save_fuse(self, fuse: Fuse) -> bool:
        table = self.database_tables.get_table(TableFuses)
        insert = self.database_tables.get_insert(TableFuses)

        insert.add_value(table.function_mrid.query_index, self._mrid_or_none(fuse.function))

        return self._save_switch(table, insert, fuse, "fuse")

    def save_ground(self, ground: Ground) -> bool:
        table = self.database_tables.get_table(TableGrounds)
        insert = self.database_tables.get_insert(TableGrounds)

        return self._save_conducting_equipment(table, insert, ground, "ground")

    def save_ground_disconnector(self, ground_disconnector: GroundDisconnector) -> bool:
        table = self.database_tables.get_table(TableGroundDisconnectors)
        insert = self.database_tables.get_insert(TableGroundDisconnectors)

        return self._save_switch(table, insert, ground_disconnector, "ground disconnector")

    def save_jumper(self, jumper: Jumper) -> bool:
        table = self.database_tables.get_table(TableJumpers)
        insert = self.database_tables.get_insert(TableJumpers)

        return self._save_switch(table, insert, jumper, "jumper")

    def save_junction(self, junction: Junction) -> bool:
        table = self.database_tables.get_table(TableJunctions)
        insert = self.database_tables.get_insert(TableJunctions)

        return self._save_connector(table, insert, junction, "junction")

    def _save_line(self, table: TableLines, insert: PreparedStatement, line: Line, description: str) -> bool:
        return self._save_equipment_container(table, insert, line, description)

    def save_linear_shunt_compensator(self, linear_shunt_compensator: LinearShuntCompensator) -> bool:
        table = self.database_tables.get_table(TableLinearShuntCompensators)
        insert = self.database_tables.get_insert(TableLinearShuntCompensators)

        insert.add_value(table.b0_per_section.query_index, linear_shunt_compensator.b0_per_section)
        insert.add_value(table.b_per_section.query_index, linear_shunt_compensator.b_per_section)
        insert.add_value(table.g0_per_section.query_index, linear_shunt_compensator.g0_per_section)
        insert.add_value(table.g_per_section.query_index, linear_shunt_compensator.g_per_section)

        return self._save_shunt_compensator(table, insert, linear_shunt_compensator, "linear shunt compensator")

    def _save_per_length_impedance(self, table: TablePerLengthImpedances,
                                   insert: PreparedStatement,
                                   per_length_sequence_impedance: PerLengthImpedance, description: str) -> bool:
        return self._save_per_length_line_parameter(table, insert, per_length_sequence_impedance, description)

    def _save_per_length_line_parameter(self, table: TablePerLengthLineParameters,
                                        insert: PreparedStatement,
                                        per_length_line_parameter: PerLengthLineParameter,
                                        description: str) -> bool:
        return self._save_identified_object(table, insert, per_length_line_parameter, description)

    def save_per_length_sequence_impedance(self, per_length_sequence_impedance: PerLengthSequenceImpedance) -> bool:
        table = self.database_tables.get_table(TablePerLengthSequenceImpedances)
        insert = self.database_tables.get_insert(TablePerLengthSequenceImpedances)

        insert.add_value(table.r.query_index, per_length_sequence_impedance.r)
        insert.add_value(table.x.query_index, per_length_sequence_impedance.x)
        insert.add_value(table.r0.query_index, per_length_sequence_impedance.r0)
        insert.add_value(table.x0.query_index, per_length_sequence_impedance.x0)
        insert.add_value(table.bch.query_index, per_length_sequence_impedance.bch)
        insert.add_value(table.gch.query_index, per_length_sequence_impedance.gch)
        insert.add_value(table.b0ch.query_index, per_length_sequence_impedance.b0ch)
        insert.add_value(table.g0ch.query_index, per_length_sequence_impedance.g0ch)

        return self._save_per_length_impedance(table, insert, per_length_sequence_impedance, "per length sequence impedance")

    def save_power_electronics_connection(self, power_electronics_connection: PowerElectronicsConnection) -> bool:
        table = self.database_tables.get_table(TablePowerElectronicsConnection)
        insert = self.database_tables.get_insert(TablePowerElectronicsConnection)

        insert.add_value(table.max_i_fault.query_index, power_electronics_connection.max_i_fault)
        insert.add_value(table.max_q.query_index, power_electronics_connection.max_q)
        insert.add_value(table.min_q.query_index, power_electronics_connection.min_q)
        insert.add_value(table.p.query_index, power_electronics_connection.p)
        insert.add_value(table.q.query_index, power_electronics_connection.q)
        insert.add_value(table.rated_s.query_index, power_electronics_connection.rated_s)
        insert.add_value(table.rated_u.query_index, power_electronics_connection.rated_u)
        insert.add_value(table.inverter_standard.query_index, power_electronics_connection.inverter_standard)
        insert.add_value(table.sustain_op_overvolt_limit.query_index, power_electronics_connection.sustain_op_overvolt_limit)
        insert.add_value(table.stop_at_over_freq.query_index, power_electronics_connection.stop_at_over_freq)
        insert.add_value(table.stop_at_under_freq.query_index, power_electronics_connection.stop_at_under_freq)
        insert.add_value(table.inv_volt_watt_resp_mode.query_index, power_electronics_connection.inv_volt_watt_resp_mode)
        insert.add_value(table.inv_watt_resp_v1.query_index, power_electronics_connection.inv_watt_resp_v1)
        insert.add_value(table.inv_watt_resp_v2.query_index, power_electronics_connection.inv_watt_resp_v2)
        insert.add_value(table.inv_watt_resp_v3.query_index, power_electronics_connection.inv_watt_resp_v3)
        insert.add_value(table.inv_watt_resp_v4.query_index, power_electronics_connection.inv_watt_resp_v4)
        insert.add_value(table.inv_watt_resp_p_at_v1.query_index, power_electronics_connection.inv_watt_resp_p_at_v1)
        insert.add_value(table.inv_watt_resp_p_at_v2.query_index, power_electronics_connection.inv_watt_resp_p_at_v2)
        insert.add_value(table.inv_watt_resp_p_at_v3.query_index, power_electronics_connection.inv_watt_resp_p_at_v3)
        insert.add_value(table.inv_watt_resp_p_at_v4.query_index, power_electronics_connection.inv_watt_resp_p_at_v4)
        insert.add_value(table.inv_volt_var_resp_mode.query_index, power_electronics_connection.inv_volt_var_resp_mode)
        insert.add_value(table.inv_var_resp_v1.query_index, power_electronics_connection.inv_var_resp_v1)
        insert.add_value(table.inv_var_resp_v2.query_index, power_electronics_connection.inv_var_resp_v2)
        insert.add_value(table.inv_var_resp_v3.query_index, power_electronics_connection.inv_var_resp_v3)
        insert.add_value(table.inv_var_resp_v4.query_index, power_electronics_connection.inv_var_resp_v4)
        insert.add_value(table.inv_var_resp_q_at_v1.query_index, power_electronics_connection.inv_var_resp_q_at_v1)
        insert.add_value(table.inv_var_resp_q_at_v2.query_index, power_electronics_connection.inv_var_resp_q_at_v2)
        insert.add_value(table.inv_var_resp_q_at_v3.query_index, power_electronics_connection.inv_var_resp_q_at_v3)
        insert.add_value(table.inv_var_resp_q_at_v4.query_index, power_electronics_connection.inv_var_resp_q_at_v4)
        insert.add_value(table.inv_reactive_power_mode.query_index, power_electronics_connection.inv_reactive_power_mode)
        insert.add_value(table.inv_fix_reactive_power.query_index, power_electronics_connection.inv_fix_reactive_power)

        return self._save_regulating_cond_eq(table, insert, power_electronics_connection, "power electronics connection")

    def save_power_electronics_connection_phase(self, power_electronics_connection_phase: PowerElectronicsConnectionPhase) -> bool:
        table = self.database_tables.get_table(TablePowerElectronicsConnectionPhases)
        insert = self.database_tables.get_insert(TablePowerElectronicsConnectionPhases)

        insert.add_value(table.power_electronics_connection_mrid.query_index,
                         self._mrid_or_none(power_electronics_connection_phase.power_electronics_connection))
        insert.add_value(table.p.query_index, power_electronics_connection_phase.p)
        insert.add_value(table.phase.query_index, power_electronics_connection_phase.phase.short_name)
        insert.add_value(table.q.query_index, power_electronics_connection_phase.q)

        return self._save_power_system_resource(table, insert, power_electronics_connection_phase,
                                                "power electronics connection phase")

    def save_power_transformer(self, power_transformer: PowerTransformer) -> bool:
        table = self.database_tables.get_table(TablePowerTransformers)
        insert = self.database_tables.get_insert(TablePowerTransformers)

        insert.add_value(table.vector_group.query_index, power_transformer.vector_group.short_name)
        insert.add_value(table.transformer_utilisation.query_index, power_transformer.transformer_utilisation)
        insert.add_value(table.construction_kind.query_index, power_transformer.construction_kind.short_name)
        insert.add_value(table.function.query_index, power_transformer.function.short_name)
        insert.add_value(table.power_transformer_info_mrid.query_index, self._mrid_or_none(power_transformer.power_transformer_info))

        return self._save_conducting_equipment(table, insert, power_transformer, "power transformer")

    def save_power_transformer_end(self, power_transformer_end: PowerTransformerEnd) -> bool:
        table = self.database_tables.get_table(TablePowerTransformerEnds)
        insert = self.database_tables.get_insert(TablePowerTransformerEnds)

        insert.add_value(table.power_transformer_mrid.query_index, self._mrid_or_none(power_transformer_end.power_transformer))
        insert.add_value(table.connection_kind.query_index, power_transformer_end.connection_kind.short_name)
        insert.add_value(table.phase_angle_clock.query_index, power_transformer_end.phase_angle_clock)
        insert.add_value(table.b.query_index, power_transformer_end.b)
        insert.add_value(table.b0.query_index, power_transformer_end.b0)
        insert.add_value(table.g.query_index, power_transformer_end.g)
        insert.add_value(table.g0.query_index, power_transformer_end.g0)
        insert.add_value(table.r.query_index, power_transformer_end.r)
        insert.add_value(table.r0.query_index, power_transformer_end.r0)
        insert.add_value(table.rated_u.query_index, power_transformer_end.rated_u)
        insert.add_value(table.x.query_index, power_transformer_end.x)
        insert.add_value(table.x0.query_index, power_transformer_end.x0)

        ratings_table = self.database_tables.get_table(TablePowerTransformerEndRatings)
        ratings_insert = self.database_tables.get_insert(TablePowerTransformerEndRatings)
        for it in power_transformer_end.s_ratings:
            ratings_insert.add_value(ratings_table.power_transformer_end_mrid.query_index, power_transformer_end.mrid)
            ratings_insert.add_value(ratings_table.cooling_type.query_index, it.cooling_type.short_name)
            ratings_insert.add_value(ratings_table.rated_s.query_index, it.rated_s)
            self._try_execute_single_update(ratings_insert, f"{power_transformer_end.mrid}-{it.cooling_type.short_name}-{it.rated_s}", "transformer end ratedS")

        return self._save_transformer_end(table, insert, power_transformer_end, "power transformer end")

    def _save_protected_switch(self, table: TableProtectedSwitches, insert: PreparedStatement, protected_switch: ProtectedSwitch, description: str) -> bool:
        insert.add_value(table.breaking_capacity.query_index, protected_switch.breaking_capacity)

        return self._save_switch(table, insert, protected_switch, description)

    def save_ratio_tap_changer(self, ratio_tap_changer: RatioTapChanger) -> bool:
        table = self.database_tables.get_table(TableRatioTapChangers)
        insert = self.database_tables.get_insert(TableRatioTapChangers)

        insert.add_value(table.transformer_end_mrid.query_index, self._mrid_or_none(ratio_tap_changer.transformer_end))
        insert.add_value(table.step_voltage_increment.query_index, ratio_tap_changer.step_voltage_increment)

        return self._save_tap_changer(table, insert, ratio_tap_changer, "ratio tap changer")

    def save_recloser(self, recloser: Recloser) -> bool:
        table = self.database_tables.get_table(TableReclosers)
        insert = self.database_tables.get_insert(TableReclosers)

        return self._save_protected_switch(table, insert, recloser, "recloser")

    def _save_regulating_cond_eq(self, table: TableRegulatingCondEq, insert: PreparedStatement, regulating_cond_eq: RegulatingCondEq, description: str) -> bool:
        insert.add_value(table.control_enabled.query_index, regulating_cond_eq.control_enabled)
        insert.add_value(table.regulating_control_mrid.query_index, self._mrid_or_none(regulating_cond_eq.regulating_control))

        return self._save_energy_connection(table, insert, regulating_cond_eq, description)

    def _save_regulating_control(self, table: TableRegulatingControls,
                                 insert: PreparedStatement, regulating_control: RegulatingControl, description: str) -> bool:
        insert.add_value(table.discrete.query_index, regulating_control.discrete)
        insert.add_value(table.mode.query_index, regulating_control.mode.short_name)
        insert.add_value(table.monitored_phase.query_index, regulating_control.monitored_phase.short_name)
        insert.add_value(table.target_deadband.query_index, regulating_control.target_deadband)
        insert.add_value(table.target_value.query_index, regulating_control.target_value)
        insert.add_value(table.enabled.query_index, regulating_control.enabled)
        insert.add_value(table.max_allowed_target_value.query_index, regulating_control.max_allowed_target_value)
        insert.add_value(table.min_allowed_target_value.query_index, regulating_control.min_allowed_target_value)
        insert.add_value(table.rated_current.query_index, regulating_control.rated_current)
        insert.add_value(table.terminal_mrid.query_index, self._mrid_or_none(regulating_control.terminal))

        return self._save_power_system_resource(table, insert, regulating_control, description)

    def save_series_compensator(self, series_compensator: SeriesCompensator) -> bool:
        table = self.database_tables.get_table(TableSeriesCompensators)
        insert = self.database_tables.get_insert(TableSeriesCompensators)

        insert.add_value(table.r.query_index, series_compensator.r)
        insert.add_value(table.r0.query_index, series_compensator.r0)
        insert.add_value(table.x.query_index, series_compensator.x)
        insert.add_value(table.x0.query_index, series_compensator.x0)
        insert.add_value(table.varistor_rated_current.query_index, series_compensator.varistor_rated_current)
        insert.add_value(table.varistor_voltage_threshold.query_index, series_compensator.varistor_voltage_threshold)

        return self._save_conducting_equipment(table, insert, series_compensator, "series compensator")

    def _save_shunt_compensator(self, table: TableShuntCompensators, insert: PreparedStatement, shunt_compensator: ShuntCompensator, description: str) -> bool:
        insert.add_value(table.shunt_compensator_info_mrid.query_index, self._mrid_or_none(shunt_compensator.shunt_compensator_info))
        insert.add_value(table.grounded.query_index, shunt_compensator.grounded)
        insert.add_value(table.nom_u.query_index, shunt_compensator.nom_u)
        insert.add_value(table.phase_connection.query_index, shunt_compensator.phase_connection.short_name)
        insert.add_value(table.sections.query_index, shunt_compensator.sections)

        return self._save_regulating_cond_eq(table, insert, shunt_compensator, description)

    def _save_switch(self, table: TableSwitches,
                     insert: PreparedStatement, switch: Switch, description: str) -> bool:
        insert.add_value(table.rated_current.query_index, switch.rated_current)
        insert.add_value(table.normal_open.query_index, int(switch.is_normally_open()))
        insert.add_value(table.open.query_index, int(switch.is_open()))
        insert.add_value(table.switch_info_mrid.query_index, self._mrid_or_none(switch.switch_info))

        return self._save_conducting_equipment(table, insert, switch, description)

    def _save_tap_changer(self, table: TableTapChangers, insert: PreparedStatement, tap_changer: TapChanger, description: str) -> bool:
        insert.add_value(table.control_enabled.query_index, tap_changer.control_enabled)
        insert.add_value(table.high_step.query_index, tap_changer.high_step)
        insert.add_value(table.low_step.query_index, tap_changer.low_step)
        insert.add_value(table.neutral_step.query_index, tap_changer.neutral_step)
        insert.add_value(table.neutral_u.query_index, tap_changer.neutral_u)
        insert.add_value(table.normal_step.query_index, tap_changer.normal_step)
        insert.add_value(table.step.query_index, tap_changer.step)
        insert.add_value(table.tap_changer_control_mrid.query_index, self._mrid_or_none(tap_changer.tap_changer_control))

        return self._save_power_system_resource(table, insert, tap_changer, description)

    def save_tap_changer_control(self, tap_changer_control: TapChangerControl) -> bool:
        table = self.database_tables.get_table(TableTapChangerControls)
        insert = self.database_tables.get_insert(TableTapChangerControls)

        insert.add_value(table.limit_voltage.query_index, tap_changer_control.limit_voltage)
        insert.add_value(table.line_drop_compensation.query_index, tap_changer_control.line_drop_compensation)
        insert.add_value(table.line_drop_r.query_index, tap_changer_control.line_drop_r)
        insert.add_value(table.line_drop_x.query_index, tap_changer_control.line_drop_x)
        insert.add_value(table.reverse_line_drop_r.query_index, tap_changer_control.reverse_line_drop_r)
        insert.add_value(table.reverse_line_drop_x.query_index, tap_changer_control.reverse_line_drop_x)
        insert.add_value(table.forward_ldc_blocking.query_index, tap_changer_control.forward_ldc_blocking)
        insert.add_value(table.time_delay.query_index, tap_changer_control.time_delay)
        insert.add_value(table.co_generation_enabled.query_index, tap_changer_control.co_generation_enabled)

        return self._save_regulating_control(table, insert, tap_changer_control, "tap changer control")

    def _save_transformer_end(self, table: TableTransformerEnds, insert: PreparedStatement, transformer_end: TransformerEnd, description: str) -> bool:
        insert.add_value(table.end_number.query_index, transformer_end.end_number)
        insert.add_value(table.terminal_mrid.query_index, self._mrid_or_none(transformer_end.terminal))
        insert.add_value(table.base_voltage_mrid.query_index, self._mrid_or_none(transformer_end.base_voltage))
        insert.add_value(table.grounded.query_index, transformer_end.grounded)
        insert.add_value(table.r_ground.query_index, transformer_end.r_ground)
        insert.add_value(table.x_ground.query_index, transformer_end.x_ground)
        insert.add_value(table.star_impedance_mrid.query_index, self._mrid_or_none(transformer_end.star_impedance))

        return self._save_identified_object(table, insert, transformer_end, description)

    def save_transformer_star_impedance(self, transformer_star_impedance: TransformerStarImpedance) -> bool:
        table = self.database_tables.get_table(TableTransformerStarImpedance)
        insert = self.database_tables.get_insert(TableTransformerStarImpedance)

        insert.add_value(table.r.query_index, transformer_star_impedance.r)
        insert.add_value(table.r0.query_index, transformer_star_impedance.r0)
        insert.add_value(table.x.query_index, transformer_star_impedance.x)
        insert.add_value(table.x0.query_index, transformer_star_impedance.x0)
        insert.add_value(table.transformer_end_info_mrid.query_index, self._mrid_or_none(transformer_star_impedance.transformer_end_info))

        return self._save_identified_object(table, insert, transformer_star_impedance, "transformer star impedance")

    # ************ IEC61970 InfIEC61970 ************

    def save_circuit(self, circuit: Circuit) -> bool:
        table = self.database_tables.get_table(TableCircuits)
        insert = self.database_tables.get_insert(TableCircuits)

        insert.add_value(table.loop_mrid.query_index, self._mrid_or_none(circuit.loop))
        status = True
        for sub in circuit.end_substations:
            status = status and self._save_circuit_to_substation_association(circuit, sub)

        for t in circuit.end_terminals:
            status = status and self._save_circuit_to_terminal_association(circuit, t)

        return status and self._save_line(table, insert, circuit, "circuit")

    def save_loop(self, loop: Loop) -> bool:
        table = self.database_tables.get_table(TableLoops)
        insert = self.database_tables.get_insert(TableLoops)

        status = True
        for sub in loop.energizing_substations:
            status = status and self._save_loop_to_substation_association(loop, sub, LoopSubstationRelationship.SUBSTATION_ENERGIZES_LOOP)
        for sub in loop.substations:
            status = status and self._save_loop_to_substation_association(loop, sub, LoopSubstationRelationship.LOOP_ENERGIZES_SUBSTATION)
        return status and self._save_identified_object(table, insert, loop, "loop")

    def save_lv_feeder(self, lv_feeder: LvFeeder) -> bool:
        table = self.database_tables.get_table(TableLvFeeders)
        insert = self.database_tables.get_insert(TableLvFeeders)

        insert.add_value(table.normal_head_terminal_mrid.query_index, self._mrid_or_none(lv_feeder.normal_head_terminal))

        return self._save_equipment_container(table, insert, lv_feeder, "lv_feeder")

    # ************ IEC61970 InfIEC61970 WIRES GENERATION PRODUCTION ************

    def save_ev_charging_unit(self, ev_charging_unit: EvChargingUnit) -> bool:
        table = self.database_tables.get_table(TableEvChargingUnits)
        insert = self.database_tables.get_insert(TableEvChargingUnits)

        return self._save_power_electronics_unit(table, insert, ev_charging_unit, "ev charging unit")

    # ************ IEC61970 MEAS ************

    def _save_measurement(self, table: TableMeasurements, insert: PreparedStatement, measurement: Measurement, description: str) -> bool:
        insert.add_value(table.power_system_resource_mrid.query_index, measurement.power_system_resource_mrid)
        insert.add_value(table.remote_source_mrid.query_index, self._mrid_or_none(measurement.remote_source))
        insert.add_value(table.terminal_mrid.query_index, measurement.terminal_mrid)
        insert.add_value(table.phases.query_index, measurement.phases.short_name)
        insert.add_value(table.unit_symbol.query_index, measurement.unit_symbol.short_name)

        return self._save_identified_object(table, insert, measurement, description)

    def save_analog(self, analog: Analog) -> bool:
        table = self.database_tables.get_table(TableAnalogs)
        insert = self.database_tables.get_insert(TableAnalogs)

        insert.add_value(table.positive_flow_in.query_index, analog.positive_flow_in)

        return self._save_measurement(table, insert, analog, "analog")

    def save_accumulator(self, accumulator: Accumulator) -> bool:
        table = self.database_tables.get_table(TableAccumulators)
        insert = self.database_tables.get_insert(TableAccumulators)

        return self._save_measurement(table, insert, accumulator, "accumulator")

    def save_discrete(self, discrete: Discrete) -> bool:
        table = self.database_tables.get_table(TableDiscretes)
        insert = self.database_tables.get_insert(TableDiscretes)

        return self._save_measurement(table, insert, discrete, "discrete")

    def save_control(self, control: Control) -> bool:
        table = self.database_tables.get_table(TableControls)
        insert = self.database_tables.get_insert(TableControls)

        insert.add_value(table.power_system_resource_mrid.query_index, control.power_system_resource_mrid)

        return self._save_io_point(table, insert, control, "control")

    def _save_io_point(self, table: TableIoPoints, insert: PreparedStatement, io_point: IoPoint, description: str) -> bool:
        return self._save_identified_object(table, insert, io_point, description)

    # ************ IEC61970 SCADA ************

    def save_remote_control(self, remote_control: RemoteControl) -> bool:
        table = self.database_tables.get_table(TableRemoteControls)
        insert = self.database_tables.get_insert(TableRemoteControls)

        insert.add_value(table.control_mrid.query_index, self._mrid_or_none(remote_control.control))

        return self._save_remote_point(table, insert, remote_control, "remote control")

    def _save_remote_point(self, table: TableRemotePoints, insert: PreparedStatement, remote_point: RemotePoint, description: str) -> bool:
        return self._save_identified_object(table, insert, remote_point, description)

    def save_remote_source(self, remote_source: RemoteSource) -> bool:
        table = self.database_tables.get_table(TableRemoteSources)

        insert = self.database_tables.get_insert(TableRemoteSources)
        insert.add_value(table.measurement_mrid.query_index, self._mrid_or_none(remote_source.measurement))

        return self._save_remote_point(table, insert, remote_source, "remote source")

    # ************ ASSOCIATIONS ************

    def _save_asset_organisation_role_to_asset_association(self, asset_organisation_role: AssetOrganisationRole, asset: Asset) -> bool:
        table = self.database_tables.get_table(TableAssetOrganisationRolesAssets)
        insert = self.database_tables.get_insert(TableAssetOrganisationRolesAssets)

        insert.add_value(table.asset_organisation_role_mrid.query_index, asset_organisation_role.mrid)
        insert.add_value(table.asset_mrid.query_index, asset.mrid)

        return self._try_execute_single_update(insert, f"{asset_organisation_role.mrid}-to-{asset.mrid}", "asset organisation role to asset association")

    def _save_usage_point_to_end_device_association(self, usage_point: UsagePoint, end_device: EndDevice) -> bool:
        table = self.database_tables.get_table(TableUsagePointsEndDevices)
        insert = self.database_tables.get_insert(TableUsagePointsEndDevices)

        insert.add_value(table.usage_point_mrid.query_index, usage_point.mrid)
        insert.add_value(table.end_device_mrid.query_index, end_device.mrid)

        return self._try_execute_single_update(insert, f"{usage_point.mrid}-to-{end_device.mrid}", "usage point to end device association")

    def _save_equipment_to_usage_point_association(self, equipment: Equipment, usage_point: UsagePoint) -> bool:
        table = self.database_tables.get_table(TableEquipmentUsagePoints)
        insert = self.database_tables.get_insert(TableEquipmentUsagePoints)

        insert.add_value(table.equipment_mrid.query_index, equipment.mrid)
        insert.add_value(table.usage_point_mrid.query_index, usage_point.mrid)

        return self._try_execute_single_update(insert, f"{equipment.mrid}-to-{usage_point.mrid}", "Equipment to UsagePoint association ")

    def _save_equipment_to_operational_restriction_association(self, equipment: Equipment, operational_restriction: OperationalRestriction) -> bool:
        table = self.database_tables.get_table(TableEquipmentOperationalRestrictions)
        insert = self.database_tables.get_insert(TableEquipmentOperationalRestrictions)

        insert.add_value(table.equipment_mrid.query_index, equipment.mrid)
        insert.add_value(table.operational_restriction_mrid.query_index, operational_restriction.mrid)

        return self._try_execute_single_update(insert, f"{equipment.mrid}-to-{operational_restriction.mrid}",
                                               "equipment to operational restriction association")

    def _save_equipment_to_equipment_container_association(self, equipment: Equipment, equipment_container: EquipmentContainer) -> bool:
        table = self.database_tables.get_table(TableEquipmentEquipmentContainers)
        insert = self.database_tables.get_insert(TableEquipmentEquipmentContainers)

        insert.add_value(table.equipment_mrid.query_index, equipment.mrid)
        insert.add_value(table.equipment_container_mrid.query_index, equipment_container.mrid)

        return self._try_execute_single_update(insert, f"{equipment.mrid}-to-{equipment_container.mrid}", "equipment to equipment container association")

    def _save_circuit_to_substation_association(self, circuit: Circuit, substation: Substation) -> bool:
        table = self.database_tables.get_table(TableCircuitsSubstations)
        insert = self.database_tables.get_insert(TableCircuitsSubstations)

        insert.add_value(table.circuit_mrid.query_index, circuit.mrid)
        insert.add_value(table.substation_mrid.query_index, substation.mrid)

        return self._try_execute_single_update(insert, f"{circuit.mrid}-to-{substation.mrid}", "circuit to substation association")

    def _save_circuit_to_terminal_association(self, circuit: Circuit, terminal: Terminal) -> bool:
        table = self.database_tables.get_table(TableCircuitsTerminals)
        insert = self.database_tables.get_insert(TableCircuitsTerminals)

        insert.add_value(table.circuit_mrid.query_index, circuit.mrid)
        insert.add_value(table.terminal_mrid.query_index, terminal.mrid)

        return self._try_execute_single_update(insert, f"{circuit.mrid}-to-{terminal.mrid}", "circuit to terminal association")

    def _save_loop_to_substation_association(self, loop: Loop, substation: Substation, relationship: LoopSubstationRelationship) -> bool:
        table = self.database_tables.get_table(TableLoopsSubstations)
        insert = self.database_tables.get_insert(TableLoopsSubstations)

        insert.add_value(table.loop_mrid.query_index, loop.mrid)
        insert.add_value(table.substation_mrid.query_index, substation.mrid)
        insert.add_value(table.relationship.query_index, relationship.short_name)

        return self._try_execute_single_update(insert, f"{loop.mrid}-to-{substation.mrid}", f"loop to substation association")

    def _save_protection_relay_function_protected_switch(self, protection_relay_function: ProtectionRelayFunction, protected_switch: ProtectedSwitch) -> bool:
        table = self.database_tables.get_table(TableProtectionRelayFunctionsProtectedSwitches)
        insert = self.database_tables.get_insert(TableProtectionRelayFunctionsProtectedSwitches)

        insert.add_value(table.protection_relay_function_mrid.query_index, protection_relay_function.mrid)
        insert.add_value(table.protected_switch_mrid.query_index, protected_switch.mrid)

        return self._try_execute_single_update(insert, f"{protection_relay_function.mrid}-to-{protected_switch.mrid}",
                                               "protection equipment to protected switch association")

    def _save_protection_relay_function_sensor(self, protection_relay_function: ProtectionRelayFunction, sensor: Sensor) -> bool:
        table = self.database_tables.get_table(TableProtectionRelayFunctionsSensors)
        insert = self.database_tables.get_insert(TableProtectionRelayFunctionsSensors)

        insert.add_value(table.protection_relay_function_mrid.query_index, protection_relay_function.mrid)
        insert.add_value(table.sensor_mrid.query_index, sensor.mrid)

        return self._try_execute_single_update(insert, f"{protection_relay_function.mrid}-to-{sensor.mrid}",
                                               "sensor to protected switch association")

    def _save_protection_relay_scheme_protection_relay_function(self, protection_relay_scheme: ProtectionRelayScheme,
                                                                protection_relay_function: ProtectionRelayFunction) -> bool:
        table = self.database_tables.get_table(TableProtectionRelaySchemesProtectionRelayFunctions)
        insert = self.database_tables.get_insert(TableProtectionRelaySchemesProtectionRelayFunctions)

        insert.add_value(table.protection_relay_scheme_mrid.query_index, protection_relay_scheme.mrid)
        insert.add_value(table.protection_relay_function_mrid.query_index, protection_relay_function.mrid)

        return self._try_execute_single_update(insert, f"{protection_relay_scheme.mrid}-to-{protection_relay_function.mrid}",
                                               "protection relay function to protection relay function association")
