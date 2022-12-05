#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from typing import Callable, Optional

from dataclassy import dataclass

from zepben.evolve import TransformerTankInfo, TransformerEndInfo, TransformerStarImpedance, NoLoadTest, ShortCircuitTest, OpenCircuitTest, ShuntCompensator, \
    ShuntCompensatorInfo
from zepben.evolve.model.cim.iec61968.assetinfo.power_transformer_info import PowerTransformerInfo
from zepben.evolve.model.cim.iec61968.assetinfo.wire_info import WireInfo
from zepben.evolve.model.cim.iec61968.assets.asset import Asset
from zepben.evolve.model.cim.iec61968.assets.asset_organisation_role import AssetOrganisationRole
from zepben.evolve.model.cim.iec61968.assets.pole import Pole
from zepben.evolve.model.cim.iec61968.assets.streetlight import Streetlight
from zepben.evolve.model.cim.iec61968.common.location import Location
from zepben.evolve.model.cim.iec61968.common.organisation import Organisation
from zepben.evolve.model.cim.iec61968.common.organisation_role import OrganisationRole
from zepben.evolve.model.cim.iec61968.customers.customer import Customer
from zepben.evolve.model.cim.iec61968.customers.customer_agreement import CustomerAgreement
from zepben.evolve.model.cim.iec61968.customers.pricing_structure import PricingStructure
from zepben.evolve.model.cim.iec61968.customers.tariff import Tariff
from zepben.evolve.model.cim.iec61968.infiec61968.infassetinfo.current_transformer_info import CurrentTransformerInfo
from zepben.evolve.model.cim.iec61968.infiec61968.infassetinfo.potential_transformer_info import PotentialTransformerInfo
from zepben.evolve.model.cim.iec61968.metering.metering import EndDevice, UsagePoint
from zepben.evolve.model.cim.iec61968.operations.operational_restriction import OperationalRestriction
from zepben.evolve.model.cim.iec61970.base.auxiliaryequipment.auxiliary_equipment import AuxiliaryEquipment
from zepben.evolve.model.cim.iec61970.base.auxiliaryequipment.current_transformer import CurrentTransformer
from zepben.evolve.model.cim.iec61970.base.auxiliaryequipment.potential_transformer import PotentialTransformer
from zepben.evolve.model.cim.iec61970.base.core.base_voltage import BaseVoltage
from zepben.evolve.model.cim.iec61970.base.core.conducting_equipment import ConductingEquipment
from zepben.evolve.model.cim.iec61970.base.core.connectivity_node import ConnectivityNode
from zepben.evolve.model.cim.iec61970.base.core.equipment import Equipment
from zepben.evolve.model.cim.iec61970.base.core.equipment_container import Feeder, EquipmentContainer
from zepben.evolve.model.cim.iec61970.base.core.identified_object import IdentifiedObject
from zepben.evolve.model.cim.iec61970.base.core.power_system_resource import PowerSystemResource
from zepben.evolve.model.cim.iec61970.base.core.regions import GeographicalRegion, SubGeographicalRegion
from zepben.evolve.model.cim.iec61970.base.core.substation import Substation
from zepben.evolve.model.cim.iec61970.base.core.terminal import Terminal
from zepben.evolve.model.cim.iec61970.base.diagramlayout.diagram_layout import Diagram, DiagramObject
from zepben.evolve.model.cim.iec61970.base.meas.control import Control
from zepben.evolve.model.cim.iec61970.base.meas.measurement import Measurement
from zepben.evolve.model.cim.iec61970.base.scada.remote_control import RemoteControl
from zepben.evolve.model.cim.iec61970.base.scada.remote_source import RemoteSource
from zepben.evolve.model.cim.iec61970.base.wires.aclinesegment import AcLineSegment, Conductor
from zepben.evolve.model.cim.iec61970.base.wires.energy_consumer import EnergyConsumer, EnergyConsumerPhase
from zepben.evolve.model.cim.iec61970.base.wires.energy_source import EnergySource
from zepben.evolve.model.cim.iec61970.base.wires.energy_source_phase import EnergySourcePhase
from zepben.evolve.model.cim.iec61970.base.wires.generation.production.power_electronics_unit import PowerElectronicsUnit
from zepben.evolve.model.cim.iec61970.base.wires.per_length import PerLengthSequenceImpedance
from zepben.evolve.model.cim.iec61970.base.wires.power_electronics_connection import PowerElectronicsConnectionPhase, PowerElectronicsConnection
from zepben.evolve.model.cim.iec61970.base.wires.power_transformer import PowerTransformer, PowerTransformerEnd, RatioTapChanger, TransformerEnd
from zepben.evolve.model.cim.iec61970.infiec61970.feeder.circuit import Circuit
from zepben.evolve.model.cim.iec61970.infiec61970.feeder.loop import Loop
from zepben.evolve.model.cim.iec61970.infiec61970.feeder.lv_feeder import LvFeeder

