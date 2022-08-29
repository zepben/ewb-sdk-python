#  Copyright 2021 Zeppelin Bend Pty Ltd
# 
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Callable, Optional

from zepben.evolve import BaseCIMReader, TableCableInfo, ResultSet, CableInfo, TableNoLoadTests, NoLoadTest, TableOpenCircuitTests, \
    OpenCircuitTest, TableOverheadWireInfo, OverheadWireInfo, TablePowerTransformerInfo, PowerTransformerInfo, TableShortCircuitTests, ShortCircuitTest, \
    TableShuntCompensatorInfo, ShuntCompensatorInfo, TableTransformerEndInfo, TransformerEndInfo, WindingConnection, TransformerTankInfo, \
    TableTransformerTankInfo, TransformerTest, TableTransformerTest, WireInfo, TableWireInfo, WireMaterialKind, Asset, TableAssets, Location, AssetContainer, \
    TableAssetContainers, AssetInfo, TableAssetInfo, AssetOrganisationRole, TableAssetOrganisationRoles, Structure, TableStructures, TableAssetOwners, \
    AssetOwner, TablePoles, Pole, TableStreetlights, Streetlight, StreetlightLampKind, TableLocations, TableLocationStreetAddresses, \
    TableLocationStreetAddressField, TablePositionPoints, PositionPoint, TableStreetAddresses, StreetAddress, TableTownDetails, TownDetail, StreetDetail, \
    TransformerConstructionKind, TransformerFunctionKind, EndDevice, TableEndDevices, TableMeters, Meter, TableUsagePoints, \
    UsagePoint, TableOperationalRestrictions, OperationalRestriction, AuxiliaryEquipment, TableAuxiliaryEquipment, Terminal, TableFaultIndicators, \
    FaultIndicator, AcDcTerminal, TableAcDcTerminals, TableBaseVoltages, BaseVoltage, ConductingEquipment, TableConductingEquipment, TableConnectivityNodes, \
    ConnectivityNode, ConnectivityNodeContainer, TableConnectivityNodeContainers, Equipment, TableEquipment, EquipmentContainer, TableEquipmentContainers, \
    TableFeeders, Feeder, Substation, GeographicalRegion, TableGeographicalRegions, PowerSystemResource, TablePowerSystemResources, TableSites, Site, \
    TableSubGeographicalRegions, SubGeographicalRegion, TableSubstations, TableTerminals, PhaseCode, TableEquivalentBranches, EquivalentBranch, \
    EquivalentEquipment, TableEquivalentEquipment, TableAccumulators, Accumulator, TableAnalogs, Analog, TableControls, Control, TableDiscretes, Discrete, \
    IoPoint, TableIoPoints, Measurement, TableMeasurements, RemoteSource, UnitSymbol, TableRemoteControls, RemoteControl, RemotePoint, TableRemotePoints, \
    TableRemoteSources, TableBatteryUnit, BatteryUnit, BatteryStateKind, TablePhotoVoltaicUnit, PhotoVoltaicUnit, PowerElectronicsUnit, \
    TablePowerElectronicsUnit, PowerElectronicsConnection, TablePowerElectronicsWindUnit, PowerElectronicsWindUnit, TableAcLineSegments, AcLineSegment, \
    PerLengthSequenceImpedance, TableBreakers, Breaker, TableLoadBreakSwitches, LoadBreakSwitch, TableBusbarSections, BusbarSection, Conductor, \
    TableConductors, Connector, TableConnectors, TableDisconnectors, Disconnector, EnergyConnection, TableEnergyConnections, TableEnergyConsumers, \
    EnergyConsumer, PhaseShuntConnectionKind, TableEnergyConsumerPhases, EnergyConsumerPhase, SinglePhaseKind, TableEnergySources, EnergySource, \
    TableEnergySourcePhases, EnergySourcePhase, TableFuses, Fuse, TableJumpers, Jumper, TableJunctions, Junction, Line, TableLines, \
    TableLinearShuntCompensators, LinearShuntCompensator, PerLengthImpedance, TablePerLengthImpedances, PerLengthLineParameter, TablePerLengthLineParameters, \
    TablePerLengthSequenceImpedances, TablePowerElectronicsConnection, TablePowerElectronicsConnectionPhases, PowerElectronicsConnectionPhase, \
    TablePowerTransformers, PowerTransformer, VectorGroup, TablePowerTransformerEnds, PowerTransformerEnd, ProtectedSwitch, TableProtectedSwitches, \
    TableRatioTapChangers, RatioTapChanger, TransformerEnd, TableReclosers, Recloser, RegulatingCondEq, TableRegulatingCondEq, ShuntCompensator, \
    TableShuntCompensators, Switch, TableSwitches, TapChanger, TableTapChangers, TableTransformerEnds, TransformerStarImpedance, \
    TableTransformerStarImpedance, TableCircuits, Circuit, Loop, TableLoops, TableAssetOrganisationRolesAssets, TableEquipmentEquipmentContainers, \
    TableEquipmentOperationalRestrictions, TableEquipmentUsagePoints, TableUsagePointsEndDevices, TableCircuitsSubstations, TableCircuitsTerminals, \
    TableLoopsSubstations, LoopSubstationRelationship, LvFeeder, TableLvFeeders

__all__ = ["NetworkCIMReader"]


