#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from zepben.evolve import AcLineSegment, Asset, AuxiliaryEquipment, ConductingEquipment, Conductor, PowerTransformer, Pole, Streetlight, ConnectivityNode, \
    Control, Customer, CustomerAgreement, Diagram, DiagramObject, EndDevice, Equipment, EquipmentContainer, EnergyConsumer, EnergyConsumerPhase, EnergySource, \
    EnergySourcePhase, Feeder, GeographicalRegion, Measurement, OperationalRestriction, OrganisationRole, PowerSystemResource, PowerTransformerEnd, \
    PricingStructure, RatioTapChanger, RemoteControl, RemoteSource, SubGeographicalRegion, Substation, Terminal, TransformerEnd, UsagePoint, Circuit, Loop, \
    PowerElectronicsUnit, PowerElectronicsConnectionPhase, PowerElectronicsConnection, TransformerTankInfo, TransformerEndInfo, PowerTransformerInfo, \
    TransformerStarImpedance, ShuntCompensator, LvFeeder, PotentialTransformer, CurrentTransformer
from zepben.evolve.services.common.reference_resolvers import *

__all__ = ["per_length_sequence_impedance", "organisation_roles", "at_location", "ae_terminal", "ce_base_voltage", "ce_terminals",
           "asset_info", "streetlights", "pole", "cn_terminals", "remote_control", "agreements", "customer",
           "pricing_structures", "power_transformer_info",
           "diagram_objects", "diagram", "service_location", "ed_usage_points", "containers", "current_containers",
           "operational_restrictions",
           "eq_usage_points", "ec_equipment", "ec_phases", "energy_consumer", "es_phases", "energy_source",
           "normal_energizing_substation", "normal_head_terminal", "sub_geographical_regions", "remote_source",
           "or_equipment", "organisation",
           "psr_location", "ends", "power_transformer", "tariffs", "transformer_end", "control", "measurement",
           "geographical_region", "substations",
           "normal_energized_feeders", "sub_geographical_region", "conducting_equipment", "connectivity_node",
           "te_base_voltage", "ratio_tap_changer",
           "te_terminal", "end_devices", "up_equipment", "usage_point_location", "shunt_compensator_info",
           "transformer_end_info", "power_transformer_info_transformer_tank_info", "transformer_star_impedance",
           "star_impedance_transformer_end_info", "transformer_end_transformer_star_impedance", "normal_energized_lv_feeders",
           "normal_energizing_feeders", "lv_feeder_normal_head_terminal", "normal_energizing_feeders"]


def per_length_sequence_impedance(ac_line_segment: AcLineSegment):
    # noinspection PyArgumentList
    return BoundReferenceResolver(ac_line_segment, acls_to_plsi_resolver, None)


def organisation_roles(asset: Asset) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(asset, asset_to_asset_org_role_resolver, None)


def at_location(asset: Asset) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(asset, asset_to_location_resolver, None)


def ae_terminal(auxiliary_equipment: AuxiliaryEquipment) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(auxiliary_equipment, aux_equip_to_term_resolver, None)


def ce_base_voltage(ce: ConductingEquipment) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(ce, cond_equip_to_bv_resolver, None)


def ce_terminals(ce: ConductingEquipment) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(ce, cond_equip_to_terminal_resolver, term_to_ce_resolver)


def asset_info(conductor: Conductor) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(conductor, conductor_to_wire_info_resolver, None)


def power_transformer_info(pt: PowerTransformer) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(pt, powertransformer_to_power_transformer_info_resolver, None)


def shunt_compensator_info(sc: ShuntCompensator) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(sc, shunt_compensator_to_shunt_compensator_info_resolver, None)


def streetlights(p: Pole) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(p, pole_to_streetlight_resolver, streetlight_to_pole_resolver)


def pole(streetlight: Streetlight) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(streetlight, streetlight_to_pole_resolver, pole_to_streetlight_resolver)


def cn_terminals(cn: ConnectivityNode) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(cn, conn_node_to_term_resolver, term_to_cn_resolver)


def remote_control(c: Control) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(c, control_to_remote_control_resolver, rc_to_cont_resolver)


def agreements(c: Customer) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(c, cust_to_custagr_resolver, custagr_to_cust_resolver)


def customer(customer_agreement: CustomerAgreement) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(customer_agreement, custagr_to_cust_resolver, cust_to_custagr_resolver)