__all__ = [
    "acls_to_plsi_resolver", "asset_to_asset_org_role_resolver", "asset_to_location_resolver", "pole_to_streetlight_resolver", "streetlight_to_pole_resolver",
    "aux_equip_to_term_resolver", "cond_equip_to_bv_resolver", "cond_equip_to_terminal_resolver", "conductor_to_wire_info_resolver",
    "conn_node_to_term_resolver", "control_to_remote_control_resolver", "cust_to_custagr_resolver", "custagr_to_cust_resolver", "custagr_to_ps_resolver",
    "diag_to_diagobj_resolver", "diagobj_to_diag_resolver", "ed_to_up_resolver", "ed_to_loc_resolver", "ec_to_ecp_resolver", "ecp_to_ec_resolver",
    "es_to_esp_resolver", "esp_to_es_resolver", "eq_to_curcontainer_resolver", "powertransformer_to_power_transformer_info_resolver", "eq_to_ec_resolver",
    "eq_to_or_resolver", "eq_to_up_resolver", "ec_to_eq_resolver", "ec_to_curequipment_resolver", "feeder_to_nes_resolver", "feeder_to_nht_resolver",
    "feeder_to_nelvf_resolver", "gr_to_sgr_resolver", "meas_to_rs_resolver", "or_to_eq_resolver", "orgr_to_org_resolver", "psr_to_loc_resolver",
    "pt_to_pte_resolver", "pte_to_pt_resolver", "ps_to_tariff_resolver", "rtc_to_te_resolver", "rc_to_cont_resolver", "rs_to_meas_resolver",
    "sgr_to_gr_resolver", "sgr_to_sub_resolver", "sub_to_feeder_resolver", "sub_to_sgr_resolver", "sub_to_circuit_resolver", "sub_to_eloop_resolver",
    "sub_to_loop_resolver", "term_to_ce_resolver", "term_to_cn_resolver", "te_to_term_resolver", "te_to_bv_resolver", "te_to_rtc_resolver", "up_to_ed_resolver",
    "up_to_eq_resolver", "up_to_loc_resolver", "circuit_to_loop_resolver", "circuit_to_sub_resolver", "circuit_to_term_resolver", "loop_to_circuit_resolver",
    "loop_to_esub_resolver", "loop_to_sub_resolver", "BoundReferenceResolver", "ReferenceResolver", "UnresolvedReference", "tei_to_tti_resolver",
    "tti_to_tei_resolver", "tei_to_tsi_resolver", "tsi_to_tei_resolver", "te_to_tsi_resolver", "pti_to_tti_resolver", "peu_to_pec_resolver",
    "pec_to_peu_resolver", "pecphase_to_pec_resolver", "pec_to_pecphase_resolver", "tei_to_ee_nlt_resolver", "tei_to_ee_sct_resolver", "tei_to_ge_sct_resolver",
    "tei_to_oe_oct_resolver", "tei_to_ee_oct_resolver", "shunt_compensator_to_shunt_compensator_info_resolver", "lvfeeder_to_nht_resolver",
    "lvfeeder_to_nef_resolver", "ct_to_cti_resolver", "vt_to_vti_resolver"
]


