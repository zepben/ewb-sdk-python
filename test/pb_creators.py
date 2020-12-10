#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from google.protobuf.timestamp_pb2 import Timestamp
from zepben.protobuf.cim.iec61970.base.core.IdentifiedObject_pb2 import IdentifiedObject as PBIdentifiedObject
from zepben.protobuf.cim.iec61968.common.Document_pb2 import Document as PBDocument
from zepben.protobuf.cim.iec61968.common.Organisation_pb2 import Organisation as PBOrganisation
from zepben.protobuf.cim.iec61968.common.OrganisationRole_pb2 import OrganisationRole as PBOrganisationRole
from zepben.protobuf.cim.iec61968.assetinfo.CableInfo_pb2 import CableInfo as PBCableInfo
from zepben.protobuf.cim.iec61968.assetinfo.OverheadWireInfo_pb2 import OverheadWireInfo as PBOverheadWireInfo
from zepben.protobuf.cim.iec61968.assetinfo.WireInfo_pb2 import WireInfo as PBWireInfo
from zepben.protobuf.cim.iec61968.assetinfo.WireMaterialKind_pb2 import WireMaterialKind as PBWireMaterialKind
from zepben.protobuf.cim.iec61968.assets.AssetContainer_pb2 import AssetContainer as PBAssetContainer
from zepben.protobuf.cim.iec61968.assets.AssetInfo_pb2 import AssetInfo as PBAssetInfo
from zepben.protobuf.cim.iec61968.assets.AssetOrganisationRole_pb2 import AssetOrganisationRole as PBAssetOrganisationRole
from zepben.protobuf.cim.iec61968.assets.AssetOwner_pb2 import AssetOwner as PBAssetOwner
from zepben.protobuf.cim.iec61968.assets.Asset_pb2 import Asset as PBAsset
from zepben.protobuf.cim.iec61968.assets.Pole_pb2 import Pole as  PBPole
from zepben.protobuf.cim.iec61968.assets.StreetlightLampKind_pb2 import StreetlightLampKind as PBStreetlightLampKind
from zepben.protobuf.cim.iec61968.assets.Streetlight_pb2 import Streetlight as PBStreetlight
from zepben.protobuf.cim.iec61968.assets.Structure_pb2 import Structure as PBStructure
from zepben.protobuf.cim.iec61968.common.Location_pb2 import Location as PBLocation
from zepben.protobuf.cim.iec61968.common.PositionPoint_pb2 import PositionPoint as PBPositionPoint
from zepben.protobuf.cim.iec61968.common.StreetAddress_pb2 import StreetAddress as PBStreetAddress
from zepben.protobuf.cim.iec61968.common.TownDetail_pb2 import TownDetail as PBTownDetail
from zepben.protobuf.cim.iec61968.metering.EndDevice_pb2 import EndDevice as PBEndDevice
from zepben.protobuf.cim.iec61968.metering.Meter_pb2 import Meter as PBMeter
from zepben.protobuf.cim.iec61968.metering.UsagePoint_pb2 import UsagePoint as PBUsagePoint
from zepben.protobuf.cim.iec61968.operations.OperationalRestriction_pb2 import OperationalRestriction as PBOperationalRestriction
from zepben.protobuf.cim.iec61970.base.auxiliaryequipment.AuxiliaryEquipment_pb2 import AuxiliaryEquipment as PBAuxiliaryEquipment
from zepben.protobuf.cim.iec61970.base.auxiliaryequipment.FaultIndicator_pb2 import FaultIndicator as PBFaultIndicator
from zepben.protobuf.cim.iec61970.base.core.AcDcTerminal_pb2 import AcDcTerminal as PBAcDcTerminal
from zepben.protobuf.cim.iec61970.base.core.BaseVoltage_pb2 import BaseVoltage as PBBaseVoltage
from zepben.protobuf.cim.iec61970.base.core.ConductingEquipment_pb2 import ConductingEquipment as PBConductingEquipment
from zepben.protobuf.cim.iec61970.base.core.ConnectivityNodeContainer_pb2 import ConnectivityNodeContainer as PBConnectivityNodeContainer
from zepben.protobuf.cim.iec61970.base.core.ConnectivityNode_pb2 import ConnectivityNode as PBConnectivityNode
from zepben.protobuf.cim.iec61970.base.core.EquipmentContainer_pb2 import EquipmentContainer as PBEquipmentContainer
from zepben.protobuf.cim.iec61970.base.core.Equipment_pb2 import Equipment as PBEquipment
from zepben.protobuf.cim.iec61970.base.core.Feeder_pb2 import Feeder as PBFeeder
from zepben.protobuf.cim.iec61970.base.core.GeographicalRegion_pb2 import GeographicalRegion as PBGeographicalRegion
from zepben.protobuf.cim.iec61970.base.core.PhaseCode_pb2 import PhaseCode as PBPhaseCode
from zepben.protobuf.cim.iec61970.base.core.PowerSystemResource_pb2 import PowerSystemResource as PBPowerSystemResource
from zepben.protobuf.cim.iec61970.base.core.Site_pb2 import Site as PBSite
from zepben.protobuf.cim.iec61970.base.core.SubGeographicalRegion_pb2 import SubGeographicalRegion as PBSubGeographicalRegion
from zepben.protobuf.cim.iec61970.base.core.Substation_pb2 import Substation as PBSubstation
from zepben.protobuf.cim.iec61970.base.core.Terminal_pb2 import Terminal as PBTerminal
from zepben.protobuf.cim.iec61970.base.domain.UnitSymbol_pb2 import UnitSymbol as PBUnitSymbol
from zepben.protobuf.cim.iec61970.base.meas.Accumulator_pb2 import Accumulator as PBAccumulator
from zepben.protobuf.cim.iec61970.base.meas.Analog_pb2 import Analog as PBAnalog
from zepben.protobuf.cim.iec61970.base.meas.Control_pb2 import Control as PBControl
from zepben.protobuf.cim.iec61970.base.meas.Discrete_pb2 import Discrete as PBDiscrete
from zepben.protobuf.cim.iec61970.base.meas.IoPoint_pb2 import IoPoint as PBIoPoint
from zepben.protobuf.cim.iec61970.base.meas.Measurement_pb2 import Measurement as PBMeasurement
from zepben.protobuf.cim.iec61970.base.scada.RemoteControl_pb2 import RemoteControl as PBRemoteControl
from zepben.protobuf.cim.iec61970.base.scada.RemoteSource_pb2 import RemoteSource as PBRemoteSource
from zepben.protobuf.cim.iec61970.base.scada.RemotePoint_pb2 import RemotePoint as PBRemotePoint
from zepben.protobuf.cim.iec61970.base.wires.AcLineSegment_pb2 import AcLineSegment as PBAcLineSegment
from zepben.protobuf.cim.iec61970.base.wires.Breaker_pb2 import Breaker as PBBreaker
from zepben.protobuf.cim.iec61970.base.wires.Conductor_pb2 import Conductor as PBConductor
from zepben.protobuf.cim.iec61970.base.wires.Connector_pb2 import Connector as PBConnector
from zepben.protobuf.cim.iec61970.base.wires.Disconnector_pb2 import Disconnector as PBDisconnector
from zepben.protobuf.cim.iec61970.base.wires.EnergyConnection_pb2 import EnergyConnection as PBEnergyConnection
from zepben.protobuf.cim.iec61970.base.wires.EnergyConsumerPhase_pb2 import EnergyConsumerPhase as PBEnergyConsumerPhase
from zepben.protobuf.cim.iec61970.base.wires.EnergyConsumer_pb2 import EnergyConsumer as PBEnergyConsumer
from zepben.protobuf.cim.iec61970.base.wires.EnergySourcePhase_pb2 import EnergySourcePhase as PBEnergySourcePhase
from zepben.protobuf.cim.iec61970.base.wires.EnergySource_pb2 import EnergySource as PBEnergySource
from zepben.protobuf.cim.iec61970.base.wires.Fuse_pb2 import Fuse as PBFuse
from zepben.protobuf.cim.iec61970.base.wires.Jumper_pb2 import Jumper as PBJumper
from zepben.protobuf.cim.iec61970.base.wires.Junction_pb2 import Junction as PBJunction
from zepben.protobuf.cim.iec61970.base.wires.Line_pb2 import Line as PBLine
from zepben.protobuf.cim.iec61970.base.wires.LinearShuntCompensator_pb2 import LinearShuntCompensator as PBLinearShuntCompensator
from zepben.protobuf.cim.iec61970.base.wires.PerLengthImpedance_pb2 import PerLengthImpedance as PBPerLengthImpedance
from zepben.protobuf.cim.iec61970.base.wires.PerLengthLineParameter_pb2 import PerLengthLineParameter as PBPerLengthLineParameter
from zepben.protobuf.cim.iec61970.base.wires.PerLengthSequenceImpedance_pb2 import PerLengthSequenceImpedance as PBPerLengthSequenceImpedance
from zepben.protobuf.cim.iec61970.base.wires.PhaseShuntConnectionKind_pb2 import PhaseShuntConnectionKind as PBPhaseShuntConnectionKind
from zepben.protobuf.cim.iec61970.base.wires.PowerTransformerEnd_pb2 import PowerTransformerEnd as PBPowerTransformerEnd
from zepben.protobuf.cim.iec61970.base.wires.PowerTransformer_pb2 import PowerTransformer as PBPowerTransformer
from zepben.protobuf.cim.iec61970.base.wires.ProtectedSwitch_pb2 import ProtectedSwitch as PBProtectedSwitch
from zepben.protobuf.cim.iec61970.base.wires.RatioTapChanger_pb2 import RatioTapChanger as PBRatioTapChanger
from zepben.protobuf.cim.iec61970.base.wires.Recloser_pb2 import Recloser as PBRecloser
from zepben.protobuf.cim.iec61970.base.wires.RegulatingCondEq_pb2 import RegulatingCondEq as PBRegulatingCondEq
from zepben.protobuf.cim.iec61970.base.wires.ShuntCompensator_pb2 import ShuntCompensator as PBShuntCompensator
from zepben.protobuf.cim.iec61970.base.wires.SinglePhaseKind_pb2 import SinglePhaseKind as PBSinglePhaseKind
from zepben.protobuf.cim.iec61970.base.wires.Switch_pb2 import Switch as PBSwitch
from zepben.protobuf.cim.iec61970.base.wires.TapChanger_pb2 import TapChanger as PBTapChanger
from zepben.protobuf.cim.iec61970.base.wires.TransformerEnd_pb2 import TransformerEnd as PBTransformerEnd
from zepben.protobuf.cim.iec61970.base.wires.VectorGroup_pb2 import VectorGroup as PBVectorGroup
from zepben.protobuf.cim.iec61970.base.wires.WindingConnection_pb2 import WindingConnection as PBWindingConnection
from zepben.protobuf.cim.iec61970.infiec61970.feeder.Loop_pb2 import Loop as PBLoop
from zepben.protobuf.cim.iec61970.infiec61970.feeder.Circuit_pb2 import Circuit as PBCircuit
from zepben.protobuf.network.model.TracedPhases_pb2 import TracedPhases as PBTracedPhases

