#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = [
    # We only export the top level container classes, and a minimal set of classes for testing the consumers.
    'network_identified_objects', 'ac_line_segment',
    'customer_identified_objects', 'customer',
    'diagram_identified_objects', 'diagram', 'diagram_object'
]

from typing import Optional, Dict

# noinspection PyPackageRequirements,PyUnresolvedReferences
from google.protobuf.struct_pb2 import NullValue
# noinspection PyPackageRequirements,PyUnresolvedReferences
from google.protobuf.timestamp_pb2 import Timestamp
from hypothesis.strategies import builds, text, integers, sampled_from, lists as hypo_lists, floats as hypo_floats, booleans, composite, uuids, one_of, none
from zepben.protobuf.cc.cc_data_pb2 import CustomerIdentifiedObject
from zepben.protobuf.cim.extensions.iec61968.assetinfo.RelayInfo_pb2 import RelayInfo as PBRelayInfo
from zepben.protobuf.cim.extensions.iec61968.metering.PanDemandResponseFunction_pb2 import PanDemandResponseFunction as PBPanDemandResponseFunction
from zepben.protobuf.cim.extensions.iec61970.base.core.Site_pb2 import Site as PBSite
from zepben.protobuf.cim.extensions.iec61970.base.feeder.Loop_pb2 import Loop as PBLoop
from zepben.protobuf.cim.extensions.iec61970.base.feeder.LvFeeder_pb2 import LvFeeder as PBLvFeeder
from zepben.protobuf.cim.extensions.iec61970.base.generation.production.EvChargingUnit_pb2 import EvChargingUnit as PBEvChargingUnit
from zepben.protobuf.cim.extensions.iec61970.base.protection.DistanceRelay_pb2 import DistanceRelay as PBDistanceRelay
from zepben.protobuf.cim.extensions.iec61970.base.protection.PowerDirectionKind_pb2 import PowerDirectionKind as PBPowerDirectionKind
from zepben.protobuf.cim.extensions.iec61970.base.protection.ProtectionKind_pb2 import ProtectionKind as PBProtectionKind
from zepben.protobuf.cim.extensions.iec61970.base.protection.ProtectionRelayFunction_pb2 import ProtectionRelayFunction as PBProtectionRelayFunction
from zepben.protobuf.cim.extensions.iec61970.base.protection.ProtectionRelayScheme_pb2 import ProtectionRelayScheme as PBProtectionRelayScheme
from zepben.protobuf.cim.extensions.iec61970.base.protection.ProtectionRelaySystem_pb2 import ProtectionRelaySystem as PBProtectionRelaySystem
from zepben.protobuf.cim.extensions.iec61970.base.protection.RelaySetting_pb2 import RelaySetting as PBRelaySetting
from zepben.protobuf.cim.extensions.iec61970.base.protection.VoltageRelay_pb2 import VoltageRelay as PBVoltageRelay
from zepben.protobuf.cim.extensions.iec61970.base.wires.BatteryControlMode_pb2 import BatteryControlMode as PBBatteryControlMode
from zepben.protobuf.cim.extensions.iec61970.base.wires.BatteryControl_pb2 import BatteryControl as PBBatteryControl
from zepben.protobuf.cim.extensions.iec61970.base.wires.TransformerCoolingType_pb2 import TransformerCoolingType as PBTransformerCoolingType
from zepben.protobuf.cim.extensions.iec61970.base.wires.TransformerEndRatedS_pb2 import TransformerEndRatedS as PBTransformerEndRatedS
from zepben.protobuf.cim.extensions.iec61970.base.wires.VectorGroup_pb2 import VectorGroup as PBVectorGroup
from zepben.protobuf.cim.iec61968.assetinfo.CableInfo_pb2 import CableInfo as PBCableInfo
from zepben.protobuf.cim.iec61968.assetinfo.NoLoadTest_pb2 import NoLoadTest as PBNoLoadTest
from zepben.protobuf.cim.iec61968.assetinfo.OpenCircuitTest_pb2 import OpenCircuitTest as PBOpenCircuitTest
from zepben.protobuf.cim.iec61968.assetinfo.OverheadWireInfo_pb2 import OverheadWireInfo as PBOverheadWireInfo
from zepben.protobuf.cim.iec61968.assetinfo.PowerTransformerInfo_pb2 import PowerTransformerInfo as PBPowerTransformerInfo
from zepben.protobuf.cim.iec61968.assetinfo.ShortCircuitTest_pb2 import ShortCircuitTest as PBShortCircuitTest
from zepben.protobuf.cim.iec61968.assetinfo.ShuntCompensatorInfo_pb2 import ShuntCompensatorInfo as PBShuntCompensatorInfo
from zepben.protobuf.cim.iec61968.assetinfo.SwitchInfo_pb2 import SwitchInfo as PBSwitchInfo
from zepben.protobuf.cim.iec61968.assetinfo.TransformerEndInfo_pb2 import TransformerEndInfo as PBTransformerEndInfo
from zepben.protobuf.cim.iec61968.assetinfo.TransformerTankInfo_pb2 import TransformerTankInfo as PBTransformerTankInfo
from zepben.protobuf.cim.iec61968.assetinfo.TransformerTest_pb2 import TransformerTest as PBTransformerTest
from zepben.protobuf.cim.iec61968.assetinfo.WireInfo_pb2 import WireInfo as PBWireInfo
from zepben.protobuf.cim.iec61968.assetinfo.WireMaterialKind_pb2 import WireMaterialKind as PBWireMaterialKind
from zepben.protobuf.cim.iec61968.assets.AssetContainer_pb2 import AssetContainer as PBAssetContainer
from zepben.protobuf.cim.iec61968.assets.AssetFunction_pb2 import AssetFunction as PBAssetFunction
from zepben.protobuf.cim.iec61968.assets.AssetInfo_pb2 import AssetInfo as PBAssetInfo
from zepben.protobuf.cim.iec61968.assets.AssetOrganisationRole_pb2 import AssetOrganisationRole as PBAssetOrganisationRole
from zepben.protobuf.cim.iec61968.assets.AssetOwner_pb2 import AssetOwner as PBAssetOwner
from zepben.protobuf.cim.iec61968.assets.Asset_pb2 import Asset as PBAsset
from zepben.protobuf.cim.iec61968.assets.Streetlight_pb2 import Streetlight as PBStreetlight
from zepben.protobuf.cim.iec61968.assets.Structure_pb2 import Structure as PBStructure
from zepben.protobuf.cim.iec61968.common.Agreement_pb2 import Agreement as PBAgreement
from zepben.protobuf.cim.iec61968.common.Document_pb2 import Document as PBDocument
from zepben.protobuf.cim.iec61968.common.Location_pb2 import Location as PBLocation
from zepben.protobuf.cim.iec61968.common.OrganisationRole_pb2 import OrganisationRole as PBOrganisationRole
from zepben.protobuf.cim.iec61968.common.Organisation_pb2 import Organisation as PBOrganisation
from zepben.protobuf.cim.iec61968.common.PositionPoint_pb2 import PositionPoint as PBPositionPoint
from zepben.protobuf.cim.iec61968.common.StreetAddress_pb2 import StreetAddress as PBStreetAddress
from zepben.protobuf.cim.iec61968.common.StreetDetail_pb2 import StreetDetail as PBStreetDetail
from zepben.protobuf.cim.iec61968.common.TownDetail_pb2 import TownDetail as PBTownDetail
from zepben.protobuf.cim.iec61968.customers.CustomerAgreement_pb2 import CustomerAgreement as PBCustomerAgreement
from zepben.protobuf.cim.iec61968.customers.CustomerKind_pb2 import CustomerKind as PBCustomerKind
from zepben.protobuf.cim.iec61968.customers.Customer_pb2 import Customer as PBCustomer
from zepben.protobuf.cim.iec61968.customers.PricingStructure_pb2 import PricingStructure as PBPricingStructure
from zepben.protobuf.cim.iec61968.customers.Tariff_pb2 import Tariff as PBTariff
from zepben.protobuf.cim.iec61968.infiec61968.infassetinfo.CurrentTransformerInfo_pb2 import CurrentTransformerInfo as PBCurrentTransformerInfo
from zepben.protobuf.cim.iec61968.infiec61968.infassetinfo.PotentialTransformerInfo_pb2 import PotentialTransformerInfo as PBPotentialTransformerInfo
from zepben.protobuf.cim.iec61968.infiec61968.infassets.Pole_pb2 import Pole as PBPole
from zepben.protobuf.cim.iec61968.infiec61968.infassets.StreetlightLampKind_pb2 import StreetlightLampKind as PBStreetlightLampKind
from zepben.protobuf.cim.iec61968.infiec61968.infcommon.Ratio_pb2 import Ratio as PBRatio
from zepben.protobuf.cim.iec61968.metering.EndDeviceFunctionKind_pb2 import EndDeviceFunctionKind as PBEndDeviceFunctionKind
from zepben.protobuf.cim.iec61968.metering.EndDeviceFunction_pb2 import EndDeviceFunction as PBEndDeviceFunction
from zepben.protobuf.cim.iec61968.metering.EndDevice_pb2 import EndDevice as PBEndDevice
from zepben.protobuf.cim.iec61968.metering.Meter_pb2 import Meter as PBMeter
from zepben.protobuf.cim.iec61968.metering.UsagePoint_pb2 import UsagePoint as PBUsagePoint
from zepben.protobuf.cim.iec61968.operations.OperationalRestriction_pb2 import OperationalRestriction as PBOperationalRestriction
from zepben.protobuf.cim.iec61970.base.auxiliaryequipment.AuxiliaryEquipment_pb2 import AuxiliaryEquipment as PBAuxiliaryEquipment
from zepben.protobuf.cim.iec61970.base.auxiliaryequipment.CurrentTransformer_pb2 import CurrentTransformer as PBCurrentTransformer
from zepben.protobuf.cim.iec61970.base.auxiliaryequipment.FaultIndicator_pb2 import FaultIndicator as PBFaultIndicator
from zepben.protobuf.cim.iec61970.base.auxiliaryequipment.PotentialTransformerKind_pb2 import PotentialTransformerKind as PBPotentialTransformerKind
from zepben.protobuf.cim.iec61970.base.auxiliaryequipment.PotentialTransformer_pb2 import PotentialTransformer as PBPotentialTransformer
from zepben.protobuf.cim.iec61970.base.auxiliaryequipment.Sensor_pb2 import Sensor as PBSensor
from zepben.protobuf.cim.iec61970.base.core.AcDcTerminal_pb2 import AcDcTerminal as PBAcDcTerminal
from zepben.protobuf.cim.iec61970.base.core.BaseVoltage_pb2 import BaseVoltage as PBBaseVoltage
from zepben.protobuf.cim.iec61970.base.core.ConductingEquipment_pb2 import ConductingEquipment as PBConductingEquipment
from zepben.protobuf.cim.iec61970.base.core.ConnectivityNodeContainer_pb2 import ConnectivityNodeContainer as PBConnectivityNodeContainer
from zepben.protobuf.cim.iec61970.base.core.ConnectivityNode_pb2 import ConnectivityNode as PBConnectivityNode
from zepben.protobuf.cim.iec61970.base.core.CurveData_pb2 import CurveData as PBCurveData
from zepben.protobuf.cim.iec61970.base.core.Curve_pb2 import Curve as PBCurve
from zepben.protobuf.cim.iec61970.base.core.EquipmentContainer_pb2 import EquipmentContainer as PBEquipmentContainer
from zepben.protobuf.cim.iec61970.base.core.Equipment_pb2 import Equipment as PBEquipment
from zepben.protobuf.cim.iec61970.base.core.Feeder_pb2 import Feeder as PBFeeder
from zepben.protobuf.cim.iec61970.base.core.GeographicalRegion_pb2 import GeographicalRegion as PBGeographicalRegion
from zepben.protobuf.cim.iec61970.base.core.IdentifiedObject_pb2 import IdentifiedObject as PBIdentifiedObject
from zepben.protobuf.cim.iec61970.base.core.PhaseCode_pb2 import PhaseCode as PBPhaseCode
from zepben.protobuf.cim.iec61970.base.core.PowerSystemResource_pb2 import PowerSystemResource as PBPowerSystemResource
from zepben.protobuf.cim.iec61970.base.core.SubGeographicalRegion_pb2 import SubGeographicalRegion as PBSubGeographicalRegion
from zepben.protobuf.cim.iec61970.base.core.Substation_pb2 import Substation as PBSubstation
from zepben.protobuf.cim.iec61970.base.core.Terminal_pb2 import Terminal as PBTerminal
from zepben.protobuf.cim.iec61970.base.diagramlayout.DiagramObjectPoint_pb2 import DiagramObjectPoint as PBDiagramObjectPoint
from zepben.protobuf.cim.iec61970.base.diagramlayout.DiagramObject_pb2 import DiagramObject as PBDiagramObject
from zepben.protobuf.cim.iec61970.base.diagramlayout.DiagramStyle_pb2 import DiagramStyle as PBDiagramStyle
from zepben.protobuf.cim.iec61970.base.diagramlayout.Diagram_pb2 import Diagram as PBDiagram
from zepben.protobuf.cim.iec61970.base.diagramlayout.OrientationKind_pb2 import OrientationKind as PBOrientationKind
from zepben.protobuf.cim.iec61970.base.domain.UnitSymbol_pb2 import UnitSymbol as PBUnitSymbol
from zepben.protobuf.cim.iec61970.base.equivalents.EquivalentBranch_pb2 import EquivalentBranch as PBEquivalentBranch
from zepben.protobuf.cim.iec61970.base.equivalents.EquivalentEquipment_pb2 import EquivalentEquipment as PBEquivalentEquipment
from zepben.protobuf.cim.iec61970.base.generation.production.BatteryStateKind_pb2 import BatteryStateKind as PBBatteryStateKind
from zepben.protobuf.cim.iec61970.base.generation.production.BatteryUnit_pb2 import BatteryUnit as PBBatteryUnit
from zepben.protobuf.cim.iec61970.base.generation.production.PhotoVoltaicUnit_pb2 import PhotoVoltaicUnit as PBPhotoVoltaicUnit
from zepben.protobuf.cim.iec61970.base.generation.production.PowerElectronicsUnit_pb2 import PowerElectronicsUnit as PBPowerElectronicsUnit
from zepben.protobuf.cim.iec61970.base.generation.production.PowerElectronicsWindUnit_pb2 import PowerElectronicsWindUnit as PBPowerElectronicsWindUnit
from zepben.protobuf.cim.iec61970.base.meas.Accumulator_pb2 import Accumulator as PBAccumulator
from zepben.protobuf.cim.iec61970.base.meas.Analog_pb2 import Analog as PBAnalog
from zepben.protobuf.cim.iec61970.base.meas.Control_pb2 import Control as PBControl
from zepben.protobuf.cim.iec61970.base.meas.Discrete_pb2 import Discrete as PBDiscrete
from zepben.protobuf.cim.iec61970.base.meas.IoPoint_pb2 import IoPoint as PBIoPoint
from zepben.protobuf.cim.iec61970.base.meas.Measurement_pb2 import Measurement as PBMeasurement
from zepben.protobuf.cim.iec61970.base.protection.CurrentRelay_pb2 import CurrentRelay as PBCurrentRelay
from zepben.protobuf.cim.iec61970.base.scada.RemoteControl_pb2 import RemoteControl as PBRemoteControl
from zepben.protobuf.cim.iec61970.base.scada.RemotePoint_pb2 import RemotePoint as PBRemotePoint
from zepben.protobuf.cim.iec61970.base.scada.RemoteSource_pb2 import RemoteSource as PBRemoteSource
from zepben.protobuf.cim.iec61970.base.wires.AcLineSegment_pb2 import AcLineSegment as PBAcLineSegment
from zepben.protobuf.cim.iec61970.base.wires.Breaker_pb2 import Breaker as PBBreaker
from zepben.protobuf.cim.iec61970.base.wires.BusbarSection_pb2 import BusbarSection as PBBusbarSection
from zepben.protobuf.cim.iec61970.base.wires.Clamp_pb2 import Clamp as PBClamp
from zepben.protobuf.cim.iec61970.base.wires.Conductor_pb2 import Conductor as PBConductor
from zepben.protobuf.cim.iec61970.base.wires.Connector_pb2 import Connector as PBConnector
from zepben.protobuf.cim.iec61970.base.wires.Cut_pb2 import Cut as PBCut
from zepben.protobuf.cim.iec61970.base.wires.Disconnector_pb2 import Disconnector as PBDisconnector
from zepben.protobuf.cim.iec61970.base.wires.EarthFaultCompensator_pb2 import EarthFaultCompensator as PBEarthFaultCompensator
from zepben.protobuf.cim.iec61970.base.wires.EnergyConnection_pb2 import EnergyConnection as PBEnergyConnection
from zepben.protobuf.cim.iec61970.base.wires.EnergyConsumerPhase_pb2 import EnergyConsumerPhase as PBEnergyConsumerPhase
from zepben.protobuf.cim.iec61970.base.wires.EnergyConsumer_pb2 import EnergyConsumer as PBEnergyConsumer
from zepben.protobuf.cim.iec61970.base.wires.EnergySourcePhase_pb2 import EnergySourcePhase as PBEnergySourcePhase
from zepben.protobuf.cim.iec61970.base.wires.EnergySource_pb2 import EnergySource as PBEnergySource
from zepben.protobuf.cim.iec61970.base.wires.Fuse_pb2 import Fuse as PBFuse
from zepben.protobuf.cim.iec61970.base.wires.GroundDisconnector_pb2 import GroundDisconnector as PBGroundDisconnector
from zepben.protobuf.cim.iec61970.base.wires.Ground_pb2 import Ground as PBGround
from zepben.protobuf.cim.iec61970.base.wires.GroundingImpedance_pb2 import GroundingImpedance as PBGroundingImpedance
from zepben.protobuf.cim.iec61970.base.wires.Jumper_pb2 import Jumper as PBJumper
from zepben.protobuf.cim.iec61970.base.wires.Junction_pb2 import Junction as PBJunction
from zepben.protobuf.cim.iec61970.base.wires.Line_pb2 import Line as PBLine
from zepben.protobuf.cim.iec61970.base.wires.LinearShuntCompensator_pb2 import LinearShuntCompensator as PBLinearShuntCompensator
from zepben.protobuf.cim.iec61970.base.wires.LoadBreakSwitch_pb2 import LoadBreakSwitch as PBLoadBreakSwitch
from zepben.protobuf.cim.iec61970.base.wires.PerLengthImpedance_pb2 import PerLengthImpedance as PBPerLengthImpedance
from zepben.protobuf.cim.iec61970.base.wires.PerLengthLineParameter_pb2 import PerLengthLineParameter as PBPerLengthLineParameter
from zepben.protobuf.cim.iec61970.base.wires.PerLengthPhaseImpedance_pb2 import PerLengthPhaseImpedance as PBPerLengthPhaseImpedance
from zepben.protobuf.cim.iec61970.base.wires.PerLengthSequenceImpedance_pb2 import PerLengthSequenceImpedance as PBPerLengthSequenceImpedance
from zepben.protobuf.cim.iec61970.base.wires.PhaseImpedanceData_pb2 import PhaseImpedanceData as PBPhaseImpedanceData
from zepben.protobuf.cim.iec61970.base.wires.PhaseShuntConnectionKind_pb2 import PhaseShuntConnectionKind as PBPhaseShuntConnectionKind
from zepben.protobuf.cim.iec61970.base.wires.PowerElectronicsConnectionPhase_pb2 import PowerElectronicsConnectionPhase as PBPowerElectronicsConnectionPhase
from zepben.protobuf.cim.iec61970.base.wires.PowerElectronicsConnection_pb2 import PowerElectronicsConnection as PBPowerElectronicsConnection
from zepben.protobuf.cim.iec61970.base.wires.PowerTransformerEnd_pb2 import PowerTransformerEnd as PBPowerTransformerEnd
from zepben.protobuf.cim.iec61970.base.wires.PowerTransformer_pb2 import PowerTransformer as PBPowerTransformer
from zepben.protobuf.cim.iec61970.base.wires.ProtectedSwitch_pb2 import ProtectedSwitch as PBProtectedSwitch
from zepben.protobuf.cim.iec61970.base.wires.RatioTapChanger_pb2 import RatioTapChanger as PBRatioTapChanger
from zepben.protobuf.cim.iec61970.base.wires.ReactiveCapabilityCurve_pb2 import ReactiveCapabilityCurve as PBReactiveCapabilityCurve
from zepben.protobuf.cim.iec61970.base.wires.Recloser_pb2 import Recloser as PBRecloser
from zepben.protobuf.cim.iec61970.base.wires.RegulatingCondEq_pb2 import RegulatingCondEq as PBRegulatingCondEq
from zepben.protobuf.cim.iec61970.base.wires.RegulatingControlModeKind_pb2 import RegulatingControlModeKind as PBRegulatingControlModeKind
from zepben.protobuf.cim.iec61970.base.wires.RegulatingControl_pb2 import RegulatingControl as PBRegulatingControl
from zepben.protobuf.cim.iec61970.base.wires.RotatingMachine_pb2 import RotatingMachine as PBRotatingMachine
from zepben.protobuf.cim.iec61970.base.wires.SVCControlMode_pb2 import SVCControlMode as PBSVCControlMode
from zepben.protobuf.cim.iec61970.base.wires.SeriesCompensator_pb2 import SeriesCompensator as PBSeriesCompensator
from zepben.protobuf.cim.iec61970.base.wires.ShuntCompensator_pb2 import ShuntCompensator as PBShuntCompensator
from zepben.protobuf.cim.iec61970.base.wires.SinglePhaseKind_pb2 import SinglePhaseKind as PBSinglePhaseKind
from zepben.protobuf.cim.iec61970.base.wires.StaticVarCompensator_pb2 import StaticVarCompensator as PBStaticVarCompensator
from zepben.protobuf.cim.iec61970.base.wires.Switch_pb2 import Switch as PBSwitch
from zepben.protobuf.cim.iec61970.base.wires.SynchronousMachineKind_pb2 import SynchronousMachineKind as PBSynchronousMachineKind
from zepben.protobuf.cim.iec61970.base.wires.SynchronousMachine_pb2 import SynchronousMachine as PBSynchronousMachine
from zepben.protobuf.cim.iec61970.base.wires.TapChangerControl_pb2 import TapChangerControl as PBTapChangerControl
from zepben.protobuf.cim.iec61970.base.wires.TapChanger_pb2 import TapChanger as PBTapChanger
from zepben.protobuf.cim.iec61970.base.wires.TransformerEnd_pb2 import TransformerEnd as PBTransformerEnd
from zepben.protobuf.cim.iec61970.base.wires.TransformerStarImpedance_pb2 import TransformerStarImpedance as PBTransformerStarImpedance
from zepben.protobuf.cim.iec61970.base.wires.WindingConnection_pb2 import WindingConnection as PBWindingConnection
from zepben.protobuf.cim.iec61970.infiec61970.feeder.Circuit_pb2 import Circuit as PBCircuit
from zepben.protobuf.dc.dc_data_pb2 import DiagramIdentifiedObject
from zepben.protobuf.nc.nc_data_pb2 import NetworkIdentifiedObject

