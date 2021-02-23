#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from random import choice

from zepben.evolve import *

from hypothesis.strategies import builds, text, integers, sampled_from, lists, floats, booleans, uuids, datetimes

# WARNING!! # THIS IS A WORK IN PROGRESS AND MANY FUNCTIONS ARE LIKELY BROKEN
from zepben.evolve.model.cim.iec61970.base.wires.generation.production.battery_state_kind import BatteryStateKind
from zepben.evolve.model.cim.iec61970.base.wires.generation.production.power_electronics_unit import BatteryUnit, PhotoVoltaicUnit, PowerElectronicsWindUnit
from zepben.evolve.model.cim.iec61970.base.wires.power_electronics_connection import PowerElectronicsConnection, PowerElectronicsConnectionPhase

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
    return {"mrid": uuids(version=4).map(lambda x: str(x)), "name": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
            "description": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE)}


# IEC61968 COMMON #
def document():
    return {**identifiedobject(), "title": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), "created_date_time": datetimes(),
            "author_name": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), "type": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE),
            "status": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), "comment": text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE)
            }


def agreement():
    return {**document()}


def organisation():
    return builds(Organisation, **identifiedobject())


def organisationrole():
    return {**identifiedobject(), "organisations": builds(Organisation, **identifiedobject())}


# IEC61968 ASSET INFO #
def cableinfo():
    return builds(CableInfo, **wireinfo())


def wirematerialkind():
    return sampled_from(WireMaterialKind)


def wireinfo():
    return {**assetinfo(), "ratedCurrent": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER), "material": wirematerialkind()}


def overheadwireinfo():
    return builds(OverheadWireInfo, **wireinfo())


def powertransformerinfo():
    return builds(PowerTransformerInfo, **assetinfo())


# IEC61968 ASSETS #
def asset():
    return {**identifiedobject(), "location": builds(Location, **identifiedobject()),
            "organisation_roles": lists(builds(AssetOwner, **identifiedobject()), max_size=2)}


def assetcontainer():
    return {**asset()}


def assetinfo():
    return {**identifiedobject()}


def assetorganisationrole():
    return {**organisationrole()}


def assetowner():
    return builds(AssetOwner, **assetorganisationrole())


def structure():
    return {**assetcontainer()}


def pole():
    return builds(Pole, **structure(), streetlights=lists(builds(Streetlight, **identifiedobject()), max_size=2), classification=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE))


def customer():
    return builds(Customer, **organisationrole(), kind=customerkind(), customer_agreements=builds(CustomerAgreement, **identifiedobject()))


def customeragreements():
    # Note - customer is not set
    return builds(CustomerAgreement, **agreement(), pricing_structures=lists(builds(PricingStructure, **identifiedobject()), max_size=2))


def customerkind():
    return sampled_from(CustomerKind)


def pricingstructure():
    return builds(PricingStructure, **document(), tariffs=lists(builds(Tariff, **identifiedobject()), max_size=2))


def tariffs():
    return builds(Tariff, **document())


def streetlightlampkind():
    return sampled_from(StreetlightLampKind)


def streetlight():
    return builds(Streetlight, **asset(), pole=builds(Pole, **identifiedobject()), light_rating=integers(min_value=0, max_value=MAX_32_BIT_INTEGER),
                  lamp_kind=streetlightlampkind())


# IEC61968 COMMON #
def location():
    return builds(Location, **identifiedobject(), main_address=builds(StreetAddress), position_points=lists(positionpoint(), max_size=4))


def positionpoint():
    return builds(PositionPoint, x_position=floats(min_value=-180.0, max_value=180.0), y_position=floats(min_value=-90.0, max_value=90.0))


def streetaddress():
    return builds(StreetAddress, postal_code=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), town_detail=builds(TownDetail))


def towndetail():
    return builds(TownDetail, name=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE), state_or_province=text(alphabet=ALPHANUM, max_size=TEXT_MAX_SIZE))


# IEC61968 METERING #
def enddevice():
    return {**assetcontainer(), "usage_points": lists(builds(UsagePoint, **identifiedobject()), max_size=2), "customer": builds(Customer, **identifiedobject()), "service_location": builds(Location, **identifiedobject())}


def meter():
    return builds(Meter, **enddevice())


def usagepoint():
    return builds(UsagePoint, **identifiedobject(), usage_point_location=builds(Location, **identifiedobject()),
                  equipment=lists(builds(EnergyConsumer, **identifiedobject()), max_size=2),
                  end_devices=lists(builds(Meter, **identifiedobject()), max_size=2))


