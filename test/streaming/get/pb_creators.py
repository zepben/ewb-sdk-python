#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ['network_identified_objects', 'customer_identified_objects', 'diagram_identified_objects']

from zepben.protobuf.cc.cc_data_pb2 import CustomerIdentifiable
from zepben.protobuf.dc.dc_data_pb2 import DiagramIdentifiable
from zepben.protobuf.nc.nc_data_pb2 import NetworkIdentifiable
from hypothesis.strategies import composite
from zepben.protobuf.cc.cc_data_pb2 import CustomerIdentifiedObject
from zepben.protobuf.dc.dc_data_pb2 import DiagramIdentifiedObject
from zepben.protobuf.nc.nc_data_pb2 import NetworkIdentifiedObject

from cim.fill_fields import *


##############################
# Network Identified Objects #
##############################

@composite
def network_identified_objects(draw):
    nios = [
        ##################################
        # Extensions IEC61968 Asset Info #
        ##################################

        draw(create_relay_info().map(lambda it: NetworkIdentifiable(relayInfo=it.to_pb()))),
        draw(create_relay_info().map(lambda it: NetworkIdentifiable(relayInfo=it.to_pb()))),

        ################################
        # Extensions IEC61968 Metering #
        ################################

        draw(create_pan_demand_response_function().map(lambda it: NetworkIdentifiable(panDemandResponseFunction=it.to_pb()))),

        #################################
        # Extensions IEC61970 Base Core #
        #################################

        draw(create_site().map(lambda it: NetworkIdentifiable(site=it.to_pb()))),

        ###################################
        # Extensions IEC61970 Base Feeder #
        ###################################

        draw(create_loop().map(lambda it: NetworkIdentifiable(loop=it.to_pb()))),
        draw(create_lv_feeder().map(lambda it: NetworkIdentifiable(lvFeeder=it.to_pb()))),

        ##################################################
        # Extensions IEC61970 Base Generation Production #
        ##################################################

        draw(create_ev_charging_unit().map(lambda it: NetworkIdentifiable(evChargingUnit=it.to_pb()))),

        #######################################
        # Extensions IEC61970 Base Protection #
        #######################################

        draw(create_distance_relay().map(lambda it: NetworkIdentifiable(distanceRelay=it.to_pb()))),
        draw(create_protection_relay_scheme().map(lambda it: NetworkIdentifiable(protectionRelayScheme=it.to_pb()))),
        draw(create_protection_relay_system().map(lambda it: NetworkIdentifiable(protectionRelaySystem=it.to_pb()))),
        draw(create_voltage_relay().map(lambda it: NetworkIdentifiable(voltageRelay=it.to_pb()))),

        ##################################
        # Extensions IEC61970 Base Wires #
        ##################################

        draw(create_battery_control().map(lambda it: NetworkIdentifiable(batteryControl=it.to_pb()))),

        #######################
        # IEC61968 Asset Info #
        #######################

        draw(create_cable_info().map(lambda it: NetworkIdentifiable(cableInfo=it.to_pb()))),
        draw(create_no_load_test().map(lambda it: NetworkIdentifiable(noLoadTest=it.to_pb()))),
        draw(create_open_circuit_test().map(lambda it: NetworkIdentifiable(openCircuitTest=it.to_pb()))),
        draw(create_overhead_wire_info().map(lambda it: NetworkIdentifiable(overheadWireInfo=it.to_pb()))),
        draw(create_power_transformer_info().map(lambda it: NetworkIdentifiable(powerTransformerInfo=it.to_pb()))),
        draw(create_short_circuit_test().map(lambda it: NetworkIdentifiable(shortCircuitTest=it.to_pb()))),
        draw(create_shunt_compensator_info().map(lambda it: NetworkIdentifiable(shuntCompensatorInfo=it.to_pb()))),
        draw(create_switch_info().map(lambda it: NetworkIdentifiable(switchInfo=it.to_pb()))),
        draw(create_transformer_end_info().map(lambda it: NetworkIdentifiable(transformerEndInfo=it.to_pb()))),
        draw(create_transformer_tank_info().map(lambda it: NetworkIdentifiable(transformerTankInfo=it.to_pb()))),

        ###################
        # IEC61968 Assets #
        ###################

        draw(create_asset_owner().map(lambda it: NetworkIdentifiable(assetOwner=it.to_pb()))),
        draw(create_streetlight().map(lambda it: NetworkIdentifiable(streetlight=it.to_pb()))),

        ###################
        # IEC61968 Common #
        ###################

        draw(create_location().map(lambda it: NetworkIdentifiedObject(location=it.to_pb()))),
        draw(create_organisation().map(lambda it: NetworkIdentifiedObject(organisation=it.to_pb()))),

        #####################################
        # IEC61968 InfIEC61968 InfAssetInfo #
        #####################################

        draw(create_current_transformer_info().map(lambda it: NetworkIdentifiedObject(currentTransformerInfo=it.to_pb()))),
        draw(create_potential_transformer_info().map(lambda it: NetworkIdentifiedObject(potentialTransformerInfo=it.to_pb()))),

        ##################################
        # IEC61968 InfIEC61968 InfAssets #
        ##################################

        draw(create_pole().map(lambda it: NetworkIdentifiedObject(pole=it.to_pb()))),

        #####################
        # IEC61968 Metering #
        #####################

        draw(create_meter().map(lambda it: NetworkIdentifiedObject(meter=it.to_pb()))),
        draw(create_usage_point().map(lambda it: NetworkIdentifiedObject(usagePoint=it.to_pb()))),

        #######################
        # IEC61968 Operations #
        #######################

        draw(create_operational_restriction().map(lambda it: NetworkIdentifiedObject(operationalRestriction=it.to_pb()))),

        #####################################
        # IEC61970 Base Auxiliary Equipment #
        #####################################

        draw(create_current_transformer().map(lambda it: NetworkIdentifiedObject(currentTransformer=it.to_pb()))),
        draw(create_fault_indicator().map(lambda it: NetworkIdentifiedObject(faultIndicator=it.to_pb()))),
        draw(create_potential_transformer().map(lambda it: NetworkIdentifiedObject(potentialTransformer=it.to_pb()))),

        ######################
        # IEC61970 Base Core #
        ######################

        draw(create_base_voltage().map(lambda it: NetworkIdentifiedObject(baseVoltage=it.to_pb()))),
        draw(create_connectivity_node().map(lambda it: NetworkIdentifiedObject(connectivityNode=it.to_pb()))),
        draw(create_feeder().map(lambda it: NetworkIdentifiedObject(feeder=it.to_pb()))),
        draw(create_geographical_region().map(lambda it: NetworkIdentifiedObject(geographicalRegion=it.to_pb()))),
        draw(create_sub_geographical_region().map(lambda it: NetworkIdentifiedObject(subGeographicalRegion=it.to_pb()))),
        draw(create_substation().map(lambda it: NetworkIdentifiedObject(substation=it.to_pb()))),
        draw(create_terminal().map(lambda it: NetworkIdentifiedObject(terminal=it.to_pb()))),

        #############################
        # IEC61970 Base Equivalents #
        #############################

        draw(create_equivalent_branch().map(lambda it: NetworkIdentifiedObject(equivalentBranch=it.to_pb()))),

        #######################################
        # IEC61970 Base Generation Production #
        #######################################

        draw(create_battery_unit().map(lambda it: NetworkIdentifiedObject(batteryUnit=it.to_pb()))),
        draw(create_photo_voltaic_unit().map(lambda it: NetworkIdentifiedObject(photoVoltaicUnit=it.to_pb()))),
        draw(create_power_electronics_wind_unit().map(lambda it: NetworkIdentifiedObject(powerElectronicsWindUnit=it.to_pb()))),

        ######################
        # IEC61970 Base Meas #
        ######################

        draw(create_accumulator().map(lambda it: NetworkIdentifiedObject(accumulator=it.to_pb()))),
        draw(create_analog().map(lambda it: NetworkIdentifiedObject(analog=it.to_pb()))),
        draw(create_control().map(lambda it: NetworkIdentifiedObject(control=it.to_pb()))),
        draw(create_discrete().map(lambda it: NetworkIdentifiedObject(discrete=it.to_pb()))),

        ############################
        # IEC61970 Base Protection #
        ############################

        draw(create_current_relay().map(lambda it: NetworkIdentifiedObject(currentRelay=it.to_pb()))),

        #######################
        # IEC61970 Base Scada #
        #######################

        draw(create_remote_control().map(lambda it: NetworkIdentifiedObject(remoteControl=it.to_pb()))),
        draw(create_remote_source().map(lambda it: NetworkIdentifiedObject(remoteSource=it.to_pb()))),

        #######################
        # IEC61970 Base Wires #
        #######################

        draw(create_ac_line_segment().map(lambda it: NetworkIdentifiedObject(acLineSegment=it.to_pb()))),
        draw(create_breaker().map(lambda it: NetworkIdentifiedObject(breaker=it.to_pb()))),
        draw(create_busbar_section().map(lambda it: NetworkIdentifiedObject(busbarSection=it.to_pb()))),
        draw(create_clamp().map(lambda it: NetworkIdentifiedObject(clamp=it.to_pb()))),
        draw(create_cut().map(lambda it: NetworkIdentifiedObject(cut=it.to_pb()))),
        draw(create_disconnector().map(lambda it: NetworkIdentifiedObject(disconnector=it.to_pb()))),
        draw(create_energy_consumer().map(lambda it: NetworkIdentifiedObject(energyConsumer=it.to_pb()))),
        draw(create_energy_consumer_phase().map(lambda it: NetworkIdentifiedObject(energyConsumerPhase=it.to_pb()))),
        draw(create_energy_source().map(lambda it: NetworkIdentifiedObject(energySource=it.to_pb()))),
        draw(create_energy_source_phase().map(lambda it: NetworkIdentifiedObject(energySourcePhase=it.to_pb()))),
        draw(create_fuse().map(lambda it: NetworkIdentifiedObject(fuse=it.to_pb()))),
        draw(create_ground().map(lambda it: NetworkIdentifiedObject(ground=it.to_pb()))),
        draw(create_ground_disconnector().map(lambda it: NetworkIdentifiedObject(groundDisconnector=it.to_pb()))),
        draw(create_grounding_impedance().map(lambda it: NetworkIdentifiedObject(groundingImpedance=it.to_pb()))),
        draw(create_jumper().map(lambda it: NetworkIdentifiedObject(jumper=it.to_pb()))),
        draw(create_junction().map(lambda it: NetworkIdentifiedObject(junction=it.to_pb()))),
        draw(create_linear_shunt_compensator().map(lambda it: NetworkIdentifiedObject(linearShuntCompensator=it.to_pb()))),
        draw(create_load_break_switch().map(lambda it: NetworkIdentifiedObject(loadBreakSwitch=it.to_pb()))),
        draw(create_per_length_phase_impedance().map(lambda it: NetworkIdentifiedObject(perLengthPhaseImpedance=it.to_pb()))),
        draw(create_per_length_sequence_impedance().map(lambda it: NetworkIdentifiedObject(perLengthSequenceImpedance=it.to_pb()))),
        draw(create_power_electronics_connection().map(lambda it: NetworkIdentifiedObject(powerElectronicsConnection=it.to_pb()))),
        draw(create_power_electronics_connection_phase().map(lambda it: NetworkIdentifiedObject(powerElectronicsConnectionPhase=it.to_pb()))),
        draw(create_power_transformer().map(lambda it: NetworkIdentifiedObject(powerTransformer=it.to_pb()))),
        draw(create_power_transformer_end().map(lambda it: NetworkIdentifiedObject(powerTransformerEnd=it.to_pb()))),
        draw(create_ratio_tap_changer().map(lambda it: NetworkIdentifiedObject(ratioTapChanger=it.to_pb()))),
        draw(create_reactive_capability_curve().map(lambda it: NetworkIdentifiedObject(reactiveCapabilityCurve=it.to_pb()))),
        draw(create_recloser().map(lambda it: NetworkIdentifiedObject(recloser=it.to_pb()))),
        draw(create_series_compensator().map(lambda it: NetworkIdentifiedObject(seriesCompensator=it.to_pb()))),
        draw(create_static_var_compensator().map(lambda it: NetworkIdentifiedObject(staticVarCompensator=it.to_pb()))),
        draw(create_synchronous_machine().map(lambda it: NetworkIdentifiedObject(synchronousMachine=it.to_pb()))),
        draw(create_tap_changer_control().map(lambda it: NetworkIdentifiedObject(tapChangerControl=it.to_pb()))),
        draw(create_transformer_star_impedance().map(lambda it: NetworkIdentifiedObject(transformerStarImpedance=it.to_pb()))),

        ###############################
        # IEC61970 InfIEC61970 Feeder #
        ###############################

        draw(create_circuit().map(lambda it: NetworkIdentifiedObject(circuit=it.to_pb()))),
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

        draw(create_diagram().map(lambda it: DiagramIdentifiedObject(diagram=it.to_pb()))),
        draw(create_diagram_object().map(lambda it: DiagramIdentifiedObject(diagramObject=it.to_pb())))
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

        draw(create_organisation().map(lambda it: CustomerIdentifiedObject(organisation=it.to_pb()))),

        ######################
        # IEC61968 Customers #
        ######################

        draw(create_customer().map(lambda it: CustomerIdentifiedObject(customer=it.to_pb()))),
        draw(create_customer_agreement().map(lambda it: CustomerIdentifiedObject(customerAgreement=it.to_pb()))),
        draw(create_pricing_structure().map(lambda it: CustomerIdentifiedObject(pricingStructure=it.to_pb()))),
        draw(create_tariff().map(lambda it: CustomerIdentifiedObject(tariff=it.to_pb()))),
    ]
    return dios