class NetworkCIMReader(BaseCIMReader):

    # ************ IEC61968 ASSET INFO ************

    def load_cable_info(self, table: TableCableInfo, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        cable_info = CableInfo(mrid=set_last_mrid(rs.get_string(table.mrid.query_index)))

        return self._load_wire_info(cable_info, table, rs) and self._add_or_throw(cable_info)

    def load_no_load_test(self, table: TableNoLoadTests, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        no_load_test = NoLoadTest(mrid=set_last_mrid(rs.get_string(table.mrid.query_index)))

        no_load_test.energised_end_voltage = rs.get_int(table.energised_end_voltage.query_index, None)
        no_load_test.exciting_current = rs.get_double(table.exciting_current.query_index, None)
        no_load_test.exciting_current_zero = rs.get_double(table.exciting_current_zero.query_index, None)
        no_load_test.loss = rs.get_int(table.loss.query_index, None)
        no_load_test.loss_zero = rs.get_int(table.loss_zero.query_index, None)

        return self._load_transformer_test(no_load_test, table, rs) and self._add_or_throw(no_load_test)

    def load_open_circuit_test(self, table: TableOpenCircuitTests, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        open_circuit_test = OpenCircuitTest(mrid=set_last_mrid(rs.get_string(table.mrid.query_index)))

        open_circuit_test.energised_end_step = rs.get_int(table.energised_end_step.query_index, None)
        open_circuit_test.energised_end_voltage = rs.get_int(table.energised_end_voltage.query_index, None)
        open_circuit_test.open_end_step = rs.get_int(table.open_end_step.query_index, None)
        open_circuit_test.open_end_voltage = rs.get_int(table.open_end_voltage.query_index, None)
        open_circuit_test.phase_shift = rs.get_double(table.phase_shift.query_index, None)

        return self._load_transformer_test(open_circuit_test, table, rs) and self._add_or_throw(open_circuit_test)

    def load_overhead_wire_info(self, table: TableOverheadWireInfo, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        overhead_wire_info = OverheadWireInfo(mrid=set_last_mrid(rs.get_string(table.mrid.query_index)))

        return self._load_wire_info(overhead_wire_info, table, rs) and self._add_or_throw(overhead_wire_info)

    def load_power_transformer_info(self, table: TablePowerTransformerInfo, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        power_transformer_info = PowerTransformerInfo(mrid=set_last_mrid(rs.get_string(table.mrid.query_index)))

        return self._load_asset_info(power_transformer_info, table, rs) and self._add_or_throw(power_transformer_info)

    def load_short_circuit_test(self, table: TableShortCircuitTests, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        short_circuit_test = ShortCircuitTest(mrid=set_last_mrid(rs.get_string(table.mrid.query_index)))

        short_circuit_test.current = rs.get_double(table.current.query_index, None)
        short_circuit_test.energised_end_step = rs.get_int(table.energised_end_step.query_index, None)
        short_circuit_test.grounded_end_step = rs.get_int(table.grounded_end_step.query_index, None)
        short_circuit_test.leakage_impedance = rs.get_double(table.leakage_impedance.query_index, None)
        short_circuit_test.leakage_impedance_zero = rs.get_double(table.leakage_impedance_zero.query_index, None)
        short_circuit_test.loss = rs.get_int(table.loss.query_index, None)
        short_circuit_test.loss_zero = rs.get_int(table.loss_zero.query_index, None)
        short_circuit_test.power = rs.get_int(table.power.query_index, None)
        short_circuit_test.voltage = rs.get_double(table.voltage.query_index, None)
        short_circuit_test.voltage_ohmic_part = rs.get_double(table.voltage_ohmic_part.query_index, None)

        return self._load_transformer_test(short_circuit_test, table, rs) and self._add_or_throw(short_circuit_test)

    def load_shunt_compensator_info(self, table: TableShuntCompensatorInfo, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        shunt_compensator_info = ShuntCompensatorInfo(mrid=set_last_mrid(rs.get_string(table.mrid.query_index)))

        shunt_compensator_info.max_power_loss = rs.get_int(table.max_power_loss.query_index, None)
        shunt_compensator_info.rated_current = rs.get_int(table.rated_current.query_index, None)
        shunt_compensator_info.rated_reactive_power = rs.get_int(table.rated_reactive_power.query_index, None)
        shunt_compensator_info.rated_voltage = rs.get_int(table.rated_voltage.query_index, None)

        return self._load_asset_info(shunt_compensator_info, table, rs) and self._add_or_throw(shunt_compensator_info)

    def load_transformer_end_info(self, table: TableTransformerEndInfo, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        transformer_end_info = TransformerEndInfo(mrid=set_last_mrid(rs.get_string(table.mrid.query_index)))

        transformer_end_info.connection_kind = WindingConnection[rs.get_string(table.connection_kind.query_index)]
        transformer_end_info.emergency_s = rs.get_int(table.emergency_s.query_index, None)
        transformer_end_info.end_number = rs.get_int(table.end_number.query_index)
        transformer_end_info.insulation_u = rs.get_int(table.insulation_u.query_index, None)
        transformer_end_info.phase_angle_clock = rs.get_int(table.phase_angle_clock.query_index, None)
        transformer_end_info.r = rs.get_double(table.r.query_index, None)
        transformer_end_info.rated_s = rs.get_int(table.rated_s.query_index, None)
        transformer_end_info.rated_u = rs.get_int(table.rated_u.query_index, None)
        transformer_end_info.short_term_s = rs.get_int(table.short_term_s.query_index, None)

        transformer_end_info.transformer_tank_info = self._ensure_get(rs.get_string(table.transformer_tank_info_mrid.query_index, None), TransformerTankInfo)
        transformer_end_info.energised_end_no_load_tests = self._ensure_get(rs.get_string(table.energised_end_no_load_tests.query_index, None), NoLoadTest)
        transformer_end_info.energised_end_short_circuit_tests = self._ensure_get(rs.get_string(table.energised_end_short_circuit_tests.query_index, None),
                                                                                  ShortCircuitTest)
        transformer_end_info.grounded_end_short_circuit_tests = self._ensure_get(rs.get_string(table.grounded_end_short_circuit_tests.query_index, None),
                                                                                 ShortCircuitTest)
        transformer_end_info.open_end_open_circuit_tests = self._ensure_get(rs.get_string(table.open_end_open_circuit_tests.query_index, None), OpenCircuitTest)
        transformer_end_info.energised_end_open_circuit_tests = self._ensure_get(rs.get_string(table.energised_end_open_circuit_tests.query_index, None),
                                                                                 OpenCircuitTest)

        if transformer_end_info.transformer_tank_info is not None:
            transformer_end_info.transformer_tank_info.add_transformer_end_info(transformer_end_info)

        return self._load_asset_info(transformer_end_info, table, rs) and self._add_or_throw(transformer_end_info)

    def load_transformer_tank_info(self, table: TableTransformerTankInfo, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        transformer_tank_info = TransformerTankInfo(mrid=set_last_mrid(rs.get_string(table.mrid.query_index)))

        transformer_tank_info.power_transformer_info = self._ensure_get(rs.get_string(table.power_transformer_info_mrid.query_index, None),
                                                                        PowerTransformerInfo)
        if transformer_tank_info.power_transformer_info is not None:
            transformer_tank_info.power_transformer_info.add_transformer_tank_info(transformer_tank_info)

        return self._load_asset_info(transformer_tank_info, table, rs) and self._add_or_throw(transformer_tank_info)

    def _load_transformer_test(self, transformer_test: TransformerTest, table: TableTransformerTest, rs: ResultSet) -> bool:
        transformer_test.base_power = rs.get_int(table.base_power.query_index, None)
        transformer_test.temperature = rs.get_double(table.temperature.query_index, None)

        return self._load_identified_object(transformer_test, table, rs)

    def _load_wire_info(self, wire_info: WireInfo, table: TableWireInfo, rs: ResultSet) -> bool:
        wire_info.rated_current = rs.get_int(table.rated_current.query_index, None)
        wire_info.material = WireMaterialKind[rs.get_string(table.material.query_index)]

        return self._load_asset_info(wire_info, table, rs)

    # ************ IEC61968 ASSETS ************

    def _load_asset(self, asset: Asset, table: TableAssets, rs: ResultSet) -> bool:
        asset.location = self._ensure_get(rs.get_string(table.location_mrid.query_index, None), Location)

        return self._load_identified_object(asset, table, rs)

    def _load_asset_container(self, asset_container: AssetContainer, table: TableAssetContainers, rs: ResultSet) -> bool:
        return self._load_asset(asset_container, table, rs)

    def _load_asset_info(self, asset_info: AssetInfo, table: TableAssetInfo, rs: ResultSet) -> bool:
        return self._load_identified_object(asset_info, table, rs)

    def _load_asset_organisation_role(self, asset_organisation_role: AssetOrganisationRole, table: TableAssetOrganisationRoles, rs: ResultSet) -> bool:
        return self._load_organisation_role(asset_organisation_role, table, rs)

    def _load_structure(self, structure: Structure, table: TableStructures, rs: ResultSet) -> bool:
        return self._load_asset_container(structure, table, rs)

    def load_asset_owner(self, table: TableAssetOwners, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        asset_owner = AssetOwner(mrid=set_last_mrid(rs.get_string(table.mrid.query_index)))

        return self._load_asset_organisation_role(asset_owner, table, rs) and self._add_or_throw(asset_owner)

    def load_pole(self, table: TablePoles, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        pole = Pole(mrid=set_last_mrid(rs.get_string(table.mrid.query_index)))

        pole.classification = rs.get_string(table.classification.query_index, "")

        return self._load_structure(pole, table, rs) and self._add_or_throw(pole)

    def load_streetlight(self, table: TableStreetlights, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        streetlight = Streetlight(mrid=set_last_mrid(rs.get_string(table.mrid.query_index)))

        streetlight.lamp_kind = StreetlightLampKind[rs.get_string(table.lamp_kind.query_index)]
        streetlight.light_rating = rs.get_int(table.light_rating.query_index, None)
        streetlight.pole = self._ensure_get(rs.get_string(table.pole_mrid.query_index, None), Pole)
        if streetlight.pole is not None:
            streetlight.pole.add_streetlight(streetlight)

        return self._load_asset(streetlight, table, rs) and self._add_or_throw(streetlight)

    # ************ IEC61968 COMMON ************

    def load_location(self, table: TableLocations, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        location = Location(mrid=set_last_mrid(rs.get_string(table.mrid.query_index)))

        return self._load_identified_object(location, table, rs) and self._add_or_throw(location)

    def load_location_street_address(self, table: TableLocationStreetAddresses, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        location_mrid = set_last_mrid(rs.get_string(table.location_mrid.query_index))
        field = TableLocationStreetAddressField[rs.get_string(table.address_field.query_index)]

        set_last_mrid(f"{location_mrid}-to-{field}")
        location = self._base_service.get(location_mrid, Location)

        if field == TableLocationStreetAddressField.mainAddress:
            location.main_address = self._load_street_address(table, rs)

        return True

    def load_position_point(self, table: TablePositionPoints, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        location_mrid = set_last_mrid(rs.get_string(table.location_mrid.query_index))
        sequence_number = rs.get_int(table.sequence_number.query_index)

        set_last_mrid(f"{location_mrid}-point{sequence_number}")
        location = self._base_service.get(location_mrid, Location)

        # noinspection PyArgumentList
        position_point = PositionPoint(
            rs.get_double(table.x_position.query_index),
            rs.get_double(table.y_position.query_index)
        )

        location.insert_point(position_point, sequence_number)

        return True

    def _load_street_address(self, table: TableStreetAddresses, rs: ResultSet) -> StreetAddress:
        # noinspection PyArgumentList
        return StreetAddress(
            rs.get_string(table.postal_code.query_index, ""),
            self._load_town_detail(table, rs),
            rs.get_string(table.po_box.query_index, ""),
            self._load_street_detail(table, rs)
        )

    @staticmethod
    def _load_street_detail(table: TableStreetAddresses, rs: ResultSet) -> Optional[StreetDetail]:
        # noinspection PyArgumentList
        street_detail = StreetDetail(
            rs.get_string(table.building_name.query_index, ""),
            rs.get_string(table.floor_identification.query_index, ""),
            rs.get_string(table.street_name.query_index, ""),
            rs.get_string(table.number.query_index, ""),
            rs.get_string(table.suite_number.query_index, ""),
            rs.get_string(table.type.query_index, ""),
            rs.get_string(table.display_address.query_index, "")
        )

        return None if street_detail.all_fields_empty() else street_detail

    @staticmethod
    def _load_town_detail(table: TableTownDetails, rs: ResultSet) -> Optional[TownDetail]:
        # noinspection PyArgumentList
        town_detail = TownDetail(
            rs.get_string(table.town_name.query_index, ""),
            rs.get_string(table.state_or_province.query_index, "")
        )

        return None if town_detail.all_fields_null_or_empty() else town_detail

    # ************ IEC61968 METERING ************

    def _load_end_device(self, end_device: EndDevice, table: TableEndDevices, rs: ResultSet) -> bool:
        end_device.customer_mrid = rs.get_string(table.customer_mrid.query_index, None)
        end_device.service_location = self._ensure_get(rs.get_string(table.service_location_mrid.query_index, None), Location)

        return self._load_asset_container(end_device, table, rs)

    def load_meter(self, table: TableMeters, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        meter = Meter(mrid=set_last_mrid(rs.get_string(table.mrid.query_index)))

        return self._load_end_device(meter, table, rs) and self._add_or_throw(meter)

    def load_usage_point(self, table: TableUsagePoints, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        usage_point = UsagePoint(mrid=set_last_mrid(rs.get_string(table.mrid.query_index)))

        usage_point.usage_point_location = self._ensure_get(rs.get_string(table.location_mrid.query_index, None), Location)
        usage_point.is_virtual = rs.get_boolean(table.is_virtual.query_index)
        usage_point.connection_category = rs.get_string(table.connection_category.query_index, None)

        return self._load_identified_object(usage_point, table, rs) and self._add_or_throw(usage_point)

    # ************ IEC61968 OPERATIONS ************

    def load_operational_restriction(self, table: TableOperationalRestrictions, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        operational_restriction = OperationalRestriction(mrid=set_last_mrid(rs.get_string(table.mrid.query_index)))

        return self._load_document(operational_restriction, table, rs) and self._add_or_throw(operational_restriction)

    # ************ IEC61970 BASE AUXILIARY EQUIPMENT ************

    def _load_auxiliary_equipment(self, auxiliary_equipment: AuxiliaryEquipment, table: TableAuxiliaryEquipment, rs: ResultSet) -> bool:
        auxiliary_equipment.terminal = self._ensure_get(rs.get_string(table.terminal_mrid.query_index, None), Terminal)

        return self._load_equipment(auxiliary_equipment, table, rs)

    def load_fault_indicator(self, table: TableFaultIndicators, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        fault_indicator = FaultIndicator(mrid=set_last_mrid(rs.get_string(table.mrid.query_index)))

        return self._load_auxiliary_equipment(fault_indicator, table, rs) and self._add_or_throw(fault_indicator)

    # ************ IEC61970 BASE CORE ************

    def _load_ac_dc_terminal(self, ac_dc_terminal: AcDcTerminal, table: TableAcDcTerminals, rs: ResultSet) -> bool:
        return self._load_identified_object(ac_dc_terminal, table, rs)

    def load_base_voltage(self, table: TableBaseVoltages, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        base_voltage = BaseVoltage(mrid=set_last_mrid(rs.get_string(table.mrid.query_index)))

        base_voltage.nominal_voltage = rs.get_int(table.nominal_voltage.query_index)

        return self._load_identified_object(base_voltage, table, rs) and self._add_or_throw(base_voltage)

    def _load_conducting_equipment(self, conducting_equipment: ConductingEquipment, table: TableConductingEquipment, rs: ResultSet) -> bool:
        conducting_equipment.base_voltage = self._ensure_get(rs.get_string(table.base_voltage_mrid.query_index, None), BaseVoltage)

        return self._load_equipment(conducting_equipment, table, rs)

    def load_connectivity_node(self, table: TableConnectivityNodes, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        connectivity_node = ConnectivityNode(mrid=set_last_mrid(rs.get_string(table.mrid.query_index)))

        return self._load_identified_object(connectivity_node, table, rs) and self._add_or_throw(connectivity_node)

    def _load_connectivity_node_container(
        self,
        connectivity_node_container: ConnectivityNodeContainer,
        table: TableConnectivityNodeContainers,
        rs: ResultSet
    ) -> bool:
        return self._load_power_system_resource(connectivity_node_container, table, rs)

    def _load_equipment(self, equipment: Equipment, table: TableEquipment, rs: ResultSet) -> bool:
        equipment.normally_in_service = rs.get_boolean(table.normally_in_service.query_index)
        equipment.in_service = rs.get_boolean(table.in_service.query_index)

        return self._load_power_system_resource(equipment, table, rs)

    def _load_equipment_container(self, equipment_container: EquipmentContainer, table: TableEquipmentContainers, rs: ResultSet) -> bool:
        return self._load_connectivity_node_container(equipment_container, table, rs)

    def load_feeder(self, table: TableFeeders, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        feeder = Feeder(mrid=set_last_mrid(rs.get_string(table.mrid.query_index)))

        feeder.normal_head_terminal = self._ensure_get(rs.get_string(table.normal_head_terminal_mrid.query_index, None), Terminal)
        feeder.normal_energizing_substation = self._ensure_get(rs.get_string(table.normal_energizing_substation_mrid.query_index, None), Substation)
        if feeder.normal_energizing_substation is not None:
            feeder.normal_energizing_substation.add_feeder(feeder)

        return self._load_equipment_container(feeder, table, rs) and self._add_or_throw(feeder)

    def load_geographical_region(self, table: TableGeographicalRegions, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        geographical_region = GeographicalRegion(mrid=set_last_mrid(rs.get_string(table.mrid.query_index)))

        return self._load_identified_object(geographical_region, table, rs) and self._add_or_throw(geographical_region)

    def _load_power_system_resource(self, power_system_resource: PowerSystemResource, table: TablePowerSystemResources, rs: ResultSet) -> bool:
        power_system_resource.location = self._ensure_get(rs.get_string(table.location_mrid.query_index, None), Location)
        # Currently unused power_system_resource.num_controls = rs.get_int(table.num_controls.query_index)

        return self._load_identified_object(power_system_resource, table, rs)

    def load_site(self, table: TableSites, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        site = Site(mrid=set_last_mrid(rs.get_string(table.mrid.query_index)))

        return self._load_equipment_container(site, table, rs) and self._add_or_throw(site)

    def load_sub_geographical_region(self, table: TableSubGeographicalRegions, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        sub_geographical_region = SubGeographicalRegion(mrid=set_last_mrid(rs.get_string(table.mrid.query_index)))

        sub_geographical_region.geographical_region = self._ensure_get(rs.get_string(table.geographical_region_mrid.query_index, None), GeographicalRegion)
        if sub_geographical_region.geographical_region is not None:
            sub_geographical_region.geographical_region.add_sub_geographical_region(sub_geographical_region)

        return self._load_identified_object(sub_geographical_region, table, rs) and self._add_or_throw(sub_geographical_region)

    def load_substation(self, table: TableSubstations, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        substation = Substation(mrid=set_last_mrid(rs.get_string(table.mrid.query_index)))

        substation.sub_geographical_region = self._ensure_get(rs.get_string(table.sub_geographical_region_mrid.query_index, None), SubGeographicalRegion)
        if substation.sub_geographical_region is not None:
            substation.sub_geographical_region.add_substation(substation)

        return self._load_equipment_container(substation, table, rs) and self._add_or_throw(substation)

    def load_terminal(self, table: TableTerminals, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        terminal = Terminal(mrid=set_last_mrid(rs.get_string(table.mrid.query_index)))

        terminal.sequence_number = rs.get_int(table.sequence_number.query_index)
        terminal.conducting_equipment = self._ensure_get(rs.get_string(table.conducting_equipment_mrid.query_index, None), ConductingEquipment)
        if terminal.conducting_equipment is not None:
            terminal.conducting_equipment.add_terminal(terminal)
        terminal.phases = PhaseCode[rs.get_string(table.phases.query_index)]

        # noinspection PyUnresolvedReferences
        self._base_service.connect_by_mrid(terminal, rs.get_string(table.connectivity_node_mrid.query_index, None))

        return self._load_ac_dc_terminal(terminal, table, rs) and self._add_or_throw(terminal)

    # ************ IEC61970 BASE EQUIVALENTS ************

    def load_equivalent_branch(self, table: TableEquivalentBranches, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        equivalent_branch = EquivalentBranch(mrid=set_last_mrid(rs.get_string(table.mrid.query_index)))

        equivalent_branch.negative_r12 = rs.get_double(table.negative_r12.query_index, None)
        equivalent_branch.negative_r21 = rs.get_double(table.negative_r21.query_index, None)
        equivalent_branch.negative_x12 = rs.get_double(table.negative_x12.query_index, None)
        equivalent_branch.negative_x21 = rs.get_double(table.negative_x21.query_index, None)
        equivalent_branch.positive_r12 = rs.get_double(table.positive_r12.query_index, None)
        equivalent_branch.positive_r21 = rs.get_double(table.positive_r21.query_index, None)
        equivalent_branch.positive_x12 = rs.get_double(table.positive_x12.query_index, None)
        equivalent_branch.positive_x21 = rs.get_double(table.positive_x21.query_index, None)
        equivalent_branch.r = rs.get_double(table.r.query_index, None)
        equivalent_branch.r21 = rs.get_double(table.r21.query_index, None)
        equivalent_branch.x = rs.get_double(table.x.query_index, None)
        equivalent_branch.x21 = rs.get_double(table.x21.query_index, None)
        equivalent_branch.zero_r12 = rs.get_double(table.zero_r12.query_index, None)
        equivalent_branch.zero_r21 = rs.get_double(table.zero_r21.query_index, None)
        equivalent_branch.zero_x12 = rs.get_double(table.zero_x12.query_index, None)
        equivalent_branch.zero_x21 = rs.get_double(table.zero_x21.query_index, None)

        return self._load_equivalent_equipment(equivalent_branch, table, rs) and self._add_or_throw(equivalent_branch)

    def _load_equivalent_equipment(self, equivalent_equipment: EquivalentEquipment, table: TableEquivalentEquipment, rs: ResultSet) -> bool:
        return self._load_conducting_equipment(equivalent_equipment, table, rs)

    # ************ IEC61970 BASE MEAS ************

    def load_accumulator(self, table: TableAccumulators, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        meas = Accumulator(mrid=set_last_mrid(rs.get_string(table.mrid.query_index)))

        return self._load_measurement(meas, table, rs) and self._add_or_throw(meas)

    def load_analog(self, table: TableAnalogs, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        meas = Analog(mrid=set_last_mrid(rs.get_string(table.mrid.query_index)))

        meas.positive_flow_in = rs.get_boolean(table.positive_flow_in.query_index)

        return self._load_measurement(meas, table, rs) and self._add_or_throw(meas)

    def load_control(self, table: TableControls, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        control = Control(mrid=set_last_mrid(rs.get_string(table.mrid.query_index)))

        control.power_system_resource_mrid = rs.get_string(table.power_system_resource_mrid.query_index, None)

        return self._load_io_point(control, table, rs) and self._add_or_throw(control)

    def load_discrete(self, table: TableDiscretes, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        meas = Discrete(mrid=set_last_mrid(rs.get_string(table.mrid.query_index)))

        return self._load_measurement(meas, table, rs) and self._add_or_throw(meas)

    def _load_io_point(self, io_point: IoPoint, table: TableIoPoints, rs: ResultSet) -> bool:
        return self._load_identified_object(io_point, table, rs)

    def _load_measurement(self, measurement: Measurement, table: TableMeasurements, rs: ResultSet) -> bool:
        measurement.power_system_resource_mrid = rs.get_string(table.power_system_resource_mrid.query_index, None)
        measurement.remote_source = self._ensure_get(rs.get_string(table.remote_source_mrid.query_index, None), RemoteSource)
        if measurement.remote_source is not None:
            measurement.remote_source.measurement = measurement
        measurement.terminal_mrid = rs.get_string(table.terminal_mrid.query_index, None)
        measurement.phases = PhaseCode[rs.get_string(table.phases.query_index)]
        measurement.unit_symbol = UnitSymbol[rs.get_string(table.unit_symbol.query_index)]

        return self._load_identified_object(measurement, table, rs)

    # ************ IEC61970 BASE SCADA ************

    def load_remote_control(self, table: TableRemoteControls, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        remote_control = RemoteControl(mrid=set_last_mrid(rs.get_string(table.mrid.query_index)))

        remote_control.control = self._ensure_get(rs.get_string(table.control_mrid.query_index, None), Control)
        if remote_control.control is not None:
            remote_control.control.remote_control = remote_control

        return self._load_remote_point(remote_control, table, rs) and self._add_or_throw(remote_control)

    def _load_remote_point(self, remote_point: RemotePoint, table: TableRemotePoints, rs: ResultSet) -> bool:
        return self._load_identified_object(remote_point, table, rs)

    def load_remote_source(self, table: TableRemoteSources, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        remote_source = RemoteSource(mrid=set_last_mrid(rs.get_string(table.mrid.query_index)))

        return self._load_remote_point(remote_source, table, rs) and self._add_or_throw(remote_source)

    # ************ IEC61970 BASE WIRES GENERATION PRODUCTION ************

    def load_battery_unit(self, table: TableBatteryUnit, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        battery_unit = BatteryUnit(mrid=set_last_mrid(rs.get_string(table.mrid.query_index)))

        battery_unit.battery_state = BatteryStateKind[rs.get_string(table.battery_state.query_index)]
        battery_unit.rated_e = rs.get_int(table.rated_e.query_index, None)
        battery_unit.stored_e = rs.get_int(table.stored_e.query_index, None)

        return self._load_power_electronics_unit(battery_unit, table, rs) and self._add_or_throw(battery_unit)

    def load_photo_voltaic_unit(self, table: TablePhotoVoltaicUnit, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        photo_voltaic_unit = PhotoVoltaicUnit(mrid=set_last_mrid(rs.get_string(table.mrid.query_index)))

        return self._load_power_electronics_unit(photo_voltaic_unit, table, rs) and self._add_or_throw(photo_voltaic_unit)

    def _load_power_electronics_unit(self, power_electronics_unit: PowerElectronicsUnit, table: TablePowerElectronicsUnit, rs: ResultSet) -> bool:
        power_electronics_unit.power_electronics_connection = self._ensure_get(
            rs.get_string(table.power_electronics_connection_mrid.query_index, None),
            PowerElectronicsConnection
        )
        if power_electronics_unit.power_electronics_connection is not None:
            power_electronics_unit.power_electronics_connection.add_unit(power_electronics_unit)

        power_electronics_unit.max_p = rs.get_int(table.max_p.query_index, None)
        power_electronics_unit.min_p = rs.get_int(table.min_p.query_index, None)

        return self._load_equipment(power_electronics_unit, table, rs)

    def load_power_electronics_wind_unit(self, table: TablePowerElectronicsWindUnit, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        power_electronics_wind_unit = PowerElectronicsWindUnit(mrid=set_last_mrid(rs.get_string(table.mrid.query_index)))

        return self._load_power_electronics_unit(power_electronics_wind_unit, table, rs) and self._add_or_throw(power_electronics_wind_unit)

    # ************ IEC61970 BASE WIRES ************

    def load_ac_line_segment(self, table: TableAcLineSegments, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        ac_line_segment = AcLineSegment(mrid=set_last_mrid(rs.get_string(table.mrid.query_index)))

        ac_line_segment.per_length_sequence_impedance = self._ensure_get(
            rs.get_string(table.per_length_sequence_impedance_mrid.query_index, None),
            PerLengthSequenceImpedance
        )

        return self._load_conductor(ac_line_segment, table, rs) and self._add_or_throw(ac_line_segment)

    def load_breaker(self, table: TableBreakers, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        breaker = Breaker(mrid=set_last_mrid(rs.get_string(table.mrid.query_index)))

        return self._load_protected_switch(breaker, table, rs) and self._add_or_throw(breaker)

    def load_load_break_switch(self, table: TableLoadBreakSwitches, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        load_break_switch = LoadBreakSwitch(mrid=set_last_mrid(rs.get_string(table.mrid.query_index)))

        return self._load_protected_switch(load_break_switch, table, rs) and self._add_or_throw(load_break_switch)

    def load_busbar_section(self, table: TableBusbarSections, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        busbar_section = BusbarSection(mrid=set_last_mrid(rs.get_string(table.mrid.query_index)))

        return self._load_connector(busbar_section, table, rs) and self._add_or_throw(busbar_section)

    def _load_conductor(self, conductor: Conductor, table: TableConductors, rs: ResultSet) -> bool:
        conductor.length = rs.get_double(table.length.query_index, None)
        conductor.asset_info = self._ensure_get(rs.get_string(table.wire_info_mrid.query_index, None), WireInfo)

        return self._load_conducting_equipment(conductor, table, rs)

    def _load_connector(self, connector: Connector, table: TableConnectors, rs: ResultSet) -> bool:
        return self._load_conducting_equipment(connector, table, rs)

    def load_disconnector(self, table: TableDisconnectors, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        disconnector = Disconnector(mrid=set_last_mrid(rs.get_string(table.mrid.query_index)))

        return self._load_switch(disconnector, table, rs) and self._add_or_throw(disconnector)

    def _load_energy_connection(self, energy_connection: EnergyConnection, table: TableEnergyConnections, rs: ResultSet) -> bool:
        return self._load_conducting_equipment(energy_connection, table, rs)

    def load_energy_consumer(self, table: TableEnergyConsumers, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        energy_consumer = EnergyConsumer(mrid=set_last_mrid(rs.get_string(table.mrid.query_index)))

        energy_consumer.customer_count = rs.get_int(table.customer_count.query_index, None)
        energy_consumer.grounded = rs.get_boolean(table.grounded.query_index)
        energy_consumer.p = rs.get_double(table.p.query_index, None)
        energy_consumer.q = rs.get_double(table.q.query_index, None)
        energy_consumer.p_fixed = rs.get_double(table.p_fixed.query_index, None)
        energy_consumer.q_fixed = rs.get_double(table.q_fixed.query_index, None)
        energy_consumer.phase_connection = PhaseShuntConnectionKind[rs.get_string(table.phase_connection.query_index)]

        return self._load_energy_connection(energy_consumer, table, rs) and self._add_or_throw(energy_consumer)

    def load_energy_consumer_phase(self, table: TableEnergyConsumerPhases, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        energy_consumer_phase = EnergyConsumerPhase(mrid=set_last_mrid(rs.get_string(table.mrid.query_index)))

        energy_consumer_phase.energy_consumer = self._ensure_get(rs.get_string(table.energy_consumer_mrid.query_index, None), EnergyConsumer)
        if energy_consumer_phase.energy_consumer is not None:
            energy_consumer_phase.energy_consumer.add_phase(energy_consumer_phase)

        energy_consumer_phase.phase = SinglePhaseKind[rs.get_string(table.phase.query_index)]
        energy_consumer_phase.p = rs.get_double(table.p.query_index, None)
        energy_consumer_phase.q = rs.get_double(table.q.query_index, None)
        energy_consumer_phase.p_fixed = rs.get_double(table.p_fixed.query_index, None)
        energy_consumer_phase.q_fixed = rs.get_double(table.q_fixed.query_index, None)

        return self._load_power_system_resource(energy_consumer_phase, table, rs) and self._add_or_throw(energy_consumer_phase)

    def load_energy_source(self, table: TableEnergySources, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        energy_source = EnergySource(mrid=set_last_mrid(rs.get_string(table.mrid.query_index)))

        energy_source.active_power = rs.get_double(table.active_power.query_index, None)
        energy_source.reactive_power = rs.get_double(table.reactive_power.query_index, None)
        energy_source.voltage_angle = rs.get_double(table.voltage_angle.query_index, None)
        energy_source.voltage_magnitude = rs.get_double(table.voltage_magnitude.query_index, None)
        energy_source.p_max = rs.get_double(table.p_max.query_index, None)
        energy_source.p_min = rs.get_double(table.p_min.query_index, None)
        energy_source.r = rs.get_double(table.r.query_index, None)
        energy_source.r0 = rs.get_double(table.r0.query_index, None)
        energy_source.rn = rs.get_double(table.rn.query_index, None)
        energy_source.x = rs.get_double(table.x.query_index, None)
        energy_source.x0 = rs.get_double(table.x0.query_index, None)
        energy_source.xn = rs.get_double(table.xn.query_index, None)
        energy_source.is_external_grid = rs.get_boolean(table.is_external_grid.query_index)
        energy_source.r_min = rs.get_double(table.r_min.query_index, None)
        energy_source.rn_min = rs.get_double(table.rn_min.query_index, None)
        energy_source.r0_min = rs.get_double(table.r0_min.query_index, None)
        energy_source.x_min = rs.get_double(table.x_min.query_index, None)
        energy_source.xn_min = rs.get_double(table.xn_min.query_index, None)
        energy_source.x0_min = rs.get_double(table.x0_min.query_index, None)
        energy_source.r_max = rs.get_double(table.r_max.query_index, None)
        energy_source.rn_max = rs.get_double(table.rn_max.query_index, None)
        energy_source.r0_max = rs.get_double(table.r0_max.query_index, None)
        energy_source.x_max = rs.get_double(table.x_max.query_index, None)
        energy_source.xn_max = rs.get_double(table.xn_max.query_index, None)
        energy_source.x0_max = rs.get_double(table.x0_max.query_index, None)

        return self._load_energy_connection(energy_source, table, rs) and self._add_or_throw(energy_source)

    def load_energy_source_phase(self, table: TableEnergySourcePhases, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        energy_source_phase = EnergySourcePhase(mrid=set_last_mrid(rs.get_string(table.mrid.query_index)))

        energy_source_phase.energy_source = self._ensure_get(rs.get_string(table.energy_source_mrid.query_index, None), EnergySource)
        if energy_source_phase.energy_source is not None:
            energy_source_phase.energy_source.add_phase(energy_source_phase)

        energy_source_phase.phase = SinglePhaseKind[rs.get_string(table.phase.query_index)]

        return self._load_power_system_resource(energy_source_phase, table, rs) and self._add_or_throw(energy_source_phase)

    def load_fuse(self, table: TableFuses, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        fuse = Fuse(mrid=set_last_mrid(rs.get_string(table.mrid.query_index)))

        return self._load_switch(fuse, table, rs) and self._add_or_throw(fuse)

    def load_jumper(self, table: TableJumpers, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        jumper = Jumper(mrid=set_last_mrid(rs.get_string(table.mrid.query_index)))

        return self._load_switch(jumper, table, rs) and self._add_or_throw(jumper)

    def load_junction(self, table: TableJunctions, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        junction = Junction(mrid=set_last_mrid(rs.get_string(table.mrid.query_index)))

        return self._load_connector(junction, table, rs) and self._add_or_throw(junction)

    def _load_line(self, line: Line, table: TableLines, rs: ResultSet) -> bool:
        return self._load_equipment_container(line, table, rs)

    def load_linear_shunt_compensator(self, table: TableLinearShuntCompensators, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        linear_shunt_compensator = LinearShuntCompensator(mrid=set_last_mrid(rs.get_string(table.mrid.query_index)))

        linear_shunt_compensator.b0_per_section = rs.get_double(table.b0_per_section.query_index, None)
        linear_shunt_compensator.b_per_section = rs.get_double(table.b_per_section.query_index, None)
        linear_shunt_compensator.g0_per_section = rs.get_double(table.g0_per_section.query_index, None)
        linear_shunt_compensator.g_per_section = rs.get_double(table.g_per_section.query_index, None)

        return self._load_shunt_compensator(linear_shunt_compensator, table, rs) and self._add_or_throw(linear_shunt_compensator)

    def _load_per_length_impedance(self, per_length_impedance: PerLengthImpedance, table: TablePerLengthImpedances, rs: ResultSet) -> bool:
        return self._load_per_length_line_parameter(per_length_impedance, table, rs)

    def _load_per_length_line_parameter(self, per_length_line_parameter: PerLengthLineParameter, table: TablePerLengthLineParameters, rs: ResultSet) -> bool:
        return self._load_identified_object(per_length_line_parameter, table, rs)

    def load_per_length_sequence_impedance(self, table: TablePerLengthSequenceImpedances, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        per_length_sequence_impedance = PerLengthSequenceImpedance(mrid=set_last_mrid(rs.get_string(table.mrid.query_index)))

        per_length_sequence_impedance.r = rs.get_double(table.r.query_index, None)
        per_length_sequence_impedance.x = rs.get_double(table.x.query_index, None)
        per_length_sequence_impedance.r0 = rs.get_double(table.r0.query_index, None)
        per_length_sequence_impedance.x0 = rs.get_double(table.x0.query_index, None)
        per_length_sequence_impedance.bch = rs.get_double(table.bch.query_index, None)
        per_length_sequence_impedance.gch = rs.get_double(table.gch.query_index, None)
        per_length_sequence_impedance.b0ch = rs.get_double(table.b0ch.query_index, None)
        per_length_sequence_impedance.g0ch = rs.get_double(table.g0ch.query_index, None)

        return self._load_per_length_impedance(per_length_sequence_impedance, table, rs) and self._add_or_throw(per_length_sequence_impedance)

    def load_power_electronics_connection(self, table: TablePowerElectronicsConnection, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        power_electronics_connection = PowerElectronicsConnection(mrid=set_last_mrid(rs.get_string(table.mrid.query_index)))

        power_electronics_connection.max_i_fault = rs.get_int(table.max_i_fault.query_index, None)
        power_electronics_connection.max_q = rs.get_double(table.max_q.query_index, None)
        power_electronics_connection.min_q = rs.get_double(table.min_q.query_index, None)
        power_electronics_connection.p = rs.get_double(table.p.query_index, None)
        power_electronics_connection.q = rs.get_double(table.q.query_index, None)
        power_electronics_connection.rated_s = rs.get_int(table.rated_s.query_index, None)
        power_electronics_connection.rated_u = rs.get_int(table.rated_u.query_index, None)

        return self._load_regulating_cond_eq(power_electronics_connection, table, rs) and self._add_or_throw(power_electronics_connection)

    def load_power_electronics_connection_phase(self, table: TablePowerElectronicsConnectionPhases, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        power_electronics_connection_phase = PowerElectronicsConnectionPhase(mrid=set_last_mrid(rs.get_string(table.mrid.query_index)))
        power_electronics_connection_phase.power_electronics_connection = self._ensure_get(
            rs.get_string(table.power_electronics_connection_mrid.query_index, None),
            PowerElectronicsConnection
        )
        if power_electronics_connection_phase.power_electronics_connection is not None:
            power_electronics_connection_phase.power_electronics_connection.add_phase(power_electronics_connection_phase)

        power_electronics_connection_phase.phase = SinglePhaseKind[rs.get_string(table.phase.query_index)]
        power_electronics_connection_phase.p = rs.get_double(table.p.query_index, None)
        power_electronics_connection_phase.phase = SinglePhaseKind[rs.get_string(table.phase.query_index)]
        power_electronics_connection_phase.q = rs.get_double(table.q.query_index, None)

        return self._load_power_system_resource(power_electronics_connection_phase, table, rs) and self._add_or_throw(power_electronics_connection_phase)

    def load_power_transformer(self, table: TablePowerTransformers, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        power_transformer = PowerTransformer(mrid=set_last_mrid(rs.get_string(table.mrid.query_index)))

        power_transformer.vector_group = VectorGroup[rs.get_string(table.vector_group.query_index)]
        power_transformer.transformer_utilisation = rs.get_double(table.transformer_utilisation.query_index, None)
        power_transformer.construction_kind = TransformerConstructionKind[rs.get_string(table.construction_kind.query_index)]
        power_transformer.function = TransformerFunctionKind[rs.get_string(table.function.query_index)]
        power_transformer.asset_info = self._ensure_get(rs.get_string(table.power_transformer_info_mrid.query_index, None), PowerTransformerInfo)

        return self._load_conducting_equipment(power_transformer, table, rs) and self._add_or_throw(power_transformer)

    def load_power_transformer_end(self, table: TablePowerTransformerEnds, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        power_transformer_end = PowerTransformerEnd(mrid=set_last_mrid(rs.get_string(table.mrid.query_index)))

        power_transformer_end.end_number = rs.get_int(table.end_number.query_index)
        power_transformer_end.power_transformer = self._ensure_get(rs.get_string(table.power_transformer_mrid.query_index, None), PowerTransformer)
        if power_transformer_end.power_transformer is not None:
            power_transformer_end.power_transformer.add_end(power_transformer_end)

        power_transformer_end.connection_kind = WindingConnection[rs.get_string(table.connection_kind.query_index)]
        power_transformer_end.phase_angle_clock = rs.get_int(table.phase_angle_clock.query_index, None)
        power_transformer_end.b = rs.get_double(table.b.query_index, None)
        power_transformer_end.b0 = rs.get_double(table.b0.query_index, None)
        power_transformer_end.g = rs.get_double(table.g.query_index, None)
        power_transformer_end.g0 = rs.get_double(table.g0.query_index, None)
        power_transformer_end.r = rs.get_double(table.r.query_index, None)
        power_transformer_end.r0 = rs.get_double(table.r0.query_index, None)
        power_transformer_end.rated_s = rs.get_int(table.rated_s.query_index, None)
        power_transformer_end.rated_u = rs.get_int(table.rated_u.query_index, None)
        power_transformer_end.x = rs.get_double(table.x.query_index, None)
        power_transformer_end.x0 = rs.get_double(table.x0.query_index, None)

        return self._load_transformer_end(power_transformer_end, table, rs) and self._add_or_throw(power_transformer_end)

    def _load_protected_switch(self, protected_switch: ProtectedSwitch, table: TableProtectedSwitches, rs: ResultSet) -> bool:
        return self._load_switch(protected_switch, table, rs)

    def load_ratio_tap_changer(self, table: TableRatioTapChangers, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        ratio_tap_changer = RatioTapChanger(mrid=set_last_mrid(rs.get_string(table.mrid.query_index)))

        ratio_tap_changer.transformer_end = self._ensure_get(rs.get_string(table.transformer_end_mrid.query_index, None), TransformerEnd)
        if ratio_tap_changer.transformer_end is not None:
            ratio_tap_changer.transformer_end.ratio_tap_changer = ratio_tap_changer

        ratio_tap_changer.step_voltage_increment = rs.get_double(table.step_voltage_increment.query_index, None)

        return self._load_tap_changer(ratio_tap_changer, table, rs) and self._add_or_throw(ratio_tap_changer)

    def load_recloser(self, table: TableReclosers, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        recloser = Recloser(mrid=set_last_mrid(rs.get_string(table.mrid.query_index)))

        return self._load_protected_switch(recloser, table, rs) and self._add_or_throw(recloser)

    def _load_regulating_cond_eq(self, regulating_cond_eq: RegulatingCondEq, table: TableRegulatingCondEq, rs: ResultSet) -> bool:
        regulating_cond_eq.control_enabled = rs.get_boolean(table.control_enabled.query_index)

        return self._load_energy_connection(regulating_cond_eq, table, rs)

    def _load_shunt_compensator(self, shunt_compensator: ShuntCompensator, table: TableShuntCompensators, rs: ResultSet) -> bool:
        shunt_compensator.asset_info = self._ensure_get(rs.get_string(table.shunt_compensator_info_mrid.query_index, None), ShuntCompensatorInfo)

        shunt_compensator.grounded = rs.get_boolean(table.grounded.query_index)
        shunt_compensator.nom_u = rs.get_int(table.nom_u.query_index, None)
        shunt_compensator.phase_connection = PhaseShuntConnectionKind[rs.get_string(table.phase_connection.query_index)]
        shunt_compensator.sections = rs.get_double(table.sections.query_index, None)

        return self._load_regulating_cond_eq(shunt_compensator, table, rs)

    def _load_switch(self, switch: Switch, table: TableSwitches, rs: ResultSet) -> bool:
        switch.set_normally_open(bool(rs.get_int(table.normal_open.query_index)))
        switch.set_open(bool(rs.get_int(table.open.query_index)))

        return self._load_conducting_equipment(switch, table, rs)

    def _load_tap_changer(self, tap_changer: TapChanger, table: TableTapChangers, rs: ResultSet) -> bool:
        tap_changer.control_enabled = rs.get_boolean(table.control_enabled.query_index)
        tap_changer.high_step = rs.get_int(table.high_step.query_index, None)
        tap_changer.low_step = rs.get_int(table.low_step.query_index, None)
        tap_changer.neutral_step = rs.get_int(table.neutral_step.query_index, None)
        tap_changer.neutral_u = rs.get_int(table.neutral_u.query_index, None)
        tap_changer.normal_step = rs.get_int(table.normal_step.query_index, None)
        tap_changer.step = rs.get_double(table.step.query_index, None)

        return self._load_power_system_resource(tap_changer, table, rs)

    def _load_transformer_end(self, transformer_end: TransformerEnd, table: TableTransformerEnds, rs: ResultSet) -> bool:
        transformer_end.terminal = self._ensure_get(rs.get_string(table.terminal_mrid.query_index, None), Terminal)
        transformer_end.base_voltage = self._ensure_get(rs.get_string(table.base_voltage_mrid.query_index, None), BaseVoltage)
        transformer_end.grounded = rs.get_boolean(table.grounded.query_index)
        transformer_end.r_ground = rs.get_double(table.r_ground.query_index, None)
        transformer_end.x_ground = rs.get_double(table.x_ground.query_index, None)
        transformer_end.star_impedance = self._ensure_get(rs.get_string(table.star_impedance_mrid.query_index, None), TransformerStarImpedance)

        return self._load_identified_object(transformer_end, table, rs)

    def load_transformer_star_impedance(self, table: TableTransformerStarImpedance, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        transformer_star_impedance = TransformerStarImpedance(mrid=set_last_mrid(rs.get_string(table.mrid.query_index)))

        transformer_star_impedance.r = rs.get_double(table.r.query_index, None)
        transformer_star_impedance.r0 = rs.get_double(table.r0.query_index, None)
        transformer_star_impedance.x = rs.get_double(table.x.query_index, None)
        transformer_star_impedance.x0 = rs.get_double(table.x0.query_index, None)

        transformer_star_impedance.transformer_end_info = self._ensure_get(rs.get_string(table.transformer_end_info_mrid.query_index, None), TransformerEndInfo)
        if transformer_star_impedance.transformer_end_info is not None:
            transformer_star_impedance.transformer_end_info.transformer_star_impedance = transformer_star_impedance

        return self._load_identified_object(transformer_star_impedance, table, rs) and self._add_or_throw(transformer_star_impedance)

    # ************ IEC61970 InfIEC61970 ************

    def load_circuit(self, table: TableCircuits, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        circuit = Circuit(mrid=set_last_mrid(rs.get_string(table.mrid.query_index)))

        circuit.loop = self._ensure_get(rs.get_string(table.loop_mrid.query_index, None), Loop)
        if circuit.loop is not None:
            circuit.loop.add_circuit(circuit)

        return self._load_line(circuit, table, rs) and self._add_or_throw(circuit)

    def load_loop(self, table: TableLoops, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        loop = Loop(mrid=set_last_mrid(rs.get_string(table.mrid.query_index)))

        return self._load_identified_object(loop, table, rs) and self._add_or_throw(loop)

    def load_lv_feeder(self, table: TableLvFeeders, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        lv_feeder = LvFeeder(mrid=set_last_mrid(rs.get_string(table.mrid.query_index)))

        lv_feeder.normal_head_terminal = self._ensure_get(rs.get_string(table.normal_head_terminal_mrid.query_index, None), Terminal)

        return self._load_equipment_container(lv_feeder, table, rs) and self._add_or_throw(lv_feeder)

    # ************ ASSOCIATIONS ************

    def load_asset_organisation_role_asset(self, table: TableAssetOrganisationRolesAssets, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        asset_organisation_role_mrid = set_last_mrid(rs.get_string(table.asset_organisation_role_mrid.query_index))
        set_last_mrid(f"{asset_organisation_role_mrid}-to-UNKNOWN")

        asset_mrid = rs.get_string(table.asset_mrid.query_index)
        set_last_mrid(f"{asset_organisation_role_mrid}-to-{asset_mrid}")

        asset_organisation_role = self._base_service.get(asset_organisation_role_mrid, AssetOrganisationRole)
        asset = self._base_service.get(asset_mrid, Asset)

        asset.add_organisation_role(asset_organisation_role)

        return True

    def load_equipment_equipment_container(self, table: TableEquipmentEquipmentContainers, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        equipment_mrid = set_last_mrid(rs.get_string(table.equipment_mrid.query_index))
        set_last_mrid(f"{equipment_mrid}-to-UNKNOWN")

        equipment_container_mrid = rs.get_string(table.equipment_container_mrid.query_index)
        set_last_mrid(f"{equipment_mrid}-to-{equipment_container_mrid}")

        equipment = self._base_service.get(equipment_mrid, Equipment)
        equipment_container = self._base_service.get(equipment_container_mrid, EquipmentContainer)

        equipment_container.add_equipment(equipment)
        equipment.add_container(equipment_container)

        return True

    def load_equipment_operational_restriction(self, table: TableEquipmentOperationalRestrictions, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        equipment_mrid = set_last_mrid(rs.get_string(table.equipment_mrid.query_index))
        set_last_mrid(f"{equipment_mrid}-to-UNKNOWN")

        operational_restriction_mrid = rs.get_string(table.operational_restriction_mrid.query_index)
        set_last_mrid(f"{equipment_mrid}-to-{operational_restriction_mrid}")

        equipment = self._base_service.get(equipment_mrid, Equipment)
        operational_restriction = self._base_service.get(operational_restriction_mrid, OperationalRestriction)

        operational_restriction.add_equipment(equipment)
        equipment.add_operational_restriction(operational_restriction)

        return True

    def load_equipment_usage_point(self, table: TableEquipmentUsagePoints, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        equipment_mrid = set_last_mrid(rs.get_string(table.equipment_mrid.query_index))
        set_last_mrid(f"{equipment_mrid}-to-UNKNOWN")

        usage_point_mrid = rs.get_string(table.usage_point_mrid.query_index)
        set_last_mrid(f"{equipment_mrid}-to-{usage_point_mrid}")

        equipment = self._base_service.get(equipment_mrid, Equipment)
        usage_point = self._base_service.get(usage_point_mrid, UsagePoint)

        usage_point.add_equipment(equipment)
        equipment.add_usage_point(usage_point)

        return True

    def load_usage_point_end_device(self, table: TableUsagePointsEndDevices, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        usage_point_mrid = set_last_mrid(rs.get_string(table.usage_point_mrid.query_index))
        set_last_mrid(f"{usage_point_mrid}-to-UNKNOWN")

        end_device_mrid = rs.get_string(table.end_device_mrid.query_index)
        set_last_mrid(f"{usage_point_mrid}-to-{end_device_mrid}")

        usage_point = self._base_service.get(usage_point_mrid, UsagePoint)
        end_device = self._base_service.get(end_device_mrid, EndDevice)

        end_device.add_usage_point(usage_point)
        usage_point.add_end_device(end_device)

        return True

    def load_circuit_substation(self, table: TableCircuitsSubstations, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        circuit_mrid = set_last_mrid(rs.get_string(table.circuit_mrid.query_index))
        set_last_mrid(f"{circuit_mrid}-to-UNKNOWN")

        substation_mrid = rs.get_string(table.substation_mrid.query_index)
        set_last_mrid(f"{circuit_mrid}-to-{substation_mrid}")

        circuit = self._base_service.get(circuit_mrid, Circuit)
        substation = self._base_service.get(substation_mrid, Substation)

        substation.add_circuit(circuit)
        circuit.add_end_substation(substation)

        return True

    def load_circuit_terminal(self, table: TableCircuitsTerminals, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        circuit_mrid = set_last_mrid(rs.get_string(table.circuit_mrid.query_index))
        set_last_mrid(f"{circuit_mrid}-to-UNKNOWN")

        terminal_mrid = rs.get_string(table.terminal_mrid.query_index)
        set_last_mrid(f"{circuit_mrid}-to-{terminal_mrid}")

        circuit = self._base_service.get(circuit_mrid, Circuit)
        terminal = self._base_service.get(terminal_mrid, Terminal)

        circuit.add_end_terminal(terminal)

        return True

    def load_loop_substation(self, table: TableLoopsSubstations, rs: ResultSet, set_last_mrid: Callable[[str], str]) -> bool:
        asset_organisation_role_mrid = set_last_mrid(rs.get_string(table.loop_mrid.query_index))
        set_last_mrid(f"{asset_organisation_role_mrid}-to-UNKNOWN")

        asset_mrid = rs.get_string(table.substation_mrid.query_index)
        set_last_mrid(f"{asset_organisation_role_mrid}-to-{asset_mrid}")

        loop = self._base_service.get(asset_organisation_role_mrid, Loop)
        substation = self._base_service.get(asset_mrid, Substation)

        relationship = LoopSubstationRelationship[rs.get_string(table.relationship.query_index)]
        if relationship == LoopSubstationRelationship.LOOP_ENERGIZES_SUBSTATION:
            substation.add_loop(loop)
            loop.add_substation(substation)
        elif relationship == LoopSubstationRelationship.SUBSTATION_ENERGIZES_LOOP:
            substation.add_energized_loop(loop)
            loop.add_energizing_substation(substation)

        return True
