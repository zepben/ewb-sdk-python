#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from zepben.evolve.database.sqlite.common.base_service_writer import BaseServiceWriter
from zepben.evolve.database.sqlite.network.network_cim_writer import NetworkCimWriter
from zepben.evolve.database.sqlite.network.network_database_tables import NetworkDatabaseTables
from zepben.evolve.model.cim.extensions.iec61968.metering.pan_demand_reponse_function import PanDemandResponseFunction
from zepben.evolve.model.cim.extensions.iec61970.base.wires.battery_control import BatteryControl
from zepben.evolve.model.cim.iec61968.assetinfo.no_load_test import NoLoadTest
from zepben.evolve.model.cim.iec61968.assetinfo.open_circuit_test import OpenCircuitTest
from zepben.evolve.model.cim.iec61968.assetinfo.power_transformer_info import PowerTransformerInfo
from zepben.evolve.model.cim.iec61968.assetinfo.short_circuit_test import ShortCircuitTest
from zepben.evolve.model.cim.iec61968.assetinfo.shunt_compensator_info import ShuntCompensatorInfo
from zepben.evolve.model.cim.iec61968.assetinfo.switch_info import SwitchInfo
from zepben.evolve.model.cim.iec61968.assetinfo.transformer_end_info import TransformerEndInfo
from zepben.evolve.model.cim.iec61968.assetinfo.transformer_tank_info import TransformerTankInfo
from zepben.evolve.model.cim.iec61968.assetinfo.wire_info import CableInfo, OverheadWireInfo
from zepben.evolve.model.cim.iec61968.assets.asset_organisation_role import AssetOwner
from zepben.evolve.model.cim.iec61968.assets.pole import Pole
from zepben.evolve.model.cim.iec61968.assets.streetlight import Streetlight
from zepben.evolve.model.cim.iec61968.common.location import Location
from zepben.evolve.model.cim.iec61968.common.organisation import Organisation
from zepben.evolve.model.cim.iec61968.infiec61968.infassetinfo.current_transformer_info import CurrentTransformerInfo
from zepben.evolve.model.cim.iec61968.infiec61968.infassetinfo.potential_transformer_info import PotentialTransformerInfo
from zepben.evolve.model.cim.iec61968.infiec61968.infassetinfo.relay_info import RelayInfo
from zepben.evolve.model.cim.iec61968.metering.metering import Meter, UsagePoint
from zepben.evolve.model.cim.iec61968.operations.operational_restriction import OperationalRestriction
from zepben.evolve.model.cim.iec61970.base.auxiliaryequipment.auxiliary_equipment import FaultIndicator
from zepben.evolve.model.cim.iec61970.base.auxiliaryequipment.current_transformer import CurrentTransformer
from zepben.evolve.model.cim.iec61970.base.auxiliaryequipment.potential_transformer import PotentialTransformer
from zepben.evolve.model.cim.iec61970.base.core.base_voltage import BaseVoltage
from zepben.evolve.model.cim.iec61970.base.core.connectivity_node import ConnectivityNode
from zepben.evolve.model.cim.iec61970.base.core.equipment_container import Feeder, Site
from zepben.evolve.model.cim.iec61970.base.core.regions import GeographicalRegion, SubGeographicalRegion
from zepben.evolve.model.cim.iec61970.base.core.substation import Substation
from zepben.evolve.model.cim.iec61970.base.core.terminal import Terminal
from zepben.evolve.model.cim.iec61970.base.equivalents.equivalent_branch import EquivalentBranch
from zepben.evolve.model.cim.iec61970.base.meas.control import Control
from zepben.evolve.model.cim.iec61970.base.meas.measurement import Analog, Accumulator, Discrete
from zepben.evolve.model.cim.iec61970.base.protection.current_relay import CurrentRelay
from zepben.evolve.model.cim.iec61970.base.protection.distance_relay import DistanceRelay
from zepben.evolve.model.cim.iec61970.base.protection.protection_relay_scheme import ProtectionRelayScheme
from zepben.evolve.model.cim.iec61970.base.protection.protection_relay_system import ProtectionRelaySystem
from zepben.evolve.model.cim.iec61970.base.protection.voltage_relay import VoltageRelay
from zepben.evolve.model.cim.iec61970.base.scada.remote_control import RemoteControl
from zepben.evolve.model.cim.iec61970.base.scada.remote_source import RemoteSource
from zepben.evolve.model.cim.iec61970.base.wires.aclinesegment import AcLineSegment
from zepben.evolve.model.cim.iec61970.base.wires.breaker import Breaker
from zepben.evolve.model.cim.iec61970.base.wires.connectors import BusbarSection, Junction
from zepben.evolve.model.cim.iec61970.base.wires.clamp import Clamp
from zepben.evolve.model.cim.iec61970.base.wires.cut import Cut
from zepben.evolve.model.cim.iec61970.base.wires.disconnector import Disconnector
from zepben.evolve.model.cim.iec61970.base.wires.energy_consumer import EnergyConsumer, EnergyConsumerPhase
from zepben.evolve.model.cim.iec61970.base.wires.energy_source import EnergySource
from zepben.evolve.model.cim.iec61970.base.wires.energy_source_phase import EnergySourcePhase
from zepben.evolve.model.cim.iec61970.base.wires.fuse import Fuse
from zepben.evolve.model.cim.iec61970.base.wires.generation.production.power_electronics_unit import BatteryUnit, PhotoVoltaicUnit, PowerElectronicsWindUnit
from zepben.evolve.model.cim.iec61970.base.wires.ground import Ground
from zepben.evolve.model.cim.iec61970.base.wires.ground_disconnector import GroundDisconnector
from zepben.evolve.model.cim.iec61970.base.wires.grounding_impedance import GroundingImpedance
from zepben.evolve.model.cim.iec61970.base.wires.jumper import Jumper
from zepben.evolve.model.cim.iec61970.base.wires.load_break_switch import LoadBreakSwitch
from zepben.evolve.model.cim.iec61970.base.wires.per_length import PerLengthSequenceImpedance
from zepben.evolve.model.cim.iec61970.base.wires.per_length_phase_impedance import PerLengthPhaseImpedance
from zepben.evolve.model.cim.iec61970.base.wires.petersen_coil import PetersenCoil
from zepben.evolve.model.cim.iec61970.base.wires.power_electronics_connection import PowerElectronicsConnection, PowerElectronicsConnectionPhase
from zepben.evolve.model.cim.iec61970.base.wires.power_transformer import PowerTransformer, PowerTransformerEnd, RatioTapChanger
from zepben.evolve.model.cim.iec61970.base.wires.reactive_capability_curve import ReactiveCapabilityCurve
from zepben.evolve.model.cim.iec61970.base.wires.recloser import Recloser
from zepben.evolve.model.cim.iec61970.base.wires.series_compensator import SeriesCompensator
from zepben.evolve.model.cim.iec61970.base.wires.shunt_compensator import LinearShuntCompensator
from zepben.evolve.model.cim.iec61970.base.wires.static_var_compensator import StaticVarCompensator
from zepben.evolve.model.cim.iec61970.base.wires.synchronous_machine import SynchronousMachine
from zepben.evolve.model.cim.iec61970.base.wires.tap_changer_control import TapChangerControl
from zepben.evolve.model.cim.iec61970.base.wires.transformer_star_impedance import TransformerStarImpedance
from zepben.evolve.model.cim.iec61970.infiec61970.feeder.circuit import Circuit
from zepben.evolve.model.cim.iec61970.infiec61970.feeder.loop import Loop
from zepben.evolve.model.cim.iec61970.infiec61970.feeder.lv_feeder import LvFeeder
from zepben.evolve.model.cim.iec61970.infiec61970.wires.generation.production.ev_charging_unit import EvChargingUnit
from zepben.evolve.services.network.network_service import NetworkService