@dataclass(frozen=True, eq=False, slots=True)
class ReferenceResolver(object):
    from_class: type
    to_class: type
    resolve: Callable[[IdentifiedObject, IdentifiedObject], None]

    def __eq__(self, other):
        return self.from_class is other.from_class and self.to_class is other.to_class and self.resolve is other.resolve

    def __ne__(self, other):
        return self.from_class is not other.from_class or self.to_class is not other.to_class or self.resolve is not other.resolve

    def __hash__(self):
        return hash((type(self), self.from_class, self.to_class, self.resolve))


@dataclass(frozen=True, eq=False, slots=True)
class BoundReferenceResolver(object):
    from_obj: IdentifiedObject
    resolver: ReferenceResolver
    reverse_resolver: Optional[ReferenceResolver]

    def __eq__(self, other):
        """ We only do a reference check for `from_obj` to avoid expensive equality checks on `IdentifiedObjects`. """
        if self.reverse_resolver is None and other.reverse_resolver is None:
            return self.from_obj is other.from_obj and self.resolver == other.resolver
        elif self.reverse_resolver is not None and other.reverse_resolver is not None:
            return self.from_obj is other.from_obj and self.resolver == other.resolver and self.reverse_resolver == other.reverse_resolver
        elif self.reverse_resolver is None:
            return False
        else:
            return False

    def __ne__(self, other):
        if self.reverse_resolver is None and other.reverse_resolver is None:
            return self.from_obj is not other.from_obj or self.resolver != other.resolver
        elif self.reverse_resolver is not None and other.reverse_resolver is not None:
            return self.from_obj is not other.from_obj or self.resolver != other.resolver or self.reverse_resolver != other.reverse_resolver
        elif self.reverse_resolver is None:
            return True
        else:
            return True

    def __hash__(self):
        return hash((type(self), self.from_obj, self.resolver, self.reverse_resolver))


@dataclass(frozen=True, eq=False, slots=True)
class UnresolvedReference(object):
    from_ref: IdentifiedObject
    to_mrid: str
    resolver: ReferenceResolver
    reverse_resolver: Optional[ReferenceResolver] = None

    def __eq__(self, other: UnresolvedReference):
        # we don't check reverse resolver for equality, as it doesn't make sense to have a reverse resolver that is not the reverse of resolver
        return self.from_ref.mrid == other.from_ref.mrid and self.to_mrid == other.to_mrid and self.resolver == other.resolver

    def __ne__(self, other: UnresolvedReference):
        return self.from_ref.mrid != other.from_ref.mrid or self.to_mrid != other.to_mrid or self.resolver != other.resolver

    def __hash__(self):
        return hash((type(self), self.from_ref.mrid, self.to_mrid, self.resolver))


def _resolve_ce_term(ce, t):
    t.conducting_equipment = ce
    ce.add_terminal(t)


def _resolve_pt_pte(pt, pte):
    pte.power_transformer = pt
    pt.add_end(pte)


def _resolve_diag_diagobj(diag, diag_obj):
    diag_obj.diagram = diag
    diag.add_diagram_object(diag_obj)


acls_to_plsi_resolver = ReferenceResolver(AcLineSegment, PerLengthSequenceImpedance, lambda t, r: setattr(t, 'per_length_sequence_impedance', r))

asset_to_asset_org_role_resolver = ReferenceResolver(Asset, AssetOrganisationRole, lambda t, r: t.add_organisation_role(r))
asset_to_location_resolver = ReferenceResolver(Asset, Location, lambda t, r: setattr(t, 'location', r))

pole_to_streetlight_resolver = ReferenceResolver(Pole, Streetlight, lambda t, r: t.add_streetlight(r))
streetlight_to_pole_resolver = ReferenceResolver(Streetlight, Pole, lambda t, r: setattr(t, 'pole', r))