# IEC61968 OPERATIONS #
def operationalrestriction():
    return builds(OperationalRestriction, **document(), equipment=lists(builds(PowerTransformer, **identifiedobject()), max_size=2))


# IEC61970 AUXILIARY EQUIPMENT #
def auxiliaryequipment():
    return {**equipment(), "terminal": builds(Terminal, **identifiedobject())}


def faultindicator():
    return builds(FaultIndicator, **auxiliaryequipment())


# IEC61970 CORE #
def acdcterminal():
    return {**identifiedobject()}


def basevoltage():
    return builds(BaseVoltage, **identifiedobject(), nominal_voltage=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER))


def sampled_asset_info():
    return choice([
        builds(OverheadWireInfo, **identifiedobject()),
        builds(CableInfo, **identifiedobject()),
        builds(PowerTransformerInfo, **identifiedobject()),
    ])


def conductingequipment():
    return {**equipment(), "base_voltage": builds(BaseVoltage, **identifiedobject()),
            "terminals": lists(builds(Terminal, phases=sampled_from(PhaseCode)), max_size=2)
            }


def connectivitynode():
    return builds(ConnectivityNode, **identifiedobject(), terminals=lists(builds(Terminal, **identifiedobject()), max_size=10))


def connectivitynodecontainer():
    return {**powersystemresource()}


def sampled_equipment_container():
    return choice([
        builds(Feeder, **identifiedobject()),
        builds(Site, **identifiedobject()),
        builds(Circuit, **identifiedobject()),
        builds(Loop, **identifiedobject()),
        builds(Substation, **identifiedobject())
    ])


def sampled_equipment():
    return choice([
        builds(AcLineSegment, **identifiedobject()),
        builds(PowerTransformer, **identifiedobject()),
        builds(Breaker, **identifiedobject()),
        builds(Disconnector, **identifiedobject()),
        builds(EnergyConsumer, **identifiedobject()),
        builds(EnergySource, **identifiedobject()),
        builds(FaultIndicator, **identifiedobject())
    ])


def sampled_conducting_equipment():
    return choice([
        builds(AcLineSegment, **identifiedobject()),
        builds(PowerTransformer, **identifiedobject()),
        builds(Breaker, **identifiedobject()),
        builds(Disconnector, **identifiedobject()),
        builds(EnergyConsumer, **identifiedobject()),
        builds(EnergySource, **identifiedobject()),
    ])


def equipment():
    # Note - usage_points, operational_restrictions, current_feeders, equipment_containers unset
    return {**powersystemresource(), "in_service": booleans(), "normally_in_service": booleans(),
            "equipment_containers": lists(sampled_equipment_container(), max_size=2),
            "usage_points": lists(builds(UsagePoint, **identifiedobject()), max_size=2),
            "operational_restrictions": lists(builds(OperationalRestriction, **identifiedobject()), max_size=2),
            "current_feeders": lists(builds(Feeder, **identifiedobject()), max_size=2)}


def equipmentcontainer():
    # Note - equipment is not set
    return {**connectivitynodecontainer()}


def feeder():
    return builds(Feeder, **equipmentcontainer(), normal_head_terminal=builds(Terminal, **identifiedobject()), normal_energizing_substation=builds(Substation, **identifiedobject()))


def geographicalregion():
    return builds(GeographicalRegion, **identifiedobject(), sub_geographical_regions=lists(builds(SubGeographicalRegion, **identifiedobject()), max_size=2))


def powersystemresource():
    return {**identifiedobject(), "location": location(), "asset_info": sampled_asset_info()}


def site():
    return builds(Site, **equipmentcontainer())


def subgeographicalregion():
    return builds(SubGeographicalRegion, **identifiedobject(), geographical_region=builds(GeographicalRegion, **identifiedobject()),
                  substations=lists(builds(Substation, **identifiedobject()), max_size=2))


def substation():
    return builds(Substation, **equipmentcontainer(), sub_geographical_region=builds(SubGeographicalRegion, **identifiedobject()),
                  normal_energized_feeders=lists(builds(Feeder, **identifiedobject()), max_size=2),
                  loops=lists(builds(Loop, **identifiedobject()), max_size=2),
                  normal_energized_loops=lists(builds(Loop, **identifiedobject()), max_size=2),
                  cicuits=lists(builds(Circuit, **identifiedobject()), max_size=2))


def phasecode():
    return sampled_from(PhaseCode)


def terminal():
    return builds(Terminal, **acdcterminal(), conducting_equipment=sampled_conducting_equipment(),
                  connectivity_node=builds(ConnectivityNode, **identifiedobject()),
                  traced_phases=builds(TracedPhases), phases=phasecode(), sequence_number=integers(min_value=MIN_SEQUENCE_NUMBER, max_value=MAX_SEQUENCE_NUMBER))


