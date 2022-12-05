#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.protobuf.cim.iec61968.assetinfo.CableInfo_pb2 import CableInfo
from zepben.protobuf.cim.iec61968.assetinfo.NoLoadTest_pb2 import NoLoadTest
from zepben.protobuf.cim.iec61968.assetinfo.OpenCircuitTest_pb2 import OpenCircuitTest
from zepben.protobuf.cim.iec61968.assetinfo.OverheadWireInfo_pb2 import OverheadWireInfo
from zepben.protobuf.cim.iec61968.assetinfo.PowerTransformerInfo_pb2 import PowerTransformerInfo
from zepben.protobuf.cim.iec61968.assetinfo.ShortCircuitTest_pb2 import ShortCircuitTest
from zepben.protobuf.cim.iec61968.assetinfo.ShuntCompensatorInfo_pb2 import ShuntCompensatorInfo
from zepben.protobuf.cim.iec61968.assetinfo.TransformerEndInfo_pb2 import TransformerEndInfo
from zepben.protobuf.cim.iec61968.assetinfo.TransformerTankInfo_pb2 import TransformerTankInfo
from zepben.protobuf.cim.iec61968.assetinfo.TransformerTest_pb2 import TransformerTest
from zepben.protobuf.cim.iec61968.assetinfo.WireInfo_pb2 import WireInfo
from zepben.protobuf.cim.iec61968.assets.AssetContainer_pb2 import AssetContainer
from zepben.protobuf.cim.iec61968.assets.AssetInfo_pb2 import AssetInfo
from zepben.protobuf.cim.iec61968.assets.AssetOrganisationRole_pb2 import AssetOrganisationRole
from zepben.protobuf.cim.iec61968.assets.AssetOwner_pb2 import AssetOwner
from zepben.protobuf.cim.iec61968.assets.Asset_pb2 import Asset
from zepben.protobuf.cim.iec61968.assets.Pole_pb2 import Pole
from zepben.protobuf.cim.iec61968.assets.Streetlight_pb2 import Streetlight
from zepben.protobuf.cim.iec61968.assets.Structure_pb2 import Structure
from zepben.protobuf.cim.iec61968.common.Location_pb2 import Location
from zepben.protobuf.cim.iec61968.infiec61968.infassetinfo.CurrentTransformerInfo_pb2 import CurrentTransformerInfo
from zepben.protobuf.cim.iec61968.infiec61968.infassetinfo.PotentialTransformerInfo_pb2 import PotentialTransformerInfo
from zepben.protobuf.cim.iec61968.metering.EndDevice_pb2 import EndDevice
from zepben.protobuf.cim.iec61968.metering.Meter_pb2 import Meter
from zepben.protobuf.cim.iec61968.metering.UsagePoint_pb2 import UsagePoint
from zepben.protobuf.cim.iec61968.operations.OperationalRestriction_pb2 import OperationalRestriction
from zepben.protobuf.cim.iec61970.base.auxiliaryequipment.AuxiliaryEquipment_pb2 import AuxiliaryEquipment
from zepben.protobuf.cim.iec61970.base.auxiliaryequipment.CurrentTransformer_pb2 import CurrentTransformer
from zepben.protobuf.cim.iec61970.base.auxiliaryequipment.FaultIndicator_pb2 import FaultIndicator
from zepben.protobuf.cim.iec61970.base.auxiliaryequipment.PotentialTransformer_pb2 import PotentialTransformer
from zepben.protobuf.cim.iec61970.base.auxiliaryequipment.Sensor_pb2 import Sensor
from zepben.protobuf.cim.iec61970.base.core.AcDcTerminal_pb2 import AcDcTerminal
from zepben.protobuf.cim.iec61970.base.core.BaseVoltage_pb2 import BaseVoltage
from zepben.protobuf.cim.iec61970.base.core.ConductingEquipment_pb2 import ConductingEquipment
from zepben.protobuf.cim.iec61970.base.core.ConnectivityNodeContainer_pb2 import ConnectivityNodeContainer
from zepben.protobuf.cim.iec61970.base.core.ConnectivityNode_pb2 import ConnectivityNode
from zepben.protobuf.cim.iec61970.base.core.EquipmentContainer_pb2 import EquipmentContainer
from zepben.protobuf.cim.iec61970.base.core.Equipment_pb2 import Equipment
from zepben.protobuf.cim.iec61970.base.core.Feeder_pb2 import Feeder
from zepben.protobuf.cim.iec61970.base.core.GeographicalRegion_pb2 import GeographicalRegion
from zepben.protobuf.cim.iec61970.base.core.IdentifiedObject_pb2 import IdentifiedObject
from zepben.protobuf.cim.iec61970.base.core.PowerSystemResource_pb2 import PowerSystemResource
from zepben.protobuf.cim.iec61970.base.core.Site_pb2 import Site
from zepben.protobuf.cim.iec61970.base.core.SubGeographicalRegion_pb2 import SubGeographicalRegion
from zepben.protobuf.cim.iec61970.base.core.Substation_pb2 import Substation
from zepben.protobuf.cim.iec61970.base.core.Terminal_pb2 import Terminal
from zepben.protobuf.cim.iec61970.base.equivalents.EquivalentBranch_pb2 import EquivalentBranch
from zepben.protobuf.cim.iec61970.base.equivalents.EquivalentEquipment_pb2 import EquivalentEquipment
from zepben.protobuf.cim.iec61970.base.meas.Accumulator_pb2 import Accumulator
from zepben.protobuf.cim.iec61970.base.meas.Analog_pb2 import Analog
from zepben.protobuf.cim.iec61970.base.meas.Control_pb2 import Control
from zepben.protobuf.cim.iec61970.base.meas.Discrete_pb2 import Discrete
from zepben.protobuf.cim.iec61970.base.meas.IoPoint_pb2 import IoPoint
from zepben.protobuf.cim.iec61970.base.meas.Measurement_pb2 import Measurement
from zepben.protobuf.cim.iec61970.base.scada.RemoteControl_pb2 import RemoteControl
from zepben.protobuf.cim.iec61970.base.scada.RemotePoint_pb2 import RemotePoint
from zepben.protobuf.cim.iec61970.base.scada.RemoteSource_pb2 import RemoteSource
from zepben.protobuf.cim.iec61970.base.wires.AcLineSegment_pb2 import AcLineSegment
from zepben.protobuf.cim.iec61970.base.wires.Breaker_pb2 import Breaker
from zepben.protobuf.cim.iec61970.base.wires.BusbarSection_pb2 import BusbarSection
from zepben.protobuf.cim.iec61970.base.wires.Conductor_pb2 import Conductor
from zepben.protobuf.cim.iec61970.base.wires.Connector_pb2 import Connector
from zepben.protobuf.cim.iec61970.base.wires.Disconnector_pb2 import Disconnector
from zepben.protobuf.cim.iec61970.base.wires.EnergyConnection_pb2 import EnergyConnection
from zepben.protobuf.cim.iec61970.base.wires.EnergyConsumerPhase_pb2 import EnergyConsumerPhase
from zepben.protobuf.cim.iec61970.base.wires.EnergyConsumer_pb2 import EnergyConsumer
from zepben.protobuf.cim.iec61970.base.wires.EnergySourcePhase_pb2 import EnergySourcePhase
from zepben.protobuf.cim.iec61970.base.wires.EnergySource_pb2 import EnergySource
from zepben.protobuf.cim.iec61970.base.wires.Fuse_pb2 import Fuse
from zepben.protobuf.cim.iec61970.base.wires.Jumper_pb2 import Jumper
from zepben.protobuf.cim.iec61970.base.wires.Junction_pb2 import Junction
from zepben.protobuf.cim.iec61970.base.wires.Line_pb2 import Line
from zepben.protobuf.cim.iec61970.base.wires.LinearShuntCompensator_pb2 import LinearShuntCompensator
from zepben.protobuf.cim.iec61970.base.wires.LoadBreakSwitch_pb2 import LoadBreakSwitch
from zepben.protobuf.cim.iec61970.base.wires.PerLengthImpedance_pb2 import PerLengthImpedance
from zepben.protobuf.cim.iec61970.base.wires.PerLengthLineParameter_pb2 import PerLengthLineParameter
from zepben.protobuf.cim.iec61970.base.wires.PerLengthSequenceImpedance_pb2 import PerLengthSequenceImpedance
from zepben.protobuf.cim.iec61970.base.wires.PowerElectronicsConnectionPhase_pb2 import PowerElectronicsConnectionPhase
from zepben.protobuf.cim.iec61970.base.wires.PowerElectronicsConnection_pb2 import PowerElectronicsConnection
from zepben.protobuf.cim.iec61970.base.wires.PowerTransformerEnd_pb2 import PowerTransformerEnd
from zepben.protobuf.cim.iec61970.base.wires.PowerTransformer_pb2 import PowerTransformer
from zepben.protobuf.cim.iec61970.base.wires.ProtectedSwitch_pb2 import ProtectedSwitch
from zepben.protobuf.cim.iec61970.base.wires.RatioTapChanger_pb2 import RatioTapChanger
from zepben.protobuf.cim.iec61970.base.wires.Recloser_pb2 import Recloser
from zepben.protobuf.cim.iec61970.base.wires.RegulatingCondEq_pb2 import RegulatingCondEq
from zepben.protobuf.cim.iec61970.base.wires.ShuntCompensator_pb2 import ShuntCompensator
from zepben.protobuf.cim.iec61970.base.wires.Switch_pb2 import Switch
from zepben.protobuf.cim.iec61970.base.wires.TapChanger_pb2 import TapChanger
from zepben.protobuf.cim.iec61970.base.wires.TransformerEnd_pb2 import TransformerEnd
from zepben.protobuf.cim.iec61970.base.wires.TransformerStarImpedance_pb2 import TransformerStarImpedance
from zepben.protobuf.cim.iec61970.base.wires.generation.production.BatteryUnit_pb2 import BatteryUnit
from zepben.protobuf.cim.iec61970.base.wires.generation.production.PhotoVoltaicUnit_pb2 import PhotoVoltaicUnit
from zepben.protobuf.cim.iec61970.base.wires.generation.production.PowerElectronicsUnit_pb2 import PowerElectronicsUnit
from zepben.protobuf.cim.iec61970.base.wires.generation.production.PowerElectronicsWindUnit_pb2 import PowerElectronicsWindUnit
from zepben.protobuf.cim.iec61970.infiec61970.feeder.Circuit_pb2 import Circuit
from zepben.protobuf.cim.iec61970.infiec61970.feeder.Loop_pb2 import Loop
from zepben.protobuf.cim.iec61970.infiec61970.feeder.LvFeeder_pb2 import LvFeeder