aux_equip_to_term_resolver = ReferenceResolver(AuxiliaryEquipment, Terminal, lambda t, r: setattr(t, 'terminal', r))

cond_equip_to_bv_resolver = ReferenceResolver(ConductingEquipment, BaseVoltage, lambda t, r: setattr(t, 'base_voltage', r))
cond_equip_to_terminal_resolver = ReferenceResolver(ConductingEquipment, Terminal, _resolve_ce_term)

conductor_to_wire_info_resolver = ReferenceResolver(Conductor, WireInfo, lambda t, r: setattr(t, 'asset_info', r))

powertransformer_to_power_transformer_info_resolver = ReferenceResolver(PowerTransformer, PowerTransformerInfo, lambda t, r: setattr(t, 'asset_info', r))

shunt_compensator_to_shunt_compensator_info_resolver = ReferenceResolver(ShuntCompensator, ShuntCompensatorInfo, lambda t, r: setattr(t, 'asset_info', r))

tei_to_tti_resolver = ReferenceResolver(TransformerEndInfo, TransformerTankInfo, lambda t, r: setattr(t, 'transformer_tank_info', r))

tti_to_tei_resolver = ReferenceResolver(TransformerTankInfo, TransformerEndInfo, lambda t, r: t.add_transformer_end_info(r))

tei_to_tsi_resolver = ReferenceResolver(TransformerEndInfo, TransformerStarImpedance, lambda t, r: setattr(t, 'transformer_star_impedance', r))

tsi_to_tei_resolver = ReferenceResolver(TransformerStarImpedance, TransformerEndInfo, lambda t, r: setattr(t, 'transformer_end_info', r))

te_to_tsi_resolver = ReferenceResolver(TransformerEnd, TransformerStarImpedance, lambda t, r: setattr(t, 'star_impedance', r))

pti_to_tti_resolver = ReferenceResolver(PowerTransformerInfo, TransformerTankInfo, lambda t, r: t.add_transformer_tank_info(r))

conn_node_to_term_resolver = ReferenceResolver(ConnectivityNode, Terminal, lambda t, r: t.add_terminal(r))

control_to_remote_control_resolver = ReferenceResolver(Control, RemoteControl, lambda t, r: setattr(t, 'remote_control', r))

cust_to_custagr_resolver = ReferenceResolver(Customer, CustomerAgreement, lambda t, r: t.add_agreement(r))
custagr_to_cust_resolver = ReferenceResolver(CustomerAgreement, Customer, lambda t, r: setattr(t, 'customer', r))

custagr_to_ps_resolver = ReferenceResolver(CustomerAgreement, PricingStructure, lambda t, r: t.add_pricing_structure(r))

diag_to_diagobj_resolver = ReferenceResolver(Diagram, DiagramObject, _resolve_diag_diagobj)
diagobj_to_diag_resolver = ReferenceResolver(DiagramObject, Diagram, lambda t, r: setattr(t, 'diagram', r))

ed_to_up_resolver = ReferenceResolver(EndDevice, UsagePoint, lambda t, r: t.add_usage_point(r))
ed_to_loc_resolver = ReferenceResolver(EndDevice, Location, lambda t, r: setattr(t, 'service_location', r))

ec_to_ecp_resolver = ReferenceResolver(EnergyConsumer, EnergyConsumerPhase, lambda t, r: t.add_phase(r))
ecp_to_ec_resolver = ReferenceResolver(EnergyConsumerPhase, EnergyConsumer, lambda t, r: setattr(t, 'energy_consumer', r))

es_to_esp_resolver = ReferenceResolver(EnergySource, EnergySourcePhase, lambda t, r: t.add_phase(r))
esp_to_es_resolver = ReferenceResolver(EnergySourcePhase, EnergySource, lambda t, r: setattr(t, 'energy_source', r))