MIN_32_BIT_INTEGER = -2147483647  # _UNKNOWN_INT = -2147483648
MAX_32_BIT_INTEGER = 2147483647
MAX_32_BIT_UNSIGNED_INTEGER = 4294967294  # _UNKNOWN_UINT = 4294967295
MAX_64_BIT_INTEGER = 9223372036854775807
MIN_64_BIT_INTEGER = -9223372036854775807  # _UNKNOWN_LONG = -9223372036854775808
TEXT_MAX_SIZE = 6
FLOAT_MIN = -100.0
FLOAT_MAX = 1000.0
MAX_END_NUMBER = 3
MAX_SEQUENCE_NUMBER = 40
MIN_SEQUENCE_NUMBER = 1
ALPHANUM = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"


##################################
# Extensions IEC61968 Asset Info #
##################################

def floats(*args, **kwargs):
    kwargs.update({"width": 32})
    return hypo_floats(*args, **kwargs)

def lists(*args, **kwargs):
    kwargs.update({"min_size": 1})
    return hypo_lists(*args, **kwargs)

def relay_info():
    return builds(
        PBRelayInfo,
        ai=asset_info(),
        curveSettingSet=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        **nullable_bool_settings("recloseFast"),
        recloseDelays=lists(floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX), max_size=3)
    )