def pricing_structures(customer_agreement: CustomerAgreement) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(customer_agreement, custagr_to_ps_resolver, None)


def diagram_objects(d: Diagram) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(d, diag_to_diagobj_resolver, diagobj_to_diag_resolver)


def diagram(diagram_object: DiagramObject) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(diagram_object, diagobj_to_diag_resolver, diag_to_diagobj_resolver)


def service_location(end_device: EndDevice) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(end_device, ed_to_loc_resolver, None)


def ed_usage_points(end_device: EndDevice) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(end_device, ed_to_up_resolver, up_to_ed_resolver)


def containers(equipment: Equipment) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(equipment, eq_to_ec_resolver, ec_to_eq_resolver)


def current_containers(equipment: Equipment) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(equipment, eq_to_curcontainer_resolver, ec_to_curequipment_resolver)


def operational_restrictions(equipment: Equipment) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(equipment, eq_to_or_resolver, or_to_eq_resolver)


def eq_usage_points(equipment: Equipment) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(equipment, eq_to_up_resolver, up_to_eq_resolver)


def ec_equipment(equipment_container: EquipmentContainer) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(equipment_container, ec_to_eq_resolver, eq_to_ec_resolver)


def ec_phases(ec: EnergyConsumer) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(ec, ec_to_ecp_resolver, ecp_to_ec_resolver)


def energy_consumer(energy_consumer_phase: EnergyConsumerPhase) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(energy_consumer_phase, ecp_to_ec_resolver, ec_to_ecp_resolver)


def es_phases(es: EnergySource) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(es, es_to_esp_resolver, esp_to_es_resolver)


def energy_source(energy_source_phase: EnergySourcePhase) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(energy_source_phase, esp_to_es_resolver, es_to_esp_resolver)


def normal_energizing_substation(feeder: Feeder) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(feeder, feeder_to_nes_resolver, sub_to_feeder_resolver)


def normal_head_terminal(feeder: Feeder) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(feeder, feeder_to_nht_resolver, None)


def normal_energized_lv_feeders(feeder: Feeder) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(feeder, feeder_to_nelvf_resolver, lvfeeder_to_nef_resolver)


def sub_geographical_regions(gr: GeographicalRegion) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(gr, gr_to_sgr_resolver, sgr_to_gr_resolver)


def remote_source(m: Measurement) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(m, meas_to_rs_resolver, rs_to_meas_resolver)


def or_equipment(operational_restriction: OperationalRestriction) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(operational_restriction, or_to_eq_resolver, eq_to_or_resolver)


def organisation(organisation_role: OrganisationRole) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(organisation_role, orgr_to_org_resolver, None)


def psr_location(power_system_resource: PowerSystemResource) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(power_system_resource, psr_to_loc_resolver, None)


def ends(pt: PowerTransformer) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(pt, pt_to_pte_resolver, pte_to_pt_resolver)


def power_transformer(power_transformer_end: PowerTransformerEnd) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(power_transformer_end, pte_to_pt_resolver, pt_to_pte_resolver)


def tariffs(pricing_structure: PricingStructure) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(pricing_structure, ps_to_tariff_resolver, None)


def transformer_end(rtt: RatioTapChanger) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(rtt, rtc_to_te_resolver, te_to_rtc_resolver)


def control(rc: RemoteControl) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(rc, rc_to_cont_resolver, control_to_remote_control_resolver)


def measurement(rs: RemoteSource) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(rs, rs_to_meas_resolver, meas_to_rs_resolver)


def geographical_region(sgr: SubGeographicalRegion) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(sgr, sgr_to_gr_resolver, gr_to_sgr_resolver)


def substations(sgr: SubGeographicalRegion) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(sgr, sgr_to_sub_resolver, sub_to_sgr_resolver)


def normal_energized_feeders(substation: Substation) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(substation, sub_to_feeder_resolver, feeder_to_nes_resolver)


def sub_geographical_region(substation: Substation) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(substation, sub_to_sgr_resolver, sgr_to_sub_resolver)


def circuits(substation: Substation) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(substation, sub_to_circuit_resolver, circuit_to_sub_resolver)


def normal_energized_loops(substation: Substation) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(substation, sub_to_eloop_resolver, loop_to_esub_resolver)