eq_to_curcontainer_resolver = ReferenceResolver(Equipment, EquipmentContainer, lambda t, r: t.add_current_container(r))
eq_to_ec_resolver = ReferenceResolver(Equipment, EquipmentContainer, lambda t, r: t.add_container(r))
eq_to_or_resolver = ReferenceResolver(Equipment, OperationalRestriction, lambda t, r: t.add_operational_restriction(r))
eq_to_up_resolver = ReferenceResolver(Equipment, UsagePoint, lambda t, r: t.add_usage_point(r))

ec_to_eq_resolver = ReferenceResolver(EquipmentContainer, Equipment, lambda t, r: t.add_equipment(r))
ec_to_curequipment_resolver = ReferenceResolver(EquipmentContainer, Equipment, lambda t, r: t.add_current_equipment(r))

feeder_to_nes_resolver = ReferenceResolver(Feeder, Substation, lambda t, r: setattr(t, 'normal_energizing_substation', r))
feeder_to_nht_resolver = ReferenceResolver(Feeder, Terminal, lambda t, r: setattr(t, 'normal_head_terminal', r))
feeder_to_nelvf_resolver = ReferenceResolver(Feeder, LvFeeder, lambda t, r: t.add_normal_energized_lv_feeder(r))

gr_to_sgr_resolver = ReferenceResolver(GeographicalRegion, SubGeographicalRegion, lambda t, r: t.add_sub_geographical_region(r))

meas_to_rs_resolver = ReferenceResolver(Measurement, RemoteSource, lambda t, r: setattr(t, 'remote_source', r))

or_to_eq_resolver = ReferenceResolver(OperationalRestriction, Equipment, lambda t, r: t.add_equipment(r))

orgr_to_org_resolver = ReferenceResolver(OrganisationRole, Organisation, lambda t, r: setattr(t, 'organisation', r))

psr_to_loc_resolver = ReferenceResolver(PowerSystemResource, Location, lambda t, r: setattr(t, 'location', r))

pt_to_pte_resolver = ReferenceResolver(PowerTransformer, PowerTransformerEnd, _resolve_pt_pte)
pte_to_pt_resolver = ReferenceResolver(PowerTransformerEnd, PowerTransformer, lambda t, r: setattr(t, 'power_transformer', r))

ps_to_tariff_resolver = ReferenceResolver(PricingStructure, Tariff, lambda t, r: t.add_tariff(r))

rtc_to_te_resolver = ReferenceResolver(RatioTapChanger, PowerTransformerEnd, lambda t, r: setattr(t, 'transformer_end', r))

rc_to_cont_resolver = ReferenceResolver(RemoteControl, Control, lambda t, r: setattr(t, 'control', r))

rs_to_meas_resolver = ReferenceResolver(RemoteSource, Measurement, lambda t, r: setattr(t, 'measurement', r))

sgr_to_gr_resolver = ReferenceResolver(SubGeographicalRegion, GeographicalRegion, lambda t, r: setattr(t, 'geographical_region', r))
sgr_to_sub_resolver = ReferenceResolver(SubGeographicalRegion, Substation, lambda t, r: t.add_substation(r))

sub_to_feeder_resolver = ReferenceResolver(Substation, Feeder, lambda t, r: t.add_feeder(r))
sub_to_sgr_resolver = ReferenceResolver(Substation, SubGeographicalRegion, lambda t, r: setattr(t, 'sub_geographical_region', r))
sub_to_circuit_resolver = ReferenceResolver(Substation, Circuit, lambda t, r: t.add_circuit(r))
sub_to_loop_resolver = ReferenceResolver(Substation, Loop, lambda t, r: t.add_loop(r))
sub_to_eloop_resolver = ReferenceResolver(Substation, Loop, lambda t, r: t.add_energized_loop(r))

term_to_ce_resolver = ReferenceResolver(Terminal, ConductingEquipment, lambda t, r: setattr(t, 'conducting_equipment', r))
term_to_cn_resolver = ReferenceResolver(Terminal, ConnectivityNode, lambda t, r: setattr(t, 'connectivity_node', r))