from hypothesis.strategies import builds, text, integers, sampled_from, lists, floats, booleans, composite, uuids
from zepben.protobuf.nc.nc_data_pb2 import NetworkIdentifiedObject

MIN_32_BIT_INTEGER = -2147483648
MAX_32_BIT_INTEGER = 2147483647
MAX_64_BIT_INTEGER = 9223372036854775807
TEXT_MAX_SIZE = 6
FLOAT_MIN = -100.0
FLOAT_MAX = 1000.0
MAX_END_NUMBER = 3
MAX_SEQUENCE_NUMBER = 40
MIN_SEQUENCE_NUMBER = 1
ALPHANUM = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"


def identifiedobject():
    return builds(PBIdentifiedObject, mRID=uuids(version=4).map(lambda x: str(x)), name=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
                  description=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE))


def timestamp():
    return builds(Timestamp, seconds=integers(min_value=0, max_value=MAX_32_BIT_INTEGER), nanos=integers(min_value=0, max_value=MAX_32_BIT_INTEGER))


# IEC61968 COMMON #
def document():
    return builds(PBDocument, io=identifiedobject(), title=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), createdDateTime=timestamp(),
                  authorName=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
                  type=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), status=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
                  comment=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE))


def organisation():
    return builds(PBOrganisation, io=identifiedobject())


