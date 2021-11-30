#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Type, TypeVar

from zepben.evolve import NetworkService, IdentifiedObject, CableInfo, OverheadWireInfo, PowerTransformerInfo, TransformerTankInfo, NoLoadTest, OpenCircuitTest, \
    ShortCircuitTest, ShuntCompensatorInfo, TransformerEndInfo, AssetOwner, Pole, Streetlight, Location, Organisation, Meter, UsagePoint, \
    OperationalRestriction, FaultIndicator, BaseVoltage, ConnectivityNode, Feeder, GeographicalRegion, Site, SubGeographicalRegion, Substation, Terminal, \
    EquivalentBranch, PhotoVoltaicUnit, AcLineSegment, Breaker, LoadBreakSwitch, BusbarSection, Disconnector, EnergyConsumer, EnergyConsumerPhase, EnergySource, \
    EnergySourcePhase, Fuse, Jumper, Junction, LinearShuntCompensator, PerLengthSequenceImpedance, PowerElectronicsConnection, PowerElectronicsConnectionPhase, \
    PowerTransformer, PowerTransformerEnd, RatioTapChanger, Recloser, TransformerStarImpedance, Circuit, Loop, Analog, Accumulator, Discrete, Control, \
    RemoteControl, RemoteSource
from zepben.evolve.database.sqlite.writers.base_service_writer import BaseServiceWriter
from zepben.evolve.database.sqlite.writers.network_cim_writer import NetworkCIMWriter

T = TypeVar("T", bound=IdentifiedObject)