# IEC61970 WIRES.GENERATION.PRODUCTION #
def batterystatekind():
    return sampled_from(BatteryStateKind)


def batteryunit():
    return builds(BatteryUnit, **powerelectronicsunit(), battery_state=batterystatekind(), rated_e=floats(min_value=0.0, max_value=FLOAT_MAX),
                  stored_e=floats(min_value=0.0, max_value=FLOAT_MAX))


def photovoltaicunit():
    return builds(PhotoVoltaicUnit, **powerelectronicsunit())


def powerelectronicsunit():
    return {**equipment(), "power_electronics_connection": builds(PowerElectronicsConnection, **identifiedobject()),
            "max_p": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
            "min_p": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER)}


def powerelectronicswindunit():
    return builds(PowerElectronicsWindUnit, **powerelectronicsunit())


# IEC61970 WIRES #
def aclinesegment():
    return builds(AcLineSegment, **conductor(), per_length_sequence_impedance=builds(PerLengthSequenceImpedance, **identifiedobject()))


def breaker():
    return builds(Breaker, **protectedswitch())


def loadbreakswitch():
    return builds(LoadBreakSwitch, **protectedswitch())


def conductor():
    return {**conductingequipment(), "length": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)}


def connector():
    return {**conductingequipment()}


def disconnector():
    return builds(Disconnector, **switch())


def energyconnection():
    return {**conductingequipment()}


def phaseshuntconnectionkind():
    return sampled_from(PhaseShuntConnectionKind)


def energyconsumer():
    return builds(EnergyConsumer, **energyconnection(), energy_consumer_phases=lists(builds(EnergyConsumerPhase, **identifiedobject()), max_size=2),
                  customer_count=integers(min_value=0, max_value=MAX_32_BIT_INTEGER), grounded=booleans(),
                  p=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX), p_fixed=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
                  phase_connection=phaseshuntconnectionkind(), q=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
                  q_fixed=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX))


def singlephasekind():
    return sampled_from(SinglePhaseKind)


def energyconsumerphase():
    return builds(EnergyConsumerPhase, **powersystemresource(), energy_consumer=builds(EnergyConsumer, **identifiedobject()),
                  phase=singlephasekind(),
                  p=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX), p_fixed=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
                  q=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX), q_fixed=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX))


def energysource():
    return builds(EnergySource, **energyconnection(), energy_source_phases=lists(builds(EnergySourcePhase, **identifiedobject()), max_size=2),
                  active_power=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX), reactive_power=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
                  voltage_angle=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX), voltage_magnitude=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
                  r=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX), x=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
                  p_max=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX), p_min=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
                  r0=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX), rn=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
                  x0=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX), xn=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX))


def energysourcephase():
    return builds(EnergySourcePhase, **powersystemresource(), energy_source=builds(EnergySource, **identifiedobject()), phase=singlephasekind())


def fuse():
    return builds(Fuse, **switch())


def jumper():
    return builds(Jumper, **switch())


def junction():
    return builds(Junction, **connector())


def busbarsection():
    return builds(BusbarSection, **connector())


def line():
    return {**equipmentcontainer()}


def linearshuntcompensator():
    return builds(LinearShuntCompensator, **shuntcompensator(), b0_per_section=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
                  b_per_section=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX), g0_per_section=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
                  g_per_section=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX))


def perlengthlineparameter():
    return {**identifiedobject()}


def perlengthimpedance():
    return {**perlengthlineparameter()}


def perlengthsequenceimpedance():
    return builds(PerLengthSequenceImpedance, **perlengthimpedance(), r=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
                  x=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX), r0=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
                  x0=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX), bch=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
                  gch=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX), b0ch=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
                  g0ch=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX))


def vectorgroup():
    return sampled_from(VectorGroup)


def powerelectronicsconnection():
    return builds(PowerElectronicsConnection, **powersystemresource(), power_electronics_units=lists(builds(BatteryUnit, **identifiedobject()), max_size=2),
                  power_electronics_connection_phases=lists(builds(PowerElectronicsConnectionPhase, **identifiedobject()), max_size=2),
                  max_i_fault=integers(min_value=0, max_value=MAX_32_BIT_INTEGER), max_q=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
                  min_q=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX), p=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
                  q=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX), rated_s=integers(min_value=0, max_value=MAX_32_BIT_INTEGER),
                  rated_u=integers(min_value=0, max_value=MAX_32_BIT_INTEGER))