################################
# Extensions IEC61968 Metering #
################################

def pan_demand_response_function():
    return builds(
        PBPanDemandResponseFunction,
        edf=end_device_function(),
        kind=sampled_from(PBEndDeviceFunctionKind.values()),
        applianceSet=integers(min_value=0, max_value=4095),
    )


#################################
# Extensions IEC61970 Base Core #
#################################

def site():
    return builds(PBSite, ec=equipment_container())


###################################
# Extensions IEC61970 Base Feeder #
###################################

def loop():
    return builds(
        PBLoop,
        io=identified_object(),
        circuitMRIDs=lists(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), max_size=2),
        substationMRIDs=lists(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), max_size=2),
        normalEnergizingSubstationMRIDs=lists(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), max_size=2)
    )


def lv_feeder():
    return builds(
        PBLvFeeder,
        ec=equipment_container(),
        normalHeadTerminalMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        normalEnergizingFeederMRIDs=lists(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), max_size=2)
    )


##################################################
# Extensions IEC61970 Base Generation Production #
##################################################

def ev_charging_unit():
    return builds(PBEvChargingUnit, peu=power_electronics_unit())


#######################################
# Extensions IEC61970 Base Protection #
#######################################

def distance_relay():
    return builds(
        PBDistanceRelay,
        prf=protection_relay_function(),
        backwardBlindSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        backwardReachSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        backwardReactanceSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        forwardBlindSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        forwardReachSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        forwardReactanceSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        operationPhaseAngle1Set=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        operationPhaseAngle2Set=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        operationPhaseAngle3Set=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    )


