#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from zepben.protobuf.cim.iec61968.assetinfo.CableInfo_pb2 import CableInfo as PBCableInfo
from zepben.protobuf.cim.iec61968.assetinfo.OverheadWireInfo_pb2 import OverheadWireInfo as PBOverheadWireInfo
from zepben.protobuf.cim.iec61968.assetinfo.PowerTransformerInfo_pb2 import PowerTransformerInfo as PBPowerTransformerInfo
from zepben.protobuf.cim.iec61968.assets.AssetOwner_pb2 import AssetOwner as PBAssetOwner
from zepben.protobuf.cim.iec61968.assets.Pole_pb2 import Pole as PBPole
from zepben.protobuf.cim.iec61968.assets.Streetlight_pb2 import Streetlight as PBStreetlight
from zepben.protobuf.cim.iec61968.common.Location_pb2 import Location as PBLocation
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
from zepben.protobuf.cim.iec61970.base.wires.EnergyConsumer_pb2 import EnergyConsumer as PBEnergyConsumer
from zepben.protobuf.cim.iec61970.base.wires.EnergyConsumerPhase_pb2 import EnergyConsumerPhase as PBEnergyConsumerPhase
from zepben.protobuf.cim.iec61970.base.wires.EnergySource_pb2 import EnergySource as PBEnergySource
from zepben.protobuf.cim.iec61970.base.wires.EnergySourcePhase_pb2 import EnergySourcePhase as PBEnergySourcePhase
from zepben.protobuf.cim.iec61970.base.wires.Fuse_pb2 import Fuse as PBFuse
from zepben.protobuf.cim.iec61970.base.wires.Jumper_pb2 import Jumper as PBJumper
from zepben.protobuf.cim.iec61970.base.wires.Junction_pb2 import Junction as PBJunction
from zepben.protobuf.cim.iec61970.base.wires.LinearShuntCompensator_pb2 import LinearShuntCompensator as PBLinearShuntCompensator
from zepben.protobuf.cim.iec61970.base.wires.LoadBreakSwitch_pb2 import LoadBreakSwitch as PBLoadBreakSwitch
from zepben.protobuf.cim.iec61970.base.wires.PerLengthSequenceImpedance_pb2 import PerLengthSequenceImpedance as PBPerLengthSequenceImpedance
from zepben.protobuf.cim.iec61970.base.wires.PowerElectronicsConnectionPhase_pb2 import PowerElectronicsConnectionPhase as PBPowerElectronicsConnectionPhase
from zepben.protobuf.cim.iec61970.base.wires.PowerElectronicsConnection_pb2 import PowerElectronicsConnection as PBPowerElectronicsConnection
from zepben.protobuf.cim.iec61970.base.wires.PowerTransformer_pb2 import PowerTransformer as PBPowerTransformer
from zepben.protobuf.cim.iec61970.base.wires.PowerTransformerEnd_pb2 import PowerTransformerEnd as PBPowerTransformerEnd
from zepben.protobuf.cim.iec61970.base.wires.RatioTapChanger_pb2 import RatioTapChanger as PBRatioTapChanger
from zepben.protobuf.cim.iec61970.base.wires.Recloser_pb2 import Recloser as PBRecloser
from zepben.protobuf.cim.iec61970.base.diagramlayout.Diagram_pb2 import Diagram as PBDiagram
from zepben.protobuf.cim.iec61970.base.diagramlayout.DiagramObject_pb2 import DiagramObject as PBDiagramObject
from zepben.protobuf.cim.iec61968.customers.Customer_pb2 import Customer as PBCustomer
from zepben.protobuf.cim.iec61968.customers.CustomerAgreement_pb2 import CustomerAgreement as PBCustomerAgreement
from zepben.protobuf.cim.iec61968.customers.PricingStructure_pb2 import PricingStructure as PBPricingStructure
from zepben.protobuf.cim.iec61968.customers.Tariff_pb2 import Tariff as PBTariff
from zepben.protobuf.cim.iec61968.common.Organisation_pb2 import Organisation as PBOrganisation
from zepben.protobuf.cim.iec61970.base.wires.generation.production.BatteryUnit_pb2 import BatteryUnit as PBBatteryUnit
from zepben.protobuf.cim.iec61970.base.wires.generation.production.PhotoVoltaicUnit_pb2 import PhotoVoltaicUnit as PBPhotoVoltaicUnit
from zepben.protobuf.cim.iec61970.base.wires.generation.production.PowerElectronicsWindUnit_pb2 import PowerElectronicsWindUnit as PBPowerElectronicsWindUnit
from zepben.protobuf.cp.cp_requests_pb2 import CreateOrganisationRequest as CreateCustomerOrganisationRequest
from zepben.protobuf.mp.mp_requests_pb2 import CreateAnalogValueRequest, CreateAccumulatorValueRequest, CreateDiscreteValueRequest
from zepben.protobuf.dp.dp_requests_pb2 import *
from zepben.protobuf.cp.cp_requests_pb2 import *
from zepben.protobuf.np.np_requests_pb2 import *

