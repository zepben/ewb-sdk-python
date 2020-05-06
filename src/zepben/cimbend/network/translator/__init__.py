"""
Copyright 2019 Zeppelin Bend Pty Ltd
This file is part of cimbend.

cimbend is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

cimbend is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with cimbend.  If not, see <https://www.gnu.org/licenses/>.
"""


from zepben.protobuf.cim.iec61968.assetinfo.CableInfo_pb2 import CableInfo
from zepben.protobuf.cim.iec61968.assetinfo.WireInfo_pb2 import WireInfo
from zepben.protobuf.cim.iec61968.assetinfo.OverheadWireInfo_pb2 import OverheadWireInfo
from zepben.protobuf.cim.iec61968.assets.AssetContainer_pb2 import AssetContainer
from zepben.protobuf.cim.iec61968.assets.AssetInfo_pb2 import AssetInfo
from zepben.protobuf.cim.iec61968.assets.AssetOrganisationRole_pb2 import AssetOrganisationRole
from zepben.protobuf.cim.iec61968.assets.AssetOwner_pb2 import AssetOwner
from zepben.protobuf.cim.iec61968.assets.Asset_pb2 import Asset
from zepben.protobuf.cim.iec61968.common.Location_pb2 import Location
from zepben.protobuf.cim.iec61968.metering.EndDevice_pb2 import EndDevice
from zepben.protobuf.cim.iec61968.metering.Meter_pb2 import Meter
from zepben.protobuf.cim.iec61968.metering.UsagePoint_pb2 import UsagePoint
from zepben.protobuf.cim.iec61968.operations.OperationalRestriction_pb2 import OperationalRestriction
from zepben.protobuf.cim.iec61970.base.auxiliaryequipment.AuxiliaryEquipment_pb2 import AuxiliaryEquipment
from zepben.protobuf.cim.iec61970.base.auxiliaryequipment.FaultIndicator_pb2 import FaultIndicator
from zepben.protobuf.cim.iec61970.base.core.AcDcTerminal_pb2 import AcDcTerminal
from zepben.protobuf.cim.iec61970.base.core.BaseVoltage_pb2 import BaseVoltage
from zepben.protobuf.cim.iec61970.base.core.ConductingEquipment_pb2 import ConductingEquipment
from zepben.protobuf.cim.iec61970.base.core.ConnectivityNodeContainer_pb2 import ConnectivityNodeContainer
from zepben.protobuf.cim.iec61970.base.core.ConnectivityNode_pb2 import ConnectivityNode
from zepben.protobuf.cim.iec61970.base.core.EquipmentContainer_pb2 import EquipmentContainer
from zepben.protobuf.cim.iec61970.base.core.Equipment_pb2 import Equipment
from zepben.protobuf.cim.iec61970.base.core.Feeder_pb2 import Feeder
from zepben.protobuf.cim.iec61970.base.core.GeographicalRegion_pb2 import GeographicalRegion
from zepben.protobuf.cim.iec61970.base.core.PowerSystemResource_pb2 import PowerSystemResource
from zepben.protobuf.cim.iec61970.base.core.Site_pb2 import Site
from zepben.protobuf.cim.iec61970.base.core.SubGeographicalRegion_pb2 import SubGeographicalRegion
from zepben.protobuf.cim.iec61970.base.core.Substation_pb2 import Substation
from zepben.protobuf.cim.iec61970.base.core.Terminal_pb2 import Terminal
from zepben.protobuf.cim.iec61970.base.wires.AcLineSegment_pb2 import AcLineSegment
from zepben.protobuf.cim.iec61970.base.wires.Breaker_pb2 import Breaker
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
from zepben.protobuf.cim.iec61970.base.wires.LinearShuntCompensator_pb2 import LinearShuntCompensator
from zepben.protobuf.cim.iec61970.base.wires.PerLengthImpedance_pb2 import PerLengthImpedance
from zepben.protobuf.cim.iec61970.base.wires.PerLengthLineParameter_pb2 import PerLengthLineParameter
from zepben.protobuf.cim.iec61970.base.wires.PerLengthSequenceImpedance_pb2 import PerLengthSequenceImpedance
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
from zepben.cimbend.network.translator.network_proto2cim import *
__all__ = ["network_proto2cim.py"]