def organisationrole():
    return builds(PBOrganisationRole, io=identifiedobject(), organisationMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE))


# IEC61968 ASSET INFO #
def cableinfo():
    return builds(PBCableInfo, wi=wireinfo())


def wirematerialkind():
    return sampled_from(PBWireMaterialKind.values())


def wireinfo():
    return builds(PBWireInfo, ai=assetinfo(), ratedCurrent=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER), material=wirematerialkind())


def overheadwireinfo():
    return builds(PBOverheadWireInfo, wi=wireinfo())


# IEC61968 ASSETS #
def asset():
    return builds(PBAsset, io=identifiedobject(), locationMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
                  organisationRoleMRIDs=lists(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), max_size=2))


def assetcontainer():
    return builds(PBAssetContainer, at=asset())


def assetinfo():
    return builds(PBAssetInfo, io=identifiedobject())


def assetorganisationrole():
    d = {"or": organisationrole()}  # To set field or that's a reserved word
    return builds(PBAssetOrganisationRole, **d)


def assetowner():
    return builds(PBAssetOwner, aor=assetorganisationrole())


def structure():
    return builds(PBStructure, ac=assetcontainer())


def pole():
    return builds(PBPole, st=structure(), streetlightMRIDs=lists(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), max_size=2),
                  classification=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE))