__all__ = []


CableInfo.mrid = lambda self: self.wi.mrid()
NoLoadTest.mrid = lambda self: self.tt.mrid()
OpenCircuitTest.mrid = lambda self: self.tt.mrid()
OverheadWireInfo.mrid = lambda self: self.wi.mrid()
PowerTransformerInfo.mrid = lambda self: self.ai.mrid()
ShortCircuitTest.mrid = lambda self: self.tt.mrid()
ShuntCompensatorInfo.mrid = lambda self: self.ai.mrid()
TransformerEndInfo.mrid = lambda self: self.ai.mrid()
TransformerTankInfo.mrid = lambda self: self.ai.mrid()
TransformerTest.mrid = lambda self: self.io.mrid()
TransformerStarImpedance.mrid = lambda self: self.io.mrid()
WireInfo.mrid = lambda self: self.ai.mrid()
Asset.mrid = lambda self: self.io.mrid()
AssetContainer.mrid = lambda self: self.at.mrid()
AssetInfo.mrid = lambda self: self.io.mrid()
AssetOrganisationRole.mrid = lambda self: getattr(self, "or").mrid()
AssetOwner.mrid = lambda self: self.aor.mrid()
Pole.mrid = lambda self: self.st.mrid()
Streetlight.mrid = lambda self: self.at.mrid()
Structure.mrid = lambda self: self.ac.mrid()
Location.mrid = lambda self: self.io.mrid()
CurrentTransformerInfo.mrid = lambda self: self.ai.mrid()
PotentialTransformerInfo.mrid = lambda self: self.ai.mrid()
EndDevice.mrid = lambda self: self.ac.mrid()
Meter.mrid = lambda self: self.ed.mrid()
UsagePoint.mrid = lambda self: self.io.mrid()
OperationalRestriction.mrid = lambda self: self.doc.mrid()
AuxiliaryEquipment.mrid = lambda self: self.eq.mrid()
CurrentTransformer.mrid = lambda self: self.sn.mrid()
FaultIndicator.mrid = lambda self: self.ae.mrid()
PotentialTransformer.mrid = lambda self: self.sn.mrid()
Sensor.mrid = lambda self: self.ae.mrid()
AcDcTerminal.mrid = lambda self: self.io.mrid()
BaseVoltage.mrid = lambda self: self.io.mrid()
ConductingEquipment.mrid = lambda self: self.eq.mrid()
ConnectivityNode.mrid = lambda self: self.io.mrid()
ConnectivityNodeContainer.mrid = lambda self: self.psr.mrid()
Equipment.mrid = lambda self: self.psr.mrid()
EquipmentContainer.mrid = lambda self: self.cnc.mrid()
Feeder.mrid = lambda self: self.ec.mrid()
GeographicalRegion.mrid = lambda self: self.io.mrid()
IdentifiedObject.mrid = lambda self: self.mRID
PowerSystemResource.mrid = lambda self: self.io.mrid()
Site.mrid = lambda self: self.ec.mrid()
SubGeographicalRegion.mrid = lambda self: self.io.mrid()
Substation.mrid = lambda self: self.ec.mrid()
Terminal.mrid = lambda self: self.ad.mrid()
EquivalentBranch.mrid = lambda self: self.ee.mrid()
EquivalentEquipment.mrid = lambda self: self.ce.mrid()
Accumulator.mrid = lambda self: self.measurement.mrid()
Analog.mrid = lambda self: self.measurement.mrid()
Discrete.mrid = lambda self: self.measurement.mrid()
Control.mrid = lambda self: self.ip.mrid()
IoPoint.mrid = lambda self: self.io.mrid()
Measurement.mrid = lambda self: self.io.mrid()
RemoteControl.mrid = lambda self: self.rp.mrid()
RemotePoint.mrid = lambda self: self.io.mrid()
RemoteSource.mrid = lambda self: self.rp.mrid()
BatteryUnit.mrid = lambda self: self.peu.mrid()
PhotoVoltaicUnit.mrid = lambda self: self.peu.mrid()
PowerElectronicsUnit.mrid = lambda self: self.eq.mrid()
PowerElectronicsWindUnit.mrid = lambda self: self.peu.mrid()
AcLineSegment.mrid = lambda self: self.cd.mrid()
Breaker.mrid = lambda self: self.sw.mrid()
BusbarSection.mrid = lambda self: self.cn.mrid()
Conductor.mrid = lambda self: self.ce.mrid()
Connector.mrid = lambda self: self.ce.mrid()
Disconnector.mrid = lambda self: self.sw.mrid()
EnergyConnection.mrid = lambda self: self.ce.mrid()
EnergyConsumer.mrid = lambda self: self.ec.mrid()
EnergyConsumerPhase.mrid = lambda self: self.psr.mrid()
EnergySource.mrid = lambda self: self.ec.mrid()
EnergySourcePhase.mrid = lambda self: self.psr.mrid()
Fuse.mrid = lambda self: self.sw.mrid()
Jumper.mrid = lambda self: self.sw.mrid()
Junction.mrid = lambda self: self.cn.mrid()
Line.mrid = lambda self: self.ec.mrid()
LinearShuntCompensator.mrid = lambda self: self.sc.mrid()
LoadBreakSwitch.mrid = lambda self: self.ps.mrid()
PerLengthImpedance.mrid = lambda self: self.lp.mrid()
PerLengthLineParameter.mrid = lambda self: self.io.mrid()
PerLengthSequenceImpedance.mrid = lambda self: self.pli.mrid()
PowerTransformer.mrid = lambda self: self.ce.mrid()
PowerElectronicsConnection.mrid = lambda self: self.rce.mrid()
PowerElectronicsConnectionPhase.mrid = lambda self: self.psr.mrid()
PowerTransformerEnd.mrid = lambda self: self.te.mrid()
ProtectedSwitch.mrid = lambda self: self.sw.mrid()
RatioTapChanger.mrid = lambda self: self.tc.mrid()
Recloser.mrid = lambda self: self.sw.mrid()
RegulatingCondEq.mrid = lambda self: self.ec.mrid()
ShuntCompensator.mrid = lambda self: self.rce.mrid()
Switch.mrid = lambda self: self.ce.mrid()
TapChanger.mrid = lambda self: self.psr.mrid()
TransformerEnd.mrid = lambda self: self.io.mrid()
Loop.mrid = lambda self: self.io.mrid()
Circuit.mrid = lambda self: self.l.mrid()
LvFeeder.mrid = lambda self: self.ec.mrid()

