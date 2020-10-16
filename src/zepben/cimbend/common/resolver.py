#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.cimbend.cim.iec61968.common.organisation_role import OrganisationRole
from zepben.cimbend.cim.iec61968.assets.asset import Asset
from zepben.cimbend.cim.iec61968.assets.pole import Pole
from zepben.cimbend.cim.iec61968.assets.streetlight import Streetlight
from zepben.cimbend.cim.iec61968.customers.customer import Customer
from zepben.cimbend.cim.iec61968.customers.customer_agreement import CustomerAgreement
from zepben.cimbend.cim.iec61968.customers.pricing_structure import PricingStructure
from zepben.cimbend.cim.iec61968.metering.metering import EndDevice, UsagePoint
from zepben.cimbend.cim.iec61968.operations.operational_restriction import OperationalRestriction
from zepben.cimbend.cim.iec61970.base.auxiliaryequipment import AuxiliaryEquipment
from zepben.cimbend.cim.iec61970.base.core.conducting_equipment import ConductingEquipment
from zepben.cimbend.cim.iec61970.base.core.connectivity_node import ConnectivityNode
from zepben.cimbend.cim.iec61970.base.core.equipment import Equipment
from zepben.cimbend.cim.iec61970.base.core.equipment_container import *
from zepben.cimbend.cim.iec61970.base.core.power_system_resource import *
from zepben.cimbend.cim.iec61970.base.core.regions import *
from zepben.cimbend.cim.iec61970.base.core.substation import *
from zepben.cimbend.cim.iec61970.base.core.terminal import Terminal
from zepben.cimbend.cim.iec61970.base.diagramlayout.diagram_layout import Diagram, DiagramObject
from zepben.cimbend.cim.iec61970.base.meas.measurement import Measurement
from zepben.cimbend.cim.iec61970.base.meas.control import Control
from zepben.cimbend.cim.iec61970.base.scada.remote_source import RemoteSource
from zepben.cimbend.cim.iec61970.base.scada.remote_control import RemoteControl
from zepben.cimbend.cim.iec61970.base.wires.aclinesegment import Conductor
from zepben.cimbend.cim.iec61970.base.wires.energy_consumer import EnergyConsumer, EnergyConsumerPhase
from zepben.cimbend.cim.iec61970.base.wires.energy_source import EnergySource
from zepben.cimbend.cim.iec61970.base.wires.energy_source_phase import EnergySourcePhase
from zepben.cimbend.cim.iec61970.base.wires.power_transformer import *
from zepben.cimbend.cim.iec61970.infiec61970.feeder import Circuit, Loop
from zepben.cimbend.common.reference_resolvers import *

__all__ = ["per_length_sequence_impedance", "organisation_roles", "at_location", "ae_terminal", "ce_base_voltage", "ce_terminals",
           "asset_info", "streetlights", "pole", "cn_terminals", "remote_control", "agreements", "customer",
           "pricing_structures",
           "diagram_objects", "diagram", "service_location", "ed_usage_points", "containers", "current_feeders",
           "operational_restrictions",
           "eq_usage_points", "ec_equipment", "ec_phases", "energy_consumer", "es_phases", "energy_source", "current_equipment",
           "normal_energizing_substation", "normal_head_terminal", "sub_geographical_regions", "remote_source",
           "or_equipment", "organisation",
           "psr_location", "ends", "power_transformer", "tariffs", "transformer_end", "control", "measurement",
           "geographical_region", "substations",
           "normal_energizing_feeders", "sub_geographical_region", "conducting_equipment", "connectivity_node",
           "te_base_voltage", "ratio_tap_changer",
           "te_terminal", "end_devices", "up_equipment", "usage_point_location"]


def per_length_sequence_impedance(aclinesegment):
    return BoundReferenceResolver(aclinesegment, acls_to_plsi_resolver, None)


def organisation_roles(asset: Asset) -> BoundReferenceResolver:
    return BoundReferenceResolver(asset, asset_to_asset_org_role_resolver, None)


def at_location(asset: Asset) -> BoundReferenceResolver:
    return BoundReferenceResolver(asset, asset_to_location_resolver, None)


def ae_terminal(auxiliaryEquipment: AuxiliaryEquipment) -> BoundReferenceResolver:
    return BoundReferenceResolver(auxiliaryEquipment, aux_equip_to_term_resolver, None)


def ce_base_voltage(conducting_equipment: ConductingEquipment) -> BoundReferenceResolver:
    return BoundReferenceResolver(conducting_equipment, cond_equip_to_bv_resolver, None)


def ce_terminals(conducting_equipment: ConductingEquipment) -> BoundReferenceResolver:
    return BoundReferenceResolver(conducting_equipment, cond_equip_to_terminal_resolver, term_to_ce_resolver)


def asset_info(conductor: Conductor) -> BoundReferenceResolver:
    return BoundReferenceResolver(conductor, conductor_to_wire_info_resolver, None)


def streetlights(pole: Pole) -> BoundReferenceResolver:
    return BoundReferenceResolver(pole, pole_to_streetlight_resolver, streetlight_to_pole_resolver)