__all__ = ["NetworkServiceWriter"]


class NetworkServiceWriter(BaseServiceWriter):
    """
    A class for writing a `NetworkService` into the database.

    :param service: The `NetworkService` to save to the database.
    :param database_tables: The `NetworkDatabaseTables` to add to the database.
    """

    def __init__(
        self,
        service: NetworkService,
        database_tables: NetworkDatabaseTables,
        writer: NetworkCimWriter = None
    ):
        writer = writer if writer is not None else NetworkCimWriter(database_tables)
        super().__init__(service, writer)

        # This is not strictly necessary, it is just to update the type of the writer. It could be done with a generic
        # on the base class which looks like it works, but that actually silently breaks code insight and completion
        self._writer = writer

    def _do_save(self) -> bool:
        return all([
            self._save_each_object(CableInfo, self._writer.save_cable_info),
            self._save_each_object(OverheadWireInfo, self._writer.save_overhead_wire_info),
            self._save_each_object(PowerTransformerInfo, self._writer.save_power_transformer_info),
            self._save_each_object(TransformerTankInfo, self._writer.save_transformer_tank_info),
            self._save_each_object(NoLoadTest, self._writer.save_no_load_test),
            self._save_each_object(OpenCircuitTest, self._writer.save_open_circuit_test),
            self._save_each_object(ShortCircuitTest, self._writer.save_short_circuit_test),
            self._save_each_object(ShuntCompensatorInfo, self._writer.save_shunt_compensator_info),
            self._save_each_object(SwitchInfo, self._writer.save_switch_info),
            self._save_each_object(TransformerEndInfo, self._writer.save_transformer_end_info),
            self._save_each_object(AssetOwner, self._writer.save_asset_owner),
            self._save_each_object(Pole, self._writer.save_pole),
            self._save_each_object(Streetlight, self._writer.save_streetlight),
            self._save_each_object(Location, self._writer.save_location),
            self._save_each_object(Organisation, self._writer.save_organisation),
            self._save_each_object(Meter, self._writer.save_meter),
            self._save_each_object(UsagePoint, self._writer.save_usage_point),
            self._save_each_object(OperationalRestriction, self._writer.save_operational_restriction),
            self._save_each_object(FaultIndicator, self._writer.save_fault_indicator),
            self._save_each_object(BaseVoltage, self._writer.save_base_voltage),
            self._save_each_object(ConnectivityNode, self._writer.save_connectivity_node),
            self._save_each_object(Feeder, self._writer.save_feeder),
            self._save_each_object(GeographicalRegion, self._writer.save_geographical_region),
            self._save_each_object(Site, self._writer.save_site),
            self._save_each_object(SubGeographicalRegion, self._writer.save_sub_geographical_region),
            self._save_each_object(Substation, self._writer.save_substation),
            self._save_each_object(Terminal, self._writer.save_terminal),
            self._save_each_object(EquivalentBranch, self._writer.save_equivalent_branch),
            self._save_each_object(BatteryUnit, self._writer.save_battery_unit),
            self._save_each_object(PhotoVoltaicUnit, self._writer.save_photo_voltaic_unit),
            self._save_each_object(PowerElectronicsWindUnit, self._writer.save_power_electronics_wind_unit),
            self._save_each_object(AcLineSegment, self._writer.save_ac_line_segment),
            self._save_each_object(Breaker, self._writer.save_breaker),
            self._save_each_object(LoadBreakSwitch, self._writer.save_load_break_switch),
            self._save_each_object(BusbarSection, self._writer.save_busbar_section),
            self._save_each_object(Clamp, self._writer.save_clamp),
            self._save_each_object(Cut, self._writer.save_cut),
            self._save_each_object(Disconnector, self._writer.save_disconnector),
            self._save_each_object(EnergyConsumer, self._writer.save_energy_consumer),
            self._save_each_object(EnergyConsumerPhase, self._writer.save_energy_consumer_phase),
            self._save_each_object(EnergySource, self._writer.save_energy_source),
            self._save_each_object(EnergySourcePhase, self._writer.save_energy_source_phase),
            self._save_each_object(Fuse, self._writer.save_fuse),
            self._save_each_object(Jumper, self._writer.save_jumper),
            self._save_each_object(Junction, self._writer.save_junction),
            self._save_each_object(LinearShuntCompensator, self._writer.save_linear_shunt_compensator),
            self._save_each_object(PerLengthPhaseImpedance, self._writer.save_per_length_phase_impedance),
            self._save_each_object(PerLengthSequenceImpedance, self._writer.save_per_length_sequence_impedance),
            self._save_each_object(PowerElectronicsConnection, self._writer.save_power_electronics_connection),
            self._save_each_object(PowerElectronicsConnectionPhase, self._writer.save_power_electronics_connection_phase),
            self._save_each_object(PowerTransformer, self._writer.save_power_transformer),
            self._save_each_object(PowerTransformerEnd, self._writer.save_power_transformer_end),
            self._save_each_object(RatioTapChanger, self._writer.save_ratio_tap_changer),
            self._save_each_object(Recloser, self._writer.save_recloser),
            self._save_each_object(TransformerStarImpedance, self._writer.save_transformer_star_impedance),
            self._save_each_object(Circuit, self._writer.save_circuit),
            self._save_each_object(Loop, self._writer.save_loop),
            self._save_each_object(LvFeeder, self._writer.save_lv_feeder),
            self._save_each_object(Analog, self._writer.save_analog),
            self._save_each_object(Accumulator, self._writer.save_accumulator),
            self._save_each_object(Discrete, self._writer.save_discrete),
            self._save_each_object(Control, self._writer.save_control),
            self._save_each_object(RemoteControl, self._writer.save_remote_control),
            self._save_each_object(RemoteSource, self._writer.save_remote_source),
            self._save_each_object(CurrentTransformerInfo, self._writer.save_current_transformer_info),
            self._save_each_object(PotentialTransformerInfo, self._writer.save_potential_transformer_info),
            self._save_each_object(CurrentTransformer, self._writer.save_current_transformer),
            self._save_each_object(PotentialTransformer, self._writer.save_potential_transformer),
            self._save_each_object(RelayInfo, self._writer.save_relay_info),
            self._save_each_object(CurrentRelay, self._writer.save_current_relay),
            self._save_each_object(TapChangerControl, self._writer.save_tap_changer_control),
            self._save_each_object(EvChargingUnit, self._writer.save_ev_charging_unit),
            self._save_each_object(DistanceRelay, self._writer.save_distance_relay),
            self._save_each_object(ProtectionRelayScheme, self._writer.save_protection_relay_scheme),
            self._save_each_object(ProtectionRelaySystem, self._writer.save_protection_relay_system),
            self._save_each_object(VoltageRelay, self._writer.save_voltage_relay),
            self._save_each_object(Ground, self._writer.save_ground),
            self._save_each_object(GroundDisconnector, self._writer.save_ground_disconnector),
            self._save_each_object(SeriesCompensator, self._writer.save_series_compensator),
            self._save_each_object(SynchronousMachine, self._writer.save_synchronous_machine),
            self._save_each_object(PetersenCoil, self._writer.save_petersen_coil),
            self._save_each_object(GroundingImpedance, self._writer.save_grounding_impedance),
            self._save_each_object(ReactiveCapabilityCurve, self._writer.save_reactive_capability_curve),
            self._save_each_object(PanDemandResponseFunction, self._writer.save_pan_demand_response_function),
            self._save_each_object(BatteryControl, self._writer.save_battery_control),
            self._save_each_object(StaticVarCompensator, self._writer.save_static_var_compensator),
        ])