PowerSystemResource.name_and_mrid = lambda self: self.io.name_and_mrid()
ConductingEquipment.name_and_mrid = lambda self: self.eq.name_and_mrid()
Equipment.name_and_mrid = lambda self: self.psr.name_and_mrid()
ConnectivityNodeContainer.name_and_mrid = lambda self: self.psr.name_and_mrid()
EquipmentContainer.name_and_mrid = lambda self: self.cnc.name_and_mrid()
Feeder.name_and_mrid = lambda self: self.ec.name_and_mrid()
EnergyConsumerPhase.name_and_mrid = lambda self: self.psr.name_and_mrid()
EnergySourcePhase.name_and_mrid = lambda self: self.psr.name_and_mrid()
PowerTransformerEnd.name_and_mrid = lambda self: self.te.name_and_mrid()
AcDcTerminal.name_and_mrid = lambda self: self.io.name_and_mrid()
TransformerEnd.name_and_mrid = lambda self: self.io.name_and_mrid()
Terminal.name_and_mrid = lambda self: self.ad.name_and_mrid()
PowerTransformerInfo.name_and_mrid = lambda self: self.ce.eq.psr.io.name_and_mrid()

# location_mrid
PowerSystemResource.location_mrid = lambda self: getattr(self, "locationMRID", None)
Equipment.location_mrid = lambda self: self.psr.location_mrid()
AuxiliaryEquipment.location_mrid = lambda self: self.eq.location_mrid()
FaultIndicator.location_mrid = lambda self: self.ae.location_mrid()
ConductingEquipment.location_mrid = lambda self: self.eq.location_mrid()
Conductor.location_mrid = lambda self: self.ce.location_mrid()
Connector.location_mrid = lambda self: self.ce.location_mrid()
EnergyConnection.location_mrid = lambda self: self.ce.location_mrid()
PowerTransformer.location_mrid = lambda self: self.ce.location_mrid()
Switch.location_mrid = lambda self: self.ce.location_mrid()
AcLineSegment.location_mrid = lambda self: self.cd.location_mrid()
Junction.location_mrid = lambda self: self.cn.location_mrid()
EnergyConsumer.location_mrid = lambda self: self.ec.location_mrid()
EnergySource.location_mrid = lambda self: self.ec.location_mrid()
RegulatingCondEq.location_mrid = lambda self: self.ec.location_mrid()
Disconnector.location_mrid = lambda self: self.sw.location_mrid()
Fuse.location_mrid = lambda self: self.sw.location_mrid()
Jumper.location_mrid = lambda self: self.sw.location_mrid()
ProtectedSwitch.location_mrid = lambda self: self.sw.location_mrid()
ShuntCompensator.location_mrid = lambda self: self.rce.location_mrid()
Breaker.location_mrid = lambda self: self.sw.location_mrid()
Recloser.location_mrid = lambda self: self.sw.location_mrid()
LinearShuntCompensator.location_mrid = lambda self: self.sc.location_mrid()