def pole(streetlight: Streetlight) -> BoundReferenceResolver:
    return BoundReferenceResolver(streetlight, streetlight_to_pole_resolver, pole_to_streetlight_resolver)


def cn_terminals(connectivity_node: ConnectivityNode) -> BoundReferenceResolver:
    return BoundReferenceResolver(connectivity_node, conn_node_to_term_resolver, term_to_cn_resolver)


def remote_control(control: Control) -> BoundReferenceResolver:
    return BoundReferenceResolver(control, control_to_remote_control_resolver, rc_to_cont_resolver)


def agreements(customer: Customer) -> BoundReferenceResolver:
    return BoundReferenceResolver(customer, cust_to_custagr_resolver, custagr_to_cust_resolver)


def customer(customer_agreement: CustomerAgreement) -> BoundReferenceResolver:
    return BoundReferenceResolver(customer_agreement, custagr_to_cust_resolver, cust_to_custagr_resolver)


def pricing_structures(customer_agreement: CustomerAgreement) -> BoundReferenceResolver:
    return BoundReferenceResolver(customer_agreement, custagr_to_ps_resolver, None)


def diagram_objects(diagram: Diagram) -> BoundReferenceResolver:
    return BoundReferenceResolver(diagram, diag_to_diagobj_resolver, diagobj_to_diag_resolver)


def diagram(diagram_object: DiagramObject) -> BoundReferenceResolver:
    return BoundReferenceResolver(diagram_object, diagobj_to_diag_resolver, diag_to_diagobj_resolver)


def service_location(end_device: EndDevice) -> BoundReferenceResolver:
    return BoundReferenceResolver(end_device, ed_to_loc_resolver, None)


def ed_usage_points(end_device: EndDevice) -> BoundReferenceResolver:
    return BoundReferenceResolver(end_device, ed_to_up_resolver, up_to_ed_resolver)


def containers(equipment: Equipment) -> BoundReferenceResolver:
    return BoundReferenceResolver(equipment, eq_to_ec_resolver, ec_to_eq_resolver)


def current_feeders(equipment: Equipment) -> BoundReferenceResolver:
    return BoundReferenceResolver(equipment, eq_to_curfeeder_resolver, curfeeder_to_eq_resolver)


def operational_restrictions(equipment: Equipment) -> BoundReferenceResolver:
    return BoundReferenceResolver(equipment, eq_to_or_resolver, or_to_eq_resolver)


def eq_usage_points(equipment: Equipment) -> BoundReferenceResolver:
    return BoundReferenceResolver(equipment, eq_to_up_resolver, up_to_eq_resolver)


def ec_equipment(equipment_container: EquipmentContainer) -> BoundReferenceResolver:
    return BoundReferenceResolver(equipment_container, ec_to_eq_resolver, eq_to_ec_resolver)


def ec_phases(energy_consumer: EnergyConsumer) -> BoundReferenceResolver:
    return BoundReferenceResolver(energy_consumer, ec_to_ecp_resolver, ecp_to_ec_resolver)


def energy_consumer(energy_consumer_phase: EnergyConsumerPhase) -> BoundReferenceResolver:
    return BoundReferenceResolver(energy_consumer_phase, ecp_to_ec_resolver, ec_to_ecp_resolver)


def es_phases(energy_source: EnergySource) -> BoundReferenceResolver:
    return BoundReferenceResolver(energy_source, es_to_esp_resolver, esp_to_es_resolver)


def energy_source(energy_source_phase: EnergySourcePhase) -> BoundReferenceResolver:
    return BoundReferenceResolver(energy_source_phase, esp_to_es_resolver, es_to_esp_resolver)


def current_equipment(feeder: Feeder) -> BoundReferenceResolver:
    return BoundReferenceResolver(feeder, curfeeder_to_eq_resolver, eq_to_curfeeder_resolver)


def normal_energizing_substation(feeder: Feeder) -> BoundReferenceResolver:
    return BoundReferenceResolver(feeder, feeder_to_nes_resolver, sub_to_feeder_resolver)


def normal_head_terminal(feeder: Feeder) -> BoundReferenceResolver:
    return BoundReferenceResolver(feeder, feeder_to_nht_resolver, None)


def sub_geographical_regions(geographical_region: GeographicalRegion) -> BoundReferenceResolver:
    return BoundReferenceResolver(geographical_region, gr_to_sgr_resolver, sgr_to_gr_resolver)


def remote_source(measurement: Measurement) -> BoundReferenceResolver:
    return BoundReferenceResolver(measurement, meas_to_rs_resolver, rs_to_meas_resolver)


def or_equipment(operational_restriction: OperationalRestriction) -> BoundReferenceResolver:
    return BoundReferenceResolver(operational_restriction, or_to_eq_resolver, eq_to_or_resolver)


def organisation(organisation_role: OrganisationRole) -> BoundReferenceResolver:
    return BoundReferenceResolver(organisation_role, orgr_to_org_resolver, None)


def psr_location(power_system_resource: PowerSystemResource) -> BoundReferenceResolver:
    return BoundReferenceResolver(power_system_resource, psr_to_loc_resolver, None)