def streetlightlampkind():
    return sampled_from(PBStreetlightLampKind.values())


def streetlight():
    return builds(PBStreetlight, at=asset(), poleMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
                  lightRating=integers(min_value=0, max_value=MAX_32_BIT_INTEGER),
                  lampKind=streetlightlampkind())


# IEC61968 COMMON #
def location():
    return builds(PBLocation, io=identifiedobject(), mainAddress=streetaddress(), positionPoints=lists(positionpoint(), max_size=2))


def positionpoint():
    return builds(PBPositionPoint, xPosition=floats(min_value=-180.0, max_value=180.0), yPosition=floats(min_value=-90.0, max_value=90.0))


def streetaddress():
    return builds(PBStreetAddress, postalCode=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), townDetail=towndetail())


def towndetail():
    return builds(PBTownDetail, name=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), stateOrProvince=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE))


# IEC61968 METERING #
def enddevice():
    return builds(PBEndDevice, ac=assetcontainer(), usagePointMRIDs=lists(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), max_size=2),
                  customerMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
                  serviceLocationMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE))


def meter():
    return builds(PBMeter, ed=enddevice())


def usagepoint():
    return builds(PBUsagePoint, io=identifiedobject(), usagePointLocationMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
                  equipmentMRIDs=lists(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), max_size=2),
                  endDeviceMRIDs=lists(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), max_size=2))


# IEC61968 OPERATIONS #
def operationalrestriction():
    return builds(PBOperationalRestriction, doc=document(), equipmentMRIDs=lists(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), max_size=2))


# IEC61970 AUXILIARY EQUIPMENT #
def auxiliaryequipment():
    return builds(PBAuxiliaryEquipment, eq=equipment(), terminalMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE))


def faultindicator():
    return builds(PBFaultIndicator, ae=auxiliaryequipment())


# IEC61970 CORE #
def acdcterminal():
    return builds(PBAcDcTerminal, io=identifiedobject())


def basevoltage():
    return builds(PBBaseVoltage, io=identifiedobject(), nominalVoltage=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER))


def conductingequipment():
    return builds(PBConductingEquipment, eq=equipment(), baseVoltageMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
                  terminalMRIDs=lists(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), max_size=2))


def connectivitynode():
    return builds(PBConnectivityNode, io=identifiedobject(), terminalMRIDs=lists(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), max_size=5))


def connectivitynodecontainer():
    return builds(PBConnectivityNodeContainer, psr=powersystemresource())


