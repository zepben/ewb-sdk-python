#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from zepben.evolve import AcLineSegment, Asset, AuxiliaryEquipment, ConductingEquipment, Conductor, PowerTransformer, Pole, Streetlight, ConnectivityNode, \
    Control, Customer, CustomerAgreement, Diagram, DiagramObject, EndDevice, Equipment, EquipmentContainer, EnergyConsumer, EnergyConsumerPhase, EnergySource, \
    EnergySourcePhase, Feeder, GeographicalRegion, Measurement, OperationalRestriction, OrganisationRole, PowerSystemResource, PowerTransformerEnd, \
    PricingStructure, RatioTapChanger, RemoteControl, RemoteSource, SubGeographicalRegion, Substation, Terminal, TransformerEnd, UsagePoint, Circuit, Loop, \
    PowerElectronicsUnit, PowerElectronicsConnectionPhase, PowerElectronicsConnection, TransformerTankInfo, TransformerEndInfo, PowerTransformerInfo, \
    TransformerStarImpedance, ShuntCompensator, LvFeeder, PotentialTransformer, CurrentTransformer, ProtectedSwitch, Switch, RegulatingControl, \
    RegulatingCondEq, TapChanger, ProtectionRelayFunction, ProtectionRelayScheme, ProtectionRelaySystem, Sensor, Fuse, BatteryUnit, \
    SynchronousMachine
from zepben.evolve.model.cim.iec61970.base.wires.clamp import Clamp
from zepben.evolve.model.cim.iec61970.base.wires.cut import Cut
from zepben.evolve.services.common.reference_resolvers import *

__all__ = ["ae_terminal", "agreements", "at_location", "ce_base_voltage", "ce_terminals", "circuits", "cn_terminals", "conducting_equipment",
           "connectivity_node", "containers", "control", "current_containers", "current_transformer_info", "customer", "diagram", "diagram_objects",
           "ec_equipment", "ec_phases", "ed_usage_points", "end_devices", "end_substation", "end_terminal", "ends", "energised_end_no_load_tests",
           "energised_end_open_circuit_tests", "energised_end_short_circuit_tests", "energy_consumer", "energy_source", "eq_usage_points", "es_phases",
           "fuse_function", "geographical_region", "grounded_end_short_circuit_tests", "loop", "loop_circuits", "loop_energizing_substations",
           "loop_substations", "loops", "lv_feeder_normal_head_terminal", "measurement", "normal_energized_feeders", "normal_energized_loops",
           "normal_energized_lv_feeders", "normal_energizing_feeders", "normal_energizing_substation", "normal_head_terminal", "open_end_open_circuit_tests",
           "operational_restrictions", "or_equipment", "organisation", "organisation_roles", "per_length_impedance",
           "phase_power_electronics_connection", "pole", "potential_transformer_info", "power_electronics_connection_phase", "power_electronics_unit",
           "power_transformer", "power_transformer_info", "power_transformer_info_transformer_tank_info", "prf_protected_switch", "prf_scheme",
           "prf_sensor", "pricing_structures", "prscheme_function", "prscheme_system", "prsystem_scheme", "ps_relay_function", "psr_location",
           "ratio_tap_changer", "rc_regulating_cond_eq", "rc_terminal", "rce_regulating_control", "relay_info", "remote_control", "remote_source",
           "sen_relay_function", "service_location", "shunt_compensator_info", "star_impedance_transformer_end_info", "streetlights",
           "sub_geographical_region", "sub_geographical_regions", "substations", "switch_info", "tariffs", "tc_tap_changer_control", "te_base_voltage",
           "te_terminal", "transformer_end", "transformer_end_info", "transformer_end_transformer_star_impedance", "transformer_star_impedance",
           "transformer_tank_info", "unit_power_electronics_connection", "up_equipment", "usage_point_location", "wire_info", "cut_ac_line_segment", "cuts",
           "clamp_ac_line_segment", "clamps"]


def ae_terminal(auxiliary_equipment: AuxiliaryEquipment) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(auxiliary_equipment, aux_equip_to_term_resolver, None)


def agreements(c: Customer) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(c, cust_to_custagr_resolver, custagr_to_cust_resolver)


def assets(power_system_resource: PowerSystemResource) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(power_system_resource, psr_to_asset_resolver, asset_to_psr_resolver)


def at_location(asset: Asset) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(asset, asset_to_location_resolver, None)