# service_location_mrid
EndDevice.service_location_mrid = lambda self: getattr(self, "serviceLocationMRID", None)
Meter.service_location_mrid = lambda self: self.ed.service_location_mrid()

# usage_point_location_mrid
UsagePoint.usage_point_location_mrid = lambda self: getattr(self, "usagePointLocationMRID", None)

# terminal_mrid
AuxiliaryEquipment.terminal_mrid = lambda self: getattr(self, "terminalMRID", None)
FaultIndicator.terminal_mrid = lambda self: self.ae.terminal_mrid()

# terminal_mrids
ConductingEquipment.terminal_mrids = lambda self: getattr(self, "terminalMRIDs", [])
Conductor.terminal_mrids = lambda self: self.ce.terminal_mrids()
Connector.terminal_mrids = lambda self: self.ce.terminal_mrids()
EnergyConnection.terminal_mrids = lambda self: self.ce.terminal_mrids()
PowerTransformer.terminal_mrids = lambda self: self.ce.terminal_mrids()
Switch.terminal_mrids = lambda self: self.ce.terminal_mrids()
AcLineSegment.terminal_mrids = lambda self: self.cd.terminal_mrids()
Junction.terminal_mrids = lambda self: self.cn.terminal_mrids()
EnergyConsumer.terminal_mrids = lambda self: self.ec.terminal_mrids()
EnergySource.terminal_mrids = lambda self: self.ec.terminal_mrids()
RegulatingCondEq.terminal_mrids = lambda self: self.ec.terminal_mrids()
Disconnector.terminal_mrids = lambda self: self.sw.terminal_mrids()
Fuse.terminal_mrids = lambda self: self.sw.terminal_mrids()
Jumper.terminal_mrids = lambda self: self.sw.terminal_mrids()
ProtectedSwitch.terminal_mrids = lambda self: self.sw.terminal_mrids()
ShuntCompensator.terminal_mrids = lambda self: self.rce.terminal_mrids()
Breaker.terminal_mrids = lambda self: self.sw.terminal_mrids()
Recloser.terminal_mrids = lambda self: self.sw.terminal_mrids()
LinearShuntCompensator.terminal_mrids = lambda self: self.sc.terminal_mrids()