CableInfo.mrid = lambda self: self.wi.mrid()
OverheadWireInfo.mrid = lambda self: self.wi.mrid()
WireInfo.mrid = lambda self: self.ai.mrid()
Asset.mrid = lambda self: self.io.mRID
AssetContainer.mrid = lambda self: self.at.mrid()
AssetInfo.mrid = lambda self: self.io.mRID
AssetOrganisationRole.mrid = lambda self: getattr(self, "or").mrid()
AssetOwner.mrid = lambda self: self.aor.mrid()
Location.mrid = lambda self: self.io.mRID
EndDevice.mrid = lambda self: self.ac.mrid()
Meter.mrid = lambda self: self.ed.mrid()
UsagePoint.mrid = lambda self: self.io.mRID
OperationalRestriction.mrid = lambda self: self.doc.mrid()
AuxiliaryEquipment.mrid = lambda self: self.eq.mrid()
FaultIndicator.mrid = lambda self: self.ae.mrid()
AcDcTerminal.mrid = lambda self: self.io.mRID
BaseVoltage.mrid = lambda self: self.io.mRID
ConductingEquipment.mrid = lambda self: self.eq.mrid()
ConnectivityNode.mrid = lambda self: self.io.mRID
ConnectivityNodeContainer.mrid = lambda self: self.psr.mrid()
Equipment.mrid = lambda self: self.psr.mrid()
EquipmentContainer.mrid = lambda self: self.crc.mrid()
Feeder.mrid = lambda self: self.ec.mrid()
GeographicalRegion.mrid = lambda self: self.io.mRID
PowerSystemResource.mrid = lambda self: self.io.mRID
Site.mrid = lambda self: self.ec.mrid()
SubGeographicalRegion.mrid = lambda self: self.io.mRID
Substation.mrid = lambda self: self.ec.mrid()
Terminal.mrid = lambda self: self.ad.mrid()
AcLineSegment.mrid = lambda self: self.cd.mrid()
Breaker.mrid = lambda self: self.sw.mrid()
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
LinearShuntCompensator.mrid = lambda self: self.sc.mrid()
PerLengthImpedance.mrid = lambda self: self.lp.mrid()
PerLengthLineParameter.mrid = lambda self: self.lo.mRID
PerLengthSequenceImpedance.mrid = lambda self: self.pli.mrid()
PowerTransformer.mrid = lambda self: self.ce.mrid()
PowerTransformerEnd.mrid = lambda self: self.te.mrid()
ProtectedSwitch.mrid = lambda self: self.sw.mrid()
RatioTapChanger.mrid = lambda self: self.tc.mrid()
Recloser.mrid = lambda self: self.sw.mrid()
RegulatingCondEq.mrid = lambda self: self.ec.mrid()
ShuntCompensator.mrid = lambda self: self.rce.mrid()
Switch.mrid = lambda self: self.ce.mrid()
TapChanger.mrid = lambda self: self.psr.mrid()
TransformerEnd.mrid = lambda self: self.io.mRID

PowerSystemResource.name_and_mrid = lambda self: self.io.name_and_mrid()
ConductingEquipment.name_and_mrid = lambda self: self.eq.name_and_mrid()
Equipment.name_and_mrid = lambda self: self.psr.name_and_mrid()
ConnectivityNodeContainer.name_and_mrid = lambda self: self.psr.name_and_mrid()
EquipmentContainer.name_and_mrid = lambda self: self.cnc.name_and_mrid()
Feeder.name_and_mrid = lambda self: self.ec.name_and_mrid()
EnergyConsumerPhase.name_and_mrid = lambda self: self.psr.name_and_mrid()
EnergySourcePhase.name_and_mrid = lambda self: self.psr.name_and_mrid()
PowerTransformerEnd.name_and_mrid = lambda self: self.te.name_and_mrid()
TransformerEnd.name_and_mrid = lambda self: self.io.name_and_mrid()
Terminal.name_and_mrid = lambda self: self.ad.name_and_mrid()