te_to_term_resolver = ReferenceResolver(TransformerEnd, Terminal, lambda t, r: setattr(t, 'terminal', r))
te_to_bv_resolver = ReferenceResolver(TransformerEnd, BaseVoltage, lambda t, r: setattr(t, 'base_voltage', r))
te_to_rtc_resolver = ReferenceResolver(TransformerEnd, RatioTapChanger, lambda t, r: setattr(t, 'ratio_tap_changer', r))

up_to_ed_resolver = ReferenceResolver(UsagePoint, EndDevice, lambda t, r: t.add_end_device(r))
up_to_eq_resolver = ReferenceResolver(UsagePoint, Equipment, lambda t, r: t.add_equipment(r))
up_to_loc_resolver = ReferenceResolver(UsagePoint, Location, lambda t, r: setattr(t, 'usage_point_location', r))

circuit_to_term_resolver = ReferenceResolver(Circuit, Terminal, lambda t, r: t.add_end_terminal(r))
circuit_to_loop_resolver = ReferenceResolver(Circuit, Loop, lambda t, r: setattr(t, 'loop', r))
circuit_to_sub_resolver = ReferenceResolver(Circuit, Substation, lambda t, r: t.add_end_substation(r))

loop_to_circuit_resolver = ReferenceResolver(Loop, Circuit, lambda t, r: t.add_circuit(r))
loop_to_sub_resolver = ReferenceResolver(Loop, Substation, lambda t, r: t.add_substation(r))
loop_to_esub_resolver = ReferenceResolver(Loop, Substation, lambda t, r: t.add_energizing_substation(r))

lvfeeder_to_nht_resolver = ReferenceResolver(LvFeeder, Terminal, lambda t, r: setattr(t, 'normal_head_terminal', r))
lvfeeder_to_nef_resolver = ReferenceResolver(LvFeeder, Feeder, lambda t, r: t.add_normal_energizing_feeder(r))

pec_to_pecphase_resolver = ReferenceResolver(PowerElectronicsConnection, PowerElectronicsConnectionPhase, lambda t, r: t.add_phase(r))
pecphase_to_pec_resolver = ReferenceResolver(PowerElectronicsConnectionPhase,
                                             PowerElectronicsConnection,
                                             lambda t, r: setattr(t, 'power_electronics_connection', r))

pec_to_peu_resolver = ReferenceResolver(PowerElectronicsConnection, PowerElectronicsUnit, lambda t, r: t.add_unit(r))
peu_to_pec_resolver = ReferenceResolver(PowerElectronicsUnit, PowerElectronicsConnection, lambda t, r: setattr(t, 'power_electronics_connection', r))

tei_to_ee_nlt_resolver = ReferenceResolver(TransformerEndInfo, NoLoadTest, lambda t, r: setattr(t, 'energised_end_no_load_tests', r))
tei_to_ee_sct_resolver = ReferenceResolver(TransformerEndInfo, ShortCircuitTest, lambda t, r: setattr(t, 'energised_end_short_circuit_tests', r))
tei_to_ge_sct_resolver = ReferenceResolver(TransformerEndInfo, ShortCircuitTest, lambda t, r: setattr(t, 'grounded_end_short_circuit_tests', r))
tei_to_oe_oct_resolver = ReferenceResolver(TransformerEndInfo, OpenCircuitTest, lambda t, r: setattr(t, 'open_end_open_circuit_tests', r))
tei_to_ee_oct_resolver = ReferenceResolver(TransformerEndInfo, OpenCircuitTest, lambda t, r: setattr(t, 'energised_end_open_circuit_tests', r))

# To avoid confusion with PowerTransformer shortened as "pt", PotentialTransformer is shortened to "vt".
ct_to_cti_resolver = ReferenceResolver(CurrentTransformer, CurrentTransformerInfo, lambda t, r: setattr(t, 'asset_info', r))
vt_to_vti_resolver = ReferenceResolver(PotentialTransformer, PotentialTransformerInfo, lambda t, r: setattr(t, 'asset_info', r))