def powerelectronicsconnectionphase():
    return builds(PowerElectronicsConnectionPhase, **powersystemresource(), power_electronics_connection=builds(PowerElectronicsConnection, **identifiedobject()),
                  phase=singlephasekind(), p=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX), q=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX))



def powertransformer():
    return builds(PowerTransformer, **conductingequipment(), power_transformer_ends=lists(builds(PowerTransformerEnd, **identifiedobject()), max_size=2),
                  vectorGroup=vectorgroup(), transformer_utilisation=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX))


def windingconnectionkind():
    return sampled_from(WindingConnection)


def powertransformerend():
    # Note - powerTransformer not set
    return builds(PowerTransformerEnd, **transformerend(), rated_s=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
                  rated_u=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER), r=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
                  r0=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX), x=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
                  x0=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX), connection_kind=windingconnectionkind(),
                  b=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX), b0=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
                  g=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX), g0=floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX),
                  phase_angle_clock=integers(min_value=0, max_value=11))


def protectedswitch():
    return {**switch()}


def ratiotapchanger():
    return builds(RatioTapChanger, **tapchanger(), transformer_end=builds(PowerTransformerEnd, **identifiedobject()),
                  step_voltage_increment=floats(min_value=0.0, max_value=1.0))


def recloser():
    return builds(Recloser, **protectedswitch())


def regulatingcondeq():
    return {**energyconnection(), "control_enabled": booleans()}


def shuntcompensator():
    return {**regulatingcondeq(), "sections": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX), "grounded": booleans(),
            "nom_u": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER), "phase_connection": phaseshuntconnectionkind()}


def switch():
    return {**conductingequipment(), "_normal_open": booleans(), "_open": booleans()}


MIN_TC_INT = 0
MAX_TC_INT = 3


def tapchanger():
    return {**powersystemresource(), "high_step": integers(min_value=10, max_value=15),
            "low_step": integers(min_value=0, max_value=2), "step": floats(min_value=1.0, max_value=10.0),
            "neutral_step": integers(min_value=2, max_value=10), "neutral_u": integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
            "normal_step": integers(min_value=2, max_value=10), "control_enabled": booleans()}


def transformerend():
    return {**identifiedobject(), "terminal": builds(Terminal, **identifiedobject()),
            "base_voltage": builds(BaseVoltage, **identifiedobject()), "ratio_tap_changer": builds(RatioTapChanger, **identifiedobject()),
            "end_number": integers(min_value=MIN_SEQUENCE_NUMBER, max_value=MAX_END_NUMBER), "grounded": booleans(),
            "r_ground": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX), "x_ground": floats(min_value=FLOAT_MIN, max_value=FLOAT_MAX)}


def circuit():
    return builds(Circuit, **line(), loop=builds(Loop, **identifiedobject()),
                  end_terminals=lists(builds(Terminal, **identifiedobject()), max_size=2),
                  end_substations=lists(builds(Substation, **identifiedobject()), max_size=2))


def loop():
    return builds(Loop, **identifiedobject(), circuits=lists(builds(Circuit, **identifiedobject()), max_size=2),
                  substations=lists(builds(Substation, **identifiedobject()), max_size=2),
                  normal_energizing_substations=lists(builds(Substation, **identifiedobject()), max_size=2))


# IEC61970 MEAS #
def iopoint():
    return {**identifiedobject()}


def control():
    return builds(Control, **iopoint(), power_system_resource=sampled_equipment(),
                  remote_control=builds(RemoteControl, **identifiedobject()))


def accumulator():
    return builds(Accumulator, **measurement())


def analog():
    return builds(Analog, **measurement(), positive_flow_in=booleans())


def discrete():
    return builds(Discrete, **measurement())


def unitsymbol():
    return sampled_from(UnitSymbol)


def measurement():
    return {**identifiedobject(), "remote_source": builds(RemoteSource, **identifiedobject()), "power_system_resource": sampled_equipment(),
            "terminal": builds(Terminal, **identifiedobject()), "phases": phasecode(), "unitSymbol": unitsymbol()}


# IEC61970 SCADA #
def remotecontrol():
    return builds(RemoteControl, **remotepoint(), control=builds(Control, **identifiedobject()))


def remotepoint():
    return {**identifiedobject()}


def remotesource():
    return builds(RemoteSource, **remotepoint(), measurement=sampled_measurement())


# MODEL #
def tracedphases():
    return builds(TracedPhases, normal_status=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER),
                  current_status=integers(min_value=MIN_32_BIT_INTEGER, max_value=MAX_32_BIT_INTEGER))


def sampled_measurement():
    return choice([
        builds(Accumulator()),
        builds(Analog()),
        builds(Discrete()),
    ])
