#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve import NetworkService, CableInfo, OverheadWireInfo, PowerTransformerInfo, TransformerTankInfo, NoLoadTest, OpenCircuitTest, \
    ShortCircuitTest, ShuntCompensatorInfo, TransformerEndInfo, AssetOwner, Pole, Streetlight, Location, Organisation, Meter, UsagePoint, \
    OperationalRestriction, FaultIndicator, BaseVoltage, ConnectivityNode, Feeder, GeographicalRegion, Site, SubGeographicalRegion, Substation, Terminal, \
    EquivalentBranch, PhotoVoltaicUnit, AcLineSegment, Breaker, LoadBreakSwitch, BusbarSection, Disconnector, EnergyConsumer, EnergyConsumerPhase, \
    EnergySource, EnergySourcePhase, Fuse, Jumper, Junction, LinearShuntCompensator, PerLengthSequenceImpedance, PowerElectronicsConnection, \
    PowerElectronicsConnectionPhase, PowerTransformer, PowerTransformerEnd, RatioTapChanger, Recloser, TransformerStarImpedance, Circuit, Loop, Analog, \
    Accumulator, Discrete, Control, RemoteControl, RemoteSource, BatteryUnit, PowerElectronicsWindUnit, LvFeeder
from zepben.evolve.database.sqlite.writers.base_service_writer import BaseServiceWriter
from zepben.evolve.database.sqlite.writers.network_cim_writer import NetworkCIMWriter

__all__ = ["NetworkServiceWriter"]


class NetworkServiceWriter(BaseServiceWriter):

    def save(self, service: NetworkService, writer: NetworkCIMWriter) -> bool:
        status = super(NetworkServiceWriter, self).save(service, writer)

        status = status and self._save_all(service, CableInfo, writer.save_cable_info)
        status = status and self._save_all(service, OverheadWireInfo, writer.save_overhead_wire_info)
        status = status and self._save_all(service, PowerTransformerInfo, writer.save_power_transformer_info)
        status = status and self._save_all(service, TransformerTankInfo, writer.save_transformer_tank_info)
        status = status and self._save_all(service, NoLoadTest, writer.save_no_load_test)
        status = status and self._save_all(service, OpenCircuitTest, writer.save_open_circuit_test)
        status = status and self._save_all(service, ShortCircuitTest, writer.save_short_circuit_test)
        status = status and self._save_all(service, ShuntCompensatorInfo, writer.save_shunt_compensator_info)
        status = status and self._save_all(service, TransformerEndInfo, writer.save_transformer_end_info)
        status = status and self._save_all(service, AssetOwner, writer.save_asset_owner)
        status = status and self._save_all(service, Pole, writer.save_pole)
        status = status and self._save_all(service, Streetlight, writer.save_streetlight)
        status = status and self._save_all(service, Location, writer.save_location)
        status = status and self._save_all_common(service, Organisation, writer.save_organisation)
        status = status and self._save_all(service, Meter, writer.save_meter)
        status = status and self._save_all(service, UsagePoint, writer.save_usage_point)
        status = status and self._save_all(service, OperationalRestriction, writer.save_operational_restriction)
        status = status and self._save_all(service, FaultIndicator, writer.save_fault_indicator)
        status = status and self._save_all(service, BaseVoltage, writer.save_base_voltage)
        status = status and self._save_all(service, ConnectivityNode, writer.save_connectivity_node)
        status = status and self._save_all(service, Feeder, writer.save_feeder)
        status = status and self._save_all(service, GeographicalRegion, writer.save_geographical_region)
        status = status and self._save_all(service, Site, writer.save_site)
        status = status and self._save_all(service, SubGeographicalRegion, writer.save_sub_geographical_region)
        status = status and self._save_all(service, Substation, writer.save_substation)
        status = status and self._save_all(service, Terminal, writer.save_terminal)
        status = status and self._save_all(service, EquivalentBranch, writer.save_equivalent_branch)
        status = status and self._save_all(service, BatteryUnit, writer.save_battery_unit)
        status = status and self._save_all(service, PhotoVoltaicUnit, writer.save_photovoltaic_unit)
        status = status and self._save_all(service, PowerElectronicsWindUnit, writer.save_power_electronics_wind_unit)
        status = status and self._save_all(service, AcLineSegment, writer.save_ac_line_segment)
        status = status and self._save_all(service, Breaker, writer.save_breaker)
        status = status and self._save_all(service, LoadBreakSwitch, writer.save_load_break_switch)
        status = status and self._save_all(service, BusbarSection, writer.save_bus_bar_section)
        status = status and self._save_all(service, Disconnector, writer.save_disconnector)
        status = status and self._save_all(service, EnergyConsumer, writer.save_energy_consumer)
        status = status and self._save_all(service, EnergyConsumerPhase, writer.save_energy_consumer_phase)
        status = status and self._save_all(service, EnergySource, writer.save_energy_source)
        status = status and self._save_all(service, EnergySourcePhase, writer.save_energy_source_phase)
        status = status and self._save_all(service, Fuse, writer.save_fuse)
        status = status and self._save_all(service, Jumper, writer.save_jumper)
        status = status and self._save_all(service, Junction, writer.save_junction)
        status = status and self._save_all(service, LinearShuntCompensator, writer.save_linear_shunt_compensator)
        status = status and self._save_all(service, PerLengthSequenceImpedance, writer.save_per_length_sequence_impedance)
        status = status and self._save_all(service, PowerElectronicsConnection, writer.save_power_electronics_connection)
        status = status and self._save_all(service, PowerElectronicsConnectionPhase, writer.save_power_electronics_connection_phase)
        status = status and self._save_all(service, PowerTransformer, writer.save_power_transformer)
        status = status and self._save_all(service, PowerTransformerEnd, writer.save_power_transformer_end)
        status = status and self._save_all(service, RatioTapChanger, writer.save_ratio_tap_changer)
        status = status and self._save_all(service, Recloser, writer.save_recloser)
        status = status and self._save_all(service, TransformerStarImpedance, writer.save_transformer_star_impedance)
        status = status and self._save_all(service, Circuit, writer.save_circuit)
        status = status and self._save_all(service, Loop, writer.save_loop)
        status = status and self._save_all(service, LvFeeder, writer.save_lv_feeder)
        status = status and self._save_all(service, Analog, writer.save_analog)
        status = status and self._save_all(service, Accumulator, writer.save_accumulator)
        status = status and self._save_all(service, Discrete, writer.save_discrete)
        status = status and self._save_all(service, Control, writer.save_control)
        status = status and self._save_all(service, RemoteControl, writer.save_remote_control)
        status = status and self._save_all(service, RemoteSource, writer.save_remote_source)

        return status