def battery_controls(bu: BatteryUnit) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(bu, battery_unit_to_battery_control_resolver, None)


def ce_base_voltage(ce: ConductingEquipment) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(ce, cond_equip_to_bv_resolver, None)


def ce_terminals(ce: ConductingEquipment) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(ce, cond_equip_to_terminal_resolver, term_to_ce_resolver)


def circuits(substation: Substation) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(substation, sub_to_circuit_resolver, circuit_to_sub_resolver)


def clamp_ac_line_segment(clamp: Clamp) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(clamp, clamp_to_acls_resolver, None)


def clamps(acls: AcLineSegment) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(acls, acls_to_clamp_resolver, None)


def cn_terminals(cn: ConnectivityNode) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(cn, conn_node_to_term_resolver, term_to_cn_resolver)


def conducting_equipment(terminal: Terminal) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(terminal, term_to_ce_resolver, cond_equip_to_terminal_resolver)


def connectivity_node(terminal: Terminal) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(terminal, term_to_cn_resolver, conn_node_to_term_resolver)


def containers(equipment: Equipment) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(equipment, eq_to_ec_resolver, ec_to_eq_resolver)


def control(rc: RemoteControl) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(rc, rc_to_cont_resolver, control_to_remote_control_resolver)


def current_containers(equipment: Equipment) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(equipment, eq_to_curcontainer_resolver, ec_to_curequipment_resolver)


def current_transformer_info(current_transformer: CurrentTransformer) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(current_transformer, ct_to_cti_resolver, None)


def customer(customer_agreement: CustomerAgreement) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(customer_agreement, custagr_to_cust_resolver, cust_to_custagr_resolver)


def cut_ac_line_segment(cut: Cut) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(cut, cut_to_acls_resolver, None)


def cuts(acls: AcLineSegment) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(acls, acls_to_cut_resolver, None)


def diagram(diagram_object: DiagramObject) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(diagram_object, diagobj_to_diag_resolver, diag_to_diagobj_resolver)


def diagram_objects(d: Diagram) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(d, diag_to_diagobj_resolver, diagobj_to_diag_resolver)


def ec_equipment(equipment_container: EquipmentContainer) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(equipment_container, ec_to_eq_resolver, eq_to_ec_resolver)


def ec_phases(ec: EnergyConsumer) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(ec, ec_to_ecp_resolver, ecp_to_ec_resolver)


def ed_usage_points(end_device: EndDevice) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(end_device, ed_to_up_resolver, up_to_ed_resolver)


def end_devices(usage_point: UsagePoint) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(usage_point, up_to_ed_resolver, ed_to_up_resolver)


def end_device_functions(end_device: EndDevice) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(end_device, ed_to_edf_resolver, None)


def end_substation(circuit: Circuit) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(circuit, circuit_to_sub_resolver, sub_to_circuit_resolver)


def end_terminal(circuit: Circuit) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(circuit, circuit_to_term_resolver, None)


def ends(pt: PowerTransformer) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(pt, pt_to_pte_resolver, pte_to_pt_resolver)


def energised_end_no_load_tests(tei: TransformerEndInfo) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(tei, tei_to_ee_nlt_resolver, None)


def energised_end_open_circuit_tests(tei: TransformerEndInfo) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(tei, tei_to_ee_oct_resolver, None)


def energised_end_short_circuit_tests(tei: TransformerEndInfo) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(tei, tei_to_ee_sct_resolver, None)


def energy_consumer(energy_consumer_phase: EnergyConsumerPhase) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(energy_consumer_phase, ecp_to_ec_resolver, ec_to_ecp_resolver)


def energy_source(energy_source_phase: EnergySourcePhase) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(energy_source_phase, esp_to_es_resolver, es_to_esp_resolver)


def eq_usage_points(equipment: Equipment) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(equipment, eq_to_up_resolver, up_to_eq_resolver)


def es_phases(es: EnergySource) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(es, es_to_esp_resolver, esp_to_es_resolver)


def fuse_function(fuse: Fuse) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(fuse, fuse_to_prf_resolver, None)


def geographical_region(sgr: SubGeographicalRegion) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(sgr, sgr_to_gr_resolver, gr_to_sgr_resolver)


def grounded_end_short_circuit_tests(tei: TransformerEndInfo) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(tei, tei_to_ge_sct_resolver, None)


def loop(circuit: Circuit) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(circuit, circuit_to_loop_resolver, loop_to_circuit_resolver)