# base_voltage_mrid
ConductingEquipment.base_voltage_mrid = lambda self: getattr(self, "baseVoltageMRID", None)
Conductor.base_voltage_mrid = lambda self: self.ce.base_voltage_mrid()
Connector.base_voltage_mrid = lambda self: self.ce.base_voltage_mrid()
EnergyConnection.base_voltage_mrid = lambda self: self.ce.base_voltage_mrid()
PowerTransformer.base_voltage_mrid = lambda self: self.ce.base_voltage_mrid()
Switch.base_voltage_mrid = lambda self: self.ce.base_voltage_mrid()
AcLineSegment.base_voltage_mrid = lambda self: self.cd.base_voltage_mrid()
Junction.base_voltage_mrid = lambda self: self.cn.base_voltage_mrid()
EnergyConsumer.base_voltage_mrid = lambda self: self.ec.base_voltage_mrid()
EnergySource.base_voltage_mrid = lambda self: self.ec.base_voltage_mrid()
RegulatingCondEq.base_voltage_mrid = lambda self: self.ec.base_voltage_mrid()
Disconnector.base_voltage_mrid = lambda self: self.sw.base_voltage_mrid()
Fuse.base_voltage_mrid = lambda self: self.sw.base_voltage_mrid()
Jumper.base_voltage_mrid = lambda self: self.sw.base_voltage_mrid()
ProtectedSwitch.base_voltage_mrid = lambda self: self.sw.base_voltage_mrid()
ShuntCompensator.base_voltage_mrid = lambda self: self.rce.base_voltage_mrid()
Breaker.base_voltage_mrid = lambda self: self.sw.base_voltage_mrid()
Recloser.base_voltage_mrid = lambda self: self.sw.base_voltage_mrid()
LinearShuntCompensator.base_voltage_mrid = lambda self: self.sc.base_voltage_mrid()