from zepben.evolve.model.cim.iec61968.assetinfo.wire_info import CableInfo, OverheadWireInfo
from zepben.evolve.model.cim.iec61968.assetinfo.power_transformer_info import PowerTransformerInfo
from zepben.evolve.model.cim.iec61968.assets.asset_organisation_role import AssetOwner
from zepben.evolve.model.cim.iec61968.assets.pole import Pole
from zepben.evolve.model.cim.iec61968.assets.streetlight import Streetlight
from zepben.evolve.model.cim.iec61968.common.location import Location
from zepben.evolve.model.cim.iec61968.metering.metering import Meter, UsagePoint
from zepben.evolve.model.cim.iec61968.operations.operational_restriction import OperationalRestriction
from zepben.evolve.model.cim.iec61970.base.auxiliaryequipment.auxiliary_equipment import FaultIndicator
from zepben.evolve.model.cim.iec61970.base.core.base_voltage import BaseVoltage
from zepben.evolve.model.cim.iec61970.base.core.connectivity_node import ConnectivityNode
from zepben.evolve.model.cim.iec61970.base.core.equipment_container import Feeder, Site
from zepben.evolve.model.cim.iec61970.base.core.regions import GeographicalRegion, SubGeographicalRegion
from zepben.evolve.model.cim.iec61970.base.core.substation import Substation
from zepben.evolve.model.cim.iec61970.base.core.terminal import Terminal
from zepben.evolve.model.cim.iec61970.base.meas.measurement import Accumulator, Analog, Discrete
from zepben.evolve.model.cim.iec61970.base.meas.value import AccumulatorValue, AnalogValue, DiscreteValue
from zepben.evolve.model.cim.iec61970.base.meas.control import Control
from zepben.evolve.model.cim.iec61970.base.scada.remote_control import RemoteControl
from zepben.evolve.model.cim.iec61970.base.scada.remote_source import RemoteSource
from zepben.evolve.model.cim.iec61970.base.wires.aclinesegment import AcLineSegment
from zepben.evolve.model.cim.iec61970.base.wires.switch import Breaker, Disconnector, Fuse, Jumper, LoadBreakSwitch, Recloser
from zepben.evolve.model.cim.iec61970.base.wires.connectors import BusbarSection, Junction
from zepben.evolve.model.cim.iec61970.base.wires.energy_consumer import EnergyConsumer, EnergyConsumerPhase
from zepben.evolve.model.cim.iec61970.base.wires.energy_source import EnergySource
from zepben.evolve.model.cim.iec61970.base.wires.energy_source_phase import EnergySourcePhase
from zepben.evolve.model.cim.iec61970.base.wires.shunt_compensator import LinearShuntCompensator
from zepben.evolve.model.cim.iec61970.base.wires.per_length import PerLengthSequenceImpedance
from zepben.evolve.model.cim.iec61970.base.wires.power_electronics_connection import PowerElectronicsConnection, PowerElectronicsConnectionPhase
from zepben.evolve.model.cim.iec61970.base.wires.power_transformer import PowerTransformer, PowerTransformerEnd, RatioTapChanger
from zepben.evolve.model.cim.iec61970.infiec61970.feeder.loop import Loop
from zepben.evolve.model.cim.iec61970.infiec61970.feeder.circuit import Circuit
from zepben.evolve.model.cim.iec61970.base.diagramlayout.diagram_layout import Diagram, DiagramObject
from zepben.evolve.model.cim.iec61968.customers.customer import Customer
from zepben.evolve.model.cim.iec61968.customers.customer_agreement import CustomerAgreement
from zepben.evolve.model.cim.iec61968.customers.pricing_structure import PricingStructure
from zepben.evolve.model.cim.iec61968.customers.tariff import Tariff
from zepben.evolve.model.cim.iec61968.common.organisation import Organisation
from zepben.evolve.model.cim.iec61970.base.wires.generation.production.power_electronics_unit import BatteryUnit, PhotoVoltaicUnit, PowerElectronicsWindUnit

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

nio_type_to_cim = {
    "cableInfo": CableInfo,
    "overheadWireInfo": OverheadWireInfo,
    "assetOwner": AssetOwner,
    "organisation": Organisation,
    "location": Location,
    "meter": Meter,
    "usagePoint": UsagePoint,
    "operationalRestriction": OperationalRestriction,
    "faultIndicator": FaultIndicator,
    "baseVoltage": BaseVoltage,
    "connectivityNode": ConnectivityNode,
    "feeder": Feeder,
    "geographicalRegion": GeographicalRegion,
    "site": Site,
    "subGeographicalRegion": SubGeographicalRegion,
    "substation": Substation,
    "terminal": Terminal,
    "acLineSegment": AcLineSegment,
    "breaker": Breaker,
    "disconnector": Disconnector,
    "energyConsumer": EnergyConsumer,
    "energyConsumerPhase": EnergyConsumerPhase,
    "energySource": EnergySource,
    "energySourcePhase": EnergySourcePhase,
    "fuse": Fuse,
    "jumper": Jumper,
    "junction": Junction,
    "linearShuntCompensator": LinearShuntCompensator,
    "perLengthSequenceImpedance": PerLengthSequenceImpedance,
    "powerTransformer": PowerTransformer,
    "powerTransformerEnd": PowerTransformerEnd,
    "ratioTapChanger": RatioTapChanger,
    "recloser": Recloser,
    "circuit": Circuit,
    "loop": Loop,
    "pole": Pole,
    "streetlight": Streetlight,
    "accumulator": Accumulator,
    "analog": Analog,
    "discrete": Discrete,
    "control": Control,
    "remoteControl": RemoteControl,
    "remoteSource": RemoteSource,
    "powerTransformerInfo": PowerTransformerInfo,
    "powerElectronicsConnection": PowerElectronicsConnection,
    "powerElectronicsConnectionPhase": PowerElectronicsConnectionPhase,
    "batteryUnit": BatteryUnit,
    "photoVoltaicUnit": PhotoVoltaicUnit,
    "powerElectronicsWindUnit": PowerElectronicsWindUnit,
    "busbarSection": BusbarSection,
    "loadBreakSwitch": LoadBreakSwitch,
}
