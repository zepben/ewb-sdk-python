#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ['network_identified_objects', 'customer_identified_objects', 'diagram_identified_objects']

from zepben.protobuf.cc.cc_data_pb2 import CustomerIdentifiable
from zepben.protobuf.dc.dc_data_pb2 import DiagramIdentifiable
from zepben.protobuf.nc.nc_data_pb2 import NetworkIdentifiable
from hypothesis.strategies import composite

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

        draw(create_location().map(lambda it: NetworkIdentifiable(location=it.to_pb()))),
        draw(create_organisation().map(lambda it: NetworkIdentifiable(organisation=it.to_pb()))),

        #####################################
        # IEC61968 InfIEC61968 InfAssetInfo #
        #####################################

        draw(create_current_transformer_info().map(lambda it: NetworkIdentifiable(currentTransformerInfo=it.to_pb()))),
        draw(create_potential_transformer_info().map(lambda it: NetworkIdentifiable(potentialTransformerInfo=it.to_pb()))),

        ##################################
        # IEC61968 InfIEC61968 InfAssets #
        ##################################

        draw(create_pole().map(lambda it: NetworkIdentifiable(pole=it.to_pb()))),

        #####################
        # IEC61968 Metering #
        #####################

        draw(create_meter().map(lambda it: NetworkIdentifiable(meter=it.to_pb()))),
        draw(create_usage_point().map(lambda it: NetworkIdentifiable(usagePoint=it.to_pb()))),

        #######################
        # IEC61968 Operations #
        #######################

        draw(create_operational_restriction().map(lambda it: NetworkIdentifiable(operationalRestriction=it.to_pb()))),

        #####################################
        # IEC61970 Base Auxiliary Equipment #
        #####################################

        draw(create_current_transformer().map(lambda it: NetworkIdentifiable(currentTransformer=it.to_pb()))),
        draw(create_fault_indicator().map(lambda it: NetworkIdentifiable(faultIndicator=it.to_pb()))),
        draw(create_potential_transformer().map(lambda it: NetworkIdentifiable(potentialTransformer=it.to_pb()))),

        ######################
        # IEC61970 Base Core #
        ######################

        draw(create_base_voltage().map(lambda it: NetworkIdentifiable(baseVoltage=it.to_pb()))),
        draw(create_connectivity_node().map(lambda it: NetworkIdentifiable(connectivityNode=it.to_pb()))),
        draw(create_feeder().map(lambda it: NetworkIdentifiable(feeder=it.to_pb()))),
        draw(create_geographical_region().map(lambda it: NetworkIdentifiable(geographicalRegion=it.to_pb()))),
        draw(create_sub_geographical_region().map(lambda it: NetworkIdentifiable(subGeographicalRegion=it.to_pb()))),
        draw(create_substation().map(lambda it: NetworkIdentifiable(substation=it.to_pb()))),
        draw(create_terminal().map(lambda it: NetworkIdentifiable(terminal=it.to_pb()))),

        #############################
        # IEC61970 Base Equivalents #
        #############################

        draw(create_equivalent_branch().map(lambda it: NetworkIdentifiable(equivalentBranch=it.to_pb()))),

        #######################################
        # IEC61970 Base Generation Production #
        #######################################

        draw(create_battery_unit().map(lambda it: NetworkIdentifiable(batteryUnit=it.to_pb()))),
        draw(create_photo_voltaic_unit().map(lambda it: NetworkIdentifiable(photoVoltaicUnit=it.to_pb()))),
        draw(create_power_electronics_wind_unit().map(lambda it: NetworkIdentifiable(powerElectronicsWindUnit=it.to_pb()))),

        ######################
        # IEC61970 Base Meas #
        ######################

        draw(create_accumulator().map(lambda it: NetworkIdentifiable(accumulator=it.to_pb()))),
        draw(create_analog().map(lambda it: NetworkIdentifiable(analog=it.to_pb()))),
        draw(create_control().map(lambda it: NetworkIdentifiable(control=it.to_pb()))),
        draw(create_discrete().map(lambda it: NetworkIdentifiable(discrete=it.to_pb()))),

        ############################
        # IEC61970 Base Protection #
        ############################

        draw(create_current_relay().map(lambda it: NetworkIdentifiable(currentRelay=it.to_pb()))),

        #######################
        # IEC61970 Base Scada #
        #######################

        draw(create_remote_control().map(lambda it: NetworkIdentifiable(remoteControl=it.to_pb()))),
        draw(create_remote_source().map(lambda it: NetworkIdentifiable(remoteSource=it.to_pb()))),

        #######################
        # IEC61970 Base Wires #
        #######################

        draw(create_ac_line_segment().map(lambda it: NetworkIdentifiable(acLineSegment=it.to_pb()))),
        draw(create_breaker().map(lambda it: NetworkIdentifiable(breaker=it.to_pb()))),
        draw(create_busbar_section().map(lambda it: NetworkIdentifiable(busbarSection=it.to_pb()))),
        draw(create_clamp().map(lambda it: NetworkIdentifiable(clamp=it.to_pb()))),
        draw(create_cut().map(lambda it: NetworkIdentifiable(cut=it.to_pb()))),
        draw(create_disconnector().map(lambda it: NetworkIdentifiable(disconnector=it.to_pb()))),
        draw(create_energy_consumer().map(lambda it: NetworkIdentifiable(energyConsumer=it.to_pb()))),
        draw(create_energy_consumer_phase().map(lambda it: NetworkIdentifiable(energyConsumerPhase=it.to_pb()))),
        draw(create_energy_source().map(lambda it: NetworkIdentifiable(energySource=it.to_pb()))),
        draw(create_energy_source_phase().map(lambda it: NetworkIdentifiable(energySourcePhase=it.to_pb()))),
        draw(create_fuse().map(lambda it: NetworkIdentifiable(fuse=it.to_pb()))),
        draw(create_ground().map(lambda it: NetworkIdentifiable(ground=it.to_pb()))),
        draw(create_ground_disconnector().map(lambda it: NetworkIdentifiable(groundDisconnector=it.to_pb()))),
        draw(create_grounding_impedance().map(lambda it: NetworkIdentifiable(groundingImpedance=it.to_pb()))),
        draw(create_jumper().map(lambda it: NetworkIdentifiable(jumper=it.to_pb()))),
        draw(create_junction().map(lambda it: NetworkIdentifiable(junction=it.to_pb()))),
        draw(create_linear_shunt_compensator().map(lambda it: NetworkIdentifiable(linearShuntCompensator=it.to_pb()))),
        draw(create_load_break_switch().map(lambda it: NetworkIdentifiable(loadBreakSwitch=it.to_pb()))),
        draw(create_per_length_phase_impedance().map(lambda it: NetworkIdentifiable(perLengthPhaseImpedance=it.to_pb()))),
        draw(create_per_length_sequence_impedance().map(lambda it: NetworkIdentifiable(perLengthSequenceImpedance=it.to_pb()))),
        draw(create_power_electronics_connection().map(lambda it: NetworkIdentifiable(powerElectronicsConnection=it.to_pb()))),
        draw(create_power_electronics_connection_phase().map(lambda it: NetworkIdentifiable(powerElectronicsConnectionPhase=it.to_pb()))),
        draw(create_power_transformer().map(lambda it: NetworkIdentifiable(powerTransformer=it.to_pb()))),
        draw(create_power_transformer_end().map(lambda it: NetworkIdentifiable(powerTransformerEnd=it.to_pb()))),
        draw(create_ratio_tap_changer().map(lambda it: NetworkIdentifiable(ratioTapChanger=it.to_pb()))),
        draw(create_reactive_capability_curve().map(lambda it: NetworkIdentifiable(reactiveCapabilityCurve=it.to_pb()))),
        draw(create_recloser().map(lambda it: NetworkIdentifiable(recloser=it.to_pb()))),
        draw(create_series_compensator().map(lambda it: NetworkIdentifiable(seriesCompensator=it.to_pb()))),
        draw(create_static_var_compensator().map(lambda it: NetworkIdentifiable(staticVarCompensator=it.to_pb()))),
        draw(create_synchronous_machine().map(lambda it: NetworkIdentifiable(synchronousMachine=it.to_pb()))),
        draw(create_tap_changer_control().map(lambda it: NetworkIdentifiable(tapChangerControl=it.to_pb()))),
        draw(create_transformer_star_impedance().map(lambda it: NetworkIdentifiable(transformerStarImpedance=it.to_pb()))),

        ###############################
        # IEC61970 InfIEC61970 Feeder #
        ###############################

        draw(create_circuit().map(lambda it: NetworkIdentifiable(circuit=it.to_pb()))),
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

        draw(create_diagram().map(lambda it: DiagramIdentifiable(diagram=it.to_pb()))),
        draw(create_diagram_object().map(lambda it: DiagramIdentifiable(diagramObject=it.to_pb())))
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

        draw(create_organisation().map(lambda it: CustomerIdentifiable(organisation=it.to_pb()))),

        ######################
        # IEC61968 Customers #
        ######################

        draw(create_customer().map(lambda it: CustomerIdentifiable(customer=it.to_pb()))),
        draw(create_customer_agreement().map(lambda it: CustomerIdentifiable(customerAgreement=it.to_pb()))),
        draw(create_pricing_structure().map(lambda it: CustomerIdentifiable(pricingStructure=it.to_pb()))),
        draw(create_tariff().map(lambda it: CustomerIdentifiable(tariff=it.to_pb()))),
    ]
    return dios