def protection_relay_function():
    return builds(
        PBProtectionRelayFunction,
        psr=power_system_resource(),
        modelSet=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        **nullable_bool_settings("reclosing"),
        relayDelayTimeSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        protectionKind=sampled_from(PBProtectionKind.values()),
        **nullable_bool_settings("directable"),
        powerDirection=sampled_from(PBPowerDirectionKind.values()),
        sensorMRIDs=lists(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), max_size=2),
        protectedSwitchMRIDs=lists(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), max_size=2),
        schemeMRIDs=lists(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), max_size=2),
        timeLimits=lists(floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)),
        thresholds=lists(relay_setting(), max_size=4)
    )


def protection_relay_scheme():
    return builds(
        PBProtectionRelayScheme,
        io=identified_object(),
        systemMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        functionMRIDs=lists(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), max_size=2)
    )


def protection_relay_system():
    return builds(
        PBProtectionRelaySystem,
        eq=equipment(),
        protectionKind=sampled_from(PBProtectionKind.values()),
        schemeMRIDs=lists(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), max_size=2)
    )


def relay_setting():
    return builds(
        PBRelaySetting,
        nameSet=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        unitSymbol=sampled_from(PBUnitSymbol.values()),
        value=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)
    )


def voltage_relay():
    return builds(
        PBVoltageRelay,
        prf=protection_relay_function()
    )


##################################
# Extensions IEC61970 Base Wires #
##################################

def battery_control():
    return builds(
        PBBatteryControl,
        rc=regulating_control(),
        chargingRateSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        dischargingRateSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        reservePercentSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        controlMode=sampled_from(PBBatteryControlMode.values())
    )


def transformer_end_rated_s():
    return builds(
        PBTransformerEndRatedS,
        coolingType=sampled_from(PBTransformerCoolingType.values()),
        ratedS=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    )


#######################
# IEC61968 Asset Info #
#######################

def cable_info():
    return builds(PBCableInfo, wi=wire_info())


def no_load_test():
    return builds(
        PBNoLoadTest,
        tt=transformer_test(),
        energisedEndVoltageSet=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        excitingCurrentSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        excitingCurrentZeroSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        lossSet=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        lossZeroSet=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER)
    )


def open_circuit_test():
    return builds(
        PBOpenCircuitTest,
        tt=transformer_test(),
        energisedEndStepSet=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        energisedEndVoltageSet=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        openEndStepSet=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        openEndVoltageSet=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        phaseShiftSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)
    )


def overhead_wire_info():
    return builds(PBOverheadWireInfo, wi=wire_info())


def power_transformer_info():
    return builds(
        PBPowerTransformerInfo,
        ai=asset_info(),
        transformerTankInfoMRIDs=lists(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), max_size=2)
    )


def short_circuit_test():
    return builds(
        PBShortCircuitTest,
        tt=transformer_test(),
        currentSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        energisedEndStepSet=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        groundedEndStepSet=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        leakageImpedanceSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        leakageImpedanceZeroSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        lossSet=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        lossZeroSet=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        powerSet=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        voltageSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        voltageOhmicPartSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)
    )


def shunt_compensator_info():
    return builds(
        PBShuntCompensatorInfo,
        ai=asset_info(),
        maxPowerLossSet=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        ratedCurrentSet=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        ratedReactivePowerSet=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        ratedVoltageSet=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    )


def switch_info():
    return builds(
        PBSwitchInfo,
        ai=asset_info(),
        ratedInterruptingTimeSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)
    )


def transformer_end_info():
    return builds(
        PBTransformerEndInfo,
        ai=asset_info(),
        connectionKind=sampled_from(PBWindingConnection.values()),
        emergencySSet=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        endNumber=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        insulationUSet=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        phaseAngleClockSet=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        rSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        ratedSSet=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        ratedUSet=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        shortTermSSet=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        transformerStarImpedanceMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE)
    )


def transformer_tank_info():
    return builds(
        PBTransformerTankInfo,
        ai=asset_info(),
        transformerEndInfoMRIDs=lists(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), max_size=2)
    )


def transformer_test():
    return builds(
        PBTransformerTest,
        io=identified_object(),
        basePowerSet=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        temperatureSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)
    )


def wire_info():
    return builds(
        PBWireInfo,
        ai=asset_info(),
        ratedCurrentSet=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        material=sampled_from(PBWireMaterialKind.values())
    )


###################
# IEC61968 Assets #
###################

def asset():
    return builds(
        PBAsset,
        io=identified_object(),
        locationMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        organisationRoleMRIDs=lists(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), max_size=2),
        powerSystemResourceMRIDs=lists(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), max_size=2)
    )


def asset_container():
    return builds(PBAssetContainer, at=asset())


def asset_function():
    return builds(PBAssetFunction, io=identified_object())


def asset_info():
    return builds(PBAssetInfo, io=identified_object())


def asset_organisation_role():
    d = {"or": organisation_role()}  # To set field `or` that's a reserved word
    return builds(PBAssetOrganisationRole, **d)


def asset_owner():
    return builds(PBAssetOwner, aor=asset_organisation_role())


def streetlight():
    return builds(
        PBStreetlight,
        at=asset(),
        poleMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        lightRatingSet=integers(min_value=0, max_value=MAX_32_BIT_INTEGER),
        lampKind=sampled_from(PBStreetlightLampKind.values())
    )


def structure():
    return builds(PBStructure, ac=asset_container())


###################
# IEC61968 Common #
###################

def agreement():
    return builds(PBAgreement, doc=document())


def document():
    return builds(
        PBDocument,
        io=identified_object(),
        titleSet=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        createdDateTime=timestamp(),
        authorNameSet=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        typeSet=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        statusSet=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        commentSet=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE)
    )


def location():
    return builds(PBLocation, io=identified_object(), mainAddress=street_address(), positionPoints=lists(position_point(), max_size=2))


def organisation():
    return builds(PBOrganisation, io=identified_object())


def organisation_role():
    return builds(PBOrganisationRole, io=identified_object(), organisationMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE))


def position_point():
    return builds(PBPositionPoint, xPosition=floats(min_value=-180.0, max_value=180.0), yPosition=floats(min_value=-90.0, max_value=90.0))


def street_address():
    return builds(
        PBStreetAddress,
        postalCodeSet=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        townDetail=town_detail(),
        poBoxSet=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        streetDetail=street_detail()
    )


def street_detail():
    return builds(
        PBStreetDetail,
        buildingNameSet=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        floorIdentificationSet=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        nameSet=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        numberSet=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        suiteNumberSet=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        typeSet=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        displayAddressSet=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE)
    )


def town_detail():
    return builds(PBTownDetail, nameSet=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), stateOrProvinceSet=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE))


######################
# IEC61968 Customers #
######################


def customer():
    d = {"or": organisation_role()}  # To set field `or` that's a reserved word
    return builds(
        PBCustomer,
        kind=sampled_from(PBCustomerKind.values()),
        customerAgreementMRIDs=lists(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), max_size=2),
        **d
    )


def customer_agreement():
    return builds(
        PBCustomerAgreement,
        agr=agreement(),
        customerMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        pricingStructureMRIDs=lists(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), max_size=2),
    )