def loop_circuits(l_: Loop) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(l_, loop_to_circuit_resolver, circuit_to_loop_resolver)


def loop_energizing_substations(l_: Loop) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(l_, loop_to_esub_resolver, sub_to_eloop_resolver)


def loop_substations(l_: Loop) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(l_, loop_to_sub_resolver, sub_to_loop_resolver)


def loops(substation: Substation) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(substation, sub_to_loop_resolver, loop_to_sub_resolver)


def lv_feeder_normal_head_terminal(lv_feeder: LvFeeder) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(lv_feeder, lvfeeder_to_nht_resolver, None)


def measurement(rs: RemoteSource) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(rs, rs_to_meas_resolver, meas_to_rs_resolver)


def normal_energized_feeders(substation: Substation) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(substation, sub_to_feeder_resolver, feeder_to_nes_resolver)


def normal_energized_loops(substation: Substation) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(substation, sub_to_eloop_resolver, loop_to_esub_resolver)


def normal_energized_lv_feeders(feeder: Feeder) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(feeder, feeder_to_nelvf_resolver, lvfeeder_to_nef_resolver)


def current_energized_lv_feeders(feeder: Feeder) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(feeder, feeder_to_celvf_resolver, lvfeeder_to_cef_resolver)


def normal_energizing_feeders(lv_feeder: LvFeeder) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(lv_feeder, lvfeeder_to_nef_resolver, feeder_to_nelvf_resolver)


def current_energizing_feeders(lv_feeder: LvFeeder) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(lv_feeder, lvfeeder_to_cef_resolver, feeder_to_celvf_resolver)


def normal_energizing_substation(feeder: Feeder) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(feeder, feeder_to_nes_resolver, sub_to_feeder_resolver)


def normal_head_terminal(feeder: Feeder) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(feeder, feeder_to_nht_resolver, None)


def open_end_open_circuit_tests(tei: TransformerEndInfo) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(tei, tei_to_oe_oct_resolver, None)


def operational_restrictions(equipment: Equipment) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(equipment, eq_to_or_resolver, or_to_eq_resolver)


def or_equipment(operational_restriction: OperationalRestriction) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(operational_restriction, or_to_eq_resolver, eq_to_or_resolver)


def organisation(organisation_role: OrganisationRole) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(organisation_role, orgr_to_org_resolver, None)


def organisation_roles(asset: Asset) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(asset, asset_to_asset_org_role_resolver, None)


def per_length_impedance(ac_line_segment: AcLineSegment):
    # noinspection PyArgumentList
    return BoundReferenceResolver(ac_line_segment, acls_to_pli_resolver, None)


def phase_power_electronics_connection(pec: PowerElectronicsConnectionPhase) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(pec, pecphase_to_pec_resolver, pec_to_pecphase_resolver)


def pole(streetlight: Streetlight) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(streetlight, streetlight_to_pole_resolver, pole_to_streetlight_resolver)


def potential_transformer_info(potential_transformer: PotentialTransformer) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(potential_transformer, vt_to_vti_resolver, None)


def power_electronics_connection_phase(pec: PowerElectronicsConnection) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(pec, pec_to_pecphase_resolver, pecphase_to_pec_resolver)


def power_electronics_unit(pec: PowerElectronicsConnection) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(pec, pec_to_peu_resolver, peu_to_pec_resolver)


def power_transformer(power_transformer_end: PowerTransformerEnd) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(power_transformer_end, pte_to_pt_resolver, pt_to_pte_resolver)


def power_transformer_info(pt: PowerTransformer) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(pt, powertransformer_to_power_transformer_info_resolver, None)


def power_transformer_info_transformer_tank_info(pti: PowerTransformerInfo) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(pti, pti_to_tti_resolver, None)


def power_system_resources(asset: Asset) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(asset, asset_to_psr_resolver, psr_to_asset_resolver)


def prf_protected_switch(prf: ProtectionRelayFunction) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(prf, prf_to_psw_resolver, psw_to_prf_resolver)


def prf_scheme(prf: ProtectionRelayFunction) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(prf, prf_to_prscheme_resolver, prscheme_to_prf_resolver)


def prf_sensor(prf: ProtectionRelayFunction) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(prf, prf_to_sen_resolver, sen_to_prf_resolver)


def pricing_structures(customer_agreement: CustomerAgreement) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(customer_agreement, custagr_to_ps_resolver, None)