def equipment():
    return builds(PBEquipment, psr=powersystemresource(), inService=booleans(), normallyInService=booleans(),
                  equipmentContainerMRIDs=lists(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), max_size=2),
                  usagePointMRIDs=lists(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), max_size=2),
                  operationalRestrictionMRIDs=lists(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), max_size=2),
                  currentFeederMRIDs=lists(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), max_size=2))


def equipmentcontainer():
    return builds(PBEquipmentContainer, cnc=connectivitynodecontainer(), equipmentMRIDs=lists(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), max_size=10))


def feeder():
    return builds(PBFeeder, ec=equipmentcontainer(), normalHeadTerminalMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
                  normalEnergizingSubstationMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
                  currentEquipmentMRIDs=lists(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), max_size=2))


def geographicalregion():
    return builds(PBGeographicalRegion, io=identifiedobject(), subGeographicalRegionMRIDs=lists(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), max_size=2))


def powersystemresource():
    return builds(PBPowerSystemResource, io=identifiedobject(), assetInfoMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
                  locationMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE))


def site():
    return builds(PBSite, ec=equipmentcontainer())


def subgeographicalregion():
    return builds(PBSubGeographicalRegion, io=identifiedobject(), geographicalRegionMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
                  substationMRIDs=lists(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), max_size=2))


def substation():
    return builds(PBSubstation, ec=equipmentcontainer(), subGeographicalRegionMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
                  normalEnergizedFeederMRIDs=lists(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), max_size=2),
                  loopMRIDs=lists(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), max_size=2),
                  normalEnergizedLoopMRIDs=lists(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), max_size=2),
                  circuitMRIDs=lists(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), max_size=2))


def phasecode():
    return sampled_from(PBPhaseCode.values())


def terminal():
    return builds(PBTerminal, ad=acdcterminal(), conductingEquipmentMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
                  connectivityNodeMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
                  tracedPhases=tracedphases(), phases=phasecode(), sequenceNumber=integers(min_value=MIN_SEQUENCE_NUMBER, max_value=MAX_SEQUENCE_NUMBER))


# IEC61970 WIRES #
def aclinesegment():
    return builds(PBAcLineSegment, cd=conductor(), perLengthSequenceImpedanceMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE))


def breaker():
    return builds(PBBreaker, sw=protectedswitch())


def conductor():
    return builds(PBConductor, ce=conductingequipment(), length=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX))


def connector():
    return builds(PBConnector, ce=conductingequipment())


def disconnector():
    return builds(PBDisconnector, sw=switch())


def energyconnection():
    return builds(PBEnergyConnection, ce=conductingequipment())


def phaseshuntconnectionkind():
    return sampled_from(PBPhaseShuntConnectionKind.Enum.values())


def energyconsumer():
    return builds(PBEnergyConsumer, ec=energyconnection(), energyConsumerPhasesMRIDs=lists(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), max_size=2),
                  customerCount=integers(min_value=0, max_value=MAX_32_BIT_INTEGER), grounded=booleans(), p=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
                  pFixed=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX), phaseConnection=phaseshuntconnectionkind(),
                  q=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX), qFixed=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX))


def singlephasekind():
    return sampled_from(PBSinglePhaseKind.values())


def energyconsumerphase():
    return builds(PBEnergyConsumerPhase, psr=powersystemresource(), energyConsumerMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), phase=singlephasekind(),
                  p=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX), pFixed=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
                  q=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
                  qFixed=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX))


def energysource():
    return builds(PBEnergySource, ec=energyconnection(), energySourcePhasesMRIDs=lists(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), max_size=2),
                  activePower=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX), reactivePower=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
                  voltageAngle=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX), voltageMagnitude=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
                  r=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX), x=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
                  pMax=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX), pMin=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
                  r0=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX), rn=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
                  x0=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
                  xn=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX))


def energysourcephase():
    return builds(PBEnergySourcePhase, psr=powersystemresource(), energySourceMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), phase=singlephasekind())


def fuse():
    return builds(PBFuse, sw=switch())


def jumper():
    return builds(PBJumper, sw=switch())


def junction():
    return builds(PBJunction, cn=connector())


def line():
    return builds(PBLine, ec=equipmentcontainer())


def linearshuntcompensator():
    return builds(PBLinearShuntCompensator, sc=shuntcompensator(), b0PerSection=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
                  bPerSection=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX), g0PerSection=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
                  gPerSection=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX))


