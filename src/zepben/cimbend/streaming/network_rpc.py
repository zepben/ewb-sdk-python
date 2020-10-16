#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.


from zepben.protobuf.cim.iec61968.assetinfo.CableInfo_pb2 import CableInfo
from zepben.protobuf.cim.iec61968.assetinfo.OverheadWireInfo_pb2 import OverheadWireInfo
from zepben.protobuf.cim.iec61968.assets.AssetOwner_pb2 import AssetOwner
from zepben.protobuf.cim.iec61968.assets.Pole_pb2 import Pole
from zepben.protobuf.cim.iec61968.assets.Streetlight_pb2 import Streetlight
from zepben.protobuf.cim.iec61968.common.Location_pb2 import Location
from zepben.protobuf.cim.iec61968.common.Organisation_pb2 import Organisation
from zepben.protobuf.cim.iec61968.metering.Meter_pb2 import Meter
from zepben.protobuf.cim.iec61968.metering.UsagePoint_pb2 import UsagePoint
from zepben.protobuf.cim.iec61968.operations.OperationalRestriction_pb2 import OperationalRestriction
from zepben.protobuf.cim.iec61970.base.auxiliaryequipment.FaultIndicator_pb2 import FaultIndicator
from zepben.protobuf.cim.iec61970.base.core.BaseVoltage_pb2 import BaseVoltage
from zepben.protobuf.cim.iec61970.base.core.ConnectivityNode_pb2 import ConnectivityNode
from zepben.protobuf.cim.iec61970.base.core.Feeder_pb2 import Feeder
from zepben.protobuf.cim.iec61970.base.core.GeographicalRegion_pb2 import GeographicalRegion
from zepben.protobuf.cim.iec61970.base.core.Site_pb2 import Site
from zepben.protobuf.cim.iec61970.base.core.SubGeographicalRegion_pb2 import SubGeographicalRegion
from zepben.protobuf.cim.iec61970.base.core.Substation_pb2 import Substation
from zepben.protobuf.cim.iec61970.base.core.Terminal_pb2 import Terminal
from zepben.protobuf.cim.iec61970.base.wires.AcLineSegment_pb2 import AcLineSegment
from zepben.protobuf.cim.iec61970.base.wires.Breaker_pb2 import Breaker
from zepben.protobuf.cim.iec61970.base.wires.Disconnector_pb2 import Disconnector
from zepben.protobuf.cim.iec61970.base.wires.EnergyConsumer_pb2 import EnergyConsumer
from zepben.protobuf.cim.iec61970.base.wires.EnergyConsumerPhase_pb2 import EnergyConsumerPhase
from zepben.protobuf.cim.iec61970.base.wires.EnergySource_pb2 import EnergySource
from zepben.protobuf.cim.iec61970.base.wires.EnergySourcePhase_pb2 import EnergySourcePhase
from zepben.protobuf.cim.iec61970.base.wires.Fuse_pb2 import Fuse
from zepben.protobuf.cim.iec61970.base.wires.Jumper_pb2 import Jumper
from zepben.protobuf.cim.iec61970.base.wires.Junction_pb2 import Junction
from zepben.protobuf.cim.iec61970.base.wires.LinearShuntCompensator_pb2 import LinearShuntCompensator
from zepben.protobuf.cim.iec61970.base.wires.PerLengthSequenceImpedance_pb2 import PerLengthSequenceImpedance
from zepben.protobuf.cim.iec61970.base.wires.PowerTransformer_pb2 import PowerTransformer
from zepben.protobuf.cim.iec61970.base.wires.PowerTransformerEnd_pb2 import PowerTransformerEnd
from zepben.protobuf.cim.iec61970.base.wires.RatioTapChanger_pb2 import RatioTapChanger
from zepben.protobuf.cim.iec61970.base.wires.Recloser_pb2 import Recloser
from zepben.protobuf.np.np_requests_pb2 import *

# TODO: remove this!
def CreatePoleRequest():
    pass

def CreateStreetlightRequest():
    pass

rpc_map = {
    CableInfo: ('CreateCableInfo', CreateCableInfoRequest),
    OverheadWireInfo: ('CreateOverheadWireInfo', CreateOverheadWireInfoRequest),
    AssetOwner: ('CreateAssetOwner', CreateAssetOwnerRequest),
    Pole: ('CreatePole', CreatePoleRequest),
    Streetlight: ('CreateStreetlight', CreateStreetlightRequest),
    Location: ('CreateLocation', CreateLocationRequest),
    Organisation: ('CreateOrganisation', CreateOrganisationRequest),
    Meter: ('CreateMeter', CreateMeterRequest),
    UsagePoint: ('CreateUsagePoint', CreateUsagePointRequest),
    OperationalRestriction: ('CreateOperationalRestriction', CreateOperationalRestrictionRequest),
    FaultIndicator: ('CreateFaultIndicator', CreateFaultIndicatorRequest),
    BaseVoltage: ('CreateBaseVoltage', CreateBaseVoltageRequest),
    ConnectivityNode: ('CreateConnectivityNode', CreateConnectivityNodeRequest),
    Feeder: ('CreateFeeder', CreateFeederRequest),
    GeographicalRegion: ('CreateGeographicalRegion', CreateGeographicalRegionRequest),
    Site: ('CreateSite', CreateSiteRequest),
    SubGeographicalRegion: ('CreateSubGeographicalRegion', CreateSubGeographicalRegionRequest),
    Substation: ('CreateSubstation', CreateSubstationRequest),
    Terminal: ('CreateTerminal', CreateTerminalRequest),
    AcLineSegment: ('CreateAcLineSegment', CreateAcLineSegmentRequest),
    EnergyConsumer: ('CreateEnergyConsumer', CreateEnergyConsumerRequest),
    Disconnector: ('CreateDisconnector', CreateDisconnectorRequest),
    Breaker: ('CreateBreaker', CreateBreakerRequest),
    EnergyConsumerPhase: ('CreateEnergyConsumerPhase', CreateEnergyConsumerPhaseRequest),
    EnergySource: ('CreateEnergySource', CreateEnergySourceRequest),
    EnergySourcePhase: ('CreateEnergySourcePhase', CreateEnergySourcePhaseRequest),
    Fuse: ('CreateFuse', CreateFuseRequest),
    Jumper: ('CreateJumper', CreateJumperRequest),
    Junction: ('CreateJunction', CreateJunctionRequest),
    LinearShuntCompensator: ('CreateLinearShuntCompensator', CreateLinearShuntCompensatorRequest),
    PerLengthSequenceImpedance: ('CreatePerLengthSequenceImpedance', CreatePerLengthSequenceImpedanceRequest),
    PowerTransformer: ('CreatePowerTransformer', CreatePowerTransformerRequest),
    PowerTransformerEnd: ('CreatePowerTransformerEnd', CreatePowerTransformerEndRequest),
    RatioTapChanger: ('CreateRatioTapChanger', CreateRatioTapChangerRequest),
    Recloser: ('CreateRecloser', CreateRecloserRequest),
}