def pricing_structure():
    return builds(
        PBPricingStructure,
        doc=document(),
        tariffMRIDs=lists(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), max_size=2),
    )


def tariff():
    return builds(
        PBTariff,
        doc=document(),
    )


#####################################
# IEC61968 InfIEC61968 InfAssetInfo #
#####################################

def current_transformer_info():
    return builds(
        PBCurrentTransformerInfo,
        ai=asset_info(),
        accuracyClassSet=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        accuracyLimitSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        coreCountSet=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        ctClassSet=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        kneePointVoltageSet=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        maxRatio=ratio(),
        nominalRatio=ratio(),
        primaryRatioSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        ratedCurrentSet=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        secondaryFlsRatingSet=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        secondaryRatioSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        usageSet=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE)
    )


def potential_transformer_info():
    return builds(
        PBPotentialTransformerInfo,
        ai=asset_info(),
        accuracyClassSet=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        nominalRatio=ratio(),
        primaryRatioSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        ptClassSet=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        ratedVoltageSet=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        secondaryRatioSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)
    )


##################################
# IEC61968 InfIEC61968 InfAssets #
##################################


def pole():
    return builds(
        PBPole,
        st=structure(),
        streetlightMRIDs=lists(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), max_size=2),
        classificationSet=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE)
    )


##################################
# IEC61968 InfIEC61968 InfCommon #
##################################

def ratio():
    return builds(PBRatio, denominator=floats(min_value=0.10000000149011612, max_value=1000.0), numerator=floats(min_value=0.0, max_value=1000.0))


#####################
# IEC61968 Metering #
#####################

def end_device():
    return builds(
        PBEndDevice,
        ac=asset_container(),
        usagePointMRIDs=lists(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), max_size=2),
        customerMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        serviceLocationMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        endDeviceFunctionMRIDs=lists(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), max_size=2),
    )


def end_device_function():
    return builds(
        PBEndDeviceFunction,
        af=asset_function(),
        **nullable_bool_settings("enabled"),
    )


def meter():
    return builds(PBMeter, ed=end_device())


def usage_point():
    return builds(
        PBUsagePoint,
        io=identified_object(),
        usagePointLocationMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        equipmentMRIDs=lists(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), max_size=2),
        endDeviceMRIDs=lists(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), max_size=2),
        isVirtualSet=booleans(),
        connectionCategorySet=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        ratedPowerSet=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        approvedInverterCapacitySet=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER)
    )


#######################
# IEC61968 Operations #
#######################

def operational_restriction():
    return builds(PBOperationalRestriction, doc=document())


#####################################
# IEC61970 Base Auxiliary Equipment #
#####################################

def auxiliary_equipment():
    return builds(PBAuxiliaryEquipment, eq=equipment(), terminalMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE))


def current_transformer():
    return builds(PBCurrentTransformer, sn=sensor(), coreBurdenSet=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER))


def fault_indicator():
    return builds(PBFaultIndicator, ae=auxiliary_equipment())


def potential_transformer():
    return builds(PBPotentialTransformer, sn=sensor(), type=sampled_from(PBPotentialTransformerKind.values()))


def sensor():
    return builds(PBSensor, ae=auxiliary_equipment(), relayFunctionMRIDs=lists(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), max_size=2))


######################
# IEC61970 Base Core #
######################

def ac_dc_terminal():
    return builds(PBAcDcTerminal, io=identified_object())


def base_voltage():
    return builds(PBBaseVoltage, io=identified_object(), nominalVoltage=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER))


def conducting_equipment():
    return builds(
        PBConductingEquipment,
        eq=equipment(),
        baseVoltageMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        terminalMRIDs=lists(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), max_size=2)
    )


def connectivity_node():
    return builds(PBConnectivityNode, io=identified_object())


def connectivity_node_container():
    return builds(PBConnectivityNodeContainer, psr=power_system_resource())


def curve():
    return builds(
        PBCurve,
        io=identified_object(),
        curveData=lists(curve_data(), max_size=2)
    )


def curve_data():
    return builds(
        PBCurveData,
        xValue=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        y1Value=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        y2ValueSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        y3ValueSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    )


def equipment():
    return builds(
        PBEquipment,
        psr=power_system_resource(),
        inService=booleans(),
        normallyInService=booleans(),
        commissionedDate=timestamp(),
        equipmentContainerMRIDs=lists(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), max_size=2),
        usagePointMRIDs=lists(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), max_size=2),
        operationalRestrictionMRIDs=lists(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), max_size=2),
        currentContainerMRIDs=lists(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), max_size=2)
    )


def equipment_container():
    return builds(PBEquipmentContainer, cnc=connectivity_node_container())


def feeder():
    return builds(
        PBFeeder,
        ec=equipment_container(),
        normalHeadTerminalMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        normalEnergizingSubstationMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        normalEnergizedLvFeederMRIDs=lists(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), max_size=2)
    )


def geographical_region():
    return builds(PBGeographicalRegion, io=identified_object(), subGeographicalRegionMRIDs=lists(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), max_size=2))


def identified_object():
    return builds(
        PBIdentifiedObject,
        mRID=uuids(version=4).map(lambda x: str(x)),
        nameSet=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        descriptionSet=text(alphabet=ALPHANUM, min_size=1, max_size=TEXT_MAX_SIZE)
    )


def power_system_resource():
    return builds(
        PBPowerSystemResource,
        io=identified_object(),
        assetInfoMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        locationMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        assetMRIDs=lists(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), max_size=2)
    )


def sub_geographical_region():
    return builds(
        PBSubGeographicalRegion,
        io=identified_object(),
        geographicalRegionMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        substationMRIDs=lists(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), max_size=2)
    )


def substation():
    return builds(
        PBSubstation,
        ec=equipment_container(),
        subGeographicalRegionMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        normalEnergizedFeederMRIDs=lists(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), max_size=2),
        loopMRIDs=lists(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), max_size=2),
        normalEnergizedLoopMRIDs=lists(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), max_size=2),
        circuitMRIDs=lists(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), max_size=2)
    )


def terminal():
    return builds(
        PBTerminal,
        ad=ac_dc_terminal(),
        conductingEquipmentMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        connectivityNodeMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        tracedPhases=integers(min_value=0, max_value=65535),
        phases=sampled_from(PBPhaseCode.values()),
        sequenceNumber=integers(min_value=MIN_SEQUENCE_NUMBER, max_value=MAX_SEQUENCE_NUMBER)
    )


################################
# IEC61970 Base Diagram Layout #
################################


def diagram():
    return builds(
        PBDiagram,
        io=identified_object(),
        diagramStyle=sampled_from(PBDiagramStyle.values()),
        orientationKind=sampled_from(PBOrientationKind.values()),
        diagramObjectMRIDs=lists(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), max_size=2)
    )


def diagram_object():
    return builds(
        PBDiagramObject,
        io=identified_object(),
        diagramMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        diagramObjectStyleSet=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        rotation=floats(min_value=0.0, max_value=360.0),
        identifiedObjectMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        diagramObjectPoints=lists(diagram_object_point(), max_size=2)
    )


def diagram_object_point():
    return builds(
        PBDiagramObjectPoint,
        xPosition=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        yPosition=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    )


#############################
# IEC61970 Base Equivalents #
#############################

def equivalent_branch():
    return builds(
        PBEquivalentBranch,
        ee=equivalent_equipment(),
        negativeR12Set=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        negativeR21Set=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        negativeX12Set=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        negativeX21Set=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        positiveR12Set=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        positiveR21Set=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        positiveX12Set=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        positiveX21Set=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        rSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        r21Set=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        xSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        x21Set=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        zeroR12Set=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        zeroR21Set=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        zeroX12Set=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        zeroX21Set=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)
    )


def equivalent_equipment():
    return builds(PBEquivalentEquipment, ce=conducting_equipment())


#######################################
# IEC61970 Base Generation Production #
#######################################

def battery_unit():
    return builds(
        PBBatteryUnit,
        peu=power_electronics_unit(),
        batteryState=sampled_from(PBBatteryStateKind.values()),
        ratedESet=integers(min_value=0, max_value=MAX_64_BIT_INTEGER),
        storedESet=integers(min_value=0, max_value=MAX_64_BIT_INTEGER),
        batteryControlMRIDs=lists(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), max_size=2)
    )


def photo_voltaic_unit():
    return builds(PBPhotoVoltaicUnit, peu=power_electronics_unit())