def ends(power_transformer: PowerTransformer) -> BoundReferenceResolver:
    return BoundReferenceResolver(power_transformer, pt_to_pte_resolver, pte_to_pt_resolver)


def power_transformer(power_transformerEnd: PowerTransformerEnd) -> BoundReferenceResolver:
    return BoundReferenceResolver(power_transformerEnd, pte_to_pt_resolver, pt_to_pte_resolver)


def tariffs(pricing_structure: PricingStructure) -> BoundReferenceResolver:
    return BoundReferenceResolver(pricing_structure, ps_to_tariff_resolver, None)


def transformer_end(ratio_tap_changer: RatioTapChanger) -> BoundReferenceResolver:
    return BoundReferenceResolver(ratio_tap_changer, rtc_to_te_resolver, te_to_rtc_resolver)


def control(remote_control: RemoteControl) -> BoundReferenceResolver:
    return BoundReferenceResolver(remote_control, rc_to_cont_resolver, control_to_remote_control_resolver)


def measurement(remote_source: RemoteSource) -> BoundReferenceResolver:
    return BoundReferenceResolver(remote_source, rs_to_meas_resolver, meas_to_rs_resolver)


def geographical_region(sub_geographical_region: SubGeographicalRegion) -> BoundReferenceResolver:
    return BoundReferenceResolver(sub_geographical_region, sgr_to_gr_resolver, gr_to_sgr_resolver)


def substations(sub_geographical_region: SubGeographicalRegion) -> BoundReferenceResolver:
    return BoundReferenceResolver(sub_geographical_region, sgr_to_sub_resolver, sub_to_sgr_resolver)


def normal_energizing_feeders(substation: Substation) -> BoundReferenceResolver:
    return BoundReferenceResolver(substation, sub_to_feeder_resolver, feeder_to_nes_resolver)


def sub_geographical_region(substation: Substation) -> BoundReferenceResolver:
    return BoundReferenceResolver(substation, sub_to_sgr_resolver, sgr_to_sub_resolver)


def circuits(substation: Substation) -> BoundReferenceResolver:
    return BoundReferenceResolver(substation, sub_to_circuit_resolver, circuit_to_sub_resolver)


def normal_energized_loops(substation: Substation) -> BoundReferenceResolver:
    return BoundReferenceResolver(substation, sub_to_eloop_resolver, loop_to_esub_resolver)


def loops(substation: Substation) -> BoundReferenceResolver:
    return BoundReferenceResolver(substation, sub_to_loop_resolver, loop_to_sub_resolver)


def conducting_equipment(terminal: Terminal) -> BoundReferenceResolver:
    return BoundReferenceResolver(terminal, term_to_ce_resolver, cond_equip_to_terminal_resolver)


def connectivity_node(terminal: Terminal) -> BoundReferenceResolver:
    return BoundReferenceResolver(terminal, term_to_cn_resolver, conn_node_to_term_resolver)


def te_base_voltage(transformer_end: TransformerEnd) -> BoundReferenceResolver:
    return BoundReferenceResolver(transformer_end, te_to_bv_resolver, None)


def ratio_tap_changer(transformer_end: TransformerEnd) -> BoundReferenceResolver:
    return BoundReferenceResolver(transformer_end, te_to_rtc_resolver, rtc_to_te_resolver)


def te_terminal(transformer_end: TransformerEnd) -> BoundReferenceResolver:
    return BoundReferenceResolver(transformer_end, te_to_term_resolver, None)


def end_devices(usage_point: UsagePoint) -> BoundReferenceResolver:
    return BoundReferenceResolver(usage_point, up_to_ed_resolver, ed_to_up_resolver)


def up_equipment(usage_point: UsagePoint) -> BoundReferenceResolver:
    return BoundReferenceResolver(usage_point, up_to_eq_resolver, eq_to_up_resolver)


def usage_point_location(usage_point: UsagePoint) -> BoundReferenceResolver:
    return BoundReferenceResolver(usage_point, up_to_loc_resolver, None)


def loop(circuit: Circuit) -> BoundReferenceResolver:
    return BoundReferenceResolver(circuit, circuit_to_loop_resolver, loop_to_circuit_resolver)


def end_terminal(circuit: Circuit) -> BoundReferenceResolver:
    return BoundReferenceResolver(circuit, circuit_to_term_resolver, None)


def end_substation(circuit: Circuit) -> BoundReferenceResolver:
    return BoundReferenceResolver(circuit, circuit_to_sub_resolver, sub_to_circuit_resolver)


def loop_circuits(loop: Loop) -> BoundReferenceResolver:
    return BoundReferenceResolver(loop, loop_to_circuit_resolver, circuit_to_loop_resolver)


def loop_substations(loop: Loop) -> BoundReferenceResolver:
    return BoundReferenceResolver(loop, loop_to_sub_resolver, sub_to_loop_resolver)


def loop_energizing_substations(loop: Loop) -> BoundReferenceResolver:
    return BoundReferenceResolver(loop, loop_to_esub_resolver, sub_to_eloop_resolver)