def loops(substation: Substation) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(substation, sub_to_loop_resolver, loop_to_sub_resolver)


def conducting_equipment(terminal: Terminal) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(terminal, term_to_ce_resolver, cond_equip_to_terminal_resolver)


def connectivity_node(terminal: Terminal) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(terminal, term_to_cn_resolver, conn_node_to_term_resolver)


def te_base_voltage(te: TransformerEnd) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(te, te_to_bv_resolver, None)


def ratio_tap_changer(te: TransformerEnd) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(te, te_to_rtc_resolver, rtc_to_te_resolver)


def te_terminal(te: TransformerEnd) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(te, te_to_term_resolver, None)


def end_devices(usage_point: UsagePoint) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(usage_point, up_to_ed_resolver, ed_to_up_resolver)


def up_equipment(usage_point: UsagePoint) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(usage_point, up_to_eq_resolver, eq_to_up_resolver)


def usage_point_location(usage_point: UsagePoint) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(usage_point, up_to_loc_resolver, None)


def loop(circuit: Circuit) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(circuit, circuit_to_loop_resolver, loop_to_circuit_resolver)


def end_terminal(circuit: Circuit) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(circuit, circuit_to_term_resolver, None)


def end_substation(circuit: Circuit) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(circuit, circuit_to_sub_resolver, sub_to_circuit_resolver)


def loop_circuits(l_: Loop) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(l_, loop_to_circuit_resolver, circuit_to_loop_resolver)


def loop_substations(l_: Loop) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(l_, loop_to_sub_resolver, sub_to_loop_resolver)


def loop_energizing_substations(l_: Loop) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(l_, loop_to_esub_resolver, sub_to_eloop_resolver)


def lv_feeder_normal_head_terminal(lv_feeder: LvFeeder) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(lv_feeder, lvfeeder_to_nht_resolver, None)


def normal_energizing_feeders(lv_feeder: LvFeeder) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(lv_feeder, lvfeeder_to_nef_resolver, feeder_to_nelvf_resolver)


def unit_power_electronics_connection(pec: PowerElectronicsUnit) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(pec, peu_to_pec_resolver, pec_to_peu_resolver)


def phase_power_electronics_connection(pec: PowerElectronicsConnectionPhase) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(pec, pecphase_to_pec_resolver, pec_to_pecphase_resolver)


def power_electronics_unit(pec: PowerElectronicsConnection) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(pec, pec_to_peu_resolver, peu_to_pec_resolver)


def power_electronics_connection_phase(pec: PowerElectronicsConnection) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(pec, pec_to_pecphase_resolver, pecphase_to_pec_resolver)


def transformer_end_info(tti: TransformerTankInfo) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(tti, tti_to_tei_resolver, tei_to_tti_resolver)


def transformer_tank_info(tei: TransformerEndInfo) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(tei, tei_to_tti_resolver, tti_to_tei_resolver)


def power_transformer_info_transformer_tank_info(pti: PowerTransformerInfo) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(pti, pti_to_tti_resolver, None)


def transformer_star_impedance(tei: TransformerEndInfo) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(tei, tei_to_tsi_resolver, tsi_to_tei_resolver)


def star_impedance_transformer_end_info(tsi: TransformerStarImpedance) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(tsi, tsi_to_tei_resolver, tei_to_tsi_resolver)


def transformer_end_transformer_star_impedance(te: TransformerEnd) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(te, te_to_tsi_resolver, None)


def energised_end_no_load_tests(tei: TransformerEndInfo) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(tei, tei_to_ee_nlt_resolver, None)


def energised_end_short_circuit_tests(tei: TransformerEndInfo) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(tei, tei_to_ee_sct_resolver, None)


def grounded_end_short_circuit_tests(tei: TransformerEndInfo) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(tei, tei_to_ge_sct_resolver, None)


def open_end_open_circuit_tests(tei: TransformerEndInfo) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(tei, tei_to_oe_oct_resolver, None)


def energised_end_open_circuit_tests(tei: TransformerEndInfo) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(tei, tei_to_ee_oct_resolver, None)


def current_transformer_info(current_transformer: CurrentTransformer) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(current_transformer, ct_to_cti_resolver, None)


def potential_transformer_info(potential_transformer: PotentialTransformer) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(potential_transformer, vt_to_vti_resolver, None)