def power_electronics_unit():
    return builds(
        PBPowerElectronicsUnit,
        eq=equipment(),
        powerElectronicsConnectionMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        maxPSet=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        minPSet=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER)
    )


def power_electronics_wind_unit():
    return builds(PBPowerElectronicsWindUnit, peu=power_electronics_unit())


######################
# IEC61970 Base Meas #
######################

def accumulator():
    return builds(PBAccumulator, measurement=measurement())


def analog():
    return builds(PBAnalog, measurement=measurement(), positiveFlowInSet=booleans())


def control():
    return builds(
        PBControl,
        ip=io_point(),
        powerSystemResourceMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        remoteControlMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE)
    )


def discrete():
    return builds(PBDiscrete, measurement=measurement())


def io_point():
    return builds(PBIoPoint, io=identified_object())


def measurement():
    return builds(
        PBMeasurement,
        io=identified_object(),
        remoteSourceMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        powerSystemResourceMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        terminalMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        phases=sampled_from(PBPhaseCode.values()),
        unitSymbol=sampled_from(PBUnitSymbol.values())
    )


############################
# IEC61970 Base Protection #
############################

def current_relay():
    return builds(
        PBCurrentRelay,
        prf=protection_relay_function(),
        currentLimit1Set=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        **nullable_bool_settings("inverseTimeFlag"),
        timeDelay1Set=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)
    )


#######################
# IEC61970 Base Scada #
#######################

def remote_control():
    return builds(PBRemoteControl, rp=remote_point(), controlMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE))


def remote_point():
    return builds(PBRemotePoint, io=identified_object())


def remote_source():
    return builds(PBRemoteSource, rp=remote_point(), measurementMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE))


#######################
# IEC61970 Base Wires #
#######################

def ac_line_segment():
    return builds(PBAcLineSegment, cd=conductor(), perLengthImpedanceMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE))


def breaker():
    return builds(
        PBBreaker,
        sw=protected_switch(),
        inTransitTimeSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)
    )


def busbar_section():
    return builds(PBBusbarSection, cn=connector())


def clamp():
    return builds(
        PBClamp,
        ce=conducting_equipment(),
        lengthFromTerminal1Set=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        acLineSegmentMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
    )


def conductor():
    return builds(PBConductor, ce=conducting_equipment(), lengthSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX))


def connector():
    return builds(PBConnector, ce=conducting_equipment())


def cut():
    return builds(
        PBCut,
        sw=switch(),
        lengthFromTerminal1Set=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        acLineSegmentMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
    )


def disconnector():
    return builds(PBDisconnector, sw=switch())


def earth_fault_compensator():
    return builds(PBEarthFaultCompensator, ce=conducting_equipment(), rSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX))


def energy_connection():
    return builds(PBEnergyConnection, ce=conducting_equipment())


def energy_consumer():
    return builds(
        PBEnergyConsumer,
        ec=energy_connection(),
        energyConsumerPhasesMRIDs=lists(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), max_size=2),
        customerCountSet=integers(min_value=0, max_value=MAX_32_BIT_INTEGER),
        groundedSet=booleans(), pSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        pFixedSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        phaseConnection=sampled_from(PBPhaseShuntConnectionKind.values()),
        qSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        qFixedSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)
    )


def energy_consumer_phase():
    return builds(
        PBEnergyConsumerPhase,
        psr=power_system_resource(),
        energyConsumerMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        phase=sampled_from(PBSinglePhaseKind.values()),
        pSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        pFixedSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        qSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        qFixedSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)
    )


def energy_source():
    return builds(
        PBEnergySource,
        ec=energy_connection(),
        energySourcePhasesMRIDs=lists(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), max_size=2),
        activePowerSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        reactivePowerSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        voltageAngleSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        voltageMagnitudeSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        rSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        xSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        pMaxSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        pMinSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        r0Set=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        rnSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        x0Set=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        xnSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)
    )


def energy_source_phase():
    return builds(
        PBEnergySourcePhase,
        psr=power_system_resource(),
        energySourceMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        phase=sampled_from(PBSinglePhaseKind.values())
    )


def fuse():
    return builds(PBFuse, sw=switch(), functionMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE))


def ground():
    return builds(PBGround, ce=conducting_equipment())


def ground_disconnector():
    return builds(PBGroundDisconnector, sw=switch())


def grounding_impedance():
    return builds(PBGroundingImpedance, efc=earth_fault_compensator(), xSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX))


def jumper():
    return builds(PBJumper, sw=switch())


def junction():
    return builds(PBJunction, cn=connector())


def line():
    return builds(PBLine, ec=equipment_container())


def linear_shunt_compensator():
    return builds(
        PBLinearShuntCompensator,
        sc=shunt_compensator(),
        b0PerSectionSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        bPerSectionSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        g0PerSectionSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        gPerSectionSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)
    )


def load_break_switch():
    return builds(PBLoadBreakSwitch, ps=protected_switch())


def per_length_impedance():
    return builds(PBPerLengthImpedance, lp=per_length_line_parameter())


def per_length_line_parameter():
    return builds(PBPerLengthLineParameter, io=identified_object())


def per_length_phase_impedance():
    return builds(
        PBPerLengthPhaseImpedance,
        pli=per_length_impedance(),
        phaseImpedanceData=lists(phase_impedance_data(), max_size=2)
    )


def per_length_sequence_impedance():
    return builds(
        PBPerLengthSequenceImpedance,
        pli=per_length_impedance(),
        rSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        xSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        r0Set=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        x0Set=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        bchSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        gchSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        b0chSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        g0chSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)
    )


def phase_impedance_data():
    return builds(
        PBPhaseImpedanceData,
        fromPhase=sampled_from(PBSinglePhaseKind.values()),
        toPhase=sampled_from(PBSinglePhaseKind.values()),
        bSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        gSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        rSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        xSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
    )


def power_electronics_connection():
    return builds(
        PBPowerElectronicsConnection,
        rce=regulating_cond_eq(),
        powerElectronicsUnitMRIDs=lists(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE)),
        powerElectronicsConnectionPhaseMRIDs=lists(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE)),
        maxIFaultSet=integers(min_value=0, max_value=MAX_32_BIT_INTEGER),
        maxQSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        minQSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        pSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        qSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        ratedSSet=integers(min_value=0, max_value=MAX_32_BIT_INTEGER),
        ratedUSet=integers(min_value=0, max_value=MAX_32_BIT_INTEGER),
        inverterStandardSet=text(alphabet=ALPHANUM, min_size=1, max_size=TEXT_MAX_SIZE),
        sustainOpOvervoltLimitSet=integers(min_value=0, max_value=MAX_32_BIT_INTEGER),
        stopAtOverFreqSet=floats(min_value=51.0, max_value=52.0),
        stopAtUnderFreqSet=floats(min_value=47.0, max_value=49.0),
        **nullable_bool_settings("invVoltWattRespMode"),
        invWattRespV1Set=integers(min_value=200, max_value=300),
        invWattRespV2Set=integers(min_value=216, max_value=230),
        invWattRespV3Set=integers(min_value=235, max_value=255),
        invWattRespV4Set=integers(min_value=244, max_value=265),
        invWattRespPAtV1Set=floats(min_value=0.0, max_value=1.0),
        invWattRespPAtV2Set=floats(min_value=0.0, max_value=1.0),
        invWattRespPAtV3Set=floats(min_value=0.0, max_value=1.0),
        invWattRespPAtV4Set=floats(min_value=0.0, max_value=0.20000000298023224),
        **nullable_bool_settings("invVoltVarRespMode"),
        invVarRespV1Set=integers(min_value=200, max_value=300),
        invVarRespV2Set=integers(min_value=200, max_value=300),
        invVarRespV3Set=integers(min_value=200, max_value=300),
        invVarRespV4Set=integers(min_value=200, max_value=300),
        invVarRespQAtV1Set=floats(min_value=0.0, max_value=0.6000000238418579),
        invVarRespQAtV2Set=floats(min_value=-1.0, max_value=1.0),
        invVarRespQAtV3Set=floats(min_value=-1.0, max_value=1.0),
        invVarRespQAtV4Set=floats(min_value=-0.6000000238418579, max_value=0.0),
        **nullable_bool_settings("invReactivePowerMode"),
        invFixReactivePowerSet=floats(min_value=-1.0, max_value=1.0),
    )


def power_electronics_connection_phase():
    return builds(
        PBPowerElectronicsConnectionPhase,
        psr=power_system_resource(), powerElectronicsConnectionMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        phase=sampled_from(PBSinglePhaseKind.values()),
        pSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        qSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)
    )