def perlengthlineparameter():
    return builds(PBPerLengthLineParameter, io=identifiedobject())


def perlengthimpedance():
    return builds(PBPerLengthImpedance, lp=perlengthlineparameter())


def perlengthsequenceimpedance():
    return builds(PBPerLengthSequenceImpedance, pli=perlengthimpedance(), r=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
                  x=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX), r0=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
                  x0=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX), bch=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
                  gch=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX), b0ch=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
                  g0ch=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX))


def vectorgroup():
    return sampled_from(PBVectorGroup.values())


def powertransformer():
    return builds(PBPowerTransformer, ce=conductingequipment(), powerTransformerEndMRIDs=lists(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), max_size=2),
                  vectorGroup=vectorgroup())


def windingconnectionkind():
    return sampled_from(PBWindingConnection.values())


def powertransformerend():
    return builds(PBPowerTransformerEnd, te=transformerend(), powerTransformerMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
                  ratedS=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
                  ratedU=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER), r=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
                  r0=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX), x=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
                  x0=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
                  connectionKind=windingconnectionkind(), b=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
                  b0=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX), g=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
                  g0=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX), phaseAngleClock=integers(min_value=0, max_value=11))


def protectedswitch():
    return builds(PBProtectedSwitch, sw=switch())


def ratiotapchanger():
    return builds(PBRatioTapChanger, tc=tapchanger(), transformerEndMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
                  stepVoltageIncrement=floats(min_value=0.0, max_value=1.0))


def recloser():
    return builds(PBRecloser, sw=protectedswitch())


def regulatingcondeq():
    return builds(PBRegulatingCondEq, ec=energyconnection(), controlEnabled=booleans())


def shuntcompensator():
    return builds(PBShuntCompensator, rce=regulatingcondeq(), sections=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX), grounded=booleans(),
                  nomU=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER), phaseConnection=phaseshuntconnectionkind())


def switch():
    return builds(PBSwitch, ce=conductingequipment(), normalOpen=booleans(), open=booleans())


MIN_TC_INT = 0
MAX_TC_INT = 3


def tapchanger():
    return builds(PBTapChanger, psr=powersystemresource(), highStep=integers(min_value=10, max_value=15),
                  lowStep=integers(min_value=0, max_value=2), step=floats(min_value=1.0, max_value=10.0),
                  neutralStep=integers(min_value=2, max_value=10), neutralU=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
                  normalStep=integers(min_value=2, max_value=10), controlEnabled=booleans())


def transformerend():
    return builds(PBTransformerEnd, io=identifiedobject(), terminalMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
                  baseVoltageMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
                  ratioTapChangerMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
                  endNumber=integers(min_value=MIN_SEQUENCE_NUMBER, max_value=MAX_END_NUMBER),
                  grounded=booleans(), rGround=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX), xGround=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX))


def circuit():
    return builds(PBCircuit, l=line(), loopMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
                  endTerminalMRIDs=lists(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), max_size=2),
                  endSubstationMRIDs=lists(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), max_size=2))


def loop():
    return builds(PBLoop, io=identifiedobject(), circuitMRIDs=lists(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), max_size=2),
                  substationMRIDs=lists(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), max_size=2),
                  normalEnergizingSubstationMRIDs=lists(text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), max_size=2))


# IEC61970 MEAS #
def iopoint():
    return builds(PBIoPoint, io=identifiedobject())


def control():
    return builds(PBControl, ip=iopoint(), powerSystemResourceMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
                  remoteControlMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE))


def accumulator():
    return builds(PBAccumulator, measurement=measurement())


def analog():
    return builds(PBAnalog, measurement=measurement(), positiveFlowIn=booleans())


def discrete():
    return builds(PBDiscrete, measurement=measurement())


def unitsymbol():
    return sampled_from(PBUnitSymbol.values())


def measurement():
    return builds(PBMeasurement, io=identifiedobject(), remoteSourceMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
                  powerSystemResourceMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
                  terminalMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), phases=phasecode(),
                  unitSymbol=unitsymbol())


