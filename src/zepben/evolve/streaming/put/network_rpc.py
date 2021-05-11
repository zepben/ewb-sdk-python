#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from zepben.protobuf.cim.iec61968.assetinfo.CableInfo_pb2 import CableInfo as PBCableInfo
from zepben.protobuf.cim.iec61968.assetinfo.OverheadWireInfo_pb2 import OverheadWireInfo as PBOverheadWireInfo
from zepben.protobuf.cim.iec61968.assetinfo.PowerTransformerInfo_pb2 import PowerTransformerInfo as PBPowerTransformerInfo
from zepben.protobuf.cim.iec61968.assetinfo.TransformerEndInfo_pb2 import TransformerEndInfo as PBTransformerEndInfo
from zepben.protobuf.cim.iec61968.assetinfo.TransformerTankInfo_pb2 import TransformerTankInfo as PBTransformerTankInfo
from zepben.protobuf.cim.iec61968.assets.AssetOwner_pb2 import AssetOwner as PBAssetOwner
from zepben.protobuf.cim.iec61968.assets.Pole_pb2 import Pole as PBPole
from zepben.protobuf.cim.iec61968.assets.Streetlight_pb2 import Streetlight as PBStreetlight
from zepben.protobuf.cim.iec61968.common.Location_pb2 import Location as PBLocation
from zepben.protobuf.cim.iec61968.common.Organisation_pb2 import Organisation as PBOrganisation
from zepben.protobuf.cim.iec61968.customers.CustomerAgreement_pb2 import CustomerAgreement as PBCustomerAgreement
from zepben.protobuf.cim.iec61968.customers.Customer_pb2 import Customer as PBCustomer
from zepben.protobuf.cim.iec61968.customers.PricingStructure_pb2 import PricingStructure as PBPricingStructure
from zepben.protobuf.cim.iec61968.customers.Tariff_pb2 import Tariff as PBTariff
from zepben.protobuf.cim.iec61968.metering.Meter_pb2 import Meter as PBMeter
from zepben.protobuf.cim.iec61968.metering.UsagePoint_pb2 import UsagePoint as PBUsagePoint
from zepben.protobuf.cim.iec61968.operations.OperationalRestriction_pb2 import OperationalRestriction as PBOperationalRestriction
from zepben.protobuf.cim.iec61970.base.auxiliaryequipment.FaultIndicator_pb2 import FaultIndicator as PBFaultIndicator
from zepben.protobuf.cim.iec61970.base.core.BaseVoltage_pb2 import BaseVoltage as PBBaseVoltage
from zepben.protobuf.cim.iec61970.base.core.ConnectivityNode_pb2 import ConnectivityNode as PBConnectivityNode
from zepben.protobuf.cim.iec61970.base.core.Feeder_pb2 import Feeder as PBFeeder
from zepben.protobuf.cim.iec61970.base.core.GeographicalRegion_pb2 import GeographicalRegion as PBGeographicalRegion
from zepben.protobuf.cim.iec61970.base.core.Site_pb2 import Site as PBSite
from zepben.protobuf.cim.iec61970.base.core.SubGeographicalRegion_pb2 import SubGeographicalRegion as PBSubGeographicalRegion
from zepben.protobuf.cim.iec61970.base.core.Substation_pb2 import Substation as PBSubstation
from zepben.protobuf.cim.iec61970.base.core.Terminal_pb2 import Terminal as PBTerminal
from zepben.protobuf.cim.iec61970.base.diagramlayout.DiagramObject_pb2 import DiagramObject as PBDiagramObject
from zepben.protobuf.cim.iec61970.base.diagramlayout.Diagram_pb2 import Diagram as PBDiagram
from zepben.protobuf.cim.iec61970.base.meas.AccumulatorValue_pb2 import AccumulatorValue as PBAccumulatorValue
from zepben.protobuf.cim.iec61970.base.meas.Accumulator_pb2 import Accumulator as PBAccumulator
from zepben.protobuf.cim.iec61970.base.meas.AnalogValue_pb2 import AnalogValue as PBAnalogValue
from zepben.protobuf.cim.iec61970.base.meas.Analog_pb2 import Analog as PBAnalog
from zepben.protobuf.cim.iec61970.base.meas.DiscreteValue_pb2 import DiscreteValue as PBDiscreteValue
from zepben.protobuf.cim.iec61970.base.meas.Discrete_pb2 import Discrete as PBDiscrete
from zepben.protobuf.cim.iec61970.base.wires.AcLineSegment_pb2 import AcLineSegment as PBAcLineSegment
from zepben.protobuf.cim.iec61970.base.wires.Breaker_pb2 import Breaker as PBBreaker
from zepben.protobuf.cim.iec61970.base.wires.BusbarSection_pb2 import BusbarSection as PBBusbarSection
from zepben.protobuf.cim.iec61970.base.wires.Disconnector_pb2 import Disconnector as PBDisconnector
from zepben.protobuf.cim.iec61970.base.wires.EnergyConsumerPhase_pb2 import EnergyConsumerPhase as PBEnergyConsumerPhase
from zepben.protobuf.cim.iec61970.base.wires.EnergyConsumer_pb2 import EnergyConsumer as PBEnergyConsumer
from zepben.protobuf.cim.iec61970.base.wires.EnergySourcePhase_pb2 import EnergySourcePhase as PBEnergySourcePhase
from zepben.protobuf.cim.iec61970.base.wires.EnergySource_pb2 import EnergySource as PBEnergySource
from zepben.protobuf.cim.iec61970.base.wires.Fuse_pb2 import Fuse as PBFuse
from zepben.protobuf.cim.iec61970.base.wires.Jumper_pb2 import Jumper as PBJumper
from zepben.protobuf.cim.iec61970.base.wires.Junction_pb2 import Junction as PBJunction
from zepben.protobuf.cim.iec61970.base.wires.LinearShuntCompensator_pb2 import LinearShuntCompensator as PBLinearShuntCompensator
from zepben.protobuf.cim.iec61970.base.wires.LoadBreakSwitch_pb2 import LoadBreakSwitch as PBLoadBreakSwitch
from zepben.protobuf.cim.iec61970.base.wires.PerLengthSequenceImpedance_pb2 import PerLengthSequenceImpedance as PBPerLengthSequenceImpedance
from zepben.protobuf.cim.iec61970.base.wires.PowerElectronicsConnectionPhase_pb2 import PowerElectronicsConnectionPhase as PBPowerElectronicsConnectionPhase
from zepben.protobuf.cim.iec61970.base.wires.PowerElectronicsConnection_pb2 import PowerElectronicsConnection as PBPowerElectronicsConnection
from zepben.protobuf.cim.iec61970.base.wires.PowerTransformerEnd_pb2 import PowerTransformerEnd as PBPowerTransformerEnd
from zepben.protobuf.cim.iec61970.base.wires.PowerTransformer_pb2 import PowerTransformer as PBPowerTransformer
from zepben.protobuf.cim.iec61970.base.wires.RatioTapChanger_pb2 import RatioTapChanger as PBRatioTapChanger
from zepben.protobuf.cim.iec61970.base.wires.Recloser_pb2 import Recloser as PBRecloser
from zepben.protobuf.cim.iec61970.base.wires.TransformerStarImpedance_pb2 import TransformerStarImpedance as PBTransformerStarImpedance
from zepben.protobuf.cim.iec61970.base.wires.generation.production.BatteryUnit_pb2 import BatteryUnit as PBBatteryUnit
from zepben.protobuf.cim.iec61970.base.wires.generation.production.PhotoVoltaicUnit_pb2 import PhotoVoltaicUnit as PBPhotoVoltaicUnit
from zepben.protobuf.cim.iec61970.base.wires.generation.production.PowerElectronicsWindUnit_pb2 import PowerElectronicsWindUnit as PBPowerElectronicsWindUnit
from zepben.protobuf.cp.cp_requests_pb2 import CreateOrganisationRequest as CreateCustomerOrganisationRequest, CreateCustomerAgreementRequest, \
    CreatePricingStructureRequest, CreateTariffRequest