def power_transformer():
    return builds(
        PBPowerTransformer,
        ce=conducting_equipment(),
        powerTransformerEndMRIDs=lists(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), max_size=2),
        vectorGroup=sampled_from(PBVectorGroup.values()),
        transformerUtilisationSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)
    )


def power_transformer_end():
    return builds(
        PBPowerTransformerEnd,
        te=transformer_end(),
        powerTransformerMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        ratedUSet=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        rSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        r0Set=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        xSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        x0Set=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        connectionKind=sampled_from(PBWindingConnection.values()),
        bSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        b0Set=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        gSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        g0Set=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        phaseAngleClockSet=integers(min_value=0, max_value=11),
        ratings=lists(transformer_end_rated_s(), max_size=3)
    )


def protected_switch():
    return builds(
        PBProtectedSwitch,
        sw=switch(),
        breakingCapacitySet=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        relayFunctionMRIDs=lists(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), max_size=2)
    )


def ratio_tap_changer():
    return builds(
        PBRatioTapChanger,
        tc=tap_changer(),
        transformerEndMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        stepVoltageIncrementSet=floats(min_value=0.0, max_value=1.0)
    )


def reactive_capability_curve():
    return builds(
        PBReactiveCapabilityCurve,
        c=curve(),
    )


def recloser():
    return builds(PBRecloser, sw=protected_switch())


def regulating_cond_eq():
    return builds(
        PBRegulatingCondEq,
        ec=energy_connection(),
        controlEnabledSet=booleans(),
        regulatingControlMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE)
    )


def regulating_control():
    return builds(
        PBRegulatingControl,
        psr=power_system_resource(),
        discreteSet=booleans(),
        mode=sampled_from(PBRegulatingControlModeKind.values()),
        monitoredPhase=sampled_from(PBPhaseCode.values()),
        targetDeadbandSet=floats(min_value=0.0, max_value=FLOAT_MAX),
        targetValueSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        enabledSet=booleans(),
        maxAllowedTargetValueSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        minAllowedTargetValueSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        ratedCurrentSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        terminalMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        regulatingCondEqMRIDs=lists(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), max_size=2)
    )


def rotating_machine():
    return builds(
        PBRotatingMachine,
        rce=regulating_cond_eq(),
        ratedPowerFactorSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        ratedSSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        ratedUSet=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        pSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        qSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)
    )


def series_compensator():
    return builds(
        PBSeriesCompensator,
        ce=conducting_equipment(),
        rSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        r0Set=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        xSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        x0Set=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        varistorRatedCurrentSet=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        varistorVoltageThresholdSet=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
    )


def shunt_compensator():
    return builds(
        PBShuntCompensator,
        rce=regulating_cond_eq(),
        sectionsSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        groundedSet=booleans(),
        nomUSet=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        phaseConnection=sampled_from(PBPhaseShuntConnectionKind.values())
    )


def static_var_compensator():
    return builds(
        PBStaticVarCompensator,
        rce=regulating_cond_eq(),
        capacitiveRatingSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        inductiveRatingSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        qSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        svcControlMode=sampled_from(PBSVCControlMode.values()),
        voltageSetPointSet=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER)
    )


def switch():
    return builds(
        PBSwitch,
        ce=conducting_equipment(),
        ratedCurrentSet=integers(min_value=1, max_value=MAX_32_BIT_INTEGER),
        normalOpen=booleans(),
        open=booleans()
    )


def synchronous_machine():
    return builds(
        PBSynchronousMachine,
        rm=rotating_machine(),
        baseQSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        condenserPSet=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        earthingSet=booleans(),
        earthingStarPointRSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        earthingStarPointXSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        ikkSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        maxQSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        maxUSet=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        minQSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        minUSet=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        muSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        rSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        r0Set=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        r2Set=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        satDirectSubtransXSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        satDirectSyncXSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        satDirectTransXSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        x0Set=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        x2Set=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        type=sampled_from(PBSynchronousMachineKind.values()),
        operatingMode=sampled_from(PBSynchronousMachineKind.values()),
        reactiveCapabilityCurveMRIDs=one_of(none(), text(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE))),
    )


def tap_changer():
    return builds(
        PBTapChanger,
        psr=power_system_resource(),
        highStepSet=integers(min_value=10, max_value=15),
        lowStepSet=integers(min_value=0, max_value=2),
        stepSet=floats(min_value=2.0, max_value=10.0),
        neutralStepSet=integers(min_value=2, max_value=10),
        neutralUSet=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        normalStepSet=integers(min_value=2, max_value=10),
        controlEnabledSet=booleans(),
        tapChangerControlMRID=text(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE)),
    )


def tap_changer_control():
    return builds(
        PBTapChangerControl,
        rc=regulating_control(),
        limitVoltageSet=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
        **nullable_bool_settings("lineDropCompensation"),
        lineDropRSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        lineDropXSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        reverseLineDropRSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        reverseLineDropXSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        **nullable_bool_settings("forwardLDCBlocking"),
        timeDelaySet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        **nullable_bool_settings("coGenerationEnabled")
    )


def transformer_end():
    return builds(
        PBTransformerEnd,
        io=identified_object(),
        terminalMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        baseVoltageMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        ratioTapChangerMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        endNumber=integers(min_value=MIN_SEQUENCE_NUMBER, max_value=MAX_END_NUMBER),
        groundedSet=booleans(),
        rGroundSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        xGroundSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        starImpedanceMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE)
    )


def transformer_star_impedance():
    return builds(
        PBTransformerStarImpedance,
        io=identified_object(),
        rSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        r0Set=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        xSet=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        x0Set=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
        transformerEndInfoMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE)
    )


###############################
# IEC61970 InfIEC61970 Feeder #
###############################

def circuit():
    return builds(
        PBCircuit,
        l=line(),
        loopMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
        endTerminalMRIDs=lists(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), max_size=2),
        endSubstationMRIDs=lists(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), max_size=2)
    )


#########
# MODEL #
#########

def nullable_bool_settings(flag_name: str, value: Optional[bool] = sampled_from([False, True, None])) -> Dict:
    settings = {}
    if value is None:
        settings[f"{flag_name}Null"] = NullValue.NULL_VALUE
    else:
        settings[f"{flag_name}Set"] = value

    return settings


def timestamp():
    return builds(Timestamp, seconds=integers(min_value=0, max_value=MAX_32_BIT_INTEGER), nanos=integers(min_value=0, max_value=MAX_32_BIT_INTEGER))


##############################
# Network Identified Objects #
##############################