# normal_energizing_substation_mrid
Feeder.normal_energizing_substation_mrid = lambda self: getattr(self, "normalEnergizingSubstationMRID", None)

# per_length_sequence_impedance_mrid
AcLineSegment.per_length_sequence_impedance_mrid = lambda self: getattr(self, "perLengthSequenceImpedanceMRID", None)

# asset_info_mrid
ConductingEquipment.asset_info_mrid = lambda self: self.eq.asset_info_mrid()
Conductor.asset_info_mrid = lambda self: self.ce.asset_info_mrid()
CurrentTransformer.asset_info_mrid = lambda self: self.sn.ae.eq.asset_info_mrid()
Equipment.asset_info_mrid = lambda self: self.psr.assetInfoMRID
PotentialTransformer.asset_info_mrid = lambda self: self.sn.ae.eq.asset_info_mrid()
PowerTransformer.asset_info_mrid = lambda self: self.ce.asset_info_mrid()
ShuntCompensator.asset_info_mrid = lambda self: self.rce.ec.ce.asset_info_mrid()

# ratio_tap_changer_mrid
TransformerEnd.ratio_tap_changer_mrid = lambda self: getattr(self, "ratioTapChangerMRID", None)
PowerTransformerEnd.ratio_tap_changer_mrid = lambda self: self.te.ratio_tap_changer_mrid()