# IEC61970 SCADA #
def remotecontrol():
    return builds(PBRemoteControl, rp=remotepoint(), controlMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE))


def remotepoint():
    return builds(PBRemotePoint, io=identifiedobject())


def remotesource():
    return builds(PBRemoteSource, rp=remotepoint(), measurementMRID=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE))


# MODEL #
def tracedphases():
    return builds(PBTracedPhases, normalStatus=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
                  currentStatus=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER))


# NetworkIdentifiedObjects #

@composite
def networkidentifiedobjects(draw):
    nios = [
        draw(builds(NetworkIdentifiedObject, cableInfo=cableinfo())),
        draw(builds(NetworkIdentifiedObject, overheadWireInfo=overheadwireinfo())),
        draw(builds(NetworkIdentifiedObject, assetOwner=assetowner())),
        draw(builds(NetworkIdentifiedObject, organisation=organisation())),
        draw(builds(NetworkIdentifiedObject, location=location())),
        draw(builds(NetworkIdentifiedObject, meter=meter())),
        draw(builds(NetworkIdentifiedObject, usagePoint=usagepoint())),
        draw(builds(NetworkIdentifiedObject, operationalRestriction=operationalrestriction())),
        draw(builds(NetworkIdentifiedObject, faultIndicator=faultindicator())),
        draw(builds(NetworkIdentifiedObject, baseVoltage=basevoltage())),
        draw(builds(NetworkIdentifiedObject, connectivityNode=connectivitynode())),
        draw(builds(NetworkIdentifiedObject, feeder=feeder())),
        draw(builds(NetworkIdentifiedObject, geographicalRegion=geographicalregion())),
        draw(builds(NetworkIdentifiedObject, site=site())),
        draw(builds(NetworkIdentifiedObject, subGeographicalRegion=subgeographicalregion())),
        draw(builds(NetworkIdentifiedObject, substation=substation())),
        draw(builds(NetworkIdentifiedObject, terminal=terminal())),
        draw(builds(NetworkIdentifiedObject, acLineSegment=aclinesegment())),
        draw(builds(NetworkIdentifiedObject, breaker=breaker())),
        draw(builds(NetworkIdentifiedObject, disconnector=disconnector())),
        draw(builds(NetworkIdentifiedObject, energyConsumer=energyconsumer())),
        draw(builds(NetworkIdentifiedObject, energyConsumerPhase=energyconsumerphase())),
        draw(builds(NetworkIdentifiedObject, energySource=energysource())),
        draw(builds(NetworkIdentifiedObject, energySourcePhase=energysourcephase())),
        draw(builds(NetworkIdentifiedObject, fuse=fuse())),
        draw(builds(NetworkIdentifiedObject, jumper=jumper())),
        draw(builds(NetworkIdentifiedObject, junction=junction())),
        draw(builds(NetworkIdentifiedObject, linearShuntCompensator=linearshuntcompensator())),
        draw(builds(NetworkIdentifiedObject, perLengthSequenceImpedance=perlengthsequenceimpedance())),
        draw(builds(NetworkIdentifiedObject, powerTransformer=powertransformer())),
        draw(builds(NetworkIdentifiedObject, powerTransformerEnd=powertransformerend())),
        draw(builds(NetworkIdentifiedObject, ratioTapChanger=ratiotapchanger())),
        draw(builds(NetworkIdentifiedObject, recloser=recloser())),
        draw(builds(NetworkIdentifiedObject, circuit=circuit())),
        draw(builds(NetworkIdentifiedObject, loop=loop())),
        draw(builds(NetworkIdentifiedObject, pole=pole())),
        draw(builds(NetworkIdentifiedObject, streetlight=streetlight())),
        draw(builds(NetworkIdentifiedObject, accumulator=accumulator())),
        draw(builds(NetworkIdentifiedObject, analog=analog())),
        draw(builds(NetworkIdentifiedObject, discrete=discrete())),
        draw(builds(NetworkIdentifiedObject, control=control())),
        draw(builds(NetworkIdentifiedObject, remoteControl=remotecontrol())),
        draw(builds(NetworkIdentifiedObject, remoteSource=remotesource())),
    ]
    return nios