@composite
def network_identified_objects(draw):
    nios = [
        ##################################
        # Extensions IEC61968 Asset Info #
        ##################################

        draw(builds(NetworkIdentifiedObject, relayInfo=relay_info())),

        ################################
        # Extensions IEC61968 Metering #
        ################################

        draw(builds(NetworkIdentifiedObject, panDemandResponseFunction=pan_demand_response_function())),

        #################################
        # Extensions IEC61970 Base Core #
        #################################

        draw(builds(NetworkIdentifiedObject, site=site())),

        ###################################
        # Extensions IEC61970 Base Feeder #
        ###################################

        draw(builds(NetworkIdentifiedObject, loop=loop())),
        draw(builds(NetworkIdentifiedObject, lvFeeder=lv_feeder())),

        ##################################################
        # Extensions IEC61970 Base Generation Production #
        ##################################################

        draw(builds(NetworkIdentifiedObject, evChargingUnit=ev_charging_unit())),

        #######################################
        # Extensions IEC61970 Base Protection #
        #######################################

        draw(builds(NetworkIdentifiedObject, distanceRelay=distance_relay())),
        draw(builds(NetworkIdentifiedObject, protectionRelayScheme=protection_relay_scheme())),
        draw(builds(NetworkIdentifiedObject, protectionRelaySystem=protection_relay_system())),
        draw(builds(NetworkIdentifiedObject, voltageRelay=voltage_relay())),

        ##################################
        # Extensions IEC61970 Base Wires #
        ##################################

        draw(builds(NetworkIdentifiedObject, batteryControl=battery_control())),

        #######################
        # IEC61968 Asset Info #
        #######################

        draw(builds(NetworkIdentifiedObject, cableInfo=cable_info())),
        draw(builds(NetworkIdentifiedObject, noLoadTest=no_load_test())),
        draw(builds(NetworkIdentifiedObject, openCircuitTest=open_circuit_test())),
        draw(builds(NetworkIdentifiedObject, overheadWireInfo=overhead_wire_info())),
        draw(builds(NetworkIdentifiedObject, powerTransformerInfo=power_transformer_info())),
        draw(builds(NetworkIdentifiedObject, shortCircuitTest=short_circuit_test())),
        draw(builds(NetworkIdentifiedObject, shuntCompensatorInfo=shunt_compensator_info())),
        draw(builds(NetworkIdentifiedObject, switchInfo=switch_info())),
        draw(builds(NetworkIdentifiedObject, transformerEndInfo=transformer_end_info())),
        draw(builds(NetworkIdentifiedObject, transformerTankInfo=transformer_tank_info())),

        ###################
        # IEC61968 Assets #
        ###################

        draw(builds(NetworkIdentifiedObject, assetOwner=asset_owner())),
        draw(builds(NetworkIdentifiedObject, streetlight=streetlight())),

        ###################
        # IEC61968 Common #
        ###################

        draw(builds(NetworkIdentifiedObject, location=location())),
        draw(builds(NetworkIdentifiedObject, organisation=organisation())),

        #####################################
        # IEC61968 InfIEC61968 InfAssetInfo #
        #####################################

        draw(builds(NetworkIdentifiedObject, currentTransformerInfo=current_transformer_info())),
        draw(builds(NetworkIdentifiedObject, potentialTransformerInfo=potential_transformer_info())),

        ##################################
        # IEC61968 InfIEC61968 InfAssets #
        ##################################

        draw(builds(NetworkIdentifiedObject, pole=pole())),

        #####################
        # IEC61968 Metering #
        #####################

        draw(builds(NetworkIdentifiedObject, meter=meter())),
        draw(builds(NetworkIdentifiedObject, usagePoint=usage_point())),

        #######################
        # IEC61968 Operations #
        #######################

        draw(builds(NetworkIdentifiedObject, operationalRestriction=operational_restriction())),

        #####################################
        # IEC61970 Base Auxiliary Equipment #
        #####################################

        draw(builds(NetworkIdentifiedObject, currentTransformer=current_transformer())),
        draw(builds(NetworkIdentifiedObject, faultIndicator=fault_indicator())),
        draw(builds(NetworkIdentifiedObject, potentialTransformer=potential_transformer())),

        ######################
        # IEC61970 Base Core #
        ######################

        draw(builds(NetworkIdentifiedObject, baseVoltage=base_voltage())),
        draw(builds(NetworkIdentifiedObject, connectivityNode=connectivity_node())),
        draw(builds(NetworkIdentifiedObject, feeder=feeder())),
        draw(builds(NetworkIdentifiedObject, geographicalRegion=geographical_region())),
        draw(builds(NetworkIdentifiedObject, subGeographicalRegion=sub_geographical_region())),
        draw(builds(NetworkIdentifiedObject, substation=substation())),
        draw(builds(NetworkIdentifiedObject, terminal=terminal())),

        #############################
        # IEC61970 Base Equivalents #
        #############################

        draw(builds(NetworkIdentifiedObject, equivalentBranch=equivalent_branch())),

        #######################################
        # IEC61970 Base Generation Production #
        #######################################

        draw(builds(NetworkIdentifiedObject, batteryUnit=battery_unit())),
        draw(builds(NetworkIdentifiedObject, photoVoltaicUnit=photo_voltaic_unit())),
        draw(builds(NetworkIdentifiedObject, powerElectronicsWindUnit=power_electronics_wind_unit())),

        ######################
        # IEC61970 Base Meas #
        ######################

        draw(builds(NetworkIdentifiedObject, accumulator=accumulator())),
        draw(builds(NetworkIdentifiedObject, analog=analog())),
        draw(builds(NetworkIdentifiedObject, control=control())),
        draw(builds(NetworkIdentifiedObject, discrete=discrete())),

        ############################
        # IEC61970 Base Protection #
        ############################

        draw(builds(NetworkIdentifiedObject, currentRelay=current_relay())),

        #######################
        # IEC61970 Base Scada #
        #######################

        draw(builds(NetworkIdentifiedObject, remoteControl=remote_control())),
        draw(builds(NetworkIdentifiedObject, remoteSource=remote_source())),

        #######################
        # IEC61970 Base Wires #
        #######################

        draw(builds(NetworkIdentifiedObject, acLineSegment=ac_line_segment())),
        draw(builds(NetworkIdentifiedObject, breaker=breaker())),
        draw(builds(NetworkIdentifiedObject, busbarSection=busbar_section())),
        draw(builds(NetworkIdentifiedObject, clamp=clamp())),
        draw(builds(NetworkIdentifiedObject, cut=cut())),
        draw(builds(NetworkIdentifiedObject, disconnector=disconnector())),
        draw(builds(NetworkIdentifiedObject, energyConsumer=energy_consumer())),
        draw(builds(NetworkIdentifiedObject, energyConsumerPhase=energy_consumer_phase())),
        draw(builds(NetworkIdentifiedObject, energySource=energy_source())),
        draw(builds(NetworkIdentifiedObject, energySourcePhase=energy_source_phase())),
        draw(builds(NetworkIdentifiedObject, fuse=fuse())),
        draw(builds(NetworkIdentifiedObject, ground=ground())),
        draw(builds(NetworkIdentifiedObject, groundDisconnector=ground_disconnector())),
        draw(builds(NetworkIdentifiedObject, groundingImpedance=grounding_impedance())),
        draw(builds(NetworkIdentifiedObject, jumper=jumper())),
        draw(builds(NetworkIdentifiedObject, junction=junction())),
        draw(builds(NetworkIdentifiedObject, linearShuntCompensator=linear_shunt_compensator())),
        draw(builds(NetworkIdentifiedObject, loadBreakSwitch=load_break_switch())),
        draw(builds(NetworkIdentifiedObject, perLengthPhaseImpedance=per_length_phase_impedance())),
        draw(builds(NetworkIdentifiedObject, perLengthSequenceImpedance=per_length_sequence_impedance())),
        draw(builds(NetworkIdentifiedObject, powerElectronicsConnection=power_electronics_connection())),
        draw(builds(NetworkIdentifiedObject, powerElectronicsConnectionPhase=power_electronics_connection_phase())),
        draw(builds(NetworkIdentifiedObject, powerTransformer=power_transformer())),
        draw(builds(NetworkIdentifiedObject, powerTransformerEnd=power_transformer_end())),
        draw(builds(NetworkIdentifiedObject, ratioTapChanger=ratio_tap_changer())),
        draw(builds(NetworkIdentifiedObject, reactiveCapabilityCurve=reactive_capability_curve())),
        draw(builds(NetworkIdentifiedObject, recloser=recloser())),
        draw(builds(NetworkIdentifiedObject, seriesCompensator=series_compensator())),
        draw(builds(NetworkIdentifiedObject, staticVarCompensator=static_var_compensator())),
        draw(builds(NetworkIdentifiedObject, synchronousMachine=synchronous_machine())),
        draw(builds(NetworkIdentifiedObject, tapChangerControl=tap_changer_control())),
        draw(builds(NetworkIdentifiedObject, transformerStarImpedance=transformer_star_impedance())),

        ###############################
        # IEC61970 InfIEC61970 Feeder #
        ###############################

        draw(builds(NetworkIdentifiedObject, circuit=circuit())),
    ]
    return nios


##############################
# Diagram Identified Objects #
##############################


@composite
def diagram_identified_objects(draw):
    dios = [
        ################################
        # IEC61970 Base Diagram Layout #
        ################################

        draw(builds(DiagramIdentifiedObject, diagram=diagram())),
        draw(builds(DiagramIdentifiedObject, diagramObject=diagram_object()))
    ]
    return dios


###############################
# Customer Identified Objects #
###############################


@composite
def customer_identified_objects(draw):
    dios = [
        ###################
        # IEC61968 Common #
        ###################

        draw(builds(CustomerIdentifiedObject, organisation=organisation())),

        ######################
        # IEC61968 Customers #
        ######################

        draw(builds(CustomerIdentifiedObject, customer=customer())),
        draw(builds(CustomerIdentifiedObject, customerAgreement=customer_agreement())),
        draw(builds(CustomerIdentifiedObject, pricingStructure=pricing_structure())),
        draw(builds(CustomerIdentifiedObject, tariff=tariff())),
    ]
    return dios