class NetworkServiceWriter(BaseServiceWriter):

    def save(self, service: NetworkService, writer: NetworkCIMWriter) -> bool:
        status = super(NetworkServiceWriter, self).save(service, writer)

        for obj in service.objects(CableInfo):
            status = status and self.validate_save(obj, writer.save_cable_info)
        for obj in service.objects(OverheadWireInfo):
            status = status and self.validate_save(obj, writer.save_overhead_wire_info)
        for obj in service.objects(PowerTransformerInfo):
            status = status and self.validate_save(obj, writer.save_power_transformer_info)
        for obj in service.objects(TransformerTankInfo):
            status = status and self.validate_save(obj, writer.save_transformer_tank_info)
        for obj in service.objects(NoLoadTest):
            status = status and self.validate_save(obj, writer.save_no_load_test)
        for obj in service.objects(OpenCircuitTest):
            status = status and self.validate_save(obj, writer.save_open_circuit_test)
        for obj in service.objects(ShortCircuitTest):
            status = status and self.validate_save(obj, writer.save_short_circuit_test)
        for obj in service.objects(ShuntCompensatorInfo):
            status = status and self.validate_save(obj, writer.save_shunt_compensator_info)
        for obj in service.objects(TransformerEndInfo):
            status = status and self.validate_save(obj, writer.save_transformer_end_info)
        for obj in service.objects(AssetOwner):
            status = status and self.validate_save(obj, writer.save_asset_owner)
        for obj in service.objects(Pole):
            status = status and self.validate_save(obj, writer.save_pole)
        for obj in service.objects(Streetlight):
            status = status and self.validate_save(obj, writer.save_streetlight)
        for obj in service.objects(Location):
            status = status and self.validate_save(obj, writer.save_location)
        for obj in service.objects(Organisation):
            status = status and self.validate_save(obj, writer.save_organisation)
        for obj in service.objects(Meter):
            status = status and self.validate_save(obj, writer.save_meter)
        for obj in service.objects(UsagePoint):
            status = status and self.validate_save(obj, writer.save_usage_point)
        for obj in service.objects(OperationalRestriction):
            status = status and self.validate_save(obj, writer.save_operational_restriction)
        for obj in service.objects(FaultIndicator):
            status = status and self.validate_save(obj, writer.save_fault_indicator)
        for obj in service.objects(BaseVoltage):
            status = status and self.validate_save(obj, writer.save_base_voltage)
        for obj in service.objects(ConnectivityNode):
            status = status and self.validate_save(obj, writer.save_connectivity_node)
        for obj in service.objects(Feeder):
            status = status and self.validate_save(obj, writer.save_feeder)
        for obj in service.objects(GeographicalRegion):
            status = status and self.validate_save(obj, writer.save_geographical_region)
        for obj in service.objects(Site):
            status = status and self.validate_save(obj, writer.save_site)
        for obj in service.objects(SubGeographicalRegion):
            status = status and self.validate_save(obj, writer.save_sub_geographical_region)
        for obj in service.objects(Substation):
            status = status and self.validate_save(obj, writer.save_substation)
        for obj in service.objects(Terminal):
            status = status and self.validate_save(obj, writer.save_terminal)
        for obj in service.objects(EquivalentBranch):
            status = status and self.validate_save(obj, writer.save_equivalent_branch)
        for obj in service.objects(PhotoVoltaicUnit):
            status = status and self.validate_save(obj, writer.save_photovoltaic_unit)
        for obj in service.objects(AcLineSegment):
            status = status and self.validate_save(obj, writer.save_ac_line_segment)
        for obj in service.objects(Breaker):
            status = status and self.validate_save(obj, writer.save_breaker)
        for obj in service.objects(LoadBreakSwitch):
            status = status and self.validate_save(obj, writer.save_load_break_switch)
        for obj in service.objects(BusbarSection):
            status = status and self.validate_save(obj, writer.save_bus_bar_section)
        for obj in service.objects(Disconnector):
            status = status and self.validate_save(obj, writer.save_disconnector)
        for obj in service.objects(EnergyConsumer):
            status = status and self.validate_save(obj, writer.save_energy_consumer)
        for obj in service.objects(EnergyConsumerPhase):
            status = status and self.validate_save(obj, writer.save_EnergyConsumerPhase)
        for obj in service.objects(EnergySource):
            status = status and self.validate_save(obj, writer.save_EnergySource)
        for obj in service.objects(EnergySourcePhase):
            status = status and self.validate_save(obj, writer.save_EnergySourcePhase)
        for obj in service.objects(Fuse):
            status = status and self.validate_save(obj, writer.save_Fuse)
        for obj in service.objects(Jumper):
            status = status and self.validate_save(obj, writer.save_Jumper)
        for obj in service.objects(Junction):
            status = status and self.validate_save(obj, writer.save_Junction)
        for obj in service.objects(LinearShuntCompensator):
            status = status and self.validate_save(obj, writer.save_LinearShuntCompensator)
        for obj in service.objects(PerLengthSequenceImpedance):
            status = status and self.validate_save(obj, writer.save_PerLengthSequenceImpedance)
        for obj in service.objects(PowerElectronicsConnection):
            status = status and self.validate_save(obj, writer.save_PowerElectronicsConnection)
        for obj in service.objects(PowerElectronicsConnectionPhase):
            status = status and self.validate_save(obj, writer.save_PowerElectronicsConnectionPhase)
        for obj in service.objects(PowerTransformer):
            status = status and self.validate_save(obj, writer.save_PowerTransformer)
        for obj in service.objects(PowerTransformerEnd):
            status = status and self.validate_save(obj, writer.save_PowerTransformerEnd)
        for obj in service.objects(RatioTapChanger):
            status = status and self.validate_save(obj, writer.save_RatioTapChanger)
        for obj in service.objects(Recloser):
            status = status and self.validate_save(obj, writer.save_Recloser)
        for obj in service.objects(TransformerStarImpedance):
            status = status and self.validate_save(obj, writer.save_TransformerStarImpedance)
        for obj in service.objects(Circuit):
            status = status and self.validate_save(obj, writer.save_Circuit)
        for obj in service.objects(Loop):
            status = status and self.validate_save(obj, writer.save_Loop)
        for obj in service.objects(Analog):
            status = status and self.validate_save(obj, writer.save_Analog)
        for obj in service.objects(Accumulator):
            status = status and self.validate_save(obj, writer.save_Accumulator)
        for obj in service.objects(Discrete):
            status = status and self.validate_save(obj, writer.save_Discrete)
        for obj in service.objects(Control):
            status = status and self.validate_save(obj, writer.save_Control)
        for obj in service.objects(RemoteControl):
            status = status and self.validate_save(obj, writer.save_RemoteControl)
        for obj in service.objects(RemoteSource):
            status = status and self.validate_save(obj, writer.save_RemoteSource)

        return status