from zepben.protobuf.dp.dp_requests_pb2 import *
from zepben.protobuf.mp.mp_requests_pb2 import CreateAnalogValueRequest, CreateAccumulatorValueRequest, CreateDiscreteValueRequest
from zepben.protobuf.np.np_requests_pb2 import *

network_rpc_map = {
    PBCableInfo: ('CreateCableInfo', CreateCableInfoRequest),
    PBOverheadWireInfo: ('CreateOverheadWireInfo', CreateOverheadWireInfoRequest),
    PBAssetOwner: ('CreateAssetOwner', CreateAssetOwnerRequest),
    PBPole: ('CreatePole', CreatePoleRequest),
    PBStreetlight: ('CreateStreetlight', CreateStreetlightRequest),
    PBLocation: ('CreateLocation', CreateLocationRequest),
    PBOrganisation: ('CreateOrganisation', CreateOrganisationRequest),
    PBMeter: ('CreateMeter', CreateMeterRequest),
    PBUsagePoint: ('CreateUsagePoint', CreateUsagePointRequest),
    PBOperationalRestriction: ('CreateOperationalRestriction', CreateOperationalRestrictionRequest),
    PBFaultIndicator: ('CreateFaultIndicator', CreateFaultIndicatorRequest),
    PBBaseVoltage: ('CreateBaseVoltage', CreateBaseVoltageRequest),
    PBConnectivityNode: ('CreateConnectivityNode', CreateConnectivityNodeRequest),
    PBFeeder: ('CreateFeeder', CreateFeederRequest),
    PBGeographicalRegion: ('CreateGeographicalRegion', CreateGeographicalRegionRequest),
    PBSite: ('CreateSite', CreateSiteRequest),
    PBSubGeographicalRegion: ('CreateSubGeographicalRegion', CreateSubGeographicalRegionRequest),
    PBSubstation: ('CreateSubstation', CreateSubstationRequest),
    PBTerminal: ('CreateTerminal', CreateTerminalRequest),
    PBAccumulator: ('CreateAccumulator', CreateAccumulatorRequest),
    PBAnalog: ('CreateAnalog', CreateAnalogRequest),
    PBDiscrete: ('CreateDiscrete', CreateDiscreteRequest),
    PBBatteryUnit: ('CreateBatteryUnit', CreateBatteryUnitRequest),
    PBPhotoVoltaicUnit: ('CreatePhotoVoltaicUnit', CreatePhotoVoltaicRequest),
    PBPowerElectronicsWindUnit: ('CreatePowerElectronicsWindUnit', CreatePowerElectronicsWindUnitRequest),
    PBAcLineSegment: ('CreateAcLineSegment', CreateAcLineSegmentRequest),
    PBEnergyConsumer: ('CreateEnergyConsumer', CreateEnergyConsumerRequest),
    PBDisconnector: ('CreateDisconnector', CreateDisconnectorRequest),
    PBBreaker: ('CreateBreaker', CreateBreakerRequest),
    PBEnergyConsumerPhase: ('CreateEnergyConsumerPhase', CreateEnergyConsumerPhaseRequest),
    PBEnergySource: ('CreateEnergySource', CreateEnergySourceRequest),
    PBEnergySourcePhase: ('CreateEnergySourcePhase', CreateEnergySourcePhaseRequest),
    PBFuse: ('CreateFuse', CreateFuseRequest),
    PBJumper: ('CreateJumper', CreateJumperRequest),
    PBJunction: ('CreateJunction', CreateJunctionRequest),
    PBBusbarSection: ('CreateBusbarSection', CreateBusbarSectionRequest),
    PBLinearShuntCompensator: ('CreateLinearShuntCompensator', CreateLinearShuntCompensatorRequest),
    PBLoadBreakSwitch: ('CreateLoadBreakSwitch', CreateLoadBreakSwitchRequest),
    PBPerLengthSequenceImpedance: ('CreatePerLengthSequenceImpedance', CreatePerLengthSequenceImpedanceRequest),
    PBPowerElectronicsConnection: ('CreatePowerElectronicsConnection', CreatePowerElectronicsConnectionRequest),
    PBPowerElectronicsConnectionPhase: ('CreatePowerElectronicsConnectionPhase', CreatePowerElectronicsConnectionPhaseRequest),
    PBPowerTransformer: ('CreatePowerTransformer', CreatePowerTransformerRequest),
    PBPowerTransformerEnd: ('CreatePowerTransformerEnd', CreatePowerTransformerEndRequest),
    PBPowerTransformerInfo: ('CreatePowerTransformerInfo', CreatePowerTransformerInfoRequest),
    PBRatioTapChanger: ('CreateRatioTapChanger', CreateRatioTapChangerRequest),
    PBRecloser: ('CreateRecloser', CreateRecloserRequest),
    PBTransformerTankInfo: ('CreateTransformerTankInfo', CreateTransformerTankInfoRequest),
    PBTransformerEndInfo: ('CreateTransformerEndInfo', CreateTransformerEndInfoRequest),
    PBTransformerStarImpedance: ('CreateTransformerStarImpedance', CreateTransformerStarImpedanceRequest),
}

diagram_rpc_map = {
    PBDiagram: ('CreateDiagram', CreateDiagramRequest),
    PBDiagramObject: ('CreateDiagramObject', CreateDiagramObjectRequest),
}

customer_rpc_map = {
    PBCustomer: ('CreateCustomer', CreateCustomerRequest),
    PBCustomerAgreement: ('CreateCustomerAgreement', CreateCustomerAgreementRequest),
    PBPricingStructure: ('CreatePricingStructure', CreatePricingStructureRequest),
    PBTariff: ('CreateTariff', CreateTariffRequest),
    PBOrganisation: ('CreateOrganisation', CreateCustomerOrganisationRequest),
}

measurement_rpc_map = {
    PBAnalogValue: ('CreateAnalogValue', CreateAnalogValueRequest),
    PBAccumulatorValue: ('CreateAccumulatorValue', CreateAccumulatorValueRequest),
    PBDiscreteValue: ('CreateDiscreteValue', CreateDiscreteValueRequest),
}