def prscheme_function(prscheme: ProtectionRelayScheme) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(prscheme, prscheme_to_prf_resolver, prf_to_prscheme_resolver)


def prscheme_system(prscheme: ProtectionRelayScheme) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(prscheme, prscheme_to_prsystem_resolver, prsystem_to_prscheme_resolver)


def prsystem_scheme(prsystem: ProtectionRelaySystem) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(prsystem, prsystem_to_prscheme_resolver, prscheme_to_prsystem_resolver)


def ps_relay_function(ps: ProtectedSwitch) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(ps, psw_to_prf_resolver, prf_to_psw_resolver)


def psr_location(power_system_resource: PowerSystemResource) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(power_system_resource, psr_to_loc_resolver, None)


def ratio_tap_changer(te: TransformerEnd) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(te, te_to_rtc_resolver, rtc_to_te_resolver)


def rc_regulating_cond_eq(regulating_control: RegulatingControl) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(regulating_control, rc_to_rce_resolver, rce_to_rc_resolver)


def rc_terminal(rc: RegulatingControl) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(rc, rc_to_term_resolver, None)


def rce_regulating_control(regulating_cond_eq: RegulatingCondEq) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(regulating_cond_eq, rce_to_rc_resolver, rc_to_rce_resolver)


def reactive_capability_curve(synchronous_machine: SynchronousMachine) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(synchronous_machine, sm_to_rcc_resolver, None)


def relay_info(prf: ProtectionRelayFunction) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(prf, prf_to_relay_info_resolver, None)


def remote_control(c: Control) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(c, control_to_remote_control_resolver, rc_to_cont_resolver)


def remote_source(m: Measurement) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(m, meas_to_rs_resolver, rs_to_meas_resolver)


def sen_relay_function(sen: Sensor) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(sen, sen_to_prf_resolver, prf_to_sen_resolver)


def service_location(end_device: EndDevice) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(end_device, ed_to_loc_resolver, None)


def shunt_compensator_info(sc: ShuntCompensator) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(sc, shunt_compensator_to_shunt_compensator_info_resolver, None)


def star_impedance_transformer_end_info(tsi: TransformerStarImpedance) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(tsi, tsi_to_tei_resolver, tei_to_tsi_resolver)


def streetlights(p: Pole) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(p, pole_to_streetlight_resolver, streetlight_to_pole_resolver)


def sub_geographical_region(substation: Substation) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(substation, sub_to_sgr_resolver, sgr_to_sub_resolver)


def sub_geographical_regions(gr: GeographicalRegion) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(gr, gr_to_sgr_resolver, sgr_to_gr_resolver)


def substations(sgr: SubGeographicalRegion) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(sgr, sgr_to_sub_resolver, sub_to_sgr_resolver)


def switch_info(switch: Switch) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(switch, switch_to_switch_info_resolver, None)


def tariffs(pricing_structure: PricingStructure) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(pricing_structure, ps_to_tariff_resolver, None)


def tc_tap_changer_control(tap_changer: TapChanger) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(tap_changer, tc_to_tcc_resolver, None)


def te_base_voltage(te: TransformerEnd) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(te, te_to_bv_resolver, None)


def te_terminal(te: TransformerEnd) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(te, te_to_term_resolver, None)


def transformer_end(rtt: RatioTapChanger) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(rtt, rtc_to_te_resolver, te_to_rtc_resolver)


def transformer_end_info(tti: TransformerTankInfo) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(tti, tti_to_tei_resolver, tei_to_tti_resolver)


def transformer_end_transformer_star_impedance(te: TransformerEnd) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(te, te_to_tsi_resolver, None)


def transformer_star_impedance(tei: TransformerEndInfo) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(tei, tei_to_tsi_resolver, tsi_to_tei_resolver)


def transformer_tank_info(tei: TransformerEndInfo) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(tei, tei_to_tti_resolver, tti_to_tei_resolver)


def unit_power_electronics_connection(pec: PowerElectronicsUnit) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(pec, peu_to_pec_resolver, pec_to_peu_resolver)


def up_equipment(usage_point: UsagePoint) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(usage_point, up_to_eq_resolver, eq_to_up_resolver)


def usage_point_location(usage_point: UsagePoint) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(usage_point, up_to_loc_resolver, None)


def wire_info(conductor: Conductor) -> BoundReferenceResolver:
    # noinspection PyArgumentList
    return BoundReferenceResolver(conductor, conductor_to_wire_info_resolver, None)
